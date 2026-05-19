# --------------------------------------------------------------------------------------------- #
"""Resilience contracts for numeric encoder helpers."""
# --------------------------------------------------------------------------------------------- #

from typing import Any, cast

# --------------------------------------------------------------------------------------------- #

from pyon.encoders.numeric_types import NumEnc

# --------------------------------------------------------------------------------------------- #


def test_numeric_helpers_reject_invalid_inputs():
    """Numeric helper methods should reject invalid types gracefully."""

    # 1. Prepares helper...
    num = NumEnc()

    # 2. Validates complex guard...
    assert getattr(cast(Any, num), "_encode_complex")(cast(Any, "bad")) is None

    # 3. Validates decimal guard...
    assert getattr(cast(Any, num), "_encode_decimal")(cast(Any, 1)) is None


# --------------------------------------------------------------------------------------------- #
