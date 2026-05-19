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

    # 1. Validates missing args...
    with pytest.raises(ValueError, match="Path or Content must be provided"):
        File()


# --------------------------------------------------------------------------------------------- #


def test_init_from_content_sets_default_mime():
    """ Builds a file from bytes and checks basic defaults. """

    # 1. Creates file from bytes...
    value = File(content=b"abc")

    # 2. Checks content defaults...
    assert value.content == b"abc"
    assert value.path is None

    # 3. Checks runtime defaults...
    assert isinstance(value.mime, str) and len(value.mime) > 0
    assert value.loaded is True

    # 4. Checks temp default...
    assert value.temp is False


# --------------------------------------------------------------------------------------------- #


def test_path_precedence_prefers_main_path_when_valid(tmp_path: Path):
    """ Ensures path property prioritizes main path according to contract. """

    # 1. Creates paths...
    main_file = tmp_path / "main.txt"
    tmp_file = tmp_path / "tmp.txt"

    # 2. Writes files...
    main_file.write_bytes(b"main")
    tmp_file.write_bytes(b"tmp")

    # 3. Checks precedence...
    value = File(path=str(main_file), content=b"x")
    value._tmp_path = str(tmp_file)  # pylint: disable=protected-access

    # 4. Validates main path...
    assert value.path == str(main_file).replace("\\", "/")


# --------------------------------------------------------------------------------------------- #


def test_path_falls_back_to_temp(tmp_path: Path):
    """ Uses temp path when main path is unavailable. """

    # 1. Creates file...
    value = File(content=b"abc")
    temp_file = tmp_path / "tmp.bin"
    temp_file.write_bytes(b"abc")

    # 2. Sets temp...
    value._tmp_path = str(temp_file)  # pylint: disable=protected-access
    assert value.path == str(temp_file)


# --------------------------------------------------------------------------------------------- #


def test_to_dict_data_mode_resets_path_when_export_reset(tmp_path: Path):
    """ Validates to_dict behavior for export_mode=data with reset. """

    # 1. Creates source...
    path = tmp_path / "item.bin"
    path.write_bytes(b"hello")
    value = File(path=str(path), export_mode="data", export_reset=True)

    # 2. Exports...
    data = value.to_dict(encode=True)

    # 3. Checks path shape...
    assert data["path"] is None
    assert data["export_mode"] == "data"

    # 4. Checks content shape...
    assert data["export_reset"] is True
    assert isinstance(data.get("content"), str)


# --------------------------------------------------------------------------------------------- #


def test_from_dict_round_trip_data_mode():
    """ Rebuilds object from dictionary and preserves expected fields. """

    # 1. Builds encoded payload...
    source = File(content=b"hello", mime="text/plain", export_mode="data")
    payload = source.to_dict(encode=True)

    # 2. Restores object...
    restored = File.from_dict(payload)

    # 3. Validates restored object...
    assert isinstance(restored, File)
    assert restored.content == b"hello"

    # 4. Validates restored metadata...
    assert restored.mime == "text/plain"
    assert restored.export_mode == "data"

    # 5. Validates reset flag...
    assert restored.export_reset is False


# --------------------------------------------------------------------------------------------- #


def test_load_reads_file_content_and_clean_temp(tmp_path: Path):
    """ Loads bytes from path and clears temp file when content enters memory. """

    # 1. Prepares files...
    main_file = tmp_path / "main.txt"
    tmp_file = tmp_path / "tmp.txt"
    main_file.write_bytes(b"main")
    tmp_file.write_bytes(b"tmp")

    # 2. Loads content...
    value = File(path=str(main_file))
    value._tmp_path = str(tmp_file)  # pylint: disable=protected-access
    assert value.load() is True

    # 3. Checks state...
    assert value.content == b"tmp"
    assert value._tmp_path is None  # pylint: disable=protected-access
    assert not tmp_file.exists()


# --------------------------------------------------------------------------------------------- #


def test_unload_writes_to_explicit_path_and_clears_memory(tmp_path: Path):
    """ Unloads in-memory content to explicit output file. """

    # 1. Creates value...
    value = File(content=b"payload")
    out_file = tmp_path / "out.bin"

    # 2. Unloads...
    assert value.unload(file_path=str(out_file)) is True

    # 3. Checks output...
    assert out_file.read_bytes() == b"payload"
    assert value.content is None
    assert value.path == str(out_file).replace("\\", "/")


