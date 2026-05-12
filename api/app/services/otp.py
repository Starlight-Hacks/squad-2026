"""
Consuming the OTP (verify_and_consume) atomically deletes the key so the
same code cannot be replayed.
"""

import hashlib
import random
import string

import redis

from app.config import settings

OTP_EXPIRY_SECONDS = 600


def _redis() -> redis.Redis:
    return redis.from_url(settings.redis_url, decode_responses=True)


def generate_otp() -> str:
    return ''.join(random.choices(string.digits, k=6))


def _hash(code: str) -> str:
    return hashlib.sha256(code.encode()).hexdigest()


def store_otp(phone_number: str, code: str) -> None:
    """Hash and store the OTP in Redis with a TTL."""
    _redis().setex(f'otp:{phone_number}', OTP_EXPIRY_SECONDS, _hash(code))


def verify_and_consume(phone_number: str, code: str) -> bool:
    """Return True and delete the key if the code matches; False otherwise.

    Uses a pipeline so the get + delete is atomic from the caller's perspective.
    """
    r = _redis()
    key = f'otp:{phone_number}'
    stored = r.get(key)
    if stored is None:
        return False
    if _hash(code) != stored:
        return False
    r.delete(key)
    return True
