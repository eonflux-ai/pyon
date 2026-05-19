# --------------------------------------------------------------------------------------------- #
"""Resilience contracts for specialized encoder helpers."""
# --------------------------------------------------------------------------------------------- #
# pylint: disable=duplicate-code
# --------------------------------------------------------------------------------------------- #

from typing import Any, cast
from pyon.encoder import PyonEncoder
from pyon.encoders.specialized_types import SpecEnc
from pyon.supported_types import SupportedTypes
from pyon.utils import EConst

# --------------------------------------------------------------------------------------------- #


def _assert_helpers_return_none(target, method_inputs):
    """Checks that invalid helper calls return None."""

    # 1. Validate helper contracts...
    for method_name, invalid_input in method_inputs:
        assert getattr(target, method_name)(cast(Any, invalid_input)) is None


# --------------------------------------------------------------------------------------------- #


def test_specialized_decoder_rejects_invalid_index_type_gracefully():
    """Invalid index metadata should be rejected without raising exceptions."""

    # 1. Prepares malformed dataframe payload...
    payload = {
        EConst.TYPE: SupportedTypes.DATAFRAME.value,
        EConst.DATA: [],
        EConst.AUX1: [],
        EConst.AUX2: [],
        EConst.AUX3: [],
        EConst.AUX4: "InvalidIndex",
        EConst.AUX5: [],
        EConst.AUX6: "Index",
    }

    # 2. Decodes...
    output = SpecEnc(PyonEncoder()).decode(payload)

    # 3. Validates safe failure...
    assert output is None or hasattr(output, "shape")


# --------------------------------------------------------------------------------------------- #


def test_specialized_helpers_reject_invalid_inputs():
    """Specialized encoder helpers should fail safely on invalid values."""

    # 1. Prepares helper...
    spec = SpecEnc(PyonEncoder())

    # 2. Prepares dynamic helper...
    inner = cast(Any, spec)

    # 3. Validates simple encoders...
    _assert_helpers_return_none(
        inner,
        [
            ("_encode_bitarray", "bad"),
            ("_encode_file", "bad"),
            ("_decode_file", None),
        ],
    )

    # 4. Validates array/data encoders...
    _assert_helpers_return_none(
        inner,
        [
            ("_encode_ndarray", "bad"),
            ("_encode_uuid", "bad"),
            ("_encode_dataframe", "bad"),
            ("_encode_series", "bad"),
        ],
    )

    # 5. Validates index helpers...
    assert getattr(spec, "_SpecEnc__decode_index")({}) is None
    assert getattr(spec, "_SpecEnc__decode_columns")({}) is None

    # 6. Validates timezone helpers...
    assert getattr(spec, "_SpecEnc__parse_offset")("+00:30") is not None
    assert getattr(spec, "_SpecEnc__tzinfo_from_meta")(
        {EConst.TZ_OFFSET: "+00:00"}
    ) is not None


# --------------------------------------------------------------------------------------------- #


def test_specialized_internal_fallback_and_errors():
    """Specialized internals should fail safely on reshape/offset edge cases."""

    # 1. Prepares helper...
    spec = SpecEnc(PyonEncoder())

    # 2. Forces ndarray reshape failure branch...
    assert getattr(cast(Any, spec), "_decode_ndarray")(
        {EConst.DATA: [1, 2, 3], EConst.AUX1: (2, 2)}
    ) is None

    # 3. Builds broken index...
    class _BrokenIndex:
        tz = None

        def __len__(self):
            return 1

        def __getitem__(self, _):
            raise TypeError("bad access")

    # 4. Validates metadata fallback...
    assert getattr(spec, "_SpecEnc__build_tz_meta_from_index")(_BrokenIndex()) is None
    assert getattr(spec, "_SpecEnc__format_offset")(object()) is None

    # 5. Validates timezone fallback...
    assert getattr(spec, "_SpecEnc__tzinfo_from_meta")(
        {EConst.TZ_ZONE: "Invalid/Zone", EConst.TZ_OFFSET: "+00:00"}
    ) is not None


# --------------------------------------------------------------------------------------------- #
