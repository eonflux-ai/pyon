# --------------------------------------------------------------------------------------------- #
""" Resilience/contract tests for defensive branches across encoders/utils. """
# --------------------------------------------------------------------------------------------- #

from collections import Counter, defaultdict, deque
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
# --------------------------------------------------------------------------------------------- #

import pytest
from pyon import api as pyon_api

# --------------------------------------------------------------------------------------------- #

from pyon.encoder import PyonEncoder
from pyon.file.api import File
from pyon.supported_types import SupportedTypes
from pyon.utils import EConst, generate_unique_filename, get_class, lstrip, parse_utc_offset

# --------------------------------------------------------------------------------------------- #


class _Color(Enum):
    RED = 1


# --------------------------------------------------------------------------------------------- #


def test_encoder_public_contract_for_unsupported_and_null_inputs():
    """ Ensures top-level encoder handles unsupported and null strings defensively. """

    # 1. Prepares encoder...
    enc = PyonEncoder()

    # 2. Validates public behavior...
    assert enc.encode_str(object()) is None
    assert enc.decode_str("null") is None


# --------------------------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "payload",
    [
        {EConst.TYPE: SupportedTypes.COMPLEX.value},      # missing AUX keys
        {EConst.TYPE: SupportedTypes.DECIMAL.value},      # missing DATA
        {EConst.TYPE: SupportedTypes.BYTEARRAY.value},    # missing DATA
        {EConst.TYPE: SupportedTypes.BYTES.value},        # missing DATA
        {EConst.TYPE: SupportedTypes.COUNTER.value},      # missing DATA
        {EConst.TYPE: SupportedTypes.DEFAULTDICT.value},  # missing DATA
        {EConst.TYPE: SupportedTypes.DEQUE.value},        # missing DATA
        {EConst.TYPE: SupportedTypes.FROZENSET.value},    # missing DATA
        {EConst.TYPE: SupportedTypes.LIST.value},         # missing DATA
        {EConst.TYPE: SupportedTypes.SET.value},          # missing DATA
        {EConst.TYPE: SupportedTypes.TUPLE.value},        # missing DATA
        {EConst.TYPE: SupportedTypes.ENUM.value},         # missing DATA
        {EConst.TYPE: SupportedTypes.BITARRAY.value},     # missing DATA
        {EConst.TYPE: SupportedTypes.NDARRAY.value},      # missing DATA/AUX1
        {EConst.TYPE: SupportedTypes.UUID.value},         # missing DATA
        {EConst.TYPE: SupportedTypes.DATAFRAME.value},    # missing DATA
        {EConst.TYPE: SupportedTypes.SERIES.value},       # missing DATA
        {EConst.TYPE: SupportedTypes.DATE.value},         # missing DATA
        {EConst.TYPE: SupportedTypes.DATETIME.value},     # missing DATA
        {EConst.TYPE: SupportedTypes.TIME.value},         # missing DATA
    ],
)
def test_decode_dict_defensive_on_malformed_payloads(payload):
    """ Malformed typed payloads must decode to None, never crash. """

    # 1. Decodes malformed payload...
    enc = PyonEncoder()
    output = enc.decode_dict(payload)

    # 2. Validates contract...
    assert output is None


# --------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #


def test_generate_unique_filename_retries_on_collision(monkeypatch):
    """ Filename generation should retry when candidate already exists. """

    # 1. Controls randomness to force one collision then success...
    seq = iter(list("abcabcxyz"))

    def _choice(_alphabet):
        return next(seq)

    monkeypatch.setattr("pyon.utils.secrets.choice", _choice)

    # 2. Simulates existing first candidate...
    existing = {"base_abc.txt"}

    def _exists(path):
        return path.replace("\\", "/").endswith(tuple(existing))

    monkeypatch.setattr("pyon.utils.os.path.exists", _exists)

    # 3. Generates unique name...
    out = generate_unique_filename(name="base", extension="txt", size=3, folder_path="temp")

    # 4. Validates retry result...
    assert out == "base_xyz.txt"


# --------------------------------------------------------------------------------------------- #


