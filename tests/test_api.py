# --------------------------------------------------------------------------------------------- #
""" Tests for Pyon: Encode and Decode """
# --------------------------------------------------------------------------------------------- #

from collections import ChainMap, Counter, deque, defaultdict, namedtuple
from dataclasses import dataclass
from datetime import datetime, date, time
from decimal import Decimal
from enum import Enum
from typing import Literal, cast
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# --------------------------------------------------------------------------------------------- #

from bitarray import bitarray

# --------------------------------------------------------------------------------------------- #

import numpy as np
from numpy._typing._array_like import NDArray
import pandas as pd

# --------------------------------------------------------------------------------------------- #

import pytest
import pyon

# --------------------------------------------------------------------------------------------- #

from pyon import File

# --------------------------------------------------------------------------------------------- #


# Test Enums
class Color(Enum):
    """ For Enum Test """
    RED = 1
    GREEN = 2
    BLUE = 3


# --------------------------------------------------------------------------------------------- #


# Test Dataclasses
@dataclass
class Person:
    """ For Dataclass Test """
    name: str
    age: int


# --------------------------------------------------------------------------------------------- #


# Test Class
class Cat:  # pylint: disable=too-few-public-methods
    """ For Dataclass Test """
    name: str
    age: int
    def __init__(self, name, age):
        self.name = name
        self.age = age


# --------------------------------------------------------------------------------------------- #


class ComplexEnum(Enum):
    """Enum with complex values (tuples, dicts) for testing."""
    PAIR = ("pair", 2)
    TRIPLE = ("triple", {"x": 3})
    FULL = ("full", {"a": 2, "b": 3})


# --------------------------------------------------------------------------------------------- #


class _TestClass:  # pylint: disable=too-few-public-methods
    """ Inner test class """

    def __init__(self):
        # 1. Store public value...
        self.public = 1
        self._protected = 2

        # 2. Store private value...
        self.__private = 3  # pylint: disable=unused-private-member


# --------------------------------------------------------------------------------------------- #


class ModelConfig:  # pylint: disable=too-few-public-methods
    """ A class with post-init logic """

    def __init__(self, name):
        # 1. Store configuration...
        self.name = name
        self._model = None

        # 2. Initialize model...
        self.__init()

    def __init(self):
        # 1. Run post init...
        self.__pyon_post_init__()

    def __pyon_post_init__(self):
        # 1. Store model...
        self._model = f"Loaded model: {self.name}"


# --------------------------------------------------------------------------------------------- #


# Namedtuple for Tests
Named = namedtuple("Named", ["field1", "field2"])


# --------------------------------------------------------------------------------------------- #


DATAFRAME_INDEX_CASES = [
    # 1. Standard index...
    pd.DataFrame(
        {"col1": [1, 2], "col2": ["a", "b"]},
        index=pd.Index(["a", "b"])
    ),

    # 2. Range index...
    pd.DataFrame({"col1": [1, 2, 3]}, index=pd.RangeIndex(start=10, stop=13, step=1)),

    # 3. MultiIndex index...
    pd.DataFrame(
        {"col1": [1.0, 2.0, 3.0]},
        index=pd.MultiIndex.from_tuples(
            [("A", 1), ("A", 2), ("B", 1)],
            names=["group", "id"]
        )
    ),

    # 4. Datetime index...
    pd.DataFrame(
        {"col1": [10, 20, 30]},
        index=pd.date_range("2025-01-01", periods=3, freq="D")
    ),

    # 5. Period index...
    pd.DataFrame(
        {"col1": [100, 200]},
        index=pd.period_range("2024Q1", periods=2, freq="Q")
    ),

    # 6. Timedelta index...
    pd.DataFrame(
        {"col1": [5, 10]},
        index=pd.to_timedelta(["1 days", "2 days"])
    ),

    # 7. Categorical index...
    pd.DataFrame(
        {"col1": [42, 84]},
        index=pd.CategoricalIndex(["cat", "dog"], name="animal")
    ),

    # 8. Float64 index...
    pd.DataFrame(
        {"col1": [0.1, 0.2]},
        index=pd.Index([0.1, 0.2], dtype="float64", name="float_id")
    ),

    # 9. Int64 index...
    pd.DataFrame(
        {"col1": [10, 20]},
        index=pd.Index([100, 200], dtype="int64", name="int_id")
    ),
]


# --------------------------------------------------------------------------------------------- #


