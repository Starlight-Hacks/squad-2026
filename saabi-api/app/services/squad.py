"""
Squad Co API integration.

Architecturally, Squad holds a single merchant-pool ledger ("Squad ledger");
``/payout/transfer`` debits *that* pool. Our per-user ``Wallet`` table is an
internal virtual ledger overlaid on the merchant pool — Squad has no notion
of per-user balances tied to our users. The invariant we must preserve is:

    Σ(user wallet balances) ≤ Squad merchant ledger balance

Squad exposes three relevant endpoints:
  - ``/payout/account/lookup`` — resolve recipient name (pre-transfer check)
  - ``/payout/transfer``       — debit merchant ledger, queue an outbound wire
  - ``/payout/requery``        — ask Squad what really happened to a transfer

A transfer can return ``pending`` and later flip to ``success`` or ``failed``.
We therefore re-query on the next user interaction (and accept Squad
webhooks) instead of assuming the immediate response is terminal.
"""

import hashlib
import hmac
import logging
from typing import Any, TypedDict

import httpx

from app.config import settings

logger = logging.getLogger(__name__)


def verify_webhook_signature(raw_body: bytes, signature: str | None) -> bool:
    """Check Squad's ``x-squad-signature`` header against the raw request body.

    Squad signs collection webhooks with HMAC-SHA512 over the *exact* bytes it
    sent, keyed with our merchant secret. We compare in constant time. This
    matters most for the funding webhook — it mints wallet balance, so an
    unauthenticated caller must never be able to drive it.
    """
    if not signature:
        return False

    expected = hmac.new(
        settings.squad_secret_key.encode(),
        raw_body,
        hashlib.sha512,
    ).hexdigest()
    return hmac.compare_digest(expected, signature.strip().lower())


# Squad's response shape varies by endpoint and product. These are every key
# that has been observed to carry the transfer state across transfer /
# requery / webhook payloads. We check all of them.
_STATUS_KEYS = ('status', 'transaction_status', 'transactionStatus', 'state')


def _extract_status(payload: dict[str, Any]) -> str | None:
    """Pull a transfer status out of any reasonable Squad response shape.

    Squad sometimes nests it under ``data``, sometimes places it at the
    root, and sometimes uses ``transaction_status`` instead of ``status``.
    Returns the first non-empty value found, lower-cased; ``None`` if absent.
    """
    candidates = [payload, payload.get('data') or {}]
    for obj in candidates:
        if not isinstance(obj, dict):
            continue
        for key in _STATUS_KEYS:
            value = obj.get(key)
            if value:
                return str(value).lower()
    return None


def _extract_message(payload: dict[str, Any]) -> str:
    detail = payload.get('data') if isinstance(payload.get('data'), dict) else {}
    return str(detail.get('message') or detail.get('remark') or payload.get('message') or '')


class BankAccountInfo(TypedDict):
    account_name: str
    account_number: str
    bank_code: str


class TransferResult(TypedDict):
    reference: str
    status: str  # 'success' | 'pending' | 'failed' | 'reversed'
    message: str  # Squad-provided detail; useful for failure reasons


def _headers() -> dict[str, str]:
    return {
        'Authorization': f'Bearer {settings.squad_secret_key}',
        'Content-Type': 'application/json',
    }


async def lookup_bank_account(account_number: str, bank_code: str) -> BankAccountInfo:
    """Resolve the account name for an  account number and bank code.

    Used during registration (identity check) and before every payment
    (show recipient details to the user before they confirm).
    """
    url = f'{settings.squad_base_url}/payout/account/lookup'

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(
            url,
            headers=_headers(),
            json={'account_number': account_number, 'bank_code': bank_code},
        )

    if response.status_code != 200:
        raise ValueError(f'Bank account lookup failed: {response.text}')

    data = response.json()
    if not data.get('success'):
        raise ValueError(f'Bank account lookup unsuccessful: {data.get("message")}')

    return BankAccountInfo(
        account_name=data['data']['account_name'],
        account_number=account_number,
        bank_code=bank_code,
    )


async def transfer(
    amount_kobo: int,
    recipient_account_number: str,
    recipient_bank_code: str,
    recipient_account_name: str,
    reference: str,
) -> TransferResult:
    """Initiate an outbound bank transfer via Squad's payout API.

    amount_kobo: amount in the smallest currency unit (kobo for NGN).
    reference: unique per-transaction ID from our system.
    """
    url = f'{settings.squad_base_url}/payout/transfer'
    payload = {
        'transaction_reference': reference,
        'amount': amount_kobo,
        'bank_code': recipient_bank_code,
        'account_number': recipient_account_number,
        'account_name': recipient_account_name,
        'currency_id': 'NGN',
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, headers=_headers(), json=payload)

    if response.status_code not in (200, 201):
        raise ValueError(f'Transfer failed: {response.text}')

    data = response.json()
    logger.info('Squad transfer %s -> HTTP %s, body=%s', reference, response.status_code, data)

    if not data.get('success'):
        raise ValueError(f'Transfer unsuccessful: {data.get("message")}')

    # HTTP 200 + success=true means Squad has accepted the transfer and
    # debited the merchant pool. That is the success signal — only downgrade
    # to PROCESSING/FAILED if Squad explicitly says so in the body.
    status = _extract_status(data) or 'success'
    return TransferResult(
        reference=reference,
        status=status,
        message=_extract_message(data),
    )


async def requery(reference: str) -> TransferResult:
    """Ask Squad for the current status of a previously-submitted transfer.

    Used to upgrade our local PROCESSING transactions to SUCCESS or FAILED
    once Squad knows the terminal outcome.
    """
    url = f'{settings.squad_base_url}/payout/requery'
    payload = {'transaction_reference': reference}

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(url, headers=_headers(), json=payload)

    # Squad's requery semantics are partially conveyed by HTTP status code:
    #   200 success, 424 timeout-retry, 412 reversed, 4xx other failures.
    if response.status_code == 412:
        return TransferResult(reference=reference, status='reversed', message='Transaction reversed')
    if response.status_code == 424:
        return TransferResult(reference=reference, status='pending', message='Squad re-query timeout')
    if response.status_code not in (200, 201):
        raise ValueError(f'Requery failed (HTTP {response.status_code}): {response.text}')

    data = response.json() if response.content else {}
    logger.info('Squad requery %s -> HTTP %s, body=%s', reference, response.status_code, data)

    if data.get('success') is False:
        raise ValueError(f'Requery unsuccessful: {data.get("message")}')

    # If Squad returned 200 + success=true but no explicit status field, the
    # transfer is finalised — treat the HTTP code as the status indicator.
    status = _extract_status(data) or 'success'
    return TransferResult(
        reference=reference,
        status=status,
        message=_extract_message(data),
    )
