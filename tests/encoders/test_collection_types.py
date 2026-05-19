# --------------------------------------------------------------------------------------------- #
"""Resilience contracts for collection encoder helpers."""
# --------------------------------------------------------------------------------------------- #

from typing import Any, cast

# --------------------------------------------------------------------------------------------- #

from pyon.encoder import PyonEncoder
from pyon.encoders.collection_types import ColEnc

# --------------------------------------------------------------------------------------------- #


def _assert_helpers_return_none(target, method_inputs):
    """Checks that invalid helper calls return None."""

    # 1. Validate helper contracts...
    for method_name, invalid_input in method_inputs:
        assert getattr(target, method_name)(cast(Any, invalid_input)) is None


# --------------------------------------------------------------------------------------------- #


def test_collection_invalid_encode_paths():
    """Collection helper methods should reject wrong input types."""

    # 1. Prepares helper...
    col = ColEnc(PyonEncoder())
    inner = cast(Any, col)

    # 2. Validates simple collections...
    _assert_helpers_return_none(
        inner,
        [
            ("_encode_bytearray", "x"),
            ("_encode_bytes", "x"),
            ("_encode_chainmap", "x"),
            ("_encode_counter", "x"),
            ("_encode_defaultdict", "x"),
            ("_encode_deque", "x"),
        ],
    )

    # 3. Validates remaining collections...
    _assert_helpers_return_none(
        inner,
        [
            ("_encode_frozenset", "x"),
            ("_encode_list", "x"),
            ("_encode_namedtuple", ("x", 1)),
            ("_encode_set", "x"),
            ("_encode_tuple", "x"),
        ],
    )


# --------------------------------------------------------------------------------------------- #


def test_collection_decode_invalid_payload_logs_and_returns_none():
    """Invalid decode payloads should be rejected for chainmap and namedtuple."""

    # 1. Prepares encoder...
    col = ColEnc(PyonEncoder())

    # 2. Validates malformed decode payloads...
    assert getattr(cast(Any, col), "_decode_chainmap")({}) is None
    assert getattr(cast(Any, col), "_decode_namedtuple")({}) is None


# --------------------------------------------------------------------------------------------- #