DATAFRAME_COLUMN_CASES = [

    # 1. UInt64 index...
    pd.DataFrame(
        {"col1": [1, 2]},
        index=pd.Index([10, 20], dtype="uint64", name="uint_id")
    ),

    # 2. MultiIndex columns...
    pd.DataFrame(
        [[22.5, 60, 24.1], [23.0, 55, 23.8]],
        index=pd.Index(["row1", "row2"]),
        columns=pd.MultiIndex.from_tuples(
            [("sensor1", "temp"), ("sensor1", "humidity"), ("sensor2", "temp")],
            names=["device", "measurement"]
        )
    ),

    # 3. CategoricalIndex columns...
    pd.DataFrame(
        [[1, 2]],
        index=pd.Index(["a"]),
        columns=pd.CategoricalIndex(["col1", "col2"], name="categorical_col")
    ),

    # 4. MultiIndex index and columns...
    pd.DataFrame(
        [[1, 2], [3, 4]],
        index=pd.MultiIndex.from_tuples(
            [("X", "x1"), ("X", "x2")],
            names=["sample", "sub"]
        ),
        columns=pd.MultiIndex.from_tuples(
            [("A", 1), ("A", 2)],
            names=["group", "measure"]
        )
    ),
]


# --------------------------------------------------------------------------------------------- #


DATAFRAME_CASES = [*DATAFRAME_INDEX_CASES, *DATAFRAME_COLUMN_CASES, None, "invalid", 10, 3.14]


# --------------------------------------------------------------------------------------------- #


SERIES_INDEX_CASES = [

    # 1. Standard index...
    pd.Series([1.5, 2.0, 3.1], index=["a", "b", "c"], name="standard_series"),

    # 2. Range index...
    pd.Series(
        [100, 200, 300],
        index=pd.RangeIndex(start=0, stop=3, step=1),
        name="range_series",
    ),

    # 3. MultiIndex...
    pd.Series(
        [10, 20, 30],
        index=pd.MultiIndex.from_tuples(
            [("X", 1), ("X", 2), ("Y", 1)],
            names=["category", "code"]
        ),
        name="multiindex_series"
    ),

    # 4. Datetime index...
    pd.Series(
        [1.1, 1.2, 1.3],
        index=pd.date_range("2024-01-01", periods=3, freq="D"),
        name="datetime_series"
    ),

    # 5. Period index...
    pd.Series(
        [11, 22],
        index=pd.period_range("2024Q1", periods=2, freq="Q"),
        name="period_series"
    ),

    # 6. Timedelta index...
    pd.Series(
        [5, 10],
        index=pd.to_timedelta(["1 days", "2 days"]),
        name="timedelta_series"
    ),

    # 7. Categorical index...
    pd.Series(
        [100, 200],
        index=pd.CategoricalIndex(["low", "high"], name="risk_level"),
        name="categorical_series"
    ),

    # 8. Float64 index...
    pd.Series(
        [0.1, 0.2],
        index=pd.Index([0.1, 0.2], dtype="float64", name="float_id"),
        name="float_series"
    ),

    # 9. Int64 index...
    pd.Series(
        [10, 20],
        index=pd.Index([1, 2], dtype="int64", name="int_id"),
        name="int_series"
    ),
]


# --------------------------------------------------------------------------------------------- #


SERIES_EXTRA_CASES = [

    # 1. UInt64 index...
    pd.Series(
        [99, 100],
        index=pd.Index([11, 12], dtype="uint64", name="uint_id"),
        name="uint_series"
    ),
]


# --------------------------------------------------------------------------------------------- #


SERIES_CASES = [*SERIES_INDEX_CASES, *SERIES_EXTRA_CASES, None, "invalid", 42, 3.1415]


# --------------------------------------------------------------------------------------------- #


