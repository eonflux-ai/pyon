# --------------------------------------------------------------------------------------------- #
""" Pyon: Base Encoder """
# --------------------------------------------------------------------------------------------- #

from abc import ABC

# --------------------------------------------------------------------------------------------- #
# pylint: disable=too-few-public-methods
# --------------------------------------------------------------------------------------------- #

class BaseEncoder(ABC):
    """ Base Encoder """

    # ----------------------------------------------------------------------------------------- #

    def __init__(self, encoder):
        """ Initializes a Base Encoder """

        # . ...
        if encoder is None:
            raise ValueError("Invalid Pyon Encoder")

        # . ...
        self.__encoder = encoder

    # ----------------------------------------------------------------------------------------- #

    def _encode_as_dict(self, value) -> dict:
        return self.__encoder.encode_dict(value)

    # ----------------------------------------------------------------------------------------- #

    def _decode_from_dict(self, value: dict):
        return self.__encoder.decode_dict(value)

    # ----------------------------------------------------------------------------------------- #

    def _encode_as_str(self, value) -> str:
        return self.__encoder.encode_str(value)

    # ----------------------------------------------------------------------------------------- #

    def _decode_from_str(self, value: str):
        return self.__encoder.decode_str(value)

    # ----------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #
