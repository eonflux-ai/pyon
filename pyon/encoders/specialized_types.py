# --------------------------------------------------------------------------------------------- #
""" Pyon: Specialized Encoder """
# --------------------------------------------------------------------------------------------- #

import logging

# --------------------------------------------------------------------------------------------- #

from uuid import UUID

# --------------------------------------------------------------------------------------------- #

import numpy
import pandas

# --------------------------------------------------------------------------------------------- #

from bitarray import bitarray

# --------------------------------------------------------------------------------------------- #

from ..file import File
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

        # 1. ...
        encoded = None
        if self.is_encode(value):

            # 1.1 Bitarray...
            if isinstance(value, bitarray):
                encoded = self._encode_bitarray(value)

            # 1.2 DataFrames...
            elif isinstance(value, pandas.DataFrame):
                encoded = self._encode_dataframe(value)

            # 1.3 File...
            elif isinstance(value, File):
                encoded = self._encode_file(value)

            # 1.4 Numpy...
            elif isinstance(value, numpy.ndarray):
                encoded = self._encode_ndarray(value)

            # 1.5 UUID...
            elif isinstance(value, UUID):
                encoded = self._encode_uuid(value)

        # 2. ...
        return encoded

    # ----------------------------------------------------------------------------------------- #

    def decode(self, value):
        """ Decodes the value """

        # 1. ...
        decoded = None

        # 2. ...
        if ut.is_decode_able(value):
            _type = value.get(EConst.TYPE)

            # 1.1 Bitarray...
            if _type == SupportedTypes.BITARRAY.value:
                decoded = self._decode_bitarray(value)

            # 1.2 Dataframe...
            elif _type == SupportedTypes.DATAFRAME.value:
                decoded = self._decode_dataframe(value)

            # 1.3 File...
            elif _type == SupportedTypes.FILE.value:
                decoded = self._decode_file(value)

            # 1.4 Numpy...
            elif _type == SupportedTypes.NDARRAY.value:
                decoded = self._decode_ndarray(value)

            # 1.5 UUID...
            elif _type == SupportedTypes.UUID.value:
                decoded = self._decode_uuid(value)

        # 3. ...
        return decoded

    # ----------------------------------------------------------------------------------------- #

    def is_encode(self, value):
        """ 
            Checks if Specialized Types:
            - `bitarray.bitarray`, `numpy.ndarray`, `pandas.DataFrame`, `pyon.File`, `uuid.UUID`
        """

        # 1. ...
        return isinstance(
            value,
            (
                bitarray,
                numpy.ndarray,
                pandas.DataFrame,
                File,
                UUID
            )
        )

    # ----------------------------------------------------------------------------------------- #

    def is_decode(self, value):
        """ 
            Checks if Specialized Types:
            - `bitarray.bitarray`, `numpy.ndarray`, `pandas.DataFrame`, `pyon.File`, `uuid.UUID`
        """

        # 1. ...
        is_decode = False

        # 2. ...
        if ut.is_decode_able(value):
            _type = value.get(EConst.TYPE)

            # 1.1 Checks...
            if _type in (
                SupportedTypes.BITARRAY.value,
                SupportedTypes.DATAFRAME.value,
                SupportedTypes.FILE.value,
                SupportedTypes.NDARRAY.value,
                SupportedTypes.UUID.value,
            ):

                # 2.1 ...
                is_decode = True

        # 3. ...
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

        # 3. Returns...
        return encoded

    # ----------------------------------------------------------------------------------------- #

    def _decode_bitarray(self, value: dict):
        """ Decodes a dictionary representation back to a bitarray object. """

        # 1. ...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 ...
            output = bitarray(value[EConst.DATA])

        # 2. ...
        else:

            # 1.1 ...
            logger.error(
                "Invalid bitarray input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. ...
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
                EConst.DATA: value.to_dict()
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: File. Received: %s", type(value))

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_file(self, value: dict):
        """ Decodes to File """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Decodes...
            output = File.from_dict(value[EConst.DATA])

        # 2. If invalid...
        else:

            # 1.1 Logs...
            logger.error(
                "Invalid file input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Returns...
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

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_ndarray(self, value: dict):
        """ Decodes to Numpy ndarray """

        # 1. Checks input...
        output = None
        if (
            (value is not None)
            and isinstance(value, dict)
            and (EConst.DATA in value)
            and (EConst.AUX1 in value)
        ):

            # 1.1 Decodes...
            np_array = numpy.array(value[EConst.DATA])
            output = np_array.reshape(value[EConst.AUX1])

        # 2. If invalid...
        else:

            # 1.1 Logs...
            logger.error(
                "Invalid ndarray input. Expected: dict with %s and %s. Received: %s",
                EConst.DATA,
                EConst.AUX1,
                type(value),
            )

        # 3. Returns...
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

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_uuid(self, value: dict):
        """ Decodes a string representation back to a UUID object. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Decodes...
            output = UUID(value[EConst.DATA])

        # 2. If invalid...
        else:

            # 1.1 Logs...
            logger.error(
                "Invalid UUID input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Returns...
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
                EConst.DATA: value.to_dict(orient="records"),
                EConst.AUX1: list(value.columns),
                EConst.AUX2: self.__pre_encode_index(value.index),
                EConst.AUX3: list(value.index.names),
                EConst.AUX4: type(value.index).__name__,
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: pandas.DataFrame. Received: %s", type(value))

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_dataframe(self, value: dict):
        """ Decodes to a DataFrame. """

        # 1. Checks input...
        output = None
        if (
            (value is not None)
            and isinstance(value, dict)
            and (EConst.DATA in value)
            and (EConst.AUX1 in value)
            and (EConst.AUX2 in value)
            and (EConst.AUX3 in value)
            and (EConst.AUX4 in value)
        ):

            # 1.1 Recreates the base DataFrame...
            df = pandas.DataFrame(value[EConst.DATA])
            df = df.reindex(columns=value[EConst.AUX1])

            # 1.2 Extracts the index data...
            index_data = value[EConst.AUX2]
            index_names = value.get(EConst.AUX3)
            index_type = value.get(EConst.AUX4)

            # 1.3 Validates the index type...
            if index_type in self._DF_INDEXES:
                index_name = index_names[0] if index_names else None

                # 2.1 Pre-decodes the index data...
                index_data = self.__pre_decode_index(index_data, index_type)

                # 2.2 Rebuilds the index: Multi Index...
                if index_type == "MultiIndex":
                    df.index = pandas.MultiIndex.from_tuples(index_data, names=index_names)

                # 2.3 Range Index...
                elif (index_type == "RangeIndex") and self.__is_arithmetic_range(index_data):
                    df.index = self.__build_range_index(index_data, index_name)

                # 2.4 Datetime Index...
                elif index_type == "DatetimeIndex":
                    df.index = pandas.DatetimeIndex(index_data, name=index_name)

                # 2.5 Period Index...
                elif index_type == "PeriodIndex":
                    df.index = pandas.PeriodIndex(index_data, name=index_name)

                # 2.6 Timedelta Index ...
                elif index_type == "TimedeltaIndex":
                    df.index = pandas.TimedeltaIndex(index_data, name=index_name)

                # 2.7 Categorical Index...
                elif index_type == "CategoricalIndex":
                    df.index = pandas.CategoricalIndex(index_data, name=index_name)

                # 2.8 Generic Index...
                else:
                    df.index = pandas.Index(index_data, name=index_name)

                # 2.9 Sets the output...
                output = df

            # 1.4 Invalid index type...
            else:
                logger.error("Invalid index type: %s", index_type)

        # 2. If invalid...
        else:

            # 1.1 Logs...
            logger.error(
                "Invalid dataframe input. Expected: dict with %s, %s, %s, %s, %s. Received: %s",
                EConst.DATA,
                EConst.AUX1,
                EConst.AUX2,
                EConst.AUX3,
                EConst.AUX4,
                type(value),
            )

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __is_arithmetic_range(self, seq):
        """Validates whether a sequence represents a regular arithmetic range."""
        
        # 1. ...
        return (
            isinstance(seq, list)
            and len(seq) >= 2
            and all((seq[i + 1] - seq[i]) == (seq[1] - seq[0]) for i in range(len(seq) - 1))
        )

    # ----------------------------------------------------------------------------------------- #

    def __build_range_index(self, seq, name):
        """Builds a pandas RangeIndex from a valid arithmetic sequence."""
        
        # 1. ...
        step = seq[1] - seq[0]
        
        # 2. ...
        start = seq[0]
        stop = seq[-1] + step
        
        # 3. ...
        return pandas.RangeIndex(start=start, stop=stop, step=step, name=name)

    # ----------------------------------------------------------------------------------------- #

    def __pre_encode_index(self, index):
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

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __pre_decode_index(self, index_data, index_type):
        """ Reconstructs index elements after decoding from JSON-safe format. """

        # 1. MultiIndex elements are tuples...
        if index_type == "MultiIndex":
            output = [tuple(x) for x in index_data]

        # 2. DatetimeIndex...
        elif index_type == "DatetimeIndex":
            output = [pandas.Timestamp(x) for x in index_data]

        # 3. PeriodIndex...
        elif index_type == "PeriodIndex":
            output = [pandas.Period(x) for x in index_data]

        # 4. TimedeltaIndex...
        elif index_type == "TimedeltaIndex":
            output = [pandas.Timedelta(x) for x in index_data]

        # 5. Fallback: keep as-is...
        else:
            output = index_data

        # 6. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #
