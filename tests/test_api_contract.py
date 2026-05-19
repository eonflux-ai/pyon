# --------------------------------------------------------------------------------------------- #
""" Contract tests for: pyon/api.py """
# --------------------------------------------------------------------------------------------- #

from pathlib import Path

# --------------------------------------------------------------------------------------------- #

import pytest

# --------------------------------------------------------------------------------------------- #

from pyon import api

# --------------------------------------------------------------------------------------------- #


def test_encode_and_decode_none():
    """ Validates public API behavior for None input. """

    # 1. Check encode/decode...
    assert api.encode(None) is None
    assert api.decode(None) is None


# --------------------------------------------------------------------------------------------- #


def test_to_file_and_from_file_round_trip(tmp_path: Path):
    """ Ensures to_file/from_file round-trip for valid pyon target. """

    # 1. Prepare input...
    value = {"name": "alice", "age": 30}
    out_file = tmp_path / "item.pyon"

    # 2. Write and read...
    encoded = api.to_file(value, file_path=str(out_file), verbose=False)
    decoded = api.from_file(str(out_file))

    # 3. Validate encoded result...
    assert isinstance(encoded, str)
    assert out_file.exists()

    # 4. Validate decoded result...
    assert decoded == value


# --------------------------------------------------------------------------------------------- #


def test_to_file_rejects_invalid_extension(tmp_path: Path):
    """ Rejects non-.pyon output path. """

    # 1. Prepare target...
    out_file = tmp_path / "item.txt"

    # 2. Validate error...
    with pytest.raises(ValueError, match="Not a valid pyon output file"):
        api.to_file({"ok": True}, file_path=str(out_file), verbose=False)


# --------------------------------------------------------------------------------------------- #


def test_to_file_rejects_empty_payload(tmp_path: Path):
    """ Rejects write when encoded payload is unavailable. """

    # 1. Prepare target...
    out_file = tmp_path / "item.pyon"

    # 2. Validate error...
    with pytest.raises(ValueError, match="Not a valid pyon output file"):
        api.to_file(None, file_path=str(out_file), verbose=False)


# --------------------------------------------------------------------------------------------- #


def test_from_file_missing_path_returns_none(tmp_path: Path):
    """ Returns None when input file does not exist. """

    # 1. Read missing file...
    value = api.from_file(str(tmp_path / "missing.pyon"))

    # 2. Validate result...
    assert value is None
