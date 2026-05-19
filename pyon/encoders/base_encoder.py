# --------------------------------------------------------------------------------------------- #
""" Pyon: Base Encoder """
# --------------------------------------------------------------------------------------------- #

from abc import ABC

# --------------------------------------------------------------------------------------------- #

from typing import TYPE_CHECKING, Any

# --------------------------------------------------------------------------------------------- #

if TYPE_CHECKING:
    from pyon.encoder import PyonEncoder

# --------------------------------------------------------------------------------------------- #
# pylint: disable=too-few-public-methods
# --------------------------------------------------------------------------------------------- #

class BaseEncoder(ABC):
    """ Base Encoder """

    # ----------------------------------------------------------------------------------------- #

    def __init__(self, encoder: "PyonEncoder | None") -> None:
        """ Initializes a Base Encoder """

        # 1. Validate encoder...
        if encoder is None:
            raise ValueError("Invalid Pyon Encoder")

        # 2. Store encoder...
        self.__encoder = encoder

    # ----------------------------------------------------------------------------------------- #

    def _encode_as_dict(self, value: object | None) -> Any | None:
        return self.__encoder.encode_dict(value)

    # ----------------------------------------------------------------------------------------- #

    def _decode_from_dict(self, value: object | None) -> Any | None:
        return self.__encoder.decode_dict(value)

    # ----------------------------------------------------------------------------------------- #

    def _encode_as_str(self, value: object | None) -> str | None:
        return self.__encoder.encode_str(value)

    # ----------------------------------------------------------------------------------------- #

    def _decode_from_str(self, value: str | None) -> Any | None:
        return self.__encoder.decode_str(value)

    # ----------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #
