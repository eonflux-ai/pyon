# --------------------------------------------------------------------------------------------- #
"""Shared assertions for API round-trip tests."""
# --------------------------------------------------------------------------------------------- #

from typing import Any, cast

# --------------------------------------------------------------------------------------------- #

import pandas as pd
import pytest

# --------------------------------------------------------------------------------------------- #

import pyon

# --------------------------------------------------------------------------------------------- #


def assert_datetime_frame_round_trip(df_in: pd.DataFrame, df_out: pd.DataFrame):
    """Checks DataFrame shape, columns, and timezone-normalized equality."""

    # 1. Assert basic type...
    assert isinstance(df_out, pd.DataFrame)

    # 2. Assert shape and columns...
    assert list(df_out.columns) == list(df_in.columns)
    assert df_out.shape == df_in.shape

    # 3. Compare aligned or plain...
    if has_datetime_tz_index(df_in.index, df_out.index):
        assert_utc_aligned_frame(df_in, df_out)

    # 4. Compare plain result...
    else:
        assert df_out.equals(df_in)


# --------------------------------------------------------------------------------------------- #


def has_datetime_tz_index(index_in, index_out):
    """Checks whether both indexes are datetime indexes with input timezone metadata."""

    # 1. Check indexes...
    return (
        isinstance(index_in, pd.DatetimeIndex)
        and isinstance(index_out, pd.DatetimeIndex)
        and (index_in.tz is not None)
    )


# --------------------------------------------------------------------------------------------- #


def assert_utc_aligned_frame(df_in: pd.DataFrame, df_out: pd.DataFrame):
    """Compares two time-indexed frames after UTC normalization."""

    # 1. Prepare aligned frames...
    df_in_aligned = df_in.copy()
    df_out_aligned = df_out.copy()

    # 2. Read datetime indexes...
    index_in = cast(pd.DatetimeIndex, df_in.index)
    index_out = cast(pd.DatetimeIndex, df_out.index)

    # 3. Normalize timezones...
    df_in_aligned.index = index_in.tz_convert("UTC")
    df_out_aligned.index = index_out.tz_convert("UTC")

    # 4. Assert aligned equality...
    assert df_out_aligned.equals(df_in_aligned)


# --------------------------------------------------------------------------------------------- #


def assert_datetime_index_metadata(index_in, index_out, tz: str):
    """Checks timezone identity/offset fallback and frequency after round-trip."""

    # 1. Check index types...
    if isinstance(index_out, pd.DatetimeIndex) and isinstance(index_in, pd.DatetimeIndex):
        assert_datetime_index_timezone(index_in, index_out, tz)
        assert (index_out.freqstr or None) == (index_in.freqstr or None)


# --------------------------------------------------------------------------------------------- #


def assert_datetime_index_timezone(
    index_in: pd.DatetimeIndex, index_out: pd.DatetimeIndex, tz: str
):
    """Checks named timezone preservation or equivalent UTC offset fallback."""

    # 1. Read timezone key...
    tz_key = getattr(index_out.tz, "key", None) or getattr(index_out.tz, "zone", None)

    # 2. Assert named timezone...
    if tz_key is not None:
        assert tz_key == tz

    # 3. Assert offset fallback...
    else:
        assert_datetime_index_offset(index_in, index_out)


# --------------------------------------------------------------------------------------------- #


def assert_datetime_index_offset(index_in: pd.DatetimeIndex, index_out: pd.DatetimeIndex):
    """Checks that first timestamps preserve equivalent UTC offsets."""

    # 1. Prepare timestamps...
    out_ts = cast("pd.Timestamp", index_out[0])
    in_ts = cast("pd.Timestamp", index_in[0])

    # 2. Compare offsets...
    assert out_ts.utcoffset() == in_ts.utcoffset()


# --------------------------------------------------------------------------------------------- #


def assert_default_round_trip(value: object, clazz: type):
    """Checks the default encode/decode contract for a supported value."""

    # 1. Encode and decode...
    encoded = pyon.encode(value)
    decoded = pyon.decode(encoded)

    # 2. Assert encoded shape...
    assert encoded != value
    assert isinstance(encoded, str)

    # 3. Assert type marker...
    if not is_builtin_class(clazz) or clazz is dict:
        assert clazz.__name__.lower() in encoded.lower()

    # 4. Assert decoded value...
    assert_default_decoded(value, decoded, clazz)


# --------------------------------------------------------------------------------------------- #


def assert_default_decoded(value: object, decoded: Any, clazz: type):
    """Checks decoded equality for scalar and object values."""

    # 1. Assert direct equality...
    if not (hasattr(decoded, "__dict__") and isinstance(decoded.__dict__, dict)):
        assert decoded == value

    # 2. Assert object dictionary...
    elif hasattr(value, "__dict__") and isinstance(value.__dict__, dict):
        assert_default_object_dict(value, decoded)

    # 3. Fail unsupported decoded shape...
    else:
        pytest.fail(
            (
                f"Fail. Expected: {clazz}. "
                f"Value: {type(value)}. "
                f"Result: {type(decoded)}."
            )
        )


# --------------------------------------------------------------------------------------------- #


def assert_default_object_dict(value, decoded):
    """Checks that decoded object dictionaries preserve each field."""

    # 1. Assert dictionary values...
    for key, val in value.__dict__.items():

        # 1.1 Both must have the same key and value...
        assert key in decoded.__dict__
        assert decoded.__dict__[key] == val


# --------------------------------------------------------------------------------------------- #


def is_builtin_class(clazz: type):
    """Checks if a class is builtins."""

    # 1. Checks...
    return clazz in {int, float, bool, str, type}


# --------------------------------------------------------------------------------------------- #
