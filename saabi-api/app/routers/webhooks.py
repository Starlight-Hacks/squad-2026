from __future__ import annotations

import json
import logging
from typing import Annotated, Any, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response, status

from pydantic import BaseModel
from sqlalchemy.orm import Session
from twilio.request_validator import RequestValidator

from app.config import settings
from app.database import load_database
from app.models.user import User
from app.services import funding as funding_service
from app.services import payments, whatsapp
from app.services import squad as squad_service
from app.services.intent_parser import Intent, IntentKind
from app.services.intent_parser import parse as parse_intent



router = APIRouter(prefix='/webhooks', tags=['webhooks'])
logger = logging.getLogger(__name__)




@router.post('/twilio/whatsapp')
async def whatsapp_inbound(
    request: Request,
    From: Annotated[str, Form()],
    Body: Annotated[str, Form()],
    MessageSid: Annotated[Optional[str], Form()] = None,
    db: Session = Depends(load_database),
):
    await _validate_signature(request)

    phone_number = _normalise_from(From)
    body = (Body or '').strip()

    logger.info('WhatsApp inbound sid=%s from=%s body=%r', MessageSid, phone_number, body)

    user: User | None = db.query(User).filter(User.phone_number == phone_number).first()
    if not user:
        return _twiml('This number is not registered with Squad. Visit our portal to sign up before sending payments.')
    if not user.phone_verified:
        return _twiml('Your phone number is not yet verified. Complete OTP verification first.')

    pending = payments.get_active_pending(db, user)
    intent = parse_intent(body)

    if pending:
        if intent.kind == IntentKind.CANCEL:
            return _twiml(payments.cancel_pending(db, user))
        if intent.kind == IntentKind.PCT_LIKE:
            return _twiml(await payments.confirm(db, user, body))
        return _twiml(
            'You have a pending transaction awaiting confirmation. '
            'Reply with your Payment Confirmation Token to send, or CANCEL to abort.'
        )

    return _twiml(await _dispatch_intent(db, user, intent, body))


async def _dispatch_intent(db: Session, user: User, intent: Intent, body: str) -> str:
    if intent.kind == IntentKind.PAYMENT:
        assert intent.amount is not None
        assert intent.account_number is not None
        assert intent.bank_code is not None
        assert intent.bank_name is not None
        return await payments.initiate(
            db,
            user,
            amount=intent.amount,
            recipient_account_number=intent.account_number,
            recipient_bank_code=intent.bank_code,
            recipient_bank_name=intent.bank_name,
            raw_message=body,
        )

    if intent.kind == IntentKind.GREETING:
        return _greeting_reply()

    if intent.kind == IntentKind.PAYMENT_INCOMPLETE:
        return _missing_field_reply(intent)

    if intent.kind == IntentKind.BALANCE:
        return payments.show_balance(db, user)

    if intent.kind == IntentKind.STATUS:
        return payments.show_status(db, user)

    if intent.kind == IntentKind.HELP:
        return payments.help_text()

    if intent.kind == IntentKind.CANCEL:
        return 'You have no pending transaction to cancel.'

    if intent.kind == IntentKind.PCT_LIKE:
        return 'You have no pending transaction. Start one with something like: "send 2500 naira to 0123456789 GTBank".'

    return 'I didn\'t understand that. Try: "send 2500 naira to 0123456789 GTBank", or reply HELP for options.'


def _greeting_reply() -> str:
    return (
        'Hi! I\'m your friendly personal assistant from SAABI!, what shall we do today?\n\nSend "HELP" to learn more.'
    )


def _missing_field_reply(intent: Intent) -> str:
    if intent.missing == 'account_number':
        return 'Please include the recipient 10-digit account number.'
    if intent.missing == 'amount':
        return 'Please include the amount in naira, e.g. "send 2500 naira to 0123456789 GTBank".'
    if intent.missing == 'bank':
        return 'Please include the recipient bank name (e.g. GTBank, Access, UBA).'
    return 'Your request is missing some information. Reply HELP for the format.'


def _twiml(message: str) -> Response:
    body = whatsapp.twiml_reply(message)
    logger.info('TwiML reply: %s', body)
    return Response(content=body, media_type='application/xml')


def _normalise_from(raw: str) -> str:
    """Twilio sends 'whatsapp:+234XXX' — strip the channel prefix."""
    if raw.startswith('whatsapp:'):
        return raw[len('whatsapp:') :]
    return raw


class SquadTransferEvent(BaseModel):
    """Loose schema for Squad transfer status callbacks.

    Squad's docs don't pin the exact payload shape for transfer webhooks,
    so we accept either flat or nested forms and pull what we need.
    """

    transaction_reference: Optional[str] = None
    reference: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None
    data: Optional[dict[str, Any]] = None


