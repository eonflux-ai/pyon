# --------------------------------------------------------------------------------------------- #
""" Resilience/contract tests for defensive branches across encoders/utils. """
# --------------------------------------------------------------------------------------------- #

from collections import Counter, defaultdict, deque
from datetime import datetime, timezone, timedelta, time
from decimal import Decimal
from enum import Enum
from typing import Any, cast
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# --------------------------------------------------------------------------------------------- #

import pytest
from pyon import api as pyon_api
import pyon.encoders.datetime_types as dt_module

# --------------------------------------------------------------------------------------------- #

from pyon.encoder import PyonEncoder
from pyon.file.api import File
from pyon.encoders.base_encoder import BaseEncoder
from pyon.encoders.base_types import BaseEnc
from pyon.encoders.collection_types import ColEnc
from pyon.encoders.datetime_types import DateEnc
from pyon.encoders.mapping_types import MapEnc
from pyon.encoders.numeric_types import NumEnc
from pyon.encoders.specialized_types import SpecEnc
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


def test_datetime_decoder_fallbacks_to_offset_when_zone_is_unknown(monkeypatch):
    """ Zone lookup failure should still preserve offset-based timezone. """

    # 1. Prepares payload with explicit zone+offset...
    value = {
        EConst.TYPE: SupportedTypes.DATETIME.value,
        EConst.DATA: "2025-01-01T10:00:00",
        EConst.AUX1: {
            EConst.TZ_ZONE: "Invalid/Zone",
            EConst.TZ_OFFSET: "+02:30",
            EConst.TZ_FOLD: 1,
        },
    }

    # 2. Forces zone lookup failure...
    def _raise_zoneinfo(_):
        raise ZoneInfoNotFoundError("zone missing")

    monkeypatch.setattr("pyon.encoders.datetime_types.ZoneInfo", _raise_zoneinfo)

    # 3. Decodes...
    output = DateEnc().decode(value)

    # 4. Validates output type...
    assert isinstance(output, datetime)

    # 5. Validates offset and fold...
    assert output.utcoffset() == timedelta(hours=2, minutes=30)
    assert getattr(output, "fold", 0) == 1


# --------------------------------------------------------------------------------------------- #


def test_specialized_decoder_rejects_invalid_index_type_gracefully():
    """ Invalid index metadata should be rejected without raising exceptions. """

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
    out = generate_unique_filename(name="base", extension="txt", size=3, folder_path="/tmp")

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


def test_base_and_numeric_and_mapping_helpers_reject_invalid_inputs():
    """ Defensive helper methods should reject invalid types gracefully. """

    # 1. Prepares base helpers...
    base = BaseEnc()
    num = NumEnc()

    # 2. Prepares mapping helper...
    mapping = MapEnc(PyonEncoder())

    # 3. Validates base helper contracts...
    assert getattr(cast(Any, base), "_encode_type")(cast(Any, "not-type")) is None
    assert getattr(cast(Any, base), "_decode_type")(cast(Any, None)) is None

    # 4. Validates numeric helper contracts...
    assert getattr(cast(Any, num), "_encode_complex")(cast(Any, "bad")) is None
    assert getattr(cast(Any, num), "_encode_decimal")(cast(Any, 1)) is None

    # 5. Validates mapping helper contracts...
    assert getattr(cast(Any, mapping), "_encode_enum")(cast(Any, "bad")) is None


# --------------------------------------------------------------------------------------------- #


def test_specialized_helpers_reject_invalid_inputs():
    """ Specialized encoder helpers should fail safely on invalid values. """

    # 1. Prepares helper...
    spec = SpecEnc(PyonEncoder())

    # 2. Prepares dynamic helper...
    inner = cast(Any, spec)

    # 3. Validates simple encoders...
    assert getattr(inner, "_encode_bitarray")(cast(Any, "bad")) is None
    assert getattr(inner, "_encode_file")(cast(Any, "bad")) is None
    assert getattr(inner, "_decode_file")(cast(Any, None)) is None

    # 4. Validates array/data encoders...
    assert getattr(inner, "_encode_ndarray")(cast(Any, "bad")) is None
    assert getattr(inner, "_encode_uuid")(cast(Any, "bad")) is None
    assert getattr(inner, "_encode_dataframe")(cast(Any, "bad")) is None
    assert getattr(inner, "_encode_series")(cast(Any, "bad")) is None

    # 5. Validates index helpers...
    assert getattr(spec, "_SpecEnc__decode_index")({}) is None
    assert getattr(spec, "_SpecEnc__decode_columns")({}) is None

    # 6. Validates timezone helpers...
    assert getattr(spec, "_SpecEnc__parse_offset")("+00:30") is not None
    assert getattr(spec, "_SpecEnc__tzinfo_from_meta")(
        {EConst.TZ_OFFSET: "+00:00"}
    ) is not None


