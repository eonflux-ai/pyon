# --------------------------------------------------------------------------------------------- #
"""Resilience contracts for base encoder helpers."""
# --------------------------------------------------------------------------------------------- #

from typing import Any, cast

# --------------------------------------------------------------------------------------------- #

import pytest

# --------------------------------------------------------------------------------------------- #

from pyon.encoders.base_encoder import BaseEncoder
from pyon.encoders.base_types import BaseEnc

# --------------------------------------------------------------------------------------------- #


def test_base_helpers_reject_invalid_inputs():
    """Base helper methods should reject invalid types gracefully."""

    # 1. Prepares helper...
    base = BaseEnc()

    # 2. Validates type encoding guard...
    assert getattr(cast(Any, base), "_encode_type")(cast(Any, "not-type")) is None

    # 3. Validates type decoding guard...
    assert getattr(cast(Any, base), "_decode_type")(cast(Any, None)) is None


# --------------------------------------------------------------------------------------------- #


def test_base_encoder_requires_encoder_instance():
    """BaseEncoder must reject missing encoder dependency."""

    # 1. Validates required encoder dependency...
    with pytest.raises(ValueError, match="Invalid Pyon Encoder"):
        BaseEncoder(None)


# --------------------------------------------------------------------------------------------- #
