import logging

import httpx

from app.config import settings
from app.worker import celery_app

logger = logging.getLogger(__name__)

OTP_EXPIRY_MINUTES = 10


@celery_app.task(bind=True, max_retries=3, default_retry_delay=5)
def send_otp_sms(self, phone_number: str, otp: str) -> None:
    """
    Deliver an OTP via Twilio SMS.

    Retries up to 3 times with a 5-second delay on transient failures.
    In demo mode the OTP is logged and no network call is made.
    """
    if settings.twilio_demo_mode:
        logger.warning('DEMO MODE :::: OTP for %s: %s', phone_number, otp)
        return

    url = f'https://api.twilio.com/2010-04-01/Accounts/{settings.twilio_account_sid}/Messages.json'
    body = f'Your Squad verification code is: {otp}. It expires in {OTP_EXPIRY_MINUTES} minutes.'

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                url,
                data={'From': settings.twilio_from_number, 'To': phone_number, 'Body': body},
                auth=(settings.twilio_account_sid, settings.twilio_auth_token),
            )
        response.raise_for_status()

    except Exception as exc:
        logger.error('SMS delivery failed for %s: %s', phone_number, exc)
        raise self.retry(exc=exc)
