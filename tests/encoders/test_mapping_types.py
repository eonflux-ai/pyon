# --------------------------------------------------------------------------------------------- #
"""Resilience contracts for mapping encoder helpers."""
# --------------------------------------------------------------------------------------------- #

from typing import Any, cast

# --------------------------------------------------------------------------------------------- #

from pyon.encoder import PyonEncoder
from pyon.encoders.mapping_types import MapEnc
from pyon.utils import EConst

# --------------------------------------------------------------------------------------------- #


def test_mapping_helpers_reject_invalid_inputs():
    """Mapping helper methods should reject invalid types gracefully."""

    # 1. Prepares helper...
    mapping = MapEnc(PyonEncoder())

    # 2. Validates enum guard...
    assert getattr(cast(Any, mapping), "_encode_enum")(cast(Any, "bad")) is None


# --------------------------------------------------------------------------------------------- #


def test_mapping_encode_dict_filters_internal_keys():
    """Mapping dictionary encoding should skip internal keys."""

    # 1. Prepares helper...
    mapping = MapEnc(PyonEncoder())

    # 2. Encodes mapping...
    encoded = getattr(cast(Any, mapping), "_encode_dict")({"___internal": "x", "public": "y"})

    # 3. Validates filtered payload...
    assert len(encoded[EConst.DICT]) == 1


# --------------------------------------------------------------------------------------------- #