def test_parse_utc_offset_contract():
    """ Offset parser should accept valid forms and reject malformed text. """

    # 1. Validates supported format...
    tz = parse_utc_offset("-03:30")
    assert tz is not None
    assert datetime(2025, 1, 1, tzinfo=tz).utcoffset() == timedelta(hours=-3, minutes=-30)

    # 2. Validates malformed format...
    assert parse_utc_offset("bad") is None
    assert parse_utc_offset("+AA:BB") is None


# --------------------------------------------------------------------------------------------- #


def test_round_trip_complex_collection_contexts():
    """ Runs realistic decode/encode for mixed types to exercise integrated branches. """

    # 1. Prepares values...
    enc = PyonEncoder()
    values = [
        Counter({"a": 2}),
        defaultdict(int, a=1),
        deque([1, 2]),
        Decimal("10.5"),
        _Color.RED,
    ]

    # 2. Round-trips...
    for value in values:
        encoded = enc.encode_str(value)
        decoded = enc.decode_str(encoded) if encoded is not None else None
        assert decoded is not None


# --------------------------------------------------------------------------------------------- #


def test_to_file_verbose_logs_success(tmp_path):
    """ to_file should execute verbose logging branch on successful write. """

    # 1. Writes pyon output...
    out_file = tmp_path / "ok.pyon"
    payload = {"v": 1}
    output = pyon_api.to_file(payload, file_path=str(out_file), verbose=True)

    # 2. Validates...
    assert isinstance(output, str)
    assert out_file.exists()


# --------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #


def test_utils_guard_branches():
    """ Utility guards should handle invalid class paths and strip args. """

    # 1. Validates invalid class path...
    assert get_class({EConst.CLASS: "x.y.z"}) is None

    # 2. Validates strip guard...
    with pytest.raises(ValueError):
        lstrip("abc", "")


# --------------------------------------------------------------------------------------------- #


def test_file_remaining_branches(tmp_path, monkeypatch):
    """ Covers write/unload/mime/decode branches in realistic file workflows. """

    # 1. Prepares source/destination...
    src = tmp_path / "src.bin"
    dst = tmp_path / "dst.bin"
    src.write_bytes(b"src")

    # 2. Prepares current-path file...
    value = File(path=str(src))
    value.content = b"new"

    # 3. Forces unload current-path branch...
    value.path = str(tmp_path / "missing.bin")
    assert value.unload(update=False) is True

    # 4. Covers write copy branch...
    value2 = File(path=str(src))
    value2.content = None
    assert value2.write(str(dst)) is True
    assert dst.read_bytes() == b"src"

    # 5. Covers os.makedirs branch...
    deep = tmp_path / "a" / "b" / "out.bin"
    value3 = File(content=b"x")
    assert value3.write(str(deep)) is True

    # 6. Patches MIME helpers...
    monkeypatch.setattr("pyon.file.api.File.get_mime_from_path", lambda _: "")
    monkeypatch.setattr("pyon.file.api.File.get_mime_from_name", lambda _: "text/test")

    # 7. Covers __get_mime name branch...
    value4 = File(content=b"x")
    value4.path = "name.txt"
    value4.content = None
    value4.mime = getattr(value4, "_File__get_mime")(None)
    assert value4.mime == "text/test"

    # 8. Covers decode_content bytes branch...
    assert File._decode_content(b"abc") == b"abc"  # pylint: disable=protected-access


# --------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #


def test_file_temp_keep_branch_and_folder_cleanup(tmp_path, monkeypatch):
    """ Covers unload temp keep branch and clean empty-folder removal branch. """

    # 1. Prepares temp file...
    temp_file = tmp_path / "keep.bin"
    temp_file.write_bytes(b"old")

    # 2. Prepares file object...
    value = File(content=b"new")
    value._tmp_path = str(temp_file)  # pylint: disable=protected-access

    # 3. Forces unload else/keep branch...
    original_prop = File.path
    monkeypatch.setattr(File, "path", property(lambda self: None, original_prop.fset))
    assert value.unload(update=False) is True

    # 4. Prepares removable folder...
    folder = tmp_path / "rm"
    folder.mkdir()
    target = folder / "file.bin"
    target.write_bytes(b"x")

    # 5. Covers clean folder-removal branch...
    value2 = File(content=b"x")
    value2._tmp_path = str(target)  # pylint: disable=protected-access
    assert value2.clean() is True
    assert not folder.exists()


# --------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #
