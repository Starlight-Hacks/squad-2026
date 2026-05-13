"""
Squad Co API integration.

Squad is used solely as a payment rail, we manage user wallets and balances
internally. Squad handles:
  - Bank account name lookup   (used during registration to verify identity)
  - Outbound transfers         (used when a user sends money via WhatsApp)
"""

import json
from typing import TypedDict

import httpx

from app.config import settings
from app.utils import logger


class BankAccountInfo(TypedDict):
    account_name: str
    account_number: str
    bank_code: str


class TransferResult(TypedDict):
    reference: str
    status: str  # 'success' | 'pending' | 'failed'


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
        response = await client.post(
            url,
            headers=_headers(),
            json={'account_number': account_number, 'bank_code': bank_code},
        )

    if response.status_code != 200:
        # logger.info(f'Account lookup failed, returned\n: {json.loads(response.text)}')
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
        'account_name': '',  # populated by the caller after lookup
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

    return TransferResult(
        reference=reference,
        status=data['data'].get('status', 'pending'),
    )