# --------------------------------------------------------------------------------------------- #


def test_datetime_helpers_reject_invalid_inputs():
    """ Datetime helper methods should reject invalid values without exceptions. """

    # 1. Prepares helper...
    dt = DateEnc()

    # 2. Prepares dynamic helper...
    inner = cast(Any, dt)

    # 3. Validates encode defensive branches...
    assert getattr(inner, "_encode_date")(cast(Any, "bad")) is None
    assert getattr(inner, "_encode_datetime")(cast(Any, "bad")) is None
    assert getattr(inner, "_encode_time")(cast(Any, "bad")) is None

    # 4. Covers datetime offset-only attach...
    out_dt = getattr(inner, "_decode_datetime")(
        {
            EConst.TYPE: SupportedTypes.DATETIME.value,
            EConst.DATA: "2025-01-01T10:00:00",
            EConst.AUX1: {EConst.TZ_OFFSET: "+01:15"},
        }
    )
    assert out_dt is not None and out_dt.utcoffset() == timedelta(hours=1, minutes=15)

    # 5. Covers time encode branch...
    out_time = getattr(inner, "_encode_time")(datetime.now(timezone.utc).timetz())
    assert isinstance(out_time, dict) and EConst.AUX1 in out_time

    # 6. Covers time decode branch...
    dec_time = getattr(inner, "_decode_time")(
        {
            EConst.TYPE: SupportedTypes.TIME.value,
            EConst.DATA: "10:00:00",
            EConst.AUX1: {EConst.TZ_OFFSET: "-02:00"},
        }
    )
    assert dec_time is not None and dec_time.utcoffset() == timedelta(hours=-2)

    # 7. Covers fallback on invalid fold...
    getattr(inner, "_decode_datetime")(
        {
            EConst.TYPE: SupportedTypes.DATETIME.value,
            EConst.DATA: "2025-01-01T10:00:00",
            EConst.AUX1: {EConst.TZ_OFFSET: "+00:00", EConst.TZ_FOLD: 9},
        }
    )


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


def test_base_encoder_requires_encoder_instance():
    """ BaseEncoder must reject missing encoder dependency. """

    with pytest.raises(ValueError, match="Invalid Pyon Encoder"):
        BaseEncoder(None)


# --------------------------------------------------------------------------------------------- #


def test_collection_invalid_encode_paths():
    """ Collection helper methods should reject wrong input types. """

    col = ColEnc(PyonEncoder())
    inner = cast(Any, col)
    assert getattr(inner, "_encode_bytearray")(cast(Any, "x")) is None
    assert getattr(inner, "_encode_bytes")(cast(Any, "x")) is None
    assert getattr(inner, "_encode_chainmap")(cast(Any, "x")) is None
    assert getattr(inner, "_encode_counter")(cast(Any, "x")) is None
    assert getattr(inner, "_encode_defaultdict")(cast(Any, "x")) is None
    assert getattr(inner, "_encode_deque")(cast(Any, "x")) is None
    assert getattr(inner, "_encode_frozenset")(cast(Any, "x")) is None
    assert getattr(inner, "_encode_list")(cast(Any, "x")) is None
    assert getattr(inner, "_encode_namedtuple")(cast(Any, ("x", 1))) is None
    assert getattr(inner, "_encode_set")(cast(Any, "x")) is None
    assert getattr(inner, "_encode_tuple")(cast(Any, "x")) is None


# --------------------------------------------------------------------------------------------- #


def test_specialized_internal_fallback_and_errors():
    """ Specialized internals should fail safely on reshape/offset edge cases. """

    spec = SpecEnc(PyonEncoder())

    # 1. Forces ndarray reshape failure branch...
    assert getattr(cast(Any, spec), "_decode_ndarray")(
        {EConst.DATA: [1, 2, 3], EConst.AUX1: (2, 2)}
    ) is None

    # 2. Builds broken index...
    class _BrokenIndex:
        tz = None

        def __len__(self):
            return 1

        def __getitem__(self, _):
            raise TypeError("bad access")

    # 3. Validates metadata fallback...
    assert getattr(spec, "_SpecEnc__build_tz_meta_from_index")(_BrokenIndex()) is None
    assert getattr(spec, "_SpecEnc__format_offset")(object()) is None

    # 4. Validates timezone fallback...
    assert getattr(spec, "_SpecEnc__tzinfo_from_meta")(
        {EConst.TZ_ZONE: "Invalid/Zone", EConst.TZ_OFFSET: "+00:00"}
    ) is not None


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


