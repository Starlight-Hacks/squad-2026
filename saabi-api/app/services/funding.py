"""
Wallet funding: crediting a user's internal wallet from Squad's payment modal.

The flow has two halves:

* :func:`initiate` — called by ``POST /wallet/fund/init``. Records a PENDING
  ``WalletFunding`` row and hands its reference back to the frontend, which
  opens Squad's checkout modal with it.

* :func:`apply_charge_status` — called by Squad's collection webhook once the
  user pays. It reconciles the row by reference and, on success, credits the
  wallet exactly once.

Crediting only happens here, never from the init call — we never trust a
balance change that Squad hasn't confirmed.
"""

from __future__ import annotations

import logging
import secrets
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.wallet import Wallet
from app.models.wallet_funding import FundingStatus, WalletFunding

logger = logging.getLogger(__name__)

_SUCCESS_STATUSES = {'success', 'successful'}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _generate_reference() -> str:
    # Squad collection references are freeform; a readable prefix just makes
    # them easy to spot in logs and the Squad dashboard.
    return f'FUND_{secrets.token_hex(8)}'


def initiate(db: Session, user: User, amount: Decimal) -> WalletFunding:
    """Record a pending funding attempt and return it for the Squad modal."""
    funding = WalletFunding(
        user_id=user.id,
        reference=_generate_reference(),
        amount=amount,
        currency='NGN',
        status=FundingStatus.PENDING.value,
    )
    db.add(funding)
    db.commit()
    db.refresh(funding)
    return funding


def apply_charge_status(
    db: Session,
    reference: str,
    status: str,
    squad_transaction_ref: str | None = None,
    message: str | None = None,
) -> WalletFunding | None:
    """Reconcile a Squad collection webhook against a pending funding row.

    Returns the funding row, or ``None`` if the reference is unknown to us.
    Safe to call repeatedly — Squad retries webhooks, so a row that has
    already been settled is left untouched.
    """
    funding: WalletFunding | None = (
        db.query(WalletFunding).filter(WalletFunding.reference == reference).first()
    )
    if funding is None:
        return None

    if funding.status != FundingStatus.PENDING.value:
        logger.info('Funding webhook for %s: already %s — ignoring.', reference, funding.status)
        return funding

    if squad_transaction_ref:
        funding.squad_transaction_ref = squad_transaction_ref

    if (status or '').lower() not in _SUCCESS_STATUSES:
        funding.status = FundingStatus.FAILED.value
        funding.failure_reason = message or f'Squad reported {status}'
        db.commit()
        logger.info('Funding %s failed: %s', reference, funding.failure_reason)
        return funding

    # Lock the wallet row so two overlapping webhook deliveries can't both
    # read the old balance and double-credit.
    wallet: Wallet | None = (
        db.query(Wallet).filter(Wallet.user_id == funding.user_id).with_for_update().first()
    )
    if wallet is None:
        funding.status = FundingStatus.FAILED.value
        funding.failure_reason = 'User has no wallet to credit.'
        db.commit()
        logger.error('Funding %s succeeded at Squad but user has no wallet.', reference)
        return funding

    wallet.balance = wallet.balance + funding.amount
    funding.status = FundingStatus.SUCCESS.value
    funding.completed_at = _now()
    db.commit()

    logger.info('Funding %s credited NGN %s — wallet balance now %s', reference, funding.amount, wallet.balance)
    return funding
