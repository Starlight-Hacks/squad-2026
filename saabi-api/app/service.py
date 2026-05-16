import os
import time
import random
import hmac
import hashlib
import httpx
from typing import Optional, Dict, Any

SQUAD_API_KEY = os.getenv("SQUAD_API_KEY", "")
SQUAD_BASE_URL = os.getenv("SQUAD_BASE_URL", "https://sandbox-api-d.squadco.com")

class SquadService:
    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=SQUAD_BASE_URL,
            headers={
                "Authorization": f"Bearer {SQUAD_API_KEY}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    async def initiate_payment(self, email: str, amount_kobo: int, callback_url: Optional[str] = None, customer_name: Optional[str] = None) -> Dict[str, Any]:
        payload = {
            "email": email,
            "amount": str(amount_kobo),
            "currency": "NGN",
            "initiate_type": "inline",
            "transaction_ref": f"SB_{int(time.time() * 1000)}_{random.randint(100, 999)}",
            "callback_url": callback_url or "",
            "customer_name": customer_name or "",
            "pass_charge": False,
        }
        resp = await self.client.post("/transaction/initiate", json=payload)
        resp.raise_for_status()
        return resp.json()

    async def verify_transaction(self, transaction_ref: str) -> Dict[str, Any]:
        resp = await self.client.get(f"/transaction/verify/{transaction_ref}")
        resp.raise_for_status()
        return resp.json()

    async def create_static_virtual_account(self, bvn: str, name: str, email: str, dob: str, mobile_num: str) -> Dict[str, Any]:
        payload = {
            "bvn": bvn,
            "name": name,
            "email": email,
            "dob": dob,
            "mobile_num": mobile_num,
        }
        resp = await self.client.post("/virtual-account", json=payload)
        resp.raise_for_status()
        return resp.json()

    async def create_dynamic_virtual_account(self, amount: float, duration_seconds: int, email: str) -> Dict[str, Any]:
        payload = {
            "amount": amount,
            "duration": duration_seconds,
            "email": email,
            "transaction_ref": f"SB_DVA_{int(time.time() * 1000)}"
        }
        resp = await self.client.post("/virtual-account/initiate-dynamic-virtual-account", json=payload)
        resp.raise_for_status()
        return resp.json()

    async def account_lookup(self, bank_code: str, account_number: str) -> Dict[str, Any]:
        payload = {
            "bank_code": bank_code,
            "account_number": account_number,
        }
        resp = await self.client.post("/payout/account/lookup", json=payload)
        resp.raise_for_status()
        return resp.json()

    async def transfer_out(self, amount_kobo: int, bank_code: str, account_number: str, account_name: str, remark: str) -> Dict[str, Any]:
        payload = {
            "transaction_reference": f"SB_TRF_{int(time.time() * 1000)}",
            "amount": str(amount_kobo),
            "bank_code": bank_code,
            "account_number": account_number,
            "account_name": account_name,
            "currency_id": "NGN",
            "remark": remark,
        }
        resp = await self.client.post("/payout/transfer", json=payload)
        resp.raise_for_status()
        return resp.json()

    def validate_webhook_signature(self, payload: bytes, x_squad_signature: str) -> bool:
        secret = SQUAD_API_KEY.encode("utf-8")
        hash_obj = hmac.new(secret, payload, hashlib.sha512)
        computed = hash_obj.hexdigest().upper()
        return computed == x_squad_signature.upper()