def test_collection_decode_invalid_payload_logs_and_returns_none():
    """ Invalid decode payloads should be rejected for chainmap and namedtuple. """

    # 1. Prepares encoder...
    col = ColEnc(PyonEncoder())

    # 2. Validates malformed decode payloads...
    assert getattr(cast(Any, col), "_decode_chainmap")({}) is None
    assert getattr(cast(Any, col), "_decode_namedtuple")({}) is None


# --------------------------------------------------------------------------------------------- #


def test_datetime_decode_attach_zone_when_input_is_naive():
    """ Decoding with valid TZ zone should attach tzinfo on naive datetime payloads. """

    # 1. Prepares naive datetime payload with region metadata...
    payload = {
        EConst.TYPE: SupportedTypes.DATETIME.value,
        EConst.DATA: "2025-01-01T10:00:00",
        EConst.AUX1: {EConst.TZ_ZONE: "UTC"},
    }

    # 2. Decodes and validates zone attachment...
    output = getattr(cast(Any, DateEnc()), "_decode_datetime")(payload)
    assert output is not None
    assert output.tzinfo is not None


# --------------------------------------------------------------------------------------------- #


def test_datetime_decode_ignores_invalid_fold_replace(monkeypatch):
    """ Fold replace failures must not break decode flow. """

    # 1. Builds fake datetime object...
    class _FakeDateTimeValue:  # pylint: disable=too-few-public-methods
        tzinfo = None

        def replace(self, **kwargs):
            """Mimics datetime.replace with fold failure."""
            if "fold" in kwargs:
                raise ValueError("invalid fold")
            return self

        def astimezone(self, _zone):
            """Mimics astimezone without conversion."""
            return self

    # 2. Builds fake datetime class...
    class _FakeDateTimeClass:  # pylint: disable=too-few-public-methods
        @staticmethod
        def fromisoformat(_value):
            """Returns fake datetime object."""
            return _FakeDateTimeValue()

    # 3. Patches datetime class...
    monkeypatch.setattr(dt_module, "datetime", _FakeDateTimeClass)

    # 4. Prepares fold payload...
    payload = {
        EConst.TYPE: SupportedTypes.DATETIME.value,
        EConst.DATA: "2025-01-01T10:00:00",
        EConst.AUX1: {EConst.TZ_OFFSET: "+00:00", EConst.TZ_FOLD: 1},
    }
    # 5. Decodes payload...
    output = getattr(cast(Any, DateEnc()), "_decode_datetime")(payload)

    # 6. Validates graceful handling...
    assert output is not None


# --------------------------------------------------------------------------------------------- #


def test_datetime_time_zone_metadata_roundtrip_paths(monkeypatch):
    """ Time encode/decode should preserve zone metadata and fallback to offset when needed. """

    # 1. Encodes aware time...
    value = time(10, 20, 30, tzinfo=ZoneInfo("UTC"))
    encoded = getattr(cast(Any, DateEnc()), "_encode_time")(value)

    # 2. Validates zone metadata...
    assert isinstance(encoded, dict)
    assert EConst.TZ_ZONE in encoded[EConst.AUX1]

    # 3. Prepares offset fallback payload...
    payload = {
        EConst.TYPE: SupportedTypes.TIME.value,
        EConst.DATA: "10:00:00",
        EConst.AUX1: {EConst.TZ_ZONE: "Invalid/Zone", EConst.TZ_OFFSET: "+03:00"},
    }

    def _raise_zoneinfo(_):
        raise ZoneInfoNotFoundError("zone missing")

    # 4. Forces zone lookup failure...
    monkeypatch.setattr("pyon.encoders.datetime_types.ZoneInfo", _raise_zoneinfo)
    decoded = getattr(cast(Any, DateEnc()), "_decode_time")(payload)

    # 5. Validates offset fallback...
    assert decoded is not None
    assert decoded.utcoffset() == timedelta(hours=3)
