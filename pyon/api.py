""" Pyon: Python Object Notation - Public Interface """
# --------------------------------------------------------------------------------------------- #

import logging
import os
import hashlib

# --------------------------------------------------------------------------------------------- #

from typing import Literal

# --------------------------------------------------------------------------------------------- #

from .encoder import PyonEncoder

# --------------------------------------------------------------------------------------------- #

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------------------- #

PYON_POST_INIT = "__pyon_post_init__"

# --------------------------------------------------------------------------------------------- #

HashAlgorithm = Literal[
    "sha256",
    "sha512",
    "sha3_256",
    "sha3_512",
    "blake2b",
    "md5",
    "sha1"
]

# --------------------------------------------------------------------------------------------- #


def encode(obj, enc_protected: bool = False, enc_private: bool = False) -> str | None:
    """Encodes a Python object into a Pyon-formatted string.

    Args:
        obj: The Python object to encode.
        enc_protected (bool): Whether to encode protected attributes.
        enc_private (bool): Whether to encode private attributes.

    Returns:
        str or None: The encoded Pyon string, or None if obj is None.
    """

    # 1. ...
    output = None
    if obj is not None:

        # 1.1 ...
        encoder = PyonEncoder(enc_protected=enc_protected, enc_private=enc_private)
        output = encoder.encode_str(obj)

    # 2. ...
    return output


# --------------------------------------------------------------------------------------------- #


def decode(pyon_str: str | None):
    """
    Decodes a Pyon-formatted string into a Python object.

    Args:
        pyon_str (str | None): The Pyon string to decode.

    Returns:
        The decoded Python object, or None if pyon_str is None.
    """

    # 1. ...
    output = None
    if pyon_str is not None:

        # 1.1 ...
        encoder = PyonEncoder()
        output = encoder.decode_str(pyon_str)

        # 1.2 ...
        if (output is not None) and hasattr(output, PYON_POST_INIT):

            # 2.1 ...
            post_init = getattr(output, PYON_POST_INIT, None)
            if (post_init is not None) and callable(post_init):

                # 3.1 ...
                post_init()  # pylint: disable=not-callable

    # 2. ...
    return output


# --------------------------------------------------------------------------------------------- #


def to_file(
    obj,
    file_path: str = "./data.pyon",
    enc_protected: bool = False,
    enc_private: bool = False,
    verbose: bool = True,
):
    """ Saves to file """

    # 1. ...
    pyon_text = encode(obj, enc_protected=enc_protected, enc_private=enc_private)

    # 2. ...
    if ((pyon_text is not None) and (len(pyon_text) > 0) and file_path
        and file_path.endswith(".pyon")):

        # 1.1 ...
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 1.2 ...
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(pyon_text)

        # 1.3 ...
        if verbose:
            logger.info("Data saved at %s", file_path)

    # 3. ...
    else:
        raise ValueError(f"Not a valid pyon output file: '{file_path}'")

    # 4. ...
    return pyon_text


# --------------------------------------------------------------------------------------------- #


def from_file(file_path: str):
    """
    Loads and decodes a Pyon-formatted file into a Python object.

    Args:
        file_path (str): The path to the Pyon file.

    Returns:
        The decoded Python object, or None if the file does not exist or is invalid.
    """

    # 1. ...
    pyon_str = None
    if os.path.isfile(file_path):

        # 1.1. ...
        with open(file=file_path, mode="r", encoding="utf-8") as file:
            pyon_str = file.read()

    # 2. ...
    return decode(pyon_str)


# --------------------------------------------------------------------------------------------- #


def to_int(
    obj,
    enc_protected: bool = False,
    enc_private: bool = False
) -> int:
    """
    Converts an object into a serialized Pyon deterministic string,
    than generates a 256-bit integer.

    This function generates a consistent integer identifier derived from
    the object's content using SHA-256 hashing of its serialized form.

    Args:
        obj: The object to encode and hash.
        enc_protected (bool): Include protected attributes (_x).
        enc_private (bool): Include private attributes (__x).

    Returns:
        int: A 256-bit integer representing the object's identity.
    """

    # 1. Compute hex digest...
    hash_hex = to_hash(
        obj,
        algorithm="sha256",
        enc_protected=enc_protected,
        enc_private=enc_private
    )

    # 2. Convert hex digest to int...
    return int(hash_hex, 16)


# --------------------------------------------------------------------------------------------- #


def to_hash(
    obj,
    enc_protected: bool = False,
    enc_private: bool = False,
    algorithm: HashAlgorithm = "sha256"
) -> str:
    """
    Generates a deterministic hash string for any object via Pyon serialization.

    Args:
        obj: The object to encode and hash.
        algorithm (HashAlgorithm): Algorithm used to compute the hash:
            sha256   – Secure default (recommended)
            sha512   – Stronger than sha256, longer output, cryptographically secure
            sha3_256 – SHA-3 (Keccak), theoretically more secure
            sha3_512 – SHA-3 (Keccak), theoretically more secure
            blake2b  – Fast and modern alternative to SHA-2
            md5      – Useful for fingerprints and compact identifiers
            sha1     – Suitable for quick matching and legacy systems
        enc_protected (bool): Whether to include protected attributes (_x).
        enc_private (bool): Whether to include private attributes (__x).

    Returns:
        str: A hexadecimal digest representing the hash of the serialized object.

    Raises:
        ValueError: If the algorithm is not recognized.
    """

    # 1. ...
    pyon_str = encode(obj, enc_protected=enc_protected, enc_private=enc_private)
    return _to_hash(pyon_str, algorithm=algorithm)


# --------------------------------------------------------------------------------------------- #


def _to_hash(pyon_str: str | None, algorithm: HashAlgorithm) -> str:
    """ Simple pyon hash for any type of object. """

    # 1. ...
    hash_value = ''

    # 2. ...
    if pyon_str is not None:
        encoded: bytes = pyon_str.encode("utf-8")

        # 1.1 ...
        if algorithm == "sha256":
            hash_value = hashlib.sha256(encoded).hexdigest()

        # 1.2 ...
        elif algorithm == "sha512":
            hash_value = hashlib.sha3_256(encoded).hexdigest()

        # 1.3 ...
        elif algorithm == "sha3_256":
            hash_value = hashlib.sha3_256(encoded).hexdigest()

        # 1.4 ...
        elif algorithm == "sha3_512":
            hash_value = hashlib.sha3_512(encoded).hexdigest()

        # 1.5 ...
        elif algorithm == "blake2b":
            hash_value = hashlib.blake2b(encoded, digest_size=32).hexdigest()

        # 1.6 ...
        elif algorithm == "md5":
            hash_value = hashlib.md5(encoded).hexdigest()

        # 1.7 ...
        elif algorithm == "sha1":
            hash_value = hashlib.sha1(encoded).hexdigest()

        # 1.8 ...
        else:
            raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # 2. ...
    return hash_value


# --------------------------------------------------------------------------------------------- #
