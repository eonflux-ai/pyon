# --------------------------------------------------------------------------------------------- #
""" Contract tests for: pyon/annotations/core.py """
# --------------------------------------------------------------------------------------------- #

import pytest

# --------------------------------------------------------------------------------------------- #

from pyon.annotations.core import export, get_export_flags

# --------------------------------------------------------------------------------------------- #


def test_export_decorator_applies_flags():
    """ Applies and reads export flags from decorated class. """

    # 1. Decorate class...
    @export(private=True, protected=False)
    class _Decorated:  # pylint: disable=too-few-public-methods
        pass

    # 2. Read flags...
    value = _Decorated()
    private, protected = get_export_flags(value)

    # 3. Validate flags...
    assert private is True
    assert protected is False


# --------------------------------------------------------------------------------------------- #


def test_get_export_flags_defaults_to_false():
    """ Returns default flags when class has no export metadata. """

    # 1. Build class...
    class _Plain:  # pylint: disable=too-few-public-methods
        pass

    # 2. Validate defaults...
    private, protected = get_export_flags(_Plain())
    assert private is False
    assert protected is False


# --------------------------------------------------------------------------------------------- #


def test_get_export_flags_rejects_invalid_types():
    """ Raises ValueError when export flags are not bool values. """

    # 1. Build class with invalid flags...
    class _Invalid:  # pylint: disable=too-few-public-methods
        pass

    setattr(_Invalid, "__pyon_export_private__", "yes")
    setattr(_Invalid, "__pyon_export_protected__", 1)

    # 2. Validate error...
    with pytest.raises(ValueError, match="Invalid Pyon export flags"):
        get_export_flags(_Invalid())
