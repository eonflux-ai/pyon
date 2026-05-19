# --------------------------------------------------------------------------------------------- #
""" Pyon: Base Encoder """
# --------------------------------------------------------------------------------------------- #

import logging

# --------------------------------------------------------------------------------------------- #

from ..utils import EConst

# --------------------------------------------------------------------------------------------- #

from .. import utils as ut

# --------------------------------------------------------------------------------------------- #

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------------------- #


class BaseEnc():
    """ Base Encoder """

    # ----------------------------------------------------------------------------------------- #

    def encode(self, value):
        """ Encodes the Entity object """

        # 1. Prepare encoded value...
        encoded = None
        if self.is_encode(value):

            # 1.1 Encode type...
            if isinstance(value, type):
                encoded = self._encode_type(value)

            # 1.2 Keep base value...
            else:
                encoded = value

        # 2. Return encoded value...
        return encoded

    # ----------------------------------------------------------------------------------------- #

    def decode(self, value):
        """ Decodes the value """

        # 1. Prepare decoded value...
        decoded = None
        if self.is_decode(value):

            # 1.1 Decode type...
            if self._is_decode_type(value):
                decoded = self._decode_type(value)

            # 1.2 Keep base value...
            else:
                decoded = value

        # 2. Return decoded value...
        return decoded

    # ----------------------------------------------------------------------------------------- #

    def is_encode(self, value):
        """ 
            Checks if Base Types:
            - `bool`, `float`, `int`, `str`, `type`, `None`
        """

        # 1. Check supported value...
        return isinstance(value, (int, float, str, bool, type)) or (value is None)

    # ----------------------------------------------------------------------------------------- #

    def is_decode(self, value):
        """ 
            Checks if Base Types:
            - `bool`, `float`, `int`, `str`, `type`, `None`
        """

        # 1. Prepare decode flag...
        is_decode = False

        # 2. Check base payload...
        if self.is_encode(value) or self._is_decode_type(value):
            is_decode = True

        # 3. Return decode flag...
        return is_decode

    # ----------------------------------------------------------------------------------------- #

    def _is_decode_type(self, value):
        """ 
            Checks if Base Types:
            - `bool`, `float`, `int`, `str`, `type`, `None`
        """

        # 1. Check type payload...
        return isinstance(value, dict) and (EConst.CLASS in value) and (len(value) == 1)

    # ----------------------------------------------------------------------------------------- #

    def _encode_type(self, value: type):
        """ Encodes a type object. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, type):

            # 1.1 Resolve class name...
            class_name = ut.get_class_name(value)

            # 1.2 Build payload...
            output = {EConst.CLASS: class_name}

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: type. Received: %s", type(value))

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_type(self, value: dict):
        """ Decodes a type object. """

        # 1. Checks input...
        output = None
        if value is not None:

            # 1.1 Decodes...
            output = ut.get_class(value)

        # 2. If invalid...
        else:

            # 1.1 Log invalid type...
            logger.error(
                "Invalid type input. Expected: dict with %s. Received: %s",
                EConst.TYPE,
                type(value),
            )

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #
