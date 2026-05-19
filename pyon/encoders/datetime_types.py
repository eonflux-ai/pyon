# --------------------------------------------------------------------------------------------- #
""" Pyon: Datetime Encoder """
# --------------------------------------------------------------------------------------------- #

import logging

# --------------------------------------------------------------------------------------------- #

from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# --------------------------------------------------------------------------------------------- #

from ..utils import EConst
from ..supported_types import SupportedTypes

# --------------------------------------------------------------------------------------------- #

from .. import utils as ut

# --------------------------------------------------------------------------------------------- #

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------------------- #


class DateEnc():
    """ Pyon Encoder """

    # ----------------------------------------------------------------------------------------- #

    def encode(self, value):
        """ Encodes the Entity object """

        # 1. Prepare encoded value...
        encoded = None
        if self.is_encode(value):

            # 1.1 Encode datetime...
            if isinstance(value, datetime):
                encoded = self._encode_datetime(value)

            # 1.2 Encode date...
            elif isinstance(value, date):
                encoded = self._encode_date(value)

            # 1.3 Encode time...
            elif isinstance(value, time):
                encoded = self._encode_time(value)

        # 2. Return encoded value...
        return encoded

    # ----------------------------------------------------------------------------------------- #

    def decode(self, value):
        """ Decodes the value """

        # 1. Prepare decoded value...
        decoded = None

        # 2. Check datetime payload...
        if ut.is_decode_able(value):
            _type = value.get(EConst.TYPE)

            # 1.1 Decode date...
            if _type == SupportedTypes.DATE.value:
                decoded = self._decode_date(value)

            # 1.2 Decode datetime...
            elif _type == SupportedTypes.DATETIME.value:
                decoded = self._decode_datetime(value)

            # 1.3 Decode time...
            elif _type == SupportedTypes.TIME.value:
                decoded = self._decode_time(value)

        # 3. Return decoded value...
        return decoded

    # ----------------------------------------------------------------------------------------- #

    def is_encode(self, value):
        """ 
            Checks if Datetime Types:
            - `datetime.date`, `datetime.datetime`, `datetime.time`
        """

        # 1. Check datetime value...
        return isinstance(value, (date, datetime, time))

    # ----------------------------------------------------------------------------------------- #

    def is_decode(self, value):
        """ 
            Checks if Datetime Types:
            - `datetime.date`, `datetime.datetime`, `datetime.time`
        """

        # 1. Prepare decode flag...
        is_decode = False

        # 2. Check datetime payload...
        if ut.is_decode_able(value):
            _type = value.get(EConst.TYPE)

            # 1.1 Prepare type set...
            datetime_types = (
                SupportedTypes.DATE.value,
                SupportedTypes.DATETIME.value,
                SupportedTypes.TIME.value,
            )

            # 1.2 Check type marker...
            if _type in datetime_types:

                # 2.1 Accept datetime type...
                is_decode = True

        # 3. Return decode flag...
        return is_decode

    # ----------------------------------------------------------------------------------------- #

    def _encode_date(self, value: date):
        """ Encodes a date object to ISO 8601 format. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, date):

            # 1.1 Build payload...
            output = {
                EConst.TYPE: SupportedTypes.DATE.value,
                EConst.DATA: value.isoformat()
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: date. Received: %s", type(value))

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_date(self, value: dict):
        """ Decodes an ISO 8601 string back to a date object. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Decodes...
            output = date.fromisoformat(value[EConst.DATA])

        # 2. Log invalid payload...
        else:

            # 1.1 Log invalid date...
            logger.error(
                "Invalid date input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_datetime(self, value: datetime):
        """ Encodes a datetime object to ISO 8601 format. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, datetime):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.DATETIME.value,
                EConst.DATA: value.isoformat(),
                EConst.AUX1: {}
            }

            # 1.2 Preserve timezone identity and offset if available...
            if value.tzinfo is not None:
                tz_meta = {}

                # 2.1 Stores zone...
                tz_zone = getattr(value.tzinfo, "key", None) or getattr(value.tzinfo, "zone", None)
                tz_offset = value.utcoffset()

                # 2.2 Stores offset...
                if tz_zone:
                    tz_meta[EConst.TZ_ZONE] = tz_zone

                # 2.3 Stores fold...
                if tz_offset is not None:
                    tz_meta[EConst.TZ_OFFSET] = self.__format_offset(tz_offset)

                # 2.4 PEP 495 fold flag...
                fold = getattr(value, "fold", 0)

                # 2.5 Only include when ambiguous time fold==1...
                if isinstance(fold, int) and (fold == 1):
                    tz_meta[EConst.TZ_FOLD] = 1

                # 2.6 Attach tz meta if any...
                if tz_meta:
                    output[EConst.AUX1] = tz_meta

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: datetime. Received: %s", type(value))

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_datetime(self, value: dict):
        """ Decodes an ISO 8601 string back to a datetime object. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Decodes base datetime (includes fixed offset if present)...
            output = datetime.fromisoformat(value[EConst.DATA])

            # 1.2 Apply timezone identity if provided...
            tz_meta = value.get(EConst.AUX1)
            if isinstance(tz_meta, dict):
                output = self.__apply_datetime_tz_meta(output, tz_meta)

        # 2. Log invalid payload...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid datetime input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __apply_datetime_tz_meta(self, output, tz_meta):
        """Applies serialized timezone metadata to a decoded datetime."""

        # 1. Extract metadata...
        tz_zone = tz_meta.get(EConst.TZ_ZONE)
        tz_offset_str = tz_meta.get(EConst.TZ_OFFSET)

        # 2. Apply zone or offset...
        output = self.__apply_datetime_zone_or_offset(output, tz_zone, tz_offset_str)

        # 3. Apply fold...
        output = self.__apply_datetime_fold(output, tz_meta.get(EConst.TZ_FOLD))

        # 4. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __apply_datetime_zone_or_offset(self, output, tz_zone, tz_offset_str):
        """Applies a zone name when possible, otherwise applies a fixed offset."""

        # 1. Prefer named zone...
        if tz_zone and ZoneInfo is not None:
            try:

                # 2.1 Load zone...
                zone = ZoneInfo(tz_zone)

                # 2.2 Attach or convert...
                if output.tzinfo is None:
                    output = output.replace(tzinfo=zone)

                # 2.3 Convert aware value...
                else:
                    output = output.astimezone(zone)

            # 1.1 Fallback to offset...
            except ZoneInfoNotFoundError:
                output = self.__apply_datetime_offset(output, tz_offset_str)

        # 2. Apply fixed offset...
        else:
            output = self.__apply_datetime_offset(output, tz_offset_str)

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __apply_datetime_offset(self, output, tz_offset_str):
        """Attaches a fixed offset when the decoded datetime is naive."""

        # 1. Apply offset...
        if tz_offset_str and (output.tzinfo is None):
            output = output.replace(tzinfo=self.__parse_offset(tz_offset_str))

        # 2. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __apply_datetime_fold(self, output, tz_fold):
        """Applies a valid PEP 495 fold value."""

        # 1. Apply valid fold...
        if tz_fold in (0, 1):
            try:
                output = output.replace(fold=int(tz_fold))

            # 1.1 Preserve decoded value...
            except ValueError:
                pass

        # 2. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_time(self, value: time):
        """ Encodes a time object to ISO 8601 format. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, time):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.TIME.value,
                EConst.DATA: value.isoformat(),
                EConst.AUX1: {}
            }

            # 1.2 Preserve timezone identity and offset if available...
            if value.tzinfo is not None:
                tz_meta = {}

                # 2.1 Extracts TZ info...
                tz_zone = getattr(value.tzinfo, "key", None) or getattr(value.tzinfo, "zone", None)
                tz_offset = value.utcoffset()

                # 2.2 Attach zone name (if available)...
                if tz_zone:
                    tz_meta[EConst.TZ_ZONE] = tz_zone

                # 2.3 Attach fixed offset (if available)...
                if tz_offset is not None:
                    tz_meta[EConst.TZ_OFFSET] = self.__format_offset(tz_offset)

                # 2.4 Attach tz meta if any...
                if tz_meta:
                    output[EConst.AUX1] = tz_meta

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: time. Received: %s", type(value))

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_time(self, value: dict):
        """ Decodes an ISO 8601 string back to a time object. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Decodes base time (includes fixed offset if present)...
            output = time.fromisoformat(value[EConst.DATA])

            # 1.2 Apply timezone identity if provided...
            tz_meta = value.get(EConst.AUX1)
            if isinstance(tz_meta, dict):
                output = self.__apply_time_tz_meta(output, tz_meta)

        # 2. Log invalid payload...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid time input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __apply_time_tz_meta(self, output, tz_meta):
        """Applies serialized timezone metadata to a decoded time."""

        # 1. Extract metadata...
        tz_zone = tz_meta.get(EConst.TZ_ZONE)
        tz_offset_str = tz_meta.get(EConst.TZ_OFFSET)

        # 2. Apply zone or offset...
        output = self.__apply_time_zone_or_offset(output, tz_zone, tz_offset_str)

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __apply_time_zone_or_offset(self, output, tz_zone, tz_offset_str):
        """Applies a named time zone or an offset fallback to a time value."""

        # 1. Prefer named zone...
        if tz_zone and ZoneInfo is not None:
            try:
                output = output.replace(tzinfo=ZoneInfo(tz_zone))

            # 1.1 Fallback to offset...
            except ZoneInfoNotFoundError:
                output = self.__apply_time_offset(output, tz_offset_str)

        # 2. Apply fixed offset...
        else:
            output = self.__apply_time_offset(output, tz_offset_str)

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __apply_time_offset(self, output, tz_offset_str):
        """Attaches a fixed offset when the decoded time is naive."""

        # 1. Apply offset...
        if tz_offset_str and (output.tzinfo is None):
            output = output.replace(tzinfo=self.__parse_offset(tz_offset_str))

        # 2. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __format_offset(self, delta: timedelta) -> str:
        """Format a UTC offset timedelta as "+HH:MM" or "-HH:MM"."""

        # 1. Prepare signed seconds...
        total_seconds = int(delta.total_seconds())
        sign = "+" if total_seconds >= 0 else "-"

        # 2. Split absolute time...
        total_seconds = abs(total_seconds)
        hours, rem = divmod(total_seconds, 3600)
        minutes, _ = divmod(rem, 60)

        # 3. Return formatted offset...
        return f"{sign}{hours:02d}:{minutes:02d}"

    # ----------------------------------------------------------------------------------------- #

    def __parse_offset(self, s: str):
        """Parse a string like "+HH:MM"/"-HH:MM" to a tzinfo (fixed offset)."""

        # 1. Parse offset...
        return ut.parse_utc_offset(s)

# --------------------------------------------------------------------------------------------- #
