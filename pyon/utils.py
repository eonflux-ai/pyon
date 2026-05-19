""" Pyon: Python Object Notation - Utils """
# --------------------------------------------------------------------------------------------- #

import os
import secrets
import string
import importlib
from datetime import timedelta, timezone

# --------------------------------------------------------------------------------------------- #

MAX_ATTEMPTS = 1000

# --------------------------------------------------------------------------------------------- #

PYON_MIME = "application/vnd.pyon+json"
PYON_EXT = "pyon"

# --------------------------------------------------------------------------------------------- #


class EConst:  # pylint: disable=too-few-public-methods
    """ Constants used for encoding e decoding data in pyon source. """

    AUX1 = "__aux1__"
    AUX2 = "__aux2__"
    AUX3 = "__aux3__"
    AUX4 = "__aux4__"
    AUX5 = "__aux5__"
    AUX6 = "__aux6__"
    AUX7 = "__aux7__"
    AUX8 = "__aux8__"
    CLASS = "__class__"
    DATA = "__data__"
    DICT = "__dict__"
    TYPE = "__type__"
    FIELDS = "_fields"

    # Timezone metadata (optional)
    TZ_ZONE = "__zone__"
    TZ_OFFSET = "__offset__"
    TZ_FOLD = "__fold__"


# --------------------------------------------------------------------------------------------- #


def is_decode_able(value):
    """ Checks if `value` can be decoded. """

    # 1. Check decode marker...
    return isinstance(value, dict) and (EConst.TYPE in value)


# --------------------------------------------------------------------------------------------- #


def get_class_name(obj):
    """
    Retrieve the fully qualified class name of an object or class.

    Args:
        obj: The object or class to inspect.

    Returns:
        str: A string representing the fully qualified class name, including the module name.
    """

    # 1. Prepare name parts...
    module, name = None, None

    # 2. Read class reference...
    if isinstance(obj, type):
        module, name = f"{obj.__module__}", f"{obj.__qualname__}"

    # 3. Read object class...
    else:
        module, name = f"{obj.__class__.__module__}", f"{obj.__class__.__name__}"

    # 4. Return qualified name...
    return f"{module}.{name}"


# --------------------------------------------------------------------------------------------- #


def get_class(obj):
    """
    Retrieve the class object referenced by a serialized representation.

    Args:
        obj: A dictionary containing serialized class metadata, including the class name.

    Returns:
        type or None: The class object if it exists and can be imported; otherwise, None.
    """

    # 1. Prepare class output...
    cls = None
    if isinstance(obj, dict) and (EConst.CLASS in obj):

        # 1.1 Reads class name...
        class_name = obj[EConst.CLASS]
        if "." in class_name:

            # 2.1 Imports class...
            try:

                # 3.1 Loads module...
                module_name, class_name = class_name.rsplit(".", 1)
                module = importlib.import_module(module_name)

                # 3.2 Resolves class...
                cls = getattr(module, class_name)

            # 2.2 Handles missing class...
            except (ModuleNotFoundError, AttributeError):
                cls = None

    # 2. Return class...
    return cls


# --------------------------------------------------------------------------------------------- #


def lstrip(s: str, char: str) -> str:
    """
    Removes all leading `char` characters from the beginning of `s` 
    until the first different character is found.

    Example:
        lstrip_until(",,,hello", ",") -> "hello"
        lstrip_until("///path/to/file", "/") -> "path/to/file"
    """
    if not char or len(char) != 1:
        raise ValueError("char must be a single character")

    # 1. Initialize index
    i = 0

    # 2. Iterate until a different character is found
    while i < len(s) and s[i] == char:
        i += 1

    # 3. Return the trimmed string
    return s[i:]


# --------------------------------------------------------------------------------------------- #


def get_mangled_name(obj):
    """
    Returns the Python name-mangled prefix for private attributes of the given object's class.

    Args:
        obj: The object whose class name will be used for mangling.

    Returns:
        str: The mangled name prefix (e.g., '_ClassName__').
    """

    # 1. Normalize class name...
    mangled_name = type(obj).__name__
    mangled_name = lstrip(mangled_name, '_')

    # 2. Return prefix...
    return f"_{mangled_name}__"


# --------------------------------------------------------------------------------------------- #


def generate_unique_filename(
    name: str | None = None,
    extension: str | None = None,
    size: int = 5,
    folder_path: str | None = None
) -> str:
    """
    Generates a unique filename composed of a base name, a random suffix, and an extension.

    Args:
        name (str | None): Base name of the file (can be None).
        extension (str | None): File extension without the dot (can be None).
        size (int): Length of the random alphanumeric suffix (default is 3).
        folder_path (str | None): If provided, ensures filename does not already exist in folder.

    Returns:
        str: A unique filename with the specified structure.
    """

    # 1. Setup base values...
    base = name or "file"
    ext = f".{extension}" if extension else ""
    attempts = 0

    # 2. Loop until unique or max attempts...
    filename = f"{base}{ext}"
    while attempts < MAX_ATTEMPTS:

        # 1.1 Generate suffix...
        alphabet = string.ascii_lowercase + string.digits
        suffix = ''.join(secrets.choice(alphabet) for _ in range(size))
        filename = f"{base}_{suffix}{ext}"

        # 1.2 Check if unique or skip folder check...
        if not folder_path:
            break

        # 1.3 Checks path...
        file_path = os.path.join(folder_path, filename)
        if not os.path.exists(file_path):
            break

        # 1.4 Count attempts...
        attempts += 1

    # 3. Return result...
    return filename


# --------------------------------------------------------------------------------------------- #


def parse_utc_offset(s: str):
    """Parses a string like +HH:MM/-HH:MM into a fixed-offset tzinfo."""

    # 1. Prepare output...
    output = None
    try:

        # 1.1 Validates text...
        if isinstance(s, str) and (len(s) >= 6) and (s[3] == ":"):
            sign = 1 if s[0] == "+" else -1

            # 2.1 Parses parts...
            hours = int(s[1:3])
            minutes = int(s[4:6])
            delta = timedelta(hours=hours, minutes=minutes) * sign

            # 2.2 Builds timezone...
            output = timezone(delta)

    # 2. Handle invalid text...
    except (TypeError, ValueError, IndexError):
        pass

    # 3. Return output...
    return output


# --------------------------------------------------------------------------------------------- #
