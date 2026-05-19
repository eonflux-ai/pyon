# --------------------------------------------------------------------------------------------- #
"""Resilience contracts for datetime encoder helpers."""
# --------------------------------------------------------------------------------------------- #

from datetime import datetime, time, timedelta, timezone
from typing import Any, cast
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# --------------------------------------------------------------------------------------------- #

import pyon.encoders.datetime_types as dt_module

# --------------------------------------------------------------------------------------------- #

from pyon.encoders.datetime_types import DateEnc
from pyon.supported_types import SupportedTypes
from pyon.utils import EConst

# --------------------------------------------------------------------------------------------- #


def test_datetime_decoder_fallbacks_to_offset_when_zone_is_unknown(monkeypatch):
    """Zone lookup failure should still preserve offset-based timezone."""

    # 1. Prepares payload with explicit zone+offset...
    value = {
        EConst.TYPE: SupportedTypes.DATETIME.value,
        EConst.DATA: "2025-01-01T10:00:00",
        EConst.AUX1: {
            EConst.TZ_ZONE: "Invalid/Zone",
            EConst.TZ_OFFSET: "+02:30",
            EConst.TZ_FOLD: 1,
        },
    }

    # 2. Forces zone lookup failure...
    def _raise_zoneinfo(_):
        raise ZoneInfoNotFoundError("zone missing")

    monkeypatch.setattr("pyon.encoders.datetime_types.ZoneInfo", _raise_zoneinfo)

    # 3. Decodes...
    output = DateEnc().decode(value)

    # 4. Validates output type...
    assert isinstance(output, datetime)

    # 5. Validates offset and fold...
    assert output.utcoffset() == timedelta(hours=2, minutes=30)
    assert getattr(output, "fold", 0) == 1


# --------------------------------------------------------------------------------------------- #


def test_datetime_helpers_reject_invalid_inputs():
    """Datetime helper methods should reject invalid values without exceptions."""

    # 1. Prepares helper...
    dt = DateEnc()

    # 2. Prepares dynamic helper...
    inner = cast(Any, dt)

    # 3. Validates encode defensive branches...
    assert getattr(inner, "_encode_date")(cast(Any, "bad")) is None
    assert getattr(inner, "_encode_datetime")(cast(Any, "bad")) is None
    assert getattr(inner, "_encode_time")(cast(Any, "bad")) is None

    # 4. Covers datetime offset-only attach...
    out_dt = getattr(inner, "_decode_datetime")(
        {
            EConst.TYPE: SupportedTypes.DATETIME.value,
            EConst.DATA: "2025-01-01T10:00:00",
            EConst.AUX1: {EConst.TZ_OFFSET: "+01:15"},
        }
    )
    assert out_dt is not None and out_dt.utcoffset() == timedelta(hours=1, minutes=15)

    # 5. Covers time encode branch...
    out_time = getattr(inner, "_encode_time")(datetime.now(timezone.utc).timetz())
    assert isinstance(out_time, dict) and EConst.AUX1 in out_time

    # 6. Covers time decode branch...
    dec_time = getattr(inner, "_decode_time")(
        {
            EConst.TYPE: SupportedTypes.TIME.value,
            EConst.DATA: "10:00:00",
            EConst.AUX1: {EConst.TZ_OFFSET: "-02:00"},
        }
    )
    assert dec_time is not None and dec_time.utcoffset() == timedelta(hours=-2)

    # 7. Covers fallback on invalid fold...
    getattr(inner, "_decode_datetime")(
        {
            EConst.TYPE: SupportedTypes.DATETIME.value,
            EConst.DATA: "2025-01-01T10:00:00",
            EConst.AUX1: {EConst.TZ_OFFSET: "+00:00", EConst.TZ_FOLD: 9},
        }
    )


# --------------------------------------------------------------------------------------------- #


def test_datetime_decode_attach_zone_when_input_is_naive():
    """Decoding with valid TZ zone should attach tzinfo on naive datetime payloads."""

    # 1. Prepares naive datetime payload with region metadata...
    payload = {
        EConst.TYPE: SupportedTypes.DATETIME.value,
        EConst.DATA: "2025-01-01T10:00:00",
        EConst.AUX1: {EConst.TZ_ZONE: "UTC"},
    }

    # 2. Decodes and validates zone attachment...
    output = getattr(cast(Any, DateEnc()), "_decode_datetime")(payload)
    assert output is not None
    assert output.tzinfo is not None


# --------------------------------------------------------------------------------------------- #


def test_datetime_decode_ignores_invalid_fold_replace(monkeypatch):
    """Fold replace failures must not break decode flow."""

    # 1. Builds fake datetime object...
    class _FakeDateTimeValue:  # pylint: disable=too-few-public-methods
        tzinfo = None

        def replace(self, **kwargs):
            """Mimics datetime.replace with fold failure."""
            if "fold" in kwargs:
                raise ValueError("invalid fold")
            return self

        def astimezone(self, _zone):
            """Mimics astimezone without conversion."""
            return self

    # 2. Builds fake datetime class...
    class _FakeDateTimeClass:  # pylint: disable=too-few-public-methods
        @staticmethod
        def fromisoformat(_value):
            """Returns fake datetime object."""
            return _FakeDateTimeValue()

    # 3. Patches datetime class...
    monkeypatch.setattr(dt_module, "datetime", _FakeDateTimeClass)

    # 4. Prepares fold payload...
    payload = {
        EConst.TYPE: SupportedTypes.DATETIME.value,
        EConst.DATA: "2025-01-01T10:00:00",
        EConst.AUX1: {EConst.TZ_OFFSET: "+00:00", EConst.TZ_FOLD: 1},
    }

    # 5. Decodes payload...
    output = getattr(cast(Any, DateEnc()), "_decode_datetime")(payload)

    # 6. Validates graceful handling...
    assert output is not None


# --------------------------------------------------------------------------------------------- #


def test_datetime_time_zone_metadata_roundtrip_paths(monkeypatch):
    """Time encode/decode should preserve zone metadata and fallback to offset when needed."""

    # 1. Encodes aware time...
    value = time(10, 20, 30, tzinfo=ZoneInfo("UTC"))
    encoded = getattr(cast(Any, DateEnc()), "_encode_time")(value)

    # 2. Validates zone metadata...
    assert isinstance(encoded, dict)
    assert EConst.TZ_ZONE in encoded[EConst.AUX1]

    # 3. Prepares offset fallback payload...
    payload = {
        EConst.TYPE: SupportedTypes.TIME.value,
        EConst.DATA: "10:00:00",
        EConst.AUX1: {EConst.TZ_ZONE: "Invalid/Zone", EConst.TZ_OFFSET: "+03:00"},
    }

    def _raise_zoneinfo(_):
        raise ZoneInfoNotFoundError("zone missing")

    # 4. Forces zone lookup failure...
    monkeypatch.setattr("pyon.encoders.datetime_types.ZoneInfo", _raise_zoneinfo)
    decoded = getattr(cast(Any, DateEnc()), "_decode_time")(payload)

    # 5. Validates offset fallback...
    assert decoded is not None
    assert decoded.utcoffset() == timedelta(hours=3)


# --------------------------------------------------------------------------------------------- #
