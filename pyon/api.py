""" Pyon: Python Object Notation - Public Interface """
# --------------------------------------------------------------------------------------------- #

import logging
import os

# --------------------------------------------------------------------------------------------- #

from typing import Any, overload

# --------------------------------------------------------------------------------------------- #

from .encoder import PyonEncoder

# --------------------------------------------------------------------------------------------- #

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------------------- #


def encode(
    obj: object | None, enc_protected: bool = False, enc_private: bool = False
) -> str | None:
    """Encodes a Python object into a Pyon-formatted string.

    Args:
        obj: The Python object to encode.
        enc_protected (bool): Whether to encode protected attributes.
        enc_private (bool): Whether to encode private attributes.

    Returns:
        str or None: The encoded Pyon string, or None if obj is None.
    """

    # 1. Prepare output...
    output = None
    if obj is not None:

        # 1.1 Encode object...
        encoder = PyonEncoder(enc_protected=enc_protected, enc_private=enc_private)
        output = encoder.encode_str(obj)

    # 2. Return output...
    return output


# --------------------------------------------------------------------------------------------- #


def decode(pyon_str: str | None) -> Any | None:
    """
    Decodes a Pyon-formatted string into a Python object.

    Args:
        pyon_str (str | None): The Pyon string to decode.

    Returns:
        The decoded Python object, or None if pyon_str is None.
    """

    # 1. Prepare output...
    output = None
    if pyon_str is not None:

        # 1.1 Decode string...
        encoder = PyonEncoder()
        output = encoder.decode_str(pyon_str)

    # 2. Return output...
    return output


# --------------------------------------------------------------------------------------------- #


def to_file(
    obj: object,
    file_path: str = "./data.pyon",
    enc_protected: bool = False,
    enc_private: bool = False,
    verbose: bool = True,
) -> str:
    """ Saves to file """

    # 1. Encode object...
    pyon_text = encode(obj, enc_protected=enc_protected, enc_private=enc_private)

    # 2. Validate target...
    if ((pyon_text is not None) and (len(pyon_text) > 0) and file_path
        and file_path.endswith(".pyon")):

        # 1.1 Prepare folder...
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 1.2 Write data...
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(pyon_text)

        # 1.3 Log save...
        if verbose:
            logger.info("Data saved at %s", file_path)

    # 3. Reject target...
    else:
        raise ValueError(f"Not a valid pyon output file: '{file_path}'")

    # 4. Return text...
    return pyon_text


# --------------------------------------------------------------------------------------------- #


def from_file(file_path: str) -> Any | None:
    """
    Loads and decodes a Pyon-formatted file into a Python object.

    Args:
        file_path (str): The path to the Pyon file.

    Returns:
        The decoded Python object, or None if the file does not exist or is invalid.
    """

    # 1. Read file...
    pyon_str = None
    if os.path.isfile(file_path):

        # 1.1 Load text...
        with open(file=file_path, mode="r", encoding="utf-8") as file:
            pyon_str = file.read()

    # 2. Return decoded...
    return decode(pyon_str)


# --------------------------------------------------------------------------------------------- #
