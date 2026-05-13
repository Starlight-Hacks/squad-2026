"""
Twilio inbound webhooks.

The WhatsApp endpoint is the entire user-facing surface for payments. It
must be:

* Cheap — Twilio retries on slow responses, so we keep DB work to the
  minimum needed for the next reply.
* Trustworthy — we validate Twilio signatures in production. Demo mode
  bypasses validation so local Bruno calls can exercise the flow.
* Stateful — the same user phone number on consecutive messages drives a
  two-step conversation (intent → PCT confirmation).
"""

from __future__ import annotations

import logging
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from twilio.request_validator import RequestValidator

from app.config import settings
from app.database import load_database
from app.models.user import User
from app.services import payments, whatsapp
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

    if intent.kind == IntentKind.PAYMENT_INCOMPLETE:
        return _missing_field_reply(intent)

    if intent.kind == IntentKind.BALANCE:
        return payments.show_balance(db, user)

    if intent.kind == IntentKind.HELP:
        return payments.help_text()

    if intent.kind == IntentKind.CANCEL:
        return 'You have no pending transaction to cancel.'

    if intent.kind == IntentKind.PCT_LIKE:
        return 'You have no pending transaction. Start one with something like: "send 2500 naira to 0123456789 GTBank".'

    return 'I didn\'t understand that. Try: "send 2500 naira to 0123456789 GTBank", or reply HELP for options.'


def _missing_field_reply(intent: Intent) -> str:
    if intent.missing == 'account_number':
        return 'Please include the recipient 10-digit account number.'
    if intent.missing == 'amount':
        return 'Please include the amount in naira, e.g. "send 2500 naira to 0123456789 GTBank".'
    if intent.missing == 'bank':
        return 'Please include the recipient bank name (e.g. GTBank, Access, UBA).'
    return 'Your request is missing some information. Reply HELP for the format.'


def _twiml(message: str) -> Response:
    return Response(content=whatsapp.twiml_reply(message), media_type='application/xml')


def _normalise_from(raw: str) -> str:
    """Twilio sends 'whatsapp:+234XXX' — strip the channel prefix."""
    if raw.startswith('whatsapp:'):
        return raw[len('whatsapp:') :]
    return raw


async def _validate_signature(request: Request) -> None:
    if settings.twilio_demo_mode:
        return

    signature = request.headers.get('X-Twilio-Signature', '')
    if not signature:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Missing Twilio signature.')

    form = await request.form()
    params = {k: v for k, v in form.multi_items() if isinstance(v, str)}
    url = str(request.url)

    validator = RequestValidator(settings.twilio_auth_token)
    if not validator.validate(url, params, signature):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Twilio signature.')
