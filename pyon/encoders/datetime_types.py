# --------------------------------------------------------------------------------------------- #
""" Pyon: Datetime Encoder """
# --------------------------------------------------------------------------------------------- #

import logging

# --------------------------------------------------------------------------------------------- #

from datetime import datetime, date, time, timezone, timedelta
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

        # 1. ...
        encoded = None
        if self.is_encode(value):

            # 1.1 Datetime...
            if isinstance(value, datetime):
                encoded = self._encode_datetime(value)

            # 1.2 Date...
            elif isinstance(value, date):
                encoded = self._encode_date(value)

            # 1.3 Time...
            elif isinstance(value, time):
                encoded = self._encode_time(value)

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

            # 1.1 Date...
            if _type == SupportedTypes.DATE.value:
                decoded = self._decode_date(value)

            # 1.2 Datetime...
            elif _type == SupportedTypes.DATETIME.value:
                decoded = self._decode_datetime(value)

            # 1.3 Time...
            elif _type == SupportedTypes.TIME.value:
                decoded = self._decode_time(value)

        # 3. ...
        return decoded

    # ----------------------------------------------------------------------------------------- #

    def is_encode(self, value):
        """ 
            Checks if Datetime Types:
            - `datetime.date`, `datetime.datetime`, `datetime.time`
        """

        # 1. ...
        return isinstance(value, (date, datetime, time))

    # ----------------------------------------------------------------------------------------- #

    def is_decode(self, value):
        """ 
            Checks if Datetime Types:
            - `datetime.date`, `datetime.datetime`, `datetime.time`
        """

        # 1. ...
        is_decode = False

        # 2. ...
        if ut.is_decode_able(value):
            _type = value.get(EConst.TYPE)

            # 1.1 Checks...
            if _type in (
                SupportedTypes.DATE.value,
                SupportedTypes.DATETIME.value,
                SupportedTypes.TIME.value
            ):

                # 2.1 ...
                is_decode = True

        # 3. ...
        return is_decode

    # ----------------------------------------------------------------------------------------- #

    def _encode_date(self, value: date):
        """ Encodes a date object to ISO 8601 format. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, date):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.DATE.value,
                EConst.DATA: value.isoformat()
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: date. Received: %s", type(value))

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_date(self, value: dict):
        """ Decodes an ISO 8601 string back to a date object. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Decodes...
            output = date.fromisoformat(value[EConst.DATA])

        # 2. If invalid...
        else:

            # 1.1 Logs...
            logger.error(
                "Invalid date input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Returns...
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
                EConst.TZ: {}
            }

            # 1.2 Preserve timezone identity and offset if available...
            if value.tzinfo is not None:
                tz_meta = {}

                # 2.1 ...
                tz_zone = getattr(value.tzinfo, "key", None) or getattr(value.tzinfo, "zone", None)
                tz_offset = value.utcoffset()

                # 2.2 ...
                if tz_zone:
                    tz_meta[EConst.TZ_ZONE] = tz_zone

                # 2.3 ...
                if tz_offset is not None:
                    tz_meta[EConst.TZ_OFFSET] = self.__format_offset(tz_offset)

                # 2.4 PEP 495 fold flag...
                fold = getattr(value, "fold", 0)

                # 2.5 Only include when ambiguous time fold==1...
                if isinstance(fold, int) and (fold == 1):
                    tz_meta[EConst.TZ_FOLD] = 1

                # 2.6 Attach tz meta if any...
                if tz_meta:
                    output[EConst.TZ] = tz_meta

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: datetime. Received: %s", type(value))

        # 3. Returns...
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
            tz_meta = value.get(EConst.TZ)
            if isinstance(tz_meta, dict):

                # 2.1 Extracts TZ...
                tz_zone = tz_meta.get(EConst.TZ_ZONE)
                tz_offset_str = tz_meta.get(EConst.TZ_OFFSET)
                tz_fold = tz_meta.get(EConst.TZ_FOLD)

                # 2.2 If zone name available and ZoneInfo supported, converts...
                if tz_zone and ZoneInfo is not None:
                    try:

                        # 4.1 ...
                        output = output.astimezone(ZoneInfo(tz_zone))

                    # 3.1 ...
                    except ZoneInfoNotFoundError:

                        # 4.1 Fallback to offset if zone lookup fails...
                        if tz_offset_str and (output.tzinfo is None):
                            output = output.replace(tzinfo=self.__parse_offset(tz_offset_str))

                # 2.3 ...
                else:

                    # 3.1 If only offset is available and dt is naive, attach fixed offset...
                    if tz_offset_str and (output.tzinfo is None):
                        output = output.replace(tzinfo=self.__parse_offset(tz_offset_str))

                # 2.4 Apply fold flag when provided...
                if tz_fold in (0, 1):
                    try:

                        # 4.1 ...
                        output = output.replace(fold=int(tz_fold))

                    # 3.1 ...
                    except ValueError:
                        pass

        # 2. If invalid...
        else:

            # 1.1 Logs...
            logger.error(
                "Invalid datetime input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Returns...
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
                EConst.TZ: {}
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
                    output[EConst.TZ] = tz_meta

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: time. Received: %s", type(value))

        # 3. Returns...
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
            tz_meta = value.get(EConst.TZ)
            if isinstance(tz_meta, dict):

                # 2.1 Extracts TZ...
                tz_zone = tz_meta.get(EConst.TZ_ZONE)
                tz_offset_str = tz_meta.get(EConst.TZ_OFFSET)

                # 2.2 If zone name available and ZoneInfo supported, prefer it...
                if tz_zone and ZoneInfo is not None:
                    try:

                        # 4.1 ...
                        output = output.replace(tzinfo=ZoneInfo(tz_zone))

                    # 3.1 ...
                    except ZoneInfoNotFoundError:

                        # 4.1 Fallback to offset if zone lookup fails...
                        if tz_offset_str and (output.tzinfo is None):
                            output = output.replace(tzinfo=self.__parse_offset(tz_offset_str))

                # 2.3 Otherwise attach fixed offset...
                else:

                    # 3.1 If only offset is available and time is naive, attach fixed offset...
                    if tz_offset_str and (output.tzinfo is None):
                        output = output.replace(tzinfo=self.__parse_offset(tz_offset_str))

        # 2. If invalid...
        else:

            # 1.1 Logs...
            logger.error(
                "Invalid time input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __format_offset(self, delta: timedelta) -> str:
        """Format a UTC offset timedelta as "+HH:MM" or "-HH:MM"."""

        # 1. ...
        total_seconds = int(delta.total_seconds())
        sign = "+" if total_seconds >= 0 else "-"

        # 2. ...
        total_seconds = abs(total_seconds)
        hours, rem = divmod(total_seconds, 3600)
        minutes, _ = divmod(rem, 60)

        # 3. ...
        return f"{sign}{hours:02d}:{minutes:02d}"

    # ----------------------------------------------------------------------------------------- #

    def __parse_offset(self, s: str):
        """Parse a string like "+HH:MM"/"-HH:MM" to a tzinfo (fixed offset)."""

        # 1. ...
        output = None
        try:

            # 1.1 ...
            if isinstance(s, str) and (len(s) > 6) and (s[3] == ":"):

                # 2.1 ...
                sign = 1 if s[0] == "+" else -1
                hours = int(s[1:3])
                minutes = int(s[4:6])
                delta = timedelta(hours=hours, minutes=minutes) * sign

                # 2.2 ...
                output = timezone(delta)

        # 2. ...
        except ValueError:
            pass

        # 3. ...
        return output

# --------------------------------------------------------------------------------------------- #
