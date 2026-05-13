"""
Payment orchestration: the state machine that turns a parsed WhatsApp
message into a real bank transfer.

Two entry points exist:

* :func:`initiate` — start a new payment from a parsed PAYMENT intent.
  Performs name lookup, balance check, fraud screening, then persists a
  ``Transaction`` in ``AWAITING_CONFIRMATION`` with a 10-minute expiry.

* :func:`confirm` — verify a supplied PCT against the user's stored hash,
  debit the wallet, call Squad's payout API, finalize the transaction.

Both return a human-readable reply string the caller (the Twilio webhook)
can echo back as TwiML.
"""

from __future__ import annotations

import logging
import secrets
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session

from app.models.payment_confirmation_token import PaymentConfirmationToken
from app.models.transaction import Transaction, TransactionStatus
from app.models.user import User
from app.models.wallet import Wallet
from app.services import banks as banks_service
from app.services import fraud, squad
from app.services import pct as pct_service

logger = logging.getLogger(__name__)

CONFIRMATION_WINDOW = timedelta(minutes=10)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _generate_reference() -> str:
    # Squad's payout API accepts alphanumeric + underscore (e.g.
    # "SBS5B8VU36_Test222") and rejects hyphens / other punctuation as
    # "Bad ref format".
    return f'SQD{secrets.token_hex(6).upper()}_{secrets.token_hex(4)}'


def get_active_pending(db: Session, user: User) -> Optional[Transaction]:
    """Return the user's still-valid AWAITING_CONFIRMATION transaction, if any.

    Lazily expires any that are past their ``expires_at``. We commit the
    expiry write so the next read sees consistent state.
    """
    pending = (
        db.query(Transaction)
        .filter(
            Transaction.sender_id == user.id,
            Transaction.status == TransactionStatus.AWAITING_CONFIRMATION.value,
        )
        .order_by(Transaction.created_at.desc())
        .first()
    )
    if not pending:
        return None

    expires_at = _ensure_aware(pending.expires_at)
    if expires_at <= _now():
        pending.status = TransactionStatus.EXPIRED.value
        pending.failure_reason = 'Confirmation window elapsed.'
        db.commit()
        return None

    return pending


async def initiate(
    db: Session,
    user: User,
    amount: Decimal,
    recipient_account_number: str,
    recipient_bank_code: str,
    recipient_bank_name: str,
    raw_message: Optional[str] = None,
) -> str:
    """Begin a new payment request. Returns a user-facing reply string."""
    wallet: Wallet | None = (
        db.query(Wallet).filter(Wallet.user_id == user.id).with_for_update().first()
    )
    if wallet is None:
        return 'Your wallet has not been set up. Please complete registration first.'

    fee = Decimal('0.00')
    total = amount + fee
    if wallet.balance < total:
        return (
            f'Insufficient funds. Your balance is NGN {wallet.balance:,.2f}, '
            f'but this transfer requires NGN {total:,.2f}.'
        )

    decision = fraud.screen(db, user, amount, recipient_account_number)
    if not decision.approved:
        _record_rejected(
            db, user, amount, recipient_account_number, recipient_bank_code,
            recipient_bank_name, decision.reason or 'rejected', raw_message,
        )
        return f'Transaction rejected: {decision.reason}'

    try:
        bank_info = await squad.lookup_bank_account(recipient_account_number, recipient_bank_code)
    except ValueError as exc:
        logger.warning('Bank lookup failed: %s', exc)
        return (
            f'Could not verify the recipient account at {recipient_bank_name}. '
            'Double-check the account number and try again.'
        )

    recipient_account_name = bank_info['account_name']

    tx = Transaction(
        sender_id=user.id,
        reference=_generate_reference(),
        recipient_account_number=recipient_account_number,
        recipient_bank_code=recipient_bank_code,
        recipient_bank_name=recipient_bank_name,
        recipient_account_name=recipient_account_name,
        amount=amount,
        fee=fee,
        currency='NGN',
        status=TransactionStatus.AWAITING_CONFIRMATION.value,
        narration=f'Squad transfer to {recipient_account_name}',
        raw_message=raw_message,
        expires_at=_now() + CONFIRMATION_WINDOW,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)

    return (
        'Please confirm this transfer:\n\n'
        f'• To: {recipient_account_name}\n'
        f'• Bank: {recipient_bank_name}\n'
        f'• Account: {recipient_account_number}\n'
        f'• Amount: NGN {amount:,.2f}\n'
        f'• Reference: {tx.reference}\n\n'
        'Reply with your Payment Confirmation Token (PCT) to send, '
        'or reply CANCEL to abort. This request expires in 10 minutes.'
    )


