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

                # 2.1 Extracts TZ...
                tz_zone = tz_meta.get(EConst.TZ_ZONE)
                tz_offset_str = tz_meta.get(EConst.TZ_OFFSET)
                tz_fold = tz_meta.get(EConst.TZ_FOLD)

                # 2.2 If zone name available and ZoneInfo supported, converts...
                if tz_zone and ZoneInfo is not None:
                    try:

                        # 4.1 Prefer attach tz when naive to avoid ValueError in astimezone
                        zone = ZoneInfo(tz_zone)

                        # 4.2 Attach tz directly...
                        if output.tzinfo is None:
                            output = output.replace(tzinfo=zone)

                        # 4.3 Convert between timezones
                        else:
                            output = output.astimezone(zone)

                    # 3.1 Applies zone...
                    except ZoneInfoNotFoundError:

                        # 4.1 Fallback to offset if zone lookup fails...
                        if tz_offset_str and (output.tzinfo is None):
                            output = output.replace(tzinfo=self.__parse_offset(tz_offset_str))

                # 2.3 Applies offset...
                else:

                    # 3.1 If only offset is available and dt is naive, attach fixed offset...
                    if tz_offset_str and (output.tzinfo is None):
                        output = output.replace(tzinfo=self.__parse_offset(tz_offset_str))

                # 2.4 Apply fold flag when provided...
                if tz_fold in (0, 1):
                    try:

                        # 4.1 Marks fold...
                        output = output.replace(fold=int(tz_fold))

                    # 3.1 Applies fallback...
                    except ValueError:
                        pass

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

                # 2.1 Extracts TZ...
                tz_zone = tz_meta.get(EConst.TZ_ZONE)
                tz_offset_str = tz_meta.get(EConst.TZ_OFFSET)

                # 2.2 If zone name available and ZoneInfo supported, prefer it...
                if tz_zone and ZoneInfo is not None:
                    try:

                        # 4.1 Applies zone...
                        output = output.replace(tzinfo=ZoneInfo(tz_zone))

                    # 3.1 Applies offset...
                    except ZoneInfoNotFoundError:

                        # 4.1 Fallback to offset if zone lookup fails...
                        if tz_offset_str and (output.tzinfo is None):
                            output = output.replace(tzinfo=self.__parse_offset(tz_offset_str))

                # 2.3 Otherwise attach fixed offset...
                else:

                    # 3.1 If only offset is available and time is naive, attach fixed offset...
                    if tz_offset_str and (output.tzinfo is None):
                        output = output.replace(tzinfo=self.__parse_offset(tz_offset_str))

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