# --------------------------------------------------------------------------------------------- #


def test_unload_without_path_uses_temp_when_needed():
    """ Unloads to temp storage when no destination path exists. """

    # 1. Creates value...
    value = File(content=b"payload")

    # 2. Unloads...
    assert value.unload() is True

    # 3. Validates temp...
    assert value.content is None
    assert value.temp is True
    assert value._tmp_path is not None  # pylint: disable=protected-access


# --------------------------------------------------------------------------------------------- #


def test_write_raises_when_no_source_and_no_content(tmp_path: Path):
    """ Ensures write fails with clear error when source is missing. """

    # 1. Creates value with non-existing path...
    value = File(content=b"x")
    value.path = str(tmp_path / "missing.bin")
    value.content = None
    out_file = tmp_path / "out.bin"

    # 2. Validates failure...
    with pytest.raises(FileNotFoundError, match="Source file not found"):
        value.write(str(out_file))


# --------------------------------------------------------------------------------------------- #


def test_clean_is_safe_when_temp_missing(tmp_path: Path):
    """ Clean returns True and resets temp when target file is missing. """

    # 1. Creates value...
    value = File(content=b"x")
    value._tmp_path = str(tmp_path / "not_found.bin")  # pylint: disable=protected-access

    # 2. Cleans...
    assert value.clean() is True
    assert value._tmp_path is None  # pylint: disable=protected-access


# --------------------------------------------------------------------------------------------- #


def test_magic_helpers_and_sizes(monkeypatch):
    """ Covers static helper methods and size formatting. """

    # 1. Patches magic backend...
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

    # 2. Validates MIME helpers...
    assert File.get_mime_from_name("a.pyon") == "application/octet-stream"
    assert File.get_mime_from_name("a.unknown") == "application/octet-stream"

    # 3. Validates magic helpers...
    assert File.get_mime_from_path("some/path.txt") == "file/txt"
    assert File.get_mime_from_content(b"abc") == "buffer/bin"

    # 4. Validates size helpers...
    assert File.get_size(0) == "0.0 bytes"
    assert File.get_size(1024) == "1.0 KB"

    # 5. Validates content codec...
    assert File._encode_content(b"abc") is not None  # pylint: disable=protected-access
    assert File._decode_content(File._encode_content(b"abc")) == b"abc"  # pylint: disable=protected-access


# --------------------------------------------------------------------------------------------- #


def test_size_directory_and_len_from_path(tmp_path: Path):
    """ Uses file-system backed File object and validates derived properties. """

    # 1. Prepares file...
    source = tmp_path / "d" / "item.txt"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_bytes(b"12345")
    value = File(path=str(source))

    # 2. Validates properties...
    assert len(value) == 5
    assert value.size == "5.0 bytes"
    assert value.directory.endswith("/d")


# --------------------------------------------------------------------------------------------- #


def test_repr_and_str_include_runtime_status(tmp_path: Path):
    """ Validates user-facing representation/status output. """

    # 1. Prepares file...
    source = tmp_path / "item.bin"
    source.write_bytes(b"xy")
    value = File(path=str(source), content=b"xy")
    value._tmp_path = str(source)  # pylint: disable=protected-access

    # 2. Builds text...
    view = str(value)
    debug = repr(value)

    # 3. Validates status view...
    assert "memory" in view
    assert "filesystem" in view

    # 4. Validates debug view...
    assert "temp" in view
    assert "mime" in debug

    # 5. Validates loaded flag...
    assert "loaded" in debug


# --------------------------------------------------------------------------------------------- #


def test_comparison_protocol_with_file_and_non_file(tmp_path: Path):
    """ Exercises rich comparisons and NotImplemented behavior. """

    # 1. Prepares paths...
    a_path = tmp_path / "a.bin"
    b_path = tmp_path / "b.bin"

    # 2. Writes values...
    a_path.write_bytes(b"1")
    b_path.write_bytes(b"123")

    # 3. Builds files...
    a = File(path=str(a_path))
    b = File(path=str(b_path))

    # 4. Compares less-than operators...
    assert (a < b) is True
    assert (a <= b) is True

    # 5. Compares greater-than operators...
    assert (b > a) is True
    assert (b >= a) is True

    # 6. Compares equality...
    assert (a == b) is False

    # 7. Validates lower non-file protocol...
    assert type(a).__lt__(a, 1) is NotImplemented
    assert type(a).__le__(a, 1) is NotImplemented

    # 8. Validates greater non-file protocol...
    assert type(a).__gt__(a, 1) is NotImplemented
    assert type(a).__ge__(a, 1) is NotImplemented


