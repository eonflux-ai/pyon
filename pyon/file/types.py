# --------------------------------------------------------------------------------------------- #
"""Public typing helpers for pyon.file."""
# --------------------------------------------------------------------------------------------- #

from typing import Literal, NotRequired, TypeAlias, TypedDict

# --------------------------------------------------------------------------------------------- #

ExportMode: TypeAlias = Literal["data", "reference"]

# --------------------------------------------------------------------------------------------- #


class FileDict(TypedDict):
    """Serialized public shape used by File.to_dict and File.from_dict."""

    path: str | None
    mime: str
    export_mode: ExportMode
    export_reset: bool
    content: NotRequired[str | bytes | None]


# --------------------------------------------------------------------------------------------- #
