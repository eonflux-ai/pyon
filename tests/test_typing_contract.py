# --------------------------------------------------------------------------------------------- #
"""Public typing contracts for external consumers."""
# --------------------------------------------------------------------------------------------- #

from pathlib import Path
from typing import Any, assert_type

# --------------------------------------------------------------------------------------------- #

from pyon import File, decode, encode, export, from_file, to_file
from pyon.encoder import PyonEncoder
from pyon.file.types import ExportMode, FileDict

# --------------------------------------------------------------------------------------------- #


def _export_mode(mode: ExportMode) -> ExportMode:
    """Widens export mode literals to the public alias."""

    # 1. Return mode...
    return mode


# --------------------------------------------------------------------------------------------- #


def test_public_api_typing_contract(tmp_path: Path) -> None:
    """Checks public function annotations through consumer-facing calls."""

    # 1. Encode value...
    encoded = encode({"name": "pyon", "count": 1})
    assert_type(encoded, str | None)
    assert encoded is not None

    # 2. Decode value...
    decoded = decode(encoded)
    assert_type(decoded, Any | None)
    assert decoded == {"name": "pyon", "count": 1}

    # 3. Write file...
    file_path = str(tmp_path / "typed.pyon")
    saved = to_file(["typed", "contract"], file_path=file_path, verbose=False)
    assert_type(saved, str)

    # 4. Read file...
    loaded = from_file(file_path)
    assert_type(loaded, Any | None)
    assert loaded == ["typed", "contract"]


# --------------------------------------------------------------------------------------------- #


def test_encoder_typing_contract() -> None:
    """Checks PyonEncoder public method annotations."""

    # 1. Prepare encoder...
    encoder = PyonEncoder(enc_protected=True, enc_private=True)

    # 2. Encode dictionary shape...
    encoded_dict = encoder.encode_dict({"value": 42})
    assert_type(encoded_dict, Any | None)
    assert encoded_dict is not None

    # 3. Decode dictionary shape...
    decoded_dict = encoder.decode_dict(encoded_dict)
    assert_type(decoded_dict, Any | None)
    assert decoded_dict == {"value": 42}

    # 4. Encode string shape...
    encoded_text = encoder.encode_str({"value": 42})
    assert_type(encoded_text, str | None)
    assert encoded_text is not None

    # 5. Decode string shape...
    decoded_text = encoder.decode_str(encoded_text)
    assert_type(decoded_text, Any | None)
    assert decoded_text == {"value": 42}


# --------------------------------------------------------------------------------------------- #


def test_file_typing_contract() -> None:
    """Checks File and FileDict public annotations."""

    # 1. Declare export mode...
    export_mode = _export_mode("data")
    assert_type(export_mode, ExportMode)

    # 2. Build file...
    file = File(
        content=b"typed content",
        mime="text/plain",
        export_mode=export_mode,
        export_reset=True,
    )

    # 3. Check properties...
    assert_type(file.path, str | None)
    assert_type(file.size, str)
    assert_type(file.name, str)
    assert_type(file.extension, str)
    assert_type(file.directory, str)
    assert_type(file.loaded, bool)
    assert_type(file.temp, bool)

    # 4. Serialize file...
    file_dict = file.to_dict()
    assert_type(file_dict, FileDict)
    assert "content" in file_dict
    assert file_dict["content"] is not None

    # 5. Restore file...
    restored = File.from_dict(file_dict)
    assert_type(restored, File | None)
    assert restored is not None
    assert restored.content == b"typed content"


# --------------------------------------------------------------------------------------------- #


def test_export_decorator_typing_contract() -> None:
    """Checks export decorator preserves the decorated class type."""

    # 1. Decorate class...
    @export(private=True, protected=True)
    class TypedModel:
        """Small model used to validate decorator typing."""

        # 1.1 Initialize value...
        def __init__(self, value: int) -> None:
            self.value = value

        # 1.2 Return value...
        def get_value(self) -> int:
            """Returns the stored value."""

            return self.value

        # 1.3 Check value...
        def has_value(self) -> bool:
            """Checks whether a value is present."""

            return self.value is not None

    # 2. Instantiate model...
    model = TypedModel(7)
    assert_type(model, TypedModel)
    assert model.has_value()
    assert model.get_value() == 7


# --------------------------------------------------------------------------------------------- #
