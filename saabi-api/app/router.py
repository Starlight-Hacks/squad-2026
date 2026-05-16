from fastapi import APIRouter, HTTPException, Request, Header
from .squad_service import SquadService
from .models import (
    CheckoutRequest, StaticVARequest, DynamicVARequest,
    AccountLookupRequest, TransferRequest
)
import traceback

router = APIRouter(prefix="/api/squad", tags=["Squad API"])
service = SquadService()

@router.post("/checkout")
async def initiate_checkout(data: CheckoutRequest):
    try:
        amount_kobo = round(data.amount * 100)
        result = await service.initiate_payment(
            email=data.email,
            amount_kobo=amount_kobo,
            callback_url=data.callback_url,
            customer_name=data.customer_name
        )
        return {"status": "success", "data": result.get("data", result)}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Checkout initiation failed: {str(e)}")

@router.get("/verify/{ref}")
async def verify_transaction(ref: str):
    try:
        result = await service.verify_transaction(ref)
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")

@router.post("/va/static")
async def create_static_va(data: StaticVARequest):
    try:
        result = await service.create_static_virtual_account(
            bvn=data.bvn,
            name=data.name,
            email=data.email,
            dob=data.dob,
            mobile_num=data.mobile_num
        )
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to create Static Virtual Account: {str(e)}")

@router.post("/va/dynamic")
async def create_dynamic_va(data: DynamicVARequest):
    try:
        result = await service.create_dynamic_virtual_account(
            amount=data.amount,
            duration_seconds=data.duration_seconds,
            email=data.email
        )
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to create Dynamic Virtual Account: {str(e)}")

@router.post("/lookup")
async def account_lookup(data: AccountLookupRequest):
    try:
        result = await service.account_lookup(
            bank_code=data.bank_code,
            account_number=data.account_number
        )
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Account lookup failed: {str(e)}")

@router.post("/payout")
async def transfer_funds(data: TransferRequest):
    try:
        amount_kobo = round(data.amount * 100)

        # Implicit lookup for security (name must match)
        lookup = await service.account_lookup(data.bank_code, data.account_number)
        lookup_data = lookup.get("data", {})
        if not lookup_data or lookup_data.get("account_name") != data.account_name:
            raise HTTPException(
                status_code=400, 
                detail="Account Name lookup mismatch. Transfer blocked for security."
            )

        result = await service.transfer_out(
            amount_kobo=amount_kobo,
            bank_code=data.bank_code,
            account_number=data.account_number,
            account_name=data.account_name,
            remark=data.remark or "SAABI Payout"
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Transfer failed: {str(e)}")

@router.post("/webhook")
async def handle_webhook(request: Request, x_squad_encrypted_body: Optional[str] = Header(None)):
    try:
        raw_body = await request.body()
        signature = x_squad_encrypted_body or ""

        if not signature or not service.validate_webhook_signature(raw_body, signature):
            raise HTTPException(status_code=401, detail="Invalid Source")

        import json
        event = json.loads(raw_body)
        print("Squad Webhook Received Event:", event.get("Event"), event.get("TransactionRef"))

        # Always acknowledge 200 per Squad requirement
        # Post-acknowledge processing (e.g., update DB) would go here
        return {"status": "success", "message": "Webhook Processed"}
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")