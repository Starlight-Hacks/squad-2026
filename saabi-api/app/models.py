from pydantic import BaseModel, Field
from typing import Optional

class CheckoutRequest(BaseModel):
    email: str
    amount: float  # Amount in Naira (converted to kobo internally)
    callback_url: Optional[str] = None
    customer_name: Optional[str] = None

class StaticVARequest(BaseModel):
    bvn: str
    name: str
    email: str
    dob: str  # DD/MM/YYYY
    mobile_num: str

class DynamicVARequest(BaseModel):
    amount: float
    duration_seconds: int = Field(..., alias="duration")
    email: str

    class Config:
        populate_by_name = True

class AccountLookupRequest(BaseModel):
    bank_code: str
    account_number: str

class TransferRequest(BaseModel):
    amount: float  # Amount in Naira (converted to kobo internally)
    bank_code: str
    account_number: str
    account_name: str
    remark: Optional[str] = "SAABI Payout"