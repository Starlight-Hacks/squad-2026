import hashlib
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import load_database
from app.models.payment_confirmation_token import PaymentConfirmationToken
from app.models.user import User
from app.models.virtual_account import VirtualAccount
from app.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    SetPCTRequest,
    SetPCTResponse,
    VerifyOTPRequest,
    VerifyOTPResponse,
    VirtualAccountDetails,
)
from app.services import otp as otp_service
from app.services import pct as pct_service
from app.services import squad as squad_service
from app.tasks.whatsapp import send_otp_whatsapp

router = APIRouter(prefix='/auth', tags=['auth'])
logger = logging.getLogger(__name__)


@router.post('/register', response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(load_database)):
    """Step 1: Register a new user and dispatch an OTP via Celery."""

    existing = db.query(User).filter(User.phone_number == payload.phone_number).first()
    if existing and existing.phone_verified:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='A verified account already exists for this phone number.',
        )

    bvn_hash = hashlib.sha256(payload.bvn.encode()).hexdigest()

    if existing:
        user = existing
        user.first_name = payload.first_name
        user.last_name = payload.last_name
        user.email = payload.email
        user.date_of_birth = payload.date_of_birth
        user.address = payload.address
        user.gender = payload.gender
        user.bvn_hash = bvn_hash
        user.account_number = payload.account_number
        user.bank_code = payload.bank_code
        user.geo_lat = payload.geo_lat
        user.geo_lng = payload.geo_lng
    else:
        user = User(
            phone_number=payload.phone_number,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            date_of_birth=payload.date_of_birth,
            address=payload.address,
            gender=payload.gender,
            bvn_hash=bvn_hash,
            bvn_verified=False,
            phone_verified=False,
            account_number=payload.account_number,
            bank_code=payload.bank_code,
            geo_lat=payload.geo_lat,
            geo_lng=payload.geo_lng,
        )
        db.add(user)

    db.commit()

    code = otp_service.generate_otp()
    otp_service.store_otp(payload.phone_number, code)

    # basedpyright lsp issues, we can ignore them.
    send_otp_whatsapp.delay(payload.phone_number, code)  # pyright: ignore[reportFunctionMemberAccess]

    return RegisterResponse(
        message='OTP sent to your phone number. Please verify within 10 minutes.',
        phone_number=payload.phone_number,
    )


@router.post('/verify-otp', response_model=VerifyOTPResponse)
async def verify_otp(payload: VerifyOTPRequest, db: Session = Depends(load_database)):
    """Step 2: Verify OTP, validate bank account, create Squad virtual account."""

    user: User | None = db.query(User).filter(User.phone_number == payload.phone_number).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')

    if user.phone_verified:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Phone number is already verified.',
        )

    if not otp_service.verify_and_consume(payload.phone_number, payload.otp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid or expired OTP.',
        )

    if hashlib.sha256(payload.bvn.encode()).hexdigest() != user.bvn_hash:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Supplied BVN does not match the registered BVN.',
        )

    try:
        bank_info = await squad_service.lookup_bank_account(user.account_number, user.bank_code)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Bank account verification failed: {exc}',
        ) from exc

    name_ok = (
        user.first_name.upper() in bank_info['account_name'].upper()
        and user.last_name.upper() in bank_info['account_name'].upper()
    )
    if not name_ok:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f'Bank account name "{bank_info["account_name"]}" does not match '
                f'the registered name "{user.first_name} {user.last_name}".'
            ),
        )

    user.bvn_verified = True

    try:
        va_info = await squad_service.create_virtual_account(
            first_name=user.first_name,
            last_name=user.last_name,
            mobile_num=user.phone_number,
            email=user.email,
            bvn=payload.bvn,
            date_of_birth=user.date_of_birth,
            address=user.address,
            gender=user.gender,
            customer_identifier=str(user.id),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f'Virtual account creation failed: {exc}',
        ) from exc

    db.add(
        VirtualAccount(
            user_id=user.id,
            virtual_account_number=va_info['virtual_account_number'],
            bank_name=va_info['bank_name'],
            account_name=va_info['account_name'],
            squad_customer_id=va_info['customer_id'],
        )
    )
    user.phone_verified = True
    db.commit()

    return VerifyOTPResponse(
        message='Phone verified and virtual account created. Please set your Payment Confirmation Token.',
        virtual_account=VirtualAccountDetails(
            virtual_account_number=va_info['virtual_account_number'],
            bank_name=va_info['bank_name'],
            account_name=va_info['account_name'],
        ),
        twilio_join_code=settings.twilio_join_code,
        twilio_whatsapp_number=settings.twilio_whatsapp_number,
        next_step='POST /auth/set-pct with your chosen Payment Confirmation Token.',
    )


@router.post('/set-pct', response_model=SetPCTResponse)
def set_pct(payload: SetPCTRequest, db: Session = Depends(load_database)):
    user: User | None = db.query(User).filter(User.phone_number == payload.phone_number).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')

    if not user.phone_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Phone number is not yet verified.',
        )

    salt = pct_service.generate_salt()
    token_hash = pct_service.hash_pct(payload.pct, salt)

    existing_pct = db.query(PaymentConfirmationToken).filter(PaymentConfirmationToken.user_id == user.id).first()
    if existing_pct:
        existing_pct.token_hash = token_hash
        existing_pct.token_salt = salt
    else:
        db.add(PaymentConfirmationToken(user_id=user.id, token_hash=token_hash, token_salt=salt))

    db.commit()

    return SetPCTResponse(message='Payment Confirmation Token set successfully. Registration complete.')
