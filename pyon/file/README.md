# 📁 Pyon File Module

[![PyPI version](https://img.shields.io/pypi/v/pyon-core?cacheSeconds=300&include_prereleases)](https://pypi.org/project/pyon-core/)
[![GitHub stars](https://img.shields.io/github/stars/eonflux-ai/pyon?style=social)](https://github.com/eonflux-ai/pyon/tree/main/pyon/file)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/eonflux-ai/pyon/blob/main/LICENSE)

The `pyon.file` package contains the `File` class and its public typing helpers.
`File` represents either a filesystem reference, in-memory bytes, or both, and it
can be serialized through the normal `pyon.encode()` / `pyon.decode()` pipeline.

---

## 📚 Table of Contents

1. [Overview](#1-overview)
2. [Features](#2-features)
3. [Constructor](#3-constructor)
4. [Properties](#4-properties)
5. [Public Methods](#5-public-methods)
6. [Equality & Comparison](#6-equality--comparison)
7. [Temp File Support](#7-temp-file-support)
8. [Export Modes](#8-export-modes)
9. [MIME Detection](#9-mime-detection)
10. [Typing Helpers](#10-typing-helpers)
11. [Integration with Pyon](#11-integration-with-pyon)
12. [Static Utilities](#12-static-utilities)
13. [Future Ideas](#13-future-ideas)
14. [License](#14-license)
15. [Project Links](#15-project-links)

---

## 1. Overview

`File` is a lightweight wrapper for file content and file metadata. It can keep a
path reference, embedded bytes, MIME information, export policy, and temporary
runtime state.

The public package exports:

```python
from pyon import File
from pyon.file import File
from pyon.file.types import ExportMode, FileDict
```

## 2. Features

- Accepts `path`, `content`, or both.
- Detects MIME from explicit value, `.pyon` extension, file path, content, name,
  or fallback.
- Supports reference export and embedded data export.
- Supports optional path reset when exporting embedded data.
- Tracks memory and temporary-file runtime state.
- Supports equality and ordering comparisons based on file size or content/path
  fallback behavior.
- Provides a typed serialized shape through `FileDict`.

## 3. Constructor

```python
File(
    path: str | None = None,
    content: bytes | None = None,
    mime: str | None = None,
    export_mode: Literal["data", "reference"] = "reference",
    export_reset: bool = False,
) -> None
```

At least one of `path` or `content` must be provided.

## 4. Properties

| Property | Type | Description |
|----------|------|-------------|
| `path` | `str | None` | Preferred available path, using the main path or temp path. |
| `size` | `str` | Human-readable size. |
| `name` | `str` | Filename with extension when a path is available. |
| `extension` | `str` | File extension without the dot. |
| `directory` | `str` | Parent directory when a path is available. |
| `loaded` | `bool` | Whether `content` is currently in memory. |
| `temp` | `bool` | Whether a temporary file path is currently associated. |

The raw byte length is available through `len(file)`.

## 5. Public Methods

| Method | Description |
|--------|-------------|
| `to_dict(encode=True)` | Converts the file to a `FileDict` shape. |
| `from_dict(data)` | Reconstructs a `File` from `FileDict` or compatible mapping data. |
| `load()` | Loads content from the selected path into memory. |
| `unload(file_path=None, update=False)` | Writes content to a target path, current path, or temp path and clears memory on success. |
| `clean()` | Removes the current temporary file when one exists. |
| `write(outpath=None, verbose=False)` | Writes or copies content to a resolved destination. |

## 6. Equality & Comparison

`File` supports equality and ordering operators (`==`, `<`, `<=`, `>`, `>=`).
Comparison is based on file size when both operands are `File` instances. Equality
also supports comparison with non-`File` values through path/content fallback
behavior defined in the implementation.

## 7. Temp File Support

- Temporary files are written inside a `pyon_file` subfolder under
  `tempfile.gettempdir()`.
- `_write_temp()` creates or reuses a temp path for in-memory content.
- `clean()` removes the current temp file when one exists.
- `load()` can load content from a temp path and then clean that temp file.

## 8. Export Modes

| Mode | Behavior |
|------|----------|
| `reference` | Serializes the path and metadata without embedding content by default. |
| `data` | Embeds base64-encoded content in the serialized payload. |

When `export_reset=True` and `export_mode="data"`, `to_dict()` clears the
serialized path so the exported object is data-only.

## 9. MIME Detection

MIME resolution order:

1. Explicit `mime` argument.
2. Pyon extension check for `.pyon`.
3. File path detection through `python-magic-bin`.
4. Content detection through `python-magic-bin`.
5. Filename detection through `mimetypes`.
6. Fallback to `application/octet-stream`.

## 10. Typing Helpers

`pyon.file.types` defines:

- `ExportMode`: `Literal["data", "reference"]`
- `FileDict`: serialized dictionary shape used by `File.to_dict()` and
  `File.from_dict()`

The package includes `pyon/py.typed`, so these annotations are visible to
consumer type checkers.

## 11. Integration with Pyon

```python
import pyon
from pyon import File

file = File("data/img.jpg", export_mode="reference")
encoded = pyon.encode(file)
decoded = pyon.decode(encoded)
```

## 12. Static Utilities

Public static helpers:

- `get_mime_from_name(filename: str) -> str`
- `get_mime_from_path(filepath: str) -> str`
- `get_mime_from_content(content: bytes) -> str`
- `get_size(bytes_size: int) -> str`

Internal helpers such as `_encode_content()`, `_decode_content()`, `_encode()`,
and `_status()` are implementation details and should not be treated as public
API.

## 13. Future Ideas

| Feature | Description |
|---------|-------------|
| `from_url()` | Create `File` from a URL with optional headers. |
| `audit_log()` | Track load/write/unload operations. |

## 14. License

MIT License. See [LICENSE](https://github.com/eonflux-ai/pyon/blob/main/LICENSE).

## 15. Project Links

- [📦 PyPI: pyon-core](https://pypi.org/project/pyon-core/)
- [📁 GitHub: pyon.file](https://github.com/eonflux-ai/pyon/tree/main/pyon/file)
