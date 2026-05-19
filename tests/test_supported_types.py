# --------------------------------------------------------------------------------------------- #
"""Tests for public supported type markers."""
# --------------------------------------------------------------------------------------------- #

from pyon.supported_types import SupportedTypes

# --------------------------------------------------------------------------------------------- #


def test_base_supported_type_markers_remain_public():
    """Base scalar type markers are part of the public supported-type contract."""

    # 1. Assert scalar markers...
    assert SupportedTypes.BOOL.value == "bool"
    assert SupportedTypes.FLOAT.value == "float"
    assert SupportedTypes.INT.value == "int"

    # 2. Assert textual/null markers...
    assert SupportedTypes.STR.value == "str"
    assert SupportedTypes.NONE.value == "none"

    # 3. Assert enum-family markers...
    assert SupportedTypes.FLAG.value == "flag"
    assert SupportedTypes.INTENUM.value == "intenum"


# --------------------------------------------------------------------------------------------- #
