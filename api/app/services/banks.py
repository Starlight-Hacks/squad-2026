"""
Bank name → Squad bank-code resolution.

Users on WhatsApp type informal bank names ("GTBank", "first bank", "gtb").
We map a curated alias set to the canonical Squad bank code accepted by the
payout API, plus a display name we echo back to the user for confirmation.

Codes follow Squad's bank list, not standard NUBAN codes (e.g. GTBank is
``000013`` here, not ``058``). The set below covers the commercial banks,
the major digital/neobanks and the payment-service banks Nigerian users
most commonly reference; microfinance and mortgage banks are intentionally
excluded because users rarely refer to them by short aliases.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Bank:
    code: str
    name: str


_BANKS: dict[str, Bank] = {
    # ── Commercial banks ──────────────────────────────────────────────
    'sterling bank': Bank('000001', 'Sterling Bank'),
    'sterling': Bank('000001', 'Sterling Bank'),
    'keystone bank': Bank('000002', 'Keystone Bank'),
    'keystone': Bank('000002', 'Keystone Bank'),
    'fcmb': Bank('000003', 'FCMB'),
    'first city monument bank': Bank('000003', 'FCMB'),
    'uba': Bank('000004', 'United Bank for Africa'),
    'united bank for africa': Bank('000004', 'United Bank for Africa'),
    'diamond bank': Bank('000005', 'Diamond Bank'),
    'diamond': Bank('000005', 'Diamond Bank'),
    'jaiz bank': Bank('000006', 'JAIZ Bank'),
    'jaiz': Bank('000006', 'JAIZ Bank'),
    'fidelity bank': Bank('000007', 'Fidelity Bank'),
    'fidelity': Bank('000007', 'Fidelity Bank'),
    'polaris bank': Bank('000008', 'Polaris Bank'),
    'polaris': Bank('000008', 'Polaris Bank'),
    'citi bank': Bank('000009', 'Citi Bank'),
    'citibank': Bank('000009', 'Citi Bank'),
    'ecobank': Bank('000010', 'Ecobank Bank'),
    'eco bank': Bank('000010', 'Ecobank Bank'),
    'unity bank': Bank('000011', 'Unity Bank'),
    'unity': Bank('000011', 'Unity Bank'),
    'stanbic ibtc': Bank('000012', 'StanbicIBTC Bank'),
    'stanbic ibtc bank': Bank('000012', 'StanbicIBTC Bank'),
    'stanbic': Bank('000012', 'StanbicIBTC Bank'),
    'stanbicibtc': Bank('000012', 'StanbicIBTC Bank'),
    'gtbank': Bank('000013', 'GTBank Plc'),
    'gtb': Bank('000013', 'GTBank Plc'),
    'gt bank': Bank('000013', 'GTBank Plc'),
    'guaranty trust': Bank('000013', 'GTBank Plc'),
    'guaranty trust bank': Bank('000013', 'GTBank Plc'),
    'access bank': Bank('000014', 'Access Bank'),
    'access': Bank('000014', 'Access Bank'),
    'zenith bank': Bank('000015', 'Zenith Bank Plc'),
    'zenith': Bank('000015', 'Zenith Bank Plc'),
    'first bank': Bank('000016', 'First Bank of Nigeria'),
    'firstbank': Bank('000016', 'First Bank of Nigeria'),
    'first bank of nigeria': Bank('000016', 'First Bank of Nigeria'),
    'fbn': Bank('000016', 'First Bank of Nigeria'),
    'wema bank': Bank('000017', 'Wema Bank'),
    'wema': Bank('000017', 'Wema Bank'),
    'alat': Bank('000017', 'Wema Bank'),
    'union bank': Bank('000018', 'Union Bank'),
    'union': Bank('000018', 'Union Bank'),
    'enterprise bank': Bank('000019', 'Enterprise Bank'),
    'heritage bank': Bank('000020', 'Heritage'),
    'heritage': Bank('000020', 'Heritage'),
    'standard chartered': Bank('000021', 'Standard Chartered'),
    'standard chartered bank': Bank('000021', 'Standard Chartered'),
    'suntrust bank': Bank('000022', 'Suntrust Bank'),
    'suntrust': Bank('000022', 'Suntrust Bank'),
    'providus bank': Bank('000023', 'Providus Bank'),
    'providus': Bank('000023', 'Providus Bank'),
    'rand merchant bank': Bank('000024', 'Rand Merchant Bank'),
    'titan trust bank': Bank('000025', 'Titan Trust Bank'),
    'titan trust': Bank('000025', 'Titan Trust Bank'),
    'taj bank': Bank('000026', 'Taj Bank'),
    'taj': Bank('000026', 'Taj Bank'),
    'globus bank': Bank('000027', 'Globus Bank'),
    'globus': Bank('000027', 'Globus Bank'),
    'lotus bank': Bank('000029', 'Lotus Bank'),
    'lotus': Bank('000029', 'Lotus Bank'),
    'premium trust bank': Bank('000031', 'Premium Trust Bank'),
    'premium trust': Bank('000031', 'Premium Trust Bank'),
    'enaira': Bank('000033', 'eNaira'),
    'signature bank': Bank('000034', 'Signature Bank'),
    'optimus bank': Bank('000036', 'Optimus Bank'),
    'optimus': Bank('000036', 'Optimus Bank'),

    # ── Digital / neobanks (consumer-facing MFBs) ─────────────────────
    'kuda bank': Bank('090267', 'Kuda Microfinance Bank'),
    'kuda': Bank('090267', 'Kuda Microfinance Bank'),
    'sparkle bank': Bank('090325', 'Sparkle'),
    'sparkle': Bank('090325', 'Sparkle'),
    'eyowo': Bank('090328', 'Eyowo'),
    'vfd mfb': Bank('090110', 'VFD MFB'),
    'vfd': Bank('090110', 'VFD MFB'),
    'renmoney': Bank('090198', 'RenMoney Microfinance Bank'),
    'ren money': Bank('090198', 'RenMoney Microfinance Bank'),
    'fairmoney': Bank('090551', 'FairMoney Microfinance Bank'),
    'fair money': Bank('090551', 'FairMoney Microfinance Bank'),
    'mintyn': Bank('090281', 'MintFinex Microfinance Bank'),
    'mintfinex': Bank('090281', 'MintFinex Microfinance Bank'),
    'lapo': Bank('090177', 'Lapo Microfinance Bank'),
    'lapo mfb': Bank('090177', 'Lapo Microfinance Bank'),
    'accion': Bank('090134', 'Accion Microfinance Bank'),
    'accion mfb': Bank('090134', 'Accion Microfinance Bank'),
    'mkobo': Bank('090455', 'Mkobo Microfinance Bank'),
    'mkobo mfb': Bank('090455', 'Mkobo Microfinance Bank'),
    'ab microfinance': Bank('090270', 'AB Microfinance Bank'),
    'ab mfb': Bank('090270', 'AB Microfinance Bank'),
    'bowen': Bank('090148', 'Bowen Microfinance Bank'),
    'bowen mfb': Bank('090148', 'Bowen Microfinance Bank'),
    'nirsal': Bank('090194', 'NIRSAL Microfinance Bank'),
    'nirsal mfb': Bank('090194', 'NIRSAL Microfinance Bank'),
    'mutual trust': Bank('090151', 'Mutual Trust Microfinance Bank'),
    'mutual trust mfb': Bank('090151', 'Mutual Trust Microfinance Bank'),
    'mutual benefits': Bank('090190', 'Mutual Benefits Microfinance Bank'),
    'page financials': Bank('070008', 'Page Financials'),
    'page': Bank('070008', 'Page Financials'),
    'fast credit': Bank('050009', 'Fast Credit'),
    'fastcredit': Bank('050009', 'Fast Credit'),
    'branch': Bank('050006', 'Branch International Financial Services'),
    'branch international': Bank('050006', 'Branch International Financial Services'),
    'boi mfb': Bank('090444', 'BOI Microfinance Bank'),
    'safe haven': Bank('090286', 'Safe Haven Microfinance Bank'),
    'safehaven': Bank('090286', 'Safe Haven Microfinance Bank'),

    # ── Bank-mobile wallets ───────────────────────────────────────────
    'stanbic ease': Bank('100007', 'Stanbic IBTC @ease wallet'),
    'stanbic @ease': Bank('100007', 'Stanbic IBTC @ease wallet'),
    'gtmobile': Bank('100009', 'GTMobile'),
    'gt mobile': Bank('100009', 'GTMobile'),
    'fcmb easy': Bank('100031', 'FCMB Easy Account'),
    'fcmb easy account': Bank('100031', 'FCMB Easy Account'),
    'access yello': Bank('100052', 'Access Yello'),
    'fidelity mobile': Bank('100019', 'Fidelity Mobile'),
    'fbn mobile': Bank('100014', 'FBNMobile'),
    'fbnmobile': Bank('100014', 'FBNMobile'),
    'zenith eazy': Bank('100034', 'Zenith Eazy Wallet'),
    'zenith mobile': Bank('100018', 'ZenithMobile'),
    'ecobank xpress': Bank('100008', 'Ecobank Xpress Account'),
    'kegow': Bank('100036', 'Kegow (Chamsmobile)'),
    'nownow': Bank('100032', 'Contec Global Infotech Limited (NowNow)'),
    'now now': Bank('100032', 'Contec Global Infotech Limited (NowNow)'),

    # ── Payment service banks & standalone wallets ────────────────────
    'opay': Bank('100004', 'Opay Digital Services LTD'),
    'o pay': Bank('100004', 'Opay Digital Services LTD'),
    'palmpay': Bank('100033', 'PalmPay Limited'),
    'palm pay': Bank('100033', 'PalmPay Limited'),
    'paga': Bank('100002', 'Paga'),
    'gomoney': Bank('100022', 'GoMoney'),
    'go money': Bank('100022', 'GoMoney'),
    '9psb': Bank('120001', '9Payment Service Bank'),
    '9 psb': Bank('120001', '9Payment Service Bank'),
    '9mobile psb': Bank('120001', '9Payment Service Bank'),
    'hopepsb': Bank('120002', 'HopePSB'),
    'hope psb': Bank('120002', 'HopePSB'),
    'momo psb': Bank('120003', 'MoMo PSB'),
    'momo': Bank('120003', 'MoMo PSB'),
    'smartcash psb': Bank('120004', 'SmartCash PSB'),
    'smartcash': Bank('120004', 'SmartCash PSB'),
    'smart cash': Bank('120004', 'SmartCash PSB'),
}


_BY_CODE: dict[str, Bank] = {b.code: b for b in _BANKS.values()}

# Match longest aliases first so multi-word names ("first city monument bank")
# beat single-word prefixes ("first bank").
_SORTED_ALIASES: list[str] = sorted(_BANKS.keys(), key=len, reverse=True)


def resolve(text: str) -> Bank | None:
    """Find the first bank alias mentioned in ``text``.

    Matching is case-insensitive and respects token boundaries so "wema" does
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
