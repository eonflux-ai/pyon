# --------------------------------------------------------------------------------------------- #
""" Tests for: pyon/file/api.py """
# --------------------------------------------------------------------------------------------- #

from pathlib import Path

# --------------------------------------------------------------------------------------------- #

import pytest

# --------------------------------------------------------------------------------------------- #

from pyon.file.api import File

# --------------------------------------------------------------------------------------------- #


def test_init_requires_path_or_content():
    """ Validates constructor guard for missing inputs. """

    # 1. It validates missing args...
    with pytest.raises(ValueError, match="Path or Content must be provided"):
        File()


# --------------------------------------------------------------------------------------------- #


def test_init_from_content_sets_default_mime():
    """ Builds a file from bytes and checks basic defaults. """

    # 1. It creates file from bytes...
    value = File(content=b"abc")

    # 2. It checks defaults...
    assert value.content == b"abc"
    assert value.path is None
    assert isinstance(value.mime, str) and len(value.mime) > 0
    assert value.loaded is True
    assert value.temp is False


# --------------------------------------------------------------------------------------------- #


def test_path_precedence_prefers_main_path_when_valid(tmp_path: Path):
    """ Ensures path property prioritizes main path according to contract. """

    # 1. It creates real files...
    main_file = tmp_path / "main.txt"
    tmp_file = tmp_path / "tmp.txt"
    main_file.write_bytes(b"main")
    tmp_file.write_bytes(b"tmp")

    # 2. It checks precedence...
    value = File(path=str(main_file), content=b"x")
    value._tmp_path = str(tmp_file)  # pylint: disable=protected-access
    assert value.path == str(main_file).replace("\\", "/")


# --------------------------------------------------------------------------------------------- #


def test_path_falls_back_to_temp(tmp_path: Path):
    """ Uses temp path when main path is unavailable. """

    # 1. It creates file...
    value = File(content=b"abc")
    temp_file = tmp_path / "tmp.bin"
    temp_file.write_bytes(b"abc")

    # 2. It sets temp...
    value._tmp_path = str(temp_file)  # pylint: disable=protected-access
    assert value.path == str(temp_file)


# --------------------------------------------------------------------------------------------- #


def test_to_dict_data_mode_resets_path_when_export_reset(tmp_path: Path):
    """ Validates to_dict behavior for export_mode=data with reset. """

    # 1. It creates source...
    path = tmp_path / "item.bin"
    path.write_bytes(b"hello")
    value = File(path=str(path), export_mode="data", export_reset=True)

    # 2. It exports...
    data = value.to_dict(encode=True)

    # 3. It checks shape...
    assert data["path"] is None
    assert data["export_mode"] == "data"
    assert data["export_reset"] is True
    assert isinstance(data["content"], str)


# --------------------------------------------------------------------------------------------- #


def test_from_dict_round_trip_data_mode():
    """ Rebuilds object from dictionary and preserves expected fields. """

    # 1. It builds encoded payload...
    source = File(content=b"hello", mime="text/plain", export_mode="data")
    payload = source.to_dict(encode=True)

    # 2. It restores object...
    restored = File.from_dict(payload)

    # 3. It validates...
    assert isinstance(restored, File)
    assert restored.content == b"hello"
    assert restored.mime == "text/plain"
    assert restored.export_mode == "data"
    assert restored.export_reset is False


# --------------------------------------------------------------------------------------------- #


def test_load_reads_file_content_and_clean_temp(tmp_path: Path):
    """ Loads bytes from path and clears temp file when content enters memory. """

    # 1. It prepares files...
    main_file = tmp_path / "main.txt"
    tmp_file = tmp_path / "tmp.txt"
    main_file.write_bytes(b"main")
    tmp_file.write_bytes(b"tmp")

    # 2. It loads content...
    value = File(path=str(main_file))
    value._tmp_path = str(tmp_file)  # pylint: disable=protected-access
    assert value.load() is True

    # 3. It checks state...
    assert value.content == b"tmp"
    assert value._tmp_path is None  # pylint: disable=protected-access
    assert not tmp_file.exists()


# --------------------------------------------------------------------------------------------- #


def test_unload_writes_to_explicit_path_and_clears_memory(tmp_path: Path):
    """ Unloads in-memory content to explicit output file. """

    # 1. It creates value...
    value = File(content=b"payload")
    out_file = tmp_path / "out.bin"

    # 2. It unloads...
    assert value.unload(file_path=str(out_file)) is True

    # 3. It checks output...
    assert out_file.read_bytes() == b"payload"
    assert value.content is None
    assert value.path == str(out_file).replace("\\", "/")


# --------------------------------------------------------------------------------------------- #


def test_unload_without_path_uses_temp_when_needed():
    """ Unloads to temp storage when no destination path exists. """

    # 1. It creates value...
    value = File(content=b"payload")

    # 2. It unloads...
    assert value.unload() is True

    # 3. It validates temp...
    assert value.content is None
    assert value.temp is True
    assert value._tmp_path is not None  # pylint: disable=protected-access


# --------------------------------------------------------------------------------------------- #


def test_write_raises_when_no_source_and_no_content(tmp_path: Path):
    """ Ensures write fails with clear error when source is missing. """

    # 1. It creates value with non-existing path...
    value = File(content=b"x")
    value.path = str(tmp_path / "missing.bin")
    value.content = None
    out_file = tmp_path / "out.bin"

    # 2. It validates failure...
    with pytest.raises(FileNotFoundError, match="Source file not found"):
        value.write(str(out_file))


# --------------------------------------------------------------------------------------------- #


def test_clean_is_safe_when_temp_missing(tmp_path: Path):
    """ Clean returns True and resets temp when target file is missing. """

    # 1. It creates value...
    value = File(content=b"x")
    value._tmp_path = str(tmp_path / "not_found.bin")  # pylint: disable=protected-access

    # 2. It cleans...
    assert value.clean() is True
    assert value._tmp_path is None  # pylint: disable=protected-access


# --------------------------------------------------------------------------------------------- #


def test_magic_helpers_and_sizes(monkeypatch):
    """ Covers static helper methods and size formatting. """

    # 1. It patches magic backend...
    class _FakeMagic:  # pylint: disable=too-few-public-methods
        """Fake magic backend for deterministic MIME tests."""

        def __init__(self, mime=True):
            """Stores init args to mimic magic.Magic signature."""
            self.mime = mime

        def from_file(self, filepath):
            """Returns MIME inferred from filename suffix."""
            return f"file/{Path(filepath).suffix.lstrip('.') or 'octet-stream'}"

        def from_buffer(self, content):
            """Returns deterministic MIME for content."""
            return "buffer/bin" if content else "application/octet-stream"

    monkeypatch.setattr("pyon.file.api.magic.Magic", _FakeMagic)

    # 2. It validates helpers...
    assert File.get_mime_from_name("a.pyon") == "application/octet-stream"
    assert File.get_mime_from_name("a.unknown") == "application/octet-stream"
    assert File.get_mime_from_path("some/path.txt") == "file/txt"
    assert File.get_mime_from_content(b"abc") == "buffer/bin"
    assert File.get_size(0) == "0.0 bytes"
    assert File.get_size(1024) == "1.0 KB"
    assert File._encode_content(b"abc") is not None  # pylint: disable=protected-access
    assert File._decode_content(File._encode_content(b"abc")) == b"abc"  # pylint: disable=protected-access