@router.post('/squad/requery/{reference}')
async def squad_manual_requery(
    reference: str,
    db: Session = Depends(load_database),
):
    """Manually re-query a transaction against Squad and reconcile our row.

    Gated to demo mode so it isn't exposed in production. Returns both Squad's
    raw status payload and the resulting internal status — useful while a
    sandbox sit in 'pending' and you want to know whether Squad believes the
    transfer actually completed.
    """
    if not settings.twilio_demo_mode:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    try:
        result = await squad_service.requery(reference)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f'Squad requery failed: {exc}',
        ) from exc

    tx = payments.apply_external_status(db, reference, result['status'], result.get('message'))
    return {
        'squad': result,
        'local_status': tx.status if tx else None,
        'local_reference': tx.reference if tx else None,
    }


@router.post('/squad/transfer')
async def squad_transfer_status(
    request: Request,
    db: Session = Depends(load_database),
):
    """Receive Squad's transfer-status callback and reconcile our row.

    Squad pushes terminal status (success / failed / reversed) to the URL
    configured in the merchant dashboard. We use it to flip a PROCESSING
    transaction to its final state without waiting for the user to ping us.

    A spoofed callback could mark a real transfer as reversed and refund the
    wallet, so we verify Squad's signature over the raw body before trusting it.
    """
    raw_body = await request.body()
    signature = request.headers.get('x-squad-signature')

    if not squad_service.verify_webhook_signature(raw_body, signature):
        logger.warning('Squad transfer webhook rejected: bad or missing signature.')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Squad signature.')

    try:
        event = SquadTransferEvent.model_validate_json(raw_body)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Webhook body is not valid JSON.',
        ) from exc

    detail = event.data or {}
    reference = (
        event.transaction_reference or event.reference or detail.get('transaction_reference') or detail.get('reference')
    )
    status_value = event.status or detail.get('status')
    message = event.message or detail.get('message')

    if not reference or not status_value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Webhook missing transaction_reference or status.',
        )

    tx = payments.apply_external_status(db, reference, status_value, message)
    if tx is None:
        logger.info('Squad webhook for unknown reference %s — ignoring', reference)
        return {'received': True, 'matched': False}

    logger.info('Squad webhook reconciled %s -> %s', reference, tx.status)
    return {'received': True, 'matched': True, 'status': tx.status}


def _extract_charge_fields(payload: dict[str, Any]) -> tuple[str | None, str | None, str | None, str | None]:
    """Pull (reference, status, squad_ref, message) out of a Squad charge webhook.

    Squad nests the useful bits under ``Body`` and sometimes mirrors them at
    the root, so we check both. ``reference`` is *our* funding reference — the
    value we generated at init time and passed to the modal.
    """
    body = payload.get('Body') if isinstance(payload.get('Body'), dict) else {}

    reference = body.get('transaction_ref') or body.get('transaction_reference') or payload.get('TransactionRef')
    status_value = body.get('transaction_status') or body.get('status') or payload.get('Event')
    squad_ref = body.get('gateway_ref') or body.get('id') or payload.get('TransactionRef')
    message = body.get('message') or payload.get('message')

    return reference, status_value, squad_ref, message


@router.post('/squad/charge')
async def squad_charge_status(
    request: Request,
    db: Session = Depends(load_database),
):
    """Receive Squad's collection webhook and credit the user's wallet.

    Fired after a user completes payment in Squad's modal. Unlike the transfer
    webhook, this one *mints* wallet balance, so we verify Squad's signature
    before trusting a single byte of it.
    """
    raw_body = await request.body()
    signature = request.headers.get('x-squad-signature')

    if not squad_service.verify_webhook_signature(raw_body, signature):
        logger.warning('Squad charge webhook rejected: bad or missing signature.')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Squad signature.')

    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Webhook body is not valid JSON.',
        ) from exc

    reference, status_value, squad_ref, message = _extract_charge_fields(payload)
    if not reference or not status_value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Webhook missing transaction reference or status.',
        )

    funding = funding_service.apply_charge_status(db, reference, status_value, squad_ref, message)
    if funding is None:
        logger.info('Squad charge webhook for unknown reference %s — ignoring', reference)
        return {'received': True, 'matched': False}

    logger.info('Squad charge webhook reconciled %s -> %s', reference, funding.status)
    return {'received': True, 'matched': True, 'status': funding.status}


async def _validate_signature(request: Request) -> None:
    if settings.twilio_demo_mode:
        return

    signature = request.headers.get('X-Twilio-Signature', '')
    if not signature:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Missing Twilio signature.')

    form = await request.form()
    params = {k: v for k, v in form.multi_items() if isinstance(v, str)}

    validator = RequestValidator(settings.twilio_auth_token)
    for candidate in _candidate_urls(request):
        if validator.validate(candidate, params, signature):
            return

    logger.warning('Twilio signature failed. Tried URLs: %s', list(_candidate_urls(request)))
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Twilio signature.')


def _candidate_urls(request: Request) -> list[str]:
    proto = request.headers.get('x-forwarded-proto', request.url.scheme)
    host = request.headers.get('x-forwarded-host') or request.headers.get('host') or request.url.netloc
    path_qs = request.url.path

    if request.url.query:
        path_qs = f'{path_qs}?{request.url.query}'

    urls = [
        f'{proto}://{host}{path_qs}',
        f'https://{host}{path_qs}',
        str(request.url),
    ]

    seen: set[str] = set()
    return [u for u in urls if not (u in seen or seen.add(u))]