async def confirm(db: Session, user: User, supplied_pct: str) -> str:
    """Verify the PCT for the user's pending transaction and execute it."""
    pending = get_active_pending(db, user)
    if not pending:
        return 'You have no pending transaction to confirm.'

    pct_row: PaymentConfirmationToken | None = (
        db.query(PaymentConfirmationToken)
        .filter(PaymentConfirmationToken.user_id == user.id)
        .first()
    )
    if not pct_row:
        pending.status = TransactionStatus.FAILED.value
        pending.failure_reason = 'No PCT configured for this user.'
        db.commit()
        return (
            'You have not set up a Payment Confirmation Token. '
            'Set one via /auth/set-pct before initiating payments.'
        )

    if not pct_service.verify_pct(supplied_pct, pct_row.token_salt, pct_row.token_hash):
        pending.status = TransactionStatus.REJECTED.value
        pending.failure_reason = 'Invalid PCT supplied.'
        db.commit()
        return 'Invalid Payment Confirmation Token. This transaction has been cancelled for your safety.'

    decision = fraud.screen(db, user, pending.amount, pending.recipient_account_number)
    if not decision.approved:
        pending.status = TransactionStatus.REJECTED.value
        pending.failure_reason = decision.reason
        db.commit()
        return f'Transaction rejected at confirmation: {decision.reason}'

    wallet: Wallet | None = (
        db.query(Wallet).filter(Wallet.user_id == user.id).with_for_update().first()
    )
    if wallet is None or wallet.balance < pending.amount + pending.fee:
        pending.status = TransactionStatus.FAILED.value
        pending.failure_reason = 'Insufficient funds at confirmation.'
        db.commit()
        return 'Your balance has changed and is no longer sufficient. Transaction cancelled.'

    pending.status = TransactionStatus.PROCESSING.value
    pending.confirmed_at = _now()
    wallet.balance = wallet.balance - pending.amount - pending.fee
    db.commit()

    amount_kobo = int((pending.amount * 100).to_integral_value())
    try:
        result = await squad.transfer(
            amount_kobo=amount_kobo,
            recipient_account_number=pending.recipient_account_number,
            recipient_bank_code=pending.recipient_bank_code,
            recipient_account_name=pending.recipient_account_name,
            reference=pending.reference,
            narration=pending.narration,
        )
    except ValueError as exc:
        logger.error('Squad transfer failed for %s: %s', pending.reference, exc)
        wallet.balance = wallet.balance + pending.amount + pending.fee
        pending.status = TransactionStatus.FAILED.value
        pending.failure_reason = str(exc)
        db.commit()
        return (
            'We could not complete your transfer. Your balance has been restored. '
            f'Reference: {pending.reference}'
        )

    pending.squad_reference = result.get('reference')
    _apply_squad_status(db, pending, wallet, result)
    db.commit()

    return _completion_reply(pending, wallet)


_SQUAD_SUCCESS = {'success', 'successful', 'completed'}
_SQUAD_FAILED = {'failed', 'failure', 'reversed', 'rejected'}


def _apply_squad_status(
    db: Session,
    tx: Transaction,
    wallet: Wallet,
    result: dict,
) -> None:
    """Translate a Squad transfer/requery response into our internal status.

    The wallet was already debited at confirmation time. Only a terminal
    FAILED/REVERSED outcome refunds it; pending stays in PROCESSING so the
    caller can re-query later without double-counting.
    """
    status = (result.get('status') or 'pending').lower()
    if status in _SQUAD_SUCCESS:
        tx.status = TransactionStatus.SUCCESS.value
        tx.failure_reason = None
    elif status in _SQUAD_FAILED:
        if tx.status != TransactionStatus.FAILED.value:
            wallet.balance = wallet.balance + tx.amount + tx.fee
        tx.status = TransactionStatus.FAILED.value
        tx.failure_reason = result.get('message') or 'Squad reported the transfer failed.'
    else:
        tx.status = TransactionStatus.PROCESSING.value


def _completion_reply(tx: Transaction, wallet: Wallet) -> str:
    if tx.status == TransactionStatus.SUCCESS.value:
        headline = 'Payment sent.'
    elif tx.status == TransactionStatus.FAILED.value:
        return (
            'We could not complete your transfer. Your balance has been restored.\n'
            f'• Reference: {tx.reference}\n'
            f'• Reason: {tx.failure_reason}'
        )
    else:
        headline = 'Payment submitted. Awaiting Squad confirmation; reply STATUS to check.'

    return (
        f'{headline}\n\n'
        f'• To: {tx.recipient_account_name}\n'
        f'• Bank: {tx.recipient_bank_name}\n'
        f'• Account: {tx.recipient_account_number}\n'
        f'• Amount: NGN {tx.amount:,.2f}\n'
        f'• Reference: {tx.reference}\n'
        f'• Wallet balance: NGN {wallet.balance:,.2f}'
    )


