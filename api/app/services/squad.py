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

from typing import TypedDict

import httpx

from app.config import settings


class BankAccountInfo(TypedDict):
    account_name: str
    account_number: str
    bank_code: str


class TransferResult(TypedDict):
    reference: str
    status: str   # 'success' | 'pending' | 'failed' | 'reversed'
    message: str  # Squad-provided detail; useful for failure reasons


def _headers() -> dict[str, str]:
    return {
        'Authorization': f'Bearer {settings.squad_secret_key}',
        'Content-Type': 'application/json',
    }


async def lookup_bank_account(account_number: str, bank_code: str) -> BankAccountInfo:
    """Resolve the account name for a NUBAN account number and bank code.

    Used during registration (identity check) and before every payment
    (show recipient details to the user before they confirm).
    """
    url = f'{settings.squad_base_url}/payout/account/lookup'

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(
            url,
            headers=_headers(),
            params={'account_number': account_number, 'bank_code': bank_code},
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
    narration: str = 'Squad payment',
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
        'narration': narration,
        'currency_id': 'NGN',
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, headers=_headers(), json=payload)

    if response.status_code not in (200, 201):
        raise ValueError(f'Transfer failed: {response.text}')

    data = response.json()
    if not data.get('success'):
        raise ValueError(f'Transfer unsuccessful: {data.get("message")}')

    detail = data.get('data') or {}
    return TransferResult(
        reference=reference,
        status=str(detail.get('status', 'pending')).lower(),
        message=str(detail.get('message') or data.get('message') or ''),
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

    if response.status_code not in (200, 201):
        raise ValueError(f'Requery failed: {response.text}')

    data = response.json()
    if not data.get('success'):
        raise ValueError(f'Requery unsuccessful: {data.get("message")}')

    detail = data.get('data') or {}
    return TransferResult(
        reference=reference,
        status=str(detail.get('status', 'pending')).lower(),
        message=str(detail.get('message') or data.get('message') or ''),
    )