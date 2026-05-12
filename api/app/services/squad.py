from typing import TypedDict

import httpx

from app.config import settings


class BankAccountInfo(TypedDict):
    account_name: str
    account_number: str
    bank_code: str


class VirtualAccountInfo(TypedDict):
    virtual_account_number: str
    bank_name: str
    account_name: str
    customer_id: str


def _headers() -> dict[str, str]:
    return {
        'Authorization': f'Bearer {settings.squad_secret_key}',
        'Content-Type': 'application/json',
    }


async def lookup_bank_account(account_number: str, bank_code: str) -> BankAccountInfo:
    """Look up the account name for a given NUBAN account number and bank code."""
    url = f'{settings.squad_base_url}/payout/account/lookup'
    params = {'account_number': account_number, 'bank_code': bank_code}

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(url, headers=_headers(), params=params)

    if response.status_code != 200:
        raise ValueError(f'Bank account lookup failed: {response.text}')

    data = response.json()

    if not data.get('success'):
        raise ValueError(f'Bank account lookup unsuccessful: {data.get("message")}')

    account_data = data['data']
    return BankAccountInfo(
        account_name=account_data['account_name'],
        account_number=account_number,
        bank_code=bank_code,
    )


async def create_virtual_account(
    first_name: str,
    last_name: str,
    mobile_num: str,
    email: str,
    bvn: str,
    date_of_birth: str,
    address: str,
    gender: str,
    customer_identifier: str,
) -> VirtualAccountInfo:
    """Create a Squad virtual account for a verified user."""
    url = f'{settings.squad_base_url}/virtual-account'
    payload = {
        'first_name': first_name,
        'last_name': last_name,
        'mobile_num': mobile_num,
        'email': email,
        'bvn': bvn,
        'dob': date_of_birth,
        'address': address,
        'gender': gender,
        'customer_identifier': customer_identifier,
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(url, headers=_headers(), json=payload)

    if response.status_code not in (200, 201):
        raise ValueError(f'Virtual account creation failed: {response.text}')

    data = response.json()
    if not data.get('success'):
        raise ValueError(f'Virtual account creation unsuccessful: {data.get("message")}')

    account_data = data['data']
    return VirtualAccountInfo(
        virtual_account_number=account_data['virtual_account_number'],
        bank_name=account_data.get('bank_name', 'GTBank'),
        account_name=f'{first_name} {last_name}',
        customer_id=account_data.get('customer_id', customer_identifier),
    )
