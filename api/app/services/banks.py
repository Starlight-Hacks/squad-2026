"""
Bank name → NUBAN code resolution.

Users on WhatsApp type informal bank names ("GTBank", "first bank", "gtb").
We map a curated alias set to the canonical NUBAN code that Squad's payout
API accepts, plus a display name we echo back to the user for confirmation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Bank:
    code: str
    name: str


_BANKS: dict[str, Bank] = {
    'access bank': Bank('044', 'Access Bank'),
    'access': Bank('044', 'Access Bank'),
    'diamond bank': Bank('044', 'Access Bank'),
    'diamond': Bank('044', 'Access Bank'),
    'ecobank': Bank('050', 'Ecobank'),
    'eco bank': Bank('050', 'Ecobank'),
    'fidelity bank': Bank('070', 'Fidelity Bank'),
    'fidelity': Bank('070', 'Fidelity Bank'),
    'first bank': Bank('011', 'First Bank of Nigeria'),
    'firstbank': Bank('011', 'First Bank of Nigeria'),
    'fbn': Bank('011', 'First Bank of Nigeria'),
    'first bank of nigeria': Bank('011', 'First Bank of Nigeria'),
    'fcmb': Bank('214', 'FCMB'),
    'first city monument bank': Bank('214', 'FCMB'),
    'gtbank': Bank('058', 'GTBank'),
    'gtb': Bank('058', 'GTBank'),
    'gt bank': Bank('058', 'GTBank'),
    'guaranty trust': Bank('058', 'GTBank'),
    'guaranty trust bank': Bank('058', 'GTBank'),
    'heritage bank': Bank('030', 'Heritage Bank'),
    'heritage': Bank('030', 'Heritage Bank'),
    'jaiz bank': Bank('301', 'Jaiz Bank'),
    'jaiz': Bank('301', 'Jaiz Bank'),
    'keystone bank': Bank('082', 'Keystone Bank'),
    'keystone': Bank('082', 'Keystone Bank'),
    'kuda bank': Bank('50211', 'Kuda Bank'),
    'kuda': Bank('50211', 'Kuda Bank'),
    'moniepoint': Bank('50515', 'Moniepoint MFB'),
    'moniepoint mfb': Bank('50515', 'Moniepoint MFB'),
    'opay': Bank('999992', 'OPay'),
    'palmpay': Bank('999991', 'PalmPay'),
    'polaris bank': Bank('076', 'Polaris Bank'),
    'polaris': Bank('076', 'Polaris Bank'),
    'providus bank': Bank('101', 'Providus Bank'),
    'providus': Bank('101', 'Providus Bank'),
    'stanbic ibtc': Bank('221', 'Stanbic IBTC'),
    'stanbic': Bank('221', 'Stanbic IBTC'),
    'sterling bank': Bank('232', 'Sterling Bank'),
    'sterling': Bank('232', 'Sterling Bank'),
    'standard chartered': Bank('068', 'Standard Chartered'),
    'suntrust': Bank('100', 'SunTrust Bank'),
    'union bank': Bank('032', 'Union Bank'),
    'union': Bank('032', 'Union Bank'),
    'uba': Bank('033', 'UBA'),
    'united bank for africa': Bank('033', 'UBA'),
    'unity bank': Bank('215', 'Unity Bank'),
    'unity': Bank('215', 'Unity Bank'),
    'wema bank': Bank('035', 'Wema Bank'),
    'wema': Bank('035', 'Wema Bank'),
    'alat': Bank('035', 'Wema Bank'),
    'zenith bank': Bank('057', 'Zenith Bank'),
    'zenith': Bank('057', 'Zenith Bank'),
}


_BY_CODE: dict[str, Bank] = {b.code: b for b in _BANKS.values()}

# Match longest aliases first so "first bank" wins over "first".
_SORTED_ALIASES: list[str] = sorted(_BANKS.keys(), key=len, reverse=True)


def resolve(text: str) -> Bank | None:
    """Find the first bank alias mentioned in ``text``.

    Matching is case-insensitive and respects word boundaries so "wema" does
    not match "swematic". Longest aliases are tried first to avoid prefix
    collisions between, e.g., "first bank" and "first city monument bank".
    """
    haystack = text.lower()
    for alias in _SORTED_ALIASES:
        pattern = rf'(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])'
        if re.search(pattern, haystack):
            return _BANKS[alias]
    return None


def by_code(code: str) -> Bank | None:
    return _BY_CODE.get(code)