class TestPyonEncodeDecode:  # pylint: disable=too-many-public-methods
    """ Test suite for Pyon's encode and decode functions """

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [bitarray("1101"), None, "invalid", 10, 3.14])

    def test_bitarray(self, value: bitarray | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for bitarray. """

        # 1. Default test...
        self._test_default(value, bytearray)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [bytearray(b"hello"), None, "invalid", 10, 3.14])

    def test_bytearray(self, value: bytearray | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for bytearray. """

        # 1. Default test...
        self._test_default(value, bytearray)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [b"hello", None, "invalid", 10, 3.14])

    def test_bytes(self, value: None | float | bytes | str | int | float):
        """ Test encoding and decoding for bytes. """

        # 1. Default test...
        self._test_default(value, bytes)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [True, False, None, "invalid", 3.14])

    def test_bool(self, value: None | float | bool | Literal['invalid']):
        """ Test encoding and decoding for boolean values. """

        # 1. Default test...
        self._test_default(value, bool)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [ChainMap({"a": 1}, {"b": 2}), None, "invalid", 10, 3.14])

    def test_chainmap(self, value: ChainMap | None | float | str | int | float):
        """ Test encoding and decoding for ChainMap. """

        # 1. Default test...
        self._test_default(value, ChainMap)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [Cat("Malbec", 6), None, "invalid", 10, 3.14])

    def test_class(self, value: Cat | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for Class. """

        # 1. Default test...
        self._test_default(value, Cat)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [2 + 3j, None, "invalid", 10, 3.14])

    def test_complex(self, value: complex | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for complex numbers. """

        # 1. Default test...
        self._test_default(value, complex)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [Counter({"a": 1, "b": 2}), None, "invalid", 10, 3.14])

    def test_counter(self, value: Counter[str] | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for Counter. """

        # 1. Default test...
        self._test_default(value, complex)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [Person("Alice", 25), None, "invalid", 10, 3.14])

    def test_dataclass(self, value: Person | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for dataclass. """

        # 1. Default test...
        self._test_default(value, Person)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [date.today(), None, "invalid", 10, 3.14])

    def test_date(self, value: date | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for date. """

        # 1. Default test...
        self._test_default(value, date)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [datetime.now(), None, "invalid", 10, 3.14])

    def test_datetime(self, value: datetime | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for datetime. """

        # 1. Default test...
        self._test_default(value, datetime)

    # ----------------------------------------------------------------------------------------- #

    def test_datetime_with_region_round_trip(self):
        """
        Ensures exact round-trip for timezone-aware datetimes using TZDB region.
        """

        # 1. Arrange
        dt_in = datetime(2025, 1, 2, 3, 4, 5, tzinfo=ZoneInfo("America/Sao_Paulo"))

        # 2. Act
        encoded = pyon.encode(dt_in)
        dt_out = pyon.decode(encoded)

        # 3. Assert object...
        assert isinstance(dt_out, datetime)
        assert dt_out == dt_in

        # 4. Assert timezone...
        assert getattr(dt_out.tzinfo, "key", None) == "America/Sao_Paulo"

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("fold", [0, 1])
    def test_datetime_dst_fold_round_trip(self, fold):
        """
        Validates preservation of 'fold' (PEP 495) on ambiguous local times in DST zones.
        Uses America/New_York which has DST transitions.
        """

        # 1. Arrange timezone...
        try:

            # 1.1 Load timezone...
            zone = ZoneInfo("America/New_York")

        # 2. Skip missing timezone...
        except ZoneInfoNotFoundError:
            pytest.skip("Timezone data not available for America/New_York")

        # 3. Arrange ambiguous wall time...
        dt_in = datetime(2020, 11, 1, 1, 30, 0, tzinfo=zone).replace(fold=fold)
        dt_out = pyon.decode(pyon.encode(dt_in))

        # 4. Assert wall time...
        assert isinstance(dt_out, datetime)
        assert dt_out.replace(tzinfo=None) == dt_in.replace(tzinfo=None)

        # 5. Assert fold...
        assert getattr(dt_out, "fold", 0) == fold

        # 6. Assert timezone...
        tz_key = getattr(dt_out.tzinfo, "key", None) or getattr(dt_out.tzinfo, "zone", None)
        if tz_key is not None:
            assert tz_key == "America/New_York"

        # 7. Assert offset fallback...
        else:
            assert dt_out.utcoffset() == dt_in.utcoffset()

    # ----------------------------------------------------------------------------------------- #

    def test_datetime_naive_remains_naive(self):
        """
        Confirms naive datetimes remain naive after round-trip (no accidental tz injection).
        """

        # 1. Arrange
        dt_in = datetime(2025, 2, 3, 4, 5, 6)  # naive

        # 2. Act
        dt_out = pyon.decode(pyon.encode(dt_in))

        # 3. Assert value...
        assert isinstance(dt_out, datetime)
        assert dt_out == dt_in

        # 4. Assert timezone absence...
        assert dt_out.tzinfo is None

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize(
        "start,periods,freq,tz",
        [("2025-01-01", 5, "h", "America/Sao_Paulo")],
    )
    def test_dataframe_datetimeindex_with_tz_round_trip_preserves_freq(
        self, start, periods, freq, tz
    ):
        """Ensures DataFrame with DatetimeIndex(tz) + freq preserves tz region and freq."""

        # 1. Arrange
        idx = pd.date_range(start, periods=periods, freq=freq, tz=tz)
        df_in = pd.DataFrame({"v": range(periods)}, index=idx)

        # 2. Act
        df_out = pyon.decode(pyon.encode(df_in))

        # 3. Assert basic type...
        assert isinstance(df_out, pd.DataFrame)

        # 4. Assert shape and columns...
        assert list(df_out.columns) == list(df_in.columns)
        assert df_out.shape == df_in.shape

        # 5. Compare aligned timezones...
        if (
            isinstance(df_in.index, pd.DatetimeIndex)
            and isinstance(df_out.index, pd.DatetimeIndex)
            and (df_in.index.tz is not None)
        ):

            # 1.1 Prepare aligned frames...
            df_in_aligned = df_in.copy()
            df_out_aligned = df_out.copy()

            # 1.2 Normalize timezones...
            df_in_aligned.index = df_in.index.tz_convert("UTC")
            df_out_aligned.index = df_out.index.tz_convert("UTC")

            # 1.3 Assert aligned equality...
            assert df_out_aligned.equals(df_in_aligned)

        # 6. Compare plain result...
        else:
            assert df_out.equals(df_in)

        # 7. Check timezone and frequency...
        if isinstance(df_out.index, pd.DatetimeIndex) and isinstance(df_in.index, pd.DatetimeIndex):

            # 1.1 Read timezone key...
            tz_key = getattr(df_out.index.tz, "key", None) or getattr(df_out.index.tz, "zone", None)

            # 1.2 Assert named timezone...
            if tz_key is not None:
                assert tz_key == tz

            # 1.3 Assert offset fallback...
            else:

                # 2.1 Prepare timestamps...
                out_ts = cast("pd.Timestamp", df_out.index[0])
                in_ts = cast("pd.Timestamp", df_in.index[0])

                # 2.2 Compare offsets...
                assert out_ts.utcoffset() == in_ts.utcoffset()

            # 1.4 Assert frequency...
            assert (df_out.index.freqstr or None) == (df_in.index.freqstr or None)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize(
        "start,periods,freq,tz",
        [("2025-06-01", 3, "D", "America/Sao_Paulo")],
    )
    def test_series_datetimeindex_with_tz_round_trip(self, start, periods, freq, tz):
        """Ensures Series with DatetimeIndex(tz) round-trips with original region or offset."""

        # 1. Arrange
        idx = pd.date_range(start, periods=periods, freq=freq, tz=tz)
        s_in = pd.Series(list(range(10, 10 + periods * 10, 10)), index=idx, name="tz_series")

        # 2. Act
        s_out = pyon.decode(pyon.encode(s_in))

        # 3. Assert
        assert isinstance(s_out, pd.Series)

        # 4. Compare aligned timezones...
        s_in_aligned = s_in.copy()
        s_out_aligned = s_out.copy()

        # 5. Assert datetime indexes...
        assert isinstance(s_in.index, pd.DatetimeIndex)
        assert isinstance(s_out.index, pd.DatetimeIndex)

        # 6. Normalize timezones...
        s_in_aligned.index = s_in.index.tz_convert("UTC")
        s_out_aligned.index = s_out.index.tz_convert("UTC")

        # 7. Assert aligned equality...
        assert s_out_aligned.equals(s_in_aligned)

        # 8. Check region or offset...
        tz_key = getattr(s_out.index.tz, "key", None) or getattr(s_out.index.tz, "zone", None)
        if tz_key is not None:

            # 1.1 Assert named timezone...
            assert tz_key == tz

        # 9. Assert offset fallback...
        else:

            # 1.1 Prepare timestamps...
            out_ts = cast("pd.Timestamp", s_out.index[0])
            in_ts = cast("pd.Timestamp", s_in.index[0])

            # 1.2 Compare offsets...
            assert out_ts.utcoffset() == in_ts.utcoffset()

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [Decimal("123.45"), None, "invalid", 10, 3.14])

    def test_decimal(self, value: Decimal | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for complex numbers. """

        # 1. Default test...
        self._test_default(value, Decimal)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [defaultdict(int, a=1), None, "invalid", 10, 3.14])

    def test_defaultdict(self, value: defaultdict | None | str | int | float):
        """ Test encoding and decoding for defaultdict. """

        # 1. Default test...
        self._test_default(value, defaultdict)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [deque(["a", "b"]), None, "invalid", 10, 3.14])

    def test_deque(self, value: deque[str] | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for deque. """

        # 1. Default test...
        self._test_default(value, deque)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [{"key_a": 1, "key_b": 2}, {"key_a": 'a', "key_b": 'b'}])

    def test_dict(self, value: dict[str, int] | dict[str, str]):
        """ Test encoding and decoding for deque. """

        # 1. Default test...
        self._test_default(value, dict)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [Color.RED, None, "invalid", 10, 3.14])

    def test_enum(self, value: None | Color | str | int | float):
        """ Test encoding and decoding for Enum. """

        # 1. Default test...
        self._test_default(value, Enum)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [ComplexEnum.PAIR, ComplexEnum.TRIPLE, ComplexEnum.FULL])
    def test_complex_enum_encoding(self, value: ComplexEnum):
        """
        Tests encoding/decoding for Enums with complex values (tuples, dicts).
        """

        # 1. Prepare...
        encoded = pyon.encode(value)
        decoded = pyon.decode(encoded)

        # 2. Validate...
        assert isinstance(decoded, ComplexEnum)
        assert decoded is value

    # ----------------------------------------------------------------------------------------- #


    @pytest.mark.parametrize(
        "value", [File("./tests/data/img.jpg"), None, "invalid", 10, 3.14]
    )

    def test_file(self, value: File | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for File. """

        # 1. Default test...
        self._test_default(value, File)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [2.72, None, "invalid", 10, False])

    def test_float(self, value: float | None | Literal['invalid'] | Literal[10] | Literal[False]):
        """ Test encoding and decoding for float. """

        # 1. Default test...
        self._test_default(value, float)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [frozenset([1, 2, 3]), None, "invalid", 10, 3.14])

    def test_frozenset(self, value: frozenset | None | str | int | float):
        """ Test encoding and decoding for frozenset. """

        # 1. Default test...
        self._test_default(value, frozenset)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [42, None, "invalid", 10, False])

    def test_int(self, value: None | int | str | int | bool):
        """ Test encoding and decoding for int. """

        # 1. Default test...
        self._test_default(value, int)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [Named("value1", 123), None, "invalid", 10, 3.14])

    def test_namedtuple(self, value: Named | None | str | int | float):
        """ Test encoding and decoding for namedtuple. """

        # 1. Default test...
        self._test_default(value, Named)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [{1, 2, 3}, None, "invalid", 10, 3.14])

    def test_set(self, value: set | None | str | int | float):
        """ Test encoding and decoding for set. """

        # 1. Default test...
        self._test_default(value, set)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", ["Hello World", None, "invalid", 10, 3.14])

    def test_str(self, value: str | None | int | float):
        """ Test encoding and decoding for str. """

        # 1. Default test...
        self._test_default(value, str)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [time(14, 30, 15), None, "invalid", 10, 3.14])

    def test_time(self, value: time | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for time. """

        # 1. Default test...
        self._test_default(value, time)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [File, None, "invalid", 10, 3.14])

    def test_type(self, value: File | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for type. """

        # 1. Default test...
        self._test_default(value, type)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [(1, "two", 3.0), None, "invalid", 10, 3.14])

    def test_tuple(self, value: None | float | Literal[1] | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for tuple. """

        # 1. Default test...
        self._test_default(value, tuple)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [uuid4(), None, "invalid", 10, 3.14])

    def test_uuid(self, value: UUID | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for uuid. """

        # 1. Default test...
        self._test_default(value, UUID)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize(
        "value", [np.array([[1, 2, 3], [4, 5, 6]]), None, "invalid", 10, 3.14]
    )

    def test_ndarray(self, value: NDArray | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for Numpy Array. """

        # 1. Valid case...
        if isinstance(value, np.ndarray):

            # 1.1 Encode, Decode...
            encoded = pyon.encode(value)
            decoded = pyon.decode(encoded)

            # 1.2 Asserts: encoded...
            assert isinstance(encoded, str)

            # 1.3 Asserts: decoded...
            assert np.array_equal(decoded, value)  # type: ignore

        # 2. None, Other...
        else:

            # 1.1 Encode, Decode, Asserts...
            decoded = pyon.decode(pyon.encode(value))
            assert decoded == value  # type: ignore

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize(
        "value",
        DATAFRAME_CASES,
    )
    def test_dataframe(self, value: pd.DataFrame | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for Pandas Dataframe. """

        # 1. Valid case...
        if isinstance(value, pd.DataFrame):

            # 1.1 Encode, Decode...
            encoded = pyon.encode(value)
            decoded = pyon.decode(encoded)

            # 1.2 Asserts: encoded...
            assert isinstance(encoded, str)

            # 1.3 Asserts: decoded...
            assert isinstance(decoded, pd.DataFrame)
            assert decoded.equals(value)

        # 2. None, Other...
        else:

            # 1.1 Encode, Decode, Asserts...
            decoded = pyon.decode(pyon.encode(value))
            assert decoded == value  # type: ignore

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize(
        "value",
        SERIES_CASES,
    )
    def test_series(
        self, value: pd.Series | None | float | Literal["invalid"] | Literal[42]
    ):
        """ Test encoding and decoding for Pandas Series. """

        # 1. Valid case...
        if isinstance(value, pd.Series):

            # 1.1 Encode, Decode...
            encoded = pyon.encode(value)
            decoded = pyon.decode(encoded)

            # 1.2 Asserts: encoded...
            assert isinstance(encoded, str)

            # 1.3 Asserts: decoded...
            assert isinstance(decoded, pd.Series)
            assert decoded.equals(value)

        # 2. None, Other...
        else:

            # 1.1 Encode, Decode, Asserts...
            decoded = pyon.decode(pyon.encode(value))
            assert decoded == value # type: ignore

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize(
        "enc_protected, enc_private, expected_protected, expected_private",
        [
            (True,  False, 2, None),   # Only protected
            (False, True, None, 3),    # Only private
            (True,  True, 2, 3),       # Both protected and private
        ]
    )
    def test_visibility_options(
        self, enc_protected, enc_private, expected_protected, expected_private
    ):
        """
        Tests encoding/decoding with combinations of `enc_protected` and `enc_private`.
        """

        # 1. Prepare object...
        obj = _TestClass()

        # 2. Round-trip object...
        encoded = pyon.encode(obj, enc_protected=enc_protected, enc_private=enc_private)
        decoded = pyon.decode(encoded)

        # 3. Validate public value...
        assert isinstance(decoded, _TestClass)
        assert decoded.public == 1

        # 4. Validate hidden values...
        assert getattr(decoded, "_protected", None) == expected_protected  # pylint: disable=protected-access
        assert getattr(decoded, "_TestClass__private", None) == expected_private

    # ----------------------------------------------------------------------------------------- #

    def _test_default(self, value, clazz):
        """ Test encoding and decoding for complex numbers. """

        # 1. Valid case...
        if isinstance(clazz, type) and isinstance(value, clazz):

            # 1.1 Encode, Decode...
            encoded = pyon.encode(value)
            decoded = pyon.decode(encoded)

            # 1.2 Asserts: encoded...
            assert encoded != value
            assert isinstance(encoded, str)

            # 1.3 If not builtins, checks name in type...
            if not self._is_builtins(clazz) or isinstance(clazz, dict):
                assert clazz.__name__.lower() in encoded.lower()

            # 1.4 Asserts: decoded...
            if not (hasattr(decoded, "__dict__") and isinstance(decoded.__dict__, dict)):
                assert decoded == value

            # 1.5 Asserts: decode dict...
            elif hasattr(value, "__dict__") and isinstance(value.__dict__, dict):
                for key, val in value.__dict__.items():

                    # 3.1 Both must have the same key and value...
                    assert key in decoded.__dict__
                    assert decoded.__dict__[key] == val

            # 1.6 Fails...
            else:
                pytest.fail(
                    (
                        f"Fail. Expected: {clazz}. "
                        f"Value: {type(value)}. "
                        f"Result: {type(decoded)}."
                    )
                )

        # 2. None, Other...
        else:

            # 1.1 Encode, Decode, Asserts...
            decoded = pyon.decode(pyon.encode(value))
            assert decoded == value

    # ----------------------------------------------------------------------------------------- #

    def _is_builtins(self, clazz):
        """ Checks if a class is builtins """

        # 1. Checks...
        return isinstance(clazz, type) and clazz in {int, float, bool, str, type}

    # ----------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #
