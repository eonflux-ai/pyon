# 📁 Pyon File Module

[![PyPI version](https://badge.fury.io/py/pyon-core.svg)](https://pypi.org/project/pyon-core/)
[![GitHub stars](https://img.shields.io/github/stars/eonflux-ai/pyon?style=social)](https://github.com/eonflux-ai/pyon/tree/main/pyon/file)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/eonflux-ai/pyon/blob/main/LICENSE)

The `File` class encapsulates both in-memory and filesystem-based file representations, allowing unified interaction with file content and metadata. This module supports encoding/decoding to/from `.pyon` format, including base64 serialization.

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
10. [Integration with Pyon](#10-integration-with-pyon)
11. [Static Utilities](#11-static-utilities)
12. [Future Ideas](#12-future-ideas)
13. [License](#13-license)
14. [Project Links](#14-project-links)

---

## 1. Overview

The `File` class provides a robust abstraction over files, allowing them to be loaded from disk, manipulated in memory, serialized to Pyon, and saved or moved as needed.

## 2. Features

- Accepts `path` or `content` (or both)
- MIME detection via filename, path, or content
- File size calculation and human-readable formatting
- Load/unload memory content
- Temporary file support with automatic cleanup
- Equality and hashing based on content or path
- Seamless integration with `pyon.encode()` / `pyon.decode()`

## 3. Constructor

```python
File(
    path: str | None = None,
    content: bytes | None = None,
    mime: str | None = None,
    export_mode: Literal["data", "reference"] = "reference"
)
```

## 4. Properties

| Property     | Description                                  |
|--------------|----------------------------------------------|
| `name`       | Filename with extension                      |
| `extension`  | File extension                               |
| `directory`  | Parent directory (if available)              |
| `size`       | Human-readable file size                     |
| `mime`       | MIME type                                    |
| `loaded`     | Indicates if `content` is in memory          |
| `temp`       | Whether it’s a temporary file                |

## 5. Public Methods

| Method           | Description                                             |
|------------------|---------------------------------------------------------|
| `load()`         | Loads file content into memory                          |
| `unload(path)`   | Writes to disk and removes from memory                  |
| `write(path)`    | Writes file (via `content` or `path`) to destination    |
| `to_dict()`      | Converts file to dictionary (optionally encoded)        |
| `from_dict()`    | Reconstructs `File` from dictionary                     |

## 6. Equality & Comparison

`File` supports comparison operators (`==`, `<`, `>`, etc.) based on either path or content.

## 7. Temp File Support

- Temporary files are written inside a subfolder of `tempfile.gettempdir()` using `pyon_file` prefix.
- Automatically deleted after use via `__clean_tmp()`.

## 8. Export Modes

| Mode         | Behavior                                   |
|--------------|--------------------------------------------|
| `reference`  | Saves file as path only (default)          |
| `data`       | Embeds base64-encoded content in `.pyon`   |

## 9. MIME Detection

Order of resolution:

1. Manual
2. Extension-based
3. File content (`python-magic`)
4. Filename
5. Fallback: `application/octet-stream`

## 10. Integration with Pyon

```python
import pyon

encoded = pyon.encode(file_obj)
decoded = pyon.decode(encoded)
```

## 11. Static Utilities

- `get_mime_from_name(filename)`
- `get_mime_from_path(filepath)`
- `get_mime_from_content(content)`
- `get_size(bytes)`
- `_encode_content(content)`
- `_decode_content(content)`

## 12. Future Ideas

| Feature        | Description |
|----------------|-------------|
| `from_url()`   | Create `File` from a URL with optional headers. |
| `audit_log()`  | Log and track all load/write/unload operations. |

## 13. License

MIT License. See [LICENSE](https://github.com/eonflux-ai/pyon/blob/main/LICENSE).

## 14. Project Links

- [📦 PyPI: pyon-core](https://pypi.org/project/pyon-core/)
- [📁 GitHub: pyon.file](https://github.com/eonflux-ai/pyon/tree/main/pyon/file)