# --------------------------------------------------------------------------------------------- #


def test_equality_fallback_uses_content_when_paths_unavailable():
    """ Equality should fallback to loaded content when no path is available. """

    # 1. Prepares values...
    a = File(content=b"same")
    b = File(content=b"same")
    a.path = None
    b.path = None

    # 2. Validates content-based equality...
    assert (a == b) is True


# --------------------------------------------------------------------------------------------- #


def test_unload_keep_existing_path_without_update(tmp_path: Path):
    """ When target path already exists and update=False, unload keeps file untouched. """

    # 1. Prepares source...
    source = tmp_path / "source.bin"
    source.write_bytes(b"old")
    value = File(path=str(source), content=b"new")

    # 2. Unloads without update...
    assert value.unload(update=False) is True

    # 3. Validates branch outcome...
    assert source.read_bytes() == b"old"
    assert value.content is None


# --------------------------------------------------------------------------------------------- #


def test_unload_reuses_existing_temp_file_without_update(tmp_path: Path):
    """ Existing temp file should be reused when update=False. """

    # 1. Prepares value...
    temp_file = tmp_path / "temp.bin"
    temp_file.write_bytes(b"old")
    value = File(content=b"new")
    value._tmp_path = str(temp_file)  # pylint: disable=protected-access

    # 2. Unloads...
    assert value.unload(update=False) is True

    # 3. Validates no rewrite...
    assert temp_file.read_bytes() == b"old"
    assert value.content is None


# --------------------------------------------------------------------------------------------- #


def test_clean_logs_failure_and_returns_false(monkeypatch):
    """ Clean must fail safely when temp deletion raises OSError. """

    # 1. Prepares value...
    value = File(content=b"x")
    value._tmp_path = "temp-a.bin"  # pylint: disable=protected-access
    monkeypatch.setattr("pyon.file.api.os.path.isfile", lambda _: True)
    monkeypatch.setattr("pyon.file.api.os.remove", lambda _: (_ for _ in ()).throw(OSError("boom")))

    # 2. Validates failure contract...
    assert value.clean() is False
    assert value._tmp_path is not None  # pylint: disable=protected-access


# --------------------------------------------------------------------------------------------- #


def test_write_to_directory_and_verbose_path(tmp_path: Path):
    """ Writing with directory target should resolve output filename and create file. """

    # 1. Prepares value...
    out_dir = tmp_path / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    value = File(content=b"abc")

    # 2. Writes...
    assert value.write(str(out_dir), verbose=True) is True

    # 3. Validates output existence...
    assert any(out_dir.iterdir())


# --------------------------------------------------------------------------------------------- #


def test_get_content_prefers_main_path_when_temp_missing(tmp_path: Path):
    """ _get_content should read main path when temp path is unavailable. """

    # 1. Prepares file...
    source = tmp_path / "main.bin"
    source.write_bytes(b"main")
    value = File(path=str(source))
    value.content = None
    value._tmp_path = str(tmp_path / "missing.bin")  # pylint: disable=protected-access

    # 2. Reads content...
    assert value._get_content() == b"main"  # pylint: disable=protected-access


# --------------------------------------------------------------------------------------------- #


def test_get_mime_prefers_pyon_extension(monkeypatch, tmp_path: Path):
    """ __get_mime should prioritize PYON extension branch when path ends with .pyon. """

    # 1. Prepares value...
    source = tmp_path / "item.pyon"
    source.write_text("{}", encoding="utf-8")
    value = File(path=str(source))

    # 2. Validates pyon MIME...
    assert value.mime == "application/vnd.pyon+json"

    # 3. Patches MIME fallbacks...
    monkeypatch.setattr("pyon.file.api.File.get_mime_from_path", lambda _: "")
    monkeypatch.setattr("pyon.file.api.File.get_mime_from_content", lambda _: "")
    monkeypatch.setattr("pyon.file.api.File.get_mime_from_name", lambda _: "")

    # 4. Forces fallback name/content branches...
    value.path = None
    value.content = None
    value.mime = getattr(value, "_File__get_mime")(None)

    # 5. Validates fallback MIME...
    assert value.mime == "application/octet-stream"
