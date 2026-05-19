# --------------------------------------------------------------------------------------------- #
""" Pyon: Specialized Encoder """
# --------------------------------------------------------------------------------------------- #
import logging

# --------------------------------------------------------------------------------------------- #

from uuid import UUID
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# --------------------------------------------------------------------------------------------- #

import numpy
import pandas

# --------------------------------------------------------------------------------------------- #

from bitarray import bitarray
from pandas.tseries.frequencies import to_offset

# --------------------------------------------------------------------------------------------- #

from ..file.api import File
from ..utils import EConst
from ..supported_types import SupportedTypes

# --------------------------------------------------------------------------------------------- #

from .. import utils as ut

# --------------------------------------------------------------------------------------------- #

from .base_encoder import BaseEncoder

# --------------------------------------------------------------------------------------------- #

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------------------- #


class SpecEnc(BaseEncoder):
    """ Specialized Encoder """

    # ----------------------------------------------------------------------------------------- #

    _DF_INDEXES = {
        "Index",
        "RangeIndex",
        "MultiIndex",
        "DatetimeIndex",
        "TimedeltaIndex",
        "PeriodIndex",
        "CategoricalIndex",
        "Float64Index",
        "Int64Index",
        "UInt64Index"
    }

    # ----------------------------------------------------------------------------------------- #

    def encode(self, value):
        """ Encodes the Entity object """

        # 1. Prepare encoded value...
        encoded = None
        if self.is_encode(value):

            # 1.1 Encode bitarray...
            if isinstance(value, bitarray):
                encoded = self._encode_bitarray(value)

            # 1.2 Encode file...
            elif isinstance(value, File):
                encoded = self._encode_file(value)

            # 1.3 Encode ndarray...
            elif isinstance(value, numpy.ndarray):
                encoded = self._encode_ndarray(value)

            # 1.4 Encode UUID...
            elif isinstance(value, UUID):
                encoded = self._encode_uuid(value)

            # 1.5 Encode DataFrame...
            elif isinstance(value, pandas.DataFrame):
                encoded = self._encode_dataframe(value)

            # 1.6 Encode Series...
            elif isinstance(value, pandas.Series):
                encoded = self._encode_series(value)

        # 2. Return encoded value...
        return encoded

    # ----------------------------------------------------------------------------------------- #

    def decode(self, value):
        """ Decodes the value """

        # 1. Prepare decoded value...
        decoded = None

        # 2. Check specialized payload...
        if ut.is_decode_able(value):
            _type = value.get(EConst.TYPE)

            # 1.1 Decode bitarray...
            if _type == SupportedTypes.BITARRAY.value:
                decoded = self._decode_bitarray(value)

            # 1.2 Decode file...
            elif _type == SupportedTypes.FILE.value:
                decoded = self._decode_file(value)

            # 1.3 Decode ndarray...
            elif _type == SupportedTypes.NDARRAY.value:
                decoded = self._decode_ndarray(value)

            # 1.4 Decode UUID...
            elif _type == SupportedTypes.UUID.value:
                decoded = self._decode_uuid(value)

            # 1.5 Decode DataFrame...
            elif _type == SupportedTypes.DATAFRAME.value:
                decoded = self._decode_dataframe(value)

            # 1.6 Decode Series...
            elif _type == SupportedTypes.SERIES.value:
                decoded = self._decode_series(value)

        # 3. Return decoded value...
        return decoded

    # ----------------------------------------------------------------------------------------- #

    def is_encode(self, value):
        """ 
            Checks if encode of Specialized Types:
            - `bitarray.bitarray`, `numpy.ndarray`, `pyon.File`, `uuid.UUID`
            - `pandas.DataFrame`, `pandas.Series`
        """

        # 1. Check specialized value...
        return isinstance(
            value,
            (
                bitarray,
                numpy.ndarray,
                File,
                UUID,
                pandas.DataFrame,
                pandas.Series
            )
        )

    # ----------------------------------------------------------------------------------------- #

    def is_decode(self, value):
        """ 
            Checks if decode of Specialized Types:
            - `bitarray.bitarray`, `numpy.ndarray`, `pyon.File`, `uuid.UUID`
            - `pandas.DataFrame`, `pandas.Series`
        """

        # 1. Prepare decode flag...
        is_decode = False

        # 2. Check specialized payload...
        if ut.is_decode_able(value):
            _type = value.get(EConst.TYPE)

            # 1.1 Prepare type set...
            specialized_types = (
                SupportedTypes.BITARRAY.value,
                SupportedTypes.FILE.value,
                SupportedTypes.NDARRAY.value,
                SupportedTypes.UUID.value,
                SupportedTypes.DATAFRAME.value,
                SupportedTypes.SERIES.value,
            )

            # 1.2 Check type marker...
            if _type in specialized_types:

                # 2.1 Accept specialized type...
                is_decode = True

        # 3. Return decode flag...
        return is_decode

    # ----------------------------------------------------------------------------------------- #

    def _encode_bitarray(self, value: bitarray):
        """ Encodes a bitarray object to a dictionary representation. """

        # 1. Checks input...
        encoded = None
        if (value is not None) and isinstance(value, bitarray):

            # 1.1 Encodes...
            encoded = {
                EConst.TYPE: SupportedTypes.BITARRAY.value,
                EConst.DATA: value.to01()
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: bitarray. Received: %s", type(value))

        # 3. Return output...
        return encoded

    # ----------------------------------------------------------------------------------------- #

    def _decode_bitarray(self, value: dict):
        """ Decodes a dictionary representation back to a bitarray object. """

        # 1. Prepare decoded bitarray...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Decode bits...
            output = bitarray(value[EConst.DATA])

        # 2. Log invalid bitarray...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid bitarray input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Return decoded bitarray...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_file(self, value: File):
        """ Encodes the file """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, File):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.FILE.value,
                EConst.DATA: value.to_dict(encode=True)
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: File. Received: %s", type(value))

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_file(self, value: dict):
        """ Decodes to File """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Decodes...
            output = File.from_dict(value[EConst.DATA])

        # 2. Log invalid payload...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid file input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_ndarray(self, value: numpy.ndarray):
        """ Encodes the Numpy ndarray """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, numpy.ndarray):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.NDARRAY.value,
                EConst.AUX1: value.shape,
                EConst.DATA: value.tolist(),
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: numpy.ndarray. Received: %s", type(value))

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_ndarray(self, value: dict):
        """ Decodes to Numpy ndarray """

        # 1. Checks input...
        output = None
        if (
            isinstance(value, dict)
            and isinstance(value.get(EConst.DATA), list)
            and isinstance(value.get(EConst.AUX1), (list, tuple))
        ):

            # 1.1 Creates array...
            try:

                # 2.1 Reshapes array...
                np_array = numpy.array(value[EConst.DATA])
                output = np_array.reshape(value[EConst.AUX1])

            # 1.2 Handles failure...
            except Exception:  # pylint: disable=broad-except
                logger.exception("Failed to decode ndarray (reshape or cast failed).")

        # 2. Log invalid payload...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid ndarray input. Expected: dict with %s and %s. Received: %s",
                EConst.DATA,
                EConst.AUX1,
                type(value),
            )

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_uuid(self, value: UUID):
        """ Encodes a UUID object to a string representation. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, UUID):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.UUID.value,
                EConst.DATA: str(value)
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: UUID. Received: %s", type(value))

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_uuid(self, value: dict):
        """ Decodes a string representation back to a UUID object. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Decodes...
            output = UUID(value[EConst.DATA])

        # 2. Log invalid payload...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid UUID input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_dataframe(self, value: pandas.DataFrame):
        """ Encodes the DataFrame. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, pandas.DataFrame):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.DATAFRAME.value,
                EConst.DATA: self._encode_as_dict(value.to_dict(orient="records")),
                EConst.AUX1: self.__pre_encode(value.columns),
                EConst.AUX2: self.__pre_encode(value.index),
                EConst.AUX3: list(value.index.names),
                EConst.AUX4: type(value.index).__name__,
                EConst.AUX5: list(value.columns.names),
                EConst.AUX6: type(value.columns).__name__,
                EConst.AUX7: self.__index_freq(value.index),
                EConst.AUX8: self.__index_tz(value.index)
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: pandas.DataFrame. Received: %s", type(value))

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_dataframe(self, value: dict):
        """ Decodes to a DataFrame. """

        # 1. Checks input...
        output = None
        if isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Extracts components...
            data = self._decode_from_dict(value[EConst.DATA])

            # 1.2 Decodes: columns and index...
            columns = self.__decode_columns(value)
            index = self.__decode_index(value)

            # 1.3 Output...
            output = pandas.DataFrame(
                data=data, columns=columns, index=index
            )

        # 2. Log invalid payload...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid dataframe input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_series(self, value: pandas.Series):
        """ Encodes the Series. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, pandas.Series):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.SERIES.value,
                EConst.DATA: self._encode_as_dict(value.tolist()),
                EConst.AUX1: self.__pre_encode(value.index),
                EConst.AUX2: list(value.index.names),
                EConst.AUX3: type(value.index).__name__,
                EConst.AUX4: value.name,
                EConst.AUX5: self.__index_freq(value.index),
                EConst.AUX6: self.__index_tz(value.index)
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: pandas.Series. Received: %s", type(value))

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_series(self, value: dict):
        """ Decodes to a Series. """

        # 1. Checks input...
        output = None
        if isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Extracts components...
            series_data = self._decode_from_dict(value[EConst.DATA])
            index_data = value.get(EConst.AUX1)
            index_names = value.get(EConst.AUX2)
            index_type = value.get(EConst.AUX3)
            series_name = value.get(EConst.AUX4)
            series_freq = value.get(EConst.AUX5)

            # 1.2 Pre-decodes and rebuilds index...
            tz_meta = value.get(EConst.AUX6)
            index_data = self.__pre_decode(index_data, index_type)
            index = self.__rebuild_index(index_data, index_names, index_type, series_freq, tz_meta)

            # 1.3 Builds Series...
            output = pandas.Series(data=series_data, index=index, name=series_name)

        # 2. Log invalid payload...
        else:
            logger.error(
                "Invalid series input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value)
            )

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __decode_columns(self, value: dict):
        """ Decodes to a DataFrame. """

        # 1. Checks input...
        columns = None
        if (
            isinstance(value, dict)
            and (EConst.AUX1 in value)
            and (EConst.AUX5 in value)
            and (EConst.AUX6 in value)
        ):

            # 1.1 Rebuilds columns...
            columns_data = value[EConst.AUX1]
            columns_names = value[EConst.AUX5]

            # 1.2 Pre decodes...
            columns_type = value[EConst.AUX6]
            columns_elements = self.__pre_decode(columns_data, columns_type)

            # 1.3 Multi Index...
            if columns_type == "MultiIndex":
                columns = pandas.MultiIndex.from_tuples(
                    columns_elements,  # type: ignore
                    names=columns_names
                )

            # 1.4 Other types...
            else:
                columns = pandas.Index(
                    columns_elements,
                    name=columns_names[0]
                    if columns_names
                    else None
                )

        # 2. Log invalid payload...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid dataframe input. Expected: dict with %s, %s, %s. Received: %s",
                EConst.AUX1,
                EConst.AUX5,
                EConst.AUX6,
                type(value),
            )

        # 3. Return output...
        return columns

    # ----------------------------------------------------------------------------------------- #

    def __decode_index(self, value: dict):
        """ Decodes to a DataFrame. """

        # 1. Checks input...
        index = None
        if (
            isinstance(value, dict)
            and (EConst.AUX2 in value)
            and (EConst.AUX3 in value)
            and (EConst.AUX4 in value)
        ):

            # 1.1 Extracts the index data...
            index_data = value[EConst.AUX2]
            index_names = value.get(EConst.AUX3)
            index_type = value.get(EConst.AUX4)
            index_freq = value.get(EConst.AUX7)

            # 1.2 Pre-decodes and rebuilds...
            tz_meta = value.get(EConst.AUX8)
            index_data = self.__pre_decode(index_data, index_type)
            index = self.__rebuild_index(index_data, index_names, index_type, index_freq, tz_meta)

        # 2. Log invalid payload...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid dataframe input. Expected: dict with %s, %s, %s. Received: %s",
                EConst.AUX2,
                EConst.AUX3,
                EConst.AUX4,
                type(value),
            )

        # 3. Return output...
        return index

    # ----------------------------------------------------------------------------------------- #

    def __is_arithmetic_range(self, seq):
        """Validates whether a sequence represents a regular arithmetic range."""

        # 1. Check arithmetic range...
        return (
            isinstance(seq, list)
            and len(seq) >= 2
            and all((seq[i + 1] - seq[i]) == (seq[1] - seq[0]) for i in range(len(seq) - 1))
        )

    # ----------------------------------------------------------------------------------------- #

    def __build_range_index(self, seq, name):
        """Builds a pandas RangeIndex from a valid arithmetic sequence."""

        # 1. Calculate step...
        step = seq[1] - seq[0]

        # 2. Calculate bounds...
        start = seq[0]
        stop = seq[-1] + step

        # 3. Return range index...
        return pandas.RangeIndex(start=start, stop=stop, step=step, name=name)

    # ----------------------------------------------------------------------------------------- #

    def __rebuild_index(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self, index_data, index_names, index_type, freq=None, tz_meta=None
    ):
        """ Rebuilds a pandas Index or subclass based on its serialized components. """

        # 1. Checks input...
        output = None
        index_name = index_names[0] if index_names else None

        # 2. Validates the index type...
        if index_type in self._DF_INDEXES:
            freq = to_offset(freq) if freq else None

            # 1.1 MultiIndex...
            if index_type == "MultiIndex":
                output = pandas.MultiIndex.from_tuples(index_data, names=index_names)

            # 1.2 RangeIndex...
            elif (index_type == "RangeIndex") and self.__is_arithmetic_range(index_data):
                output = self.__build_range_index(index_data, index_name)

            # 1.3 DatetimeIndex...
            elif index_type == "DatetimeIndex":
                tzinfo = self.__tzinfo_from_meta(tz_meta)

                # 2.1 If no tz meta but data is tz-aware (from pre-decode UTC normalization),
                # reuse that tz to avoid incompatibility with tz=None.
                if tzinfo is None:
                    tzinfo = getattr(index_data, "tz", None)

                # 2.2 Checks step...
                output = pandas.DatetimeIndex(
                    index_data,
                    name=index_name,
                    tz=tzinfo,  # type: ignore
                    freq=freq  # type: ignore
                )

            # 1.4 PeriodIndex...
            elif index_type == "PeriodIndex":
                output = pandas.PeriodIndex(index_data, name=index_name, freq=freq)

            # 1.5 TimedeltaIndex...
            elif index_type == "TimedeltaIndex":
                output = pandas.TimedeltaIndex(index_data, name=index_name)  # type: ignore

            # 1.6 CategoricalIndex...
            elif index_type == "CategoricalIndex":
                output = pandas.CategoricalIndex(index_data, name=index_name)

            # 1.7 Generic fallback...
            else:
                output = pandas.Index(index_data, name=index_name)

        # 3. Invalid type...
        else:
            logger.error("Invalid index type: %s", index_type)

        # 4. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __pre_encode(self, index):
        """ Converts the index into a JSON-safe list structure for serialization. """

        # 1. Checks for MultiIndex...
        if isinstance(index, pandas.MultiIndex):

            # 1.1 Converts tuples to lists...
            output = [list(x) for x in index.to_list()]

        # 2. Handles pandas-specific temporal types...
        else:

            # 1.1 Converts each element as needed...
            output = [
                str(x)
                if isinstance(x, (pandas.Timestamp, pandas.Period, pandas.Timedelta))
                else x
                for x in index
            ]

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __pre_decode(self, index_data, index_type):
        """
        Reconstructs index elements after decoding from JSON-safe format.

        **Note**:
        When rebuilding a DatetimeIndex without explicit timezone metadata (no __tz__),
        force UTC unification early to avoid pandas errors with mixed tz-aware inputs.
        """

        # 1. Prepare output...
        output = None

        # 2. MultiIndex elements are tuples...
        if index_type == "MultiIndex":
            output = [tuple(x) for x in index_data]

        # 3. DatetimeIndex...
        elif index_type == "DatetimeIndex":
            output = [pandas.Timestamp(x) for x in index_data]

        # 4. PeriodIndex...
        elif index_type == "PeriodIndex":
            output = [pandas.Period(x) for x in index_data]

        # 5. TimedeltaIndex...
        elif index_type == "TimedeltaIndex":
            output = [pandas.Timedelta(x) for x in index_data]

        # 6. Fallback: keep as-is...
        else:
            output = index_data

        # 7. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __index_freq(self, index):
        """ Checks if the index has a frequency attribute. """

        # 1. Checks for Frequency...
        output = None
        if (
            isinstance(index, (pandas.DatetimeIndex, pandas.PeriodIndex))
            and index.freq is not None
        ):

            # 1.1 Outputs...
            output = index.freq.freqstr

        # 2. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __index_tz(self, index):
        """ Checks if the index has a timezone attribute. """

        # 1. Output...
        output = None

        # 2. Checks for Timezone...
        if isinstance(index, pandas.DatetimeIndex) and (index.tz is not None):
            output = self.__build_tz_meta_from_index(index)

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __build_tz_meta_from_index(self, index: pandas.DatetimeIndex):
        """Builds timezone metadata dict from a DatetimeIndex (zone or fixed offset)."""

        # 1. Prepare metadata...
        tz_meta = {}

        # 2. Zone identity when available (ZoneInfo/pytz)...
        tz = getattr(index, "tz", None)
        tz_zone = getattr(tz, "key", None) or getattr(tz, "zone", None)

        # 3. Store zone...
        if tz_zone:
            tz_meta[EConst.TZ_ZONE] = tz_zone

        # 4. Representative fixed offset from the first element (fallback)...
        if len(index) > 0:

            # 1.1 Reads offset...
            try:
                first_item = index[0]
                off = first_item.utcoffset() if isinstance(first_item, pandas.Timestamp) else None

                # 2.1 Formats offset...
                if off is not None:
                    offset_str = self.__format_offset(off)

                    # 3.1 Stores offset...
                    if offset_str is not None:
                        tz_meta[EConst.TZ_OFFSET] = offset_str

            # 1.2 Ignores failure...
            except (TypeError, ValueError, AttributeError):
                pass

        # 5. Return only if any metadata present...
        return tz_meta or None

    # ----------------------------------------------------------------------------------------- #

    def __format_offset(self, delta):
        """Format a UTC offset timedelta as "+HH:MM" or "-HH:MM"."""

        # 1. Read seconds safely...
        total_seconds = None
        try:

            # 1.1 Reads seconds...
            total_seconds = int(delta.total_seconds())

        # 2. Ignore invalid offset...
        except (TypeError, ValueError, AttributeError, OverflowError):
            pass

        # 3. Prepare output...
        output = None
        if total_seconds is not None:

            # 1.1 Prepares sign...
            sign = "+" if total_seconds >= 0 else "-"
            total_seconds = abs(total_seconds)

            # 1.2 Splits time...
            hours, rem = divmod(total_seconds, 3600)
            minutes, _ = divmod(rem, 60)

            # 1.3 Formats offset...
            output = f"{sign}{hours:02d}:{minutes:02d}"

        # 4. Return formatted offset...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __parse_offset(self, s: str):
        """Parse a string like "+HH:MM"/"-HH:MM" to a tzinfo (fixed offset)."""

        # 1. Parse offset...
        return ut.parse_utc_offset(s)

    # ----------------------------------------------------------------------------------------- #

    def __tzinfo_from_meta(self, tz_meta):
        """Build tzinfo from serialized tz metadata (zone preferred, else fixed offset)."""

        # 1. Prepare timezone...
        tzinfo = None
        if isinstance(tz_meta, dict):

            # 1.1 Reads metadata...
            tz_zone = tz_meta.get(EConst.TZ_ZONE)
            tz_offset = tz_meta.get(EConst.TZ_OFFSET)

            # 1.2 Prefer zone when available...
            if tz_zone:
                try:

                    # 3.1 Loads zone...
                    tzinfo = ZoneInfo(tz_zone)

                except (ZoneInfoNotFoundError, ValueError):
                    tzinfo = None

            # 1.3 Fallback to fixed offset...
            if (tzinfo is None) and tz_offset:
                tzinfo = self.__parse_offset(tz_offset)

        # 2. Return output...
        return tzinfo


# --------------------------------------------------------------------------------------------- #