async def refresh_processing(db: Session, user: User) -> None:
    """Re-query Squad for any of this user's PROCESSING transactions and
    promote them to SUCCESS / FAILED if Squad now reports a terminal state."""
    processing = (
        db.query(Transaction)
        .filter(
            Transaction.sender_id == user.id,
            Transaction.status == TransactionStatus.PROCESSING.value,
        )
        .all()
    )
    if not processing:
        return

    wallet: Wallet | None = (
        db.query(Wallet).filter(Wallet.user_id == user.id).with_for_update().first()
    )
    if wallet is None:
        return

    changed = False
    for tx in processing:
        try:
            result = await squad.requery(tx.reference)
        except ValueError as exc:
            logger.warning('Requery failed for %s: %s', tx.reference, exc)
            continue
        before = tx.status
        _apply_squad_status(db, tx, wallet, result)
        if tx.status != before:
            changed = True

    if changed:
        db.commit()


def apply_external_status(
    db: Session,
    reference: str,
    status: str,
    message: str | None = None,
) -> Transaction | None:
    """Reconcile a transaction from an out-of-band signal (Squad webhook).

    Returns the updated row, or ``None`` if no matching transaction exists.
    """
    tx: Transaction | None = (
        db.query(Transaction).filter(Transaction.reference == reference).first()
    )
    if tx is None:
        return None
    if tx.status in {
        TransactionStatus.SUCCESS.value,
        TransactionStatus.FAILED.value,
        TransactionStatus.REJECTED.value,
        TransactionStatus.EXPIRED.value,
        TransactionStatus.CANCELLED.value,
    }:
        return tx  # Already terminal — ignore.

    wallet: Wallet | None = (
        db.query(Wallet).filter(Wallet.user_id == tx.sender_id).with_for_update().first()
    )
    if wallet is None:
        return tx

    _apply_squad_status(db, tx, wallet, {'status': status, 'message': message})
    db.commit()
    return tx


def cancel_pending(db: Session, user: User) -> str:
    pending = get_active_pending(db, user)
    if not pending:
        return 'You have no pending transaction to cancel.'
    pending.status = TransactionStatus.CANCELLED.value
    pending.failure_reason = 'Cancelled by user.'
    db.commit()
    return f'Transaction {pending.reference} cancelled.'


def show_status(db: Session, user: User) -> str:
    recent = (
        db.query(Transaction)
        .filter(Transaction.sender_id == user.id)
        .order_by(Transaction.created_at.desc())
        .limit(3)
        .all()
    )
    if not recent:
        return 'No recent transactions found.'
    lines = ['Recent transactions:']
    for tx in recent:
        lines.append(
            f'• {tx.reference}: NGN {tx.amount:,.2f} → '
            f'{tx.recipient_account_name or tx.recipient_account_number} '
            f'[{tx.status}]'
        )
    return '\n'.join(lines)


def show_balance(db: Session, user: User) -> str:
    wallet: Wallet | None = db.query(Wallet).filter(Wallet.user_id == user.id).first()
    if wallet is None:
        return 'You have no wallet yet. Complete registration first.'
    return f'Your Squad wallet balance is NGN {wallet.balance:,.2f}.'


def help_text() -> str:
    return (
        'Squad WhatsApp commands:\n\n'
        '• Send money: "send 2500 naira to 0123456789 GTBank"\n'
        '• Check balance: "balance"\n'
        '• Recent transactions: "status"\n'
        '• Cancel a pending request: "cancel"\n'
        '• Show this help: "help"\n\n'
        'Confirm a payment by replying with your PCT within 10 minutes.'
    )


def _record_rejected(
    db: Session,
    user: User,
    amount: Decimal,
    recipient_account_number: str,
    recipient_bank_code: str,
    recipient_bank_name: str,
    reason: str,
    raw_message: Optional[str],
) -> None:
    tx = Transaction(
        sender_id=user.id,
        reference=_generate_reference(),
        recipient_account_number=recipient_account_number,
        recipient_bank_code=recipient_bank_code,
        recipient_bank_name=recipient_bank_name,
        recipient_account_name='',
        amount=amount,
        fee=Decimal('0.00'),
        currency='NGN',
        status=TransactionStatus.REJECTED.value,
        failure_reason=reason,
        narration='Rejected by fraud screening',
        raw_message=raw_message,
        expires_at=_now() + CONFIRMATION_WINDOW,
    )
    db.add(tx)
    db.commit()


def _ensure_aware(dt: datetime) -> datetime:
    """SQLAlchemy may hand back a naive datetime for ``server_default`` cols.

    We compare against tz-aware ``now()``, so coerce naive values to UTC.
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


# Keep banks resolution accessible to callers without leaking the module name
resolve_bank = banks_service.resolve