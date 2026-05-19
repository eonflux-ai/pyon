# Pyon
[![PyPI version](https://img.shields.io/pypi/v/pyon-core?cacheSeconds=300&include_prereleases)](https://pypi.org/project/pyon-core/)
[![GitHub stars](https://img.shields.io/github/stars/eonflux-ai/pyon?style=social)](https://github.com/eonflux-ai/pyon)
[![Media Type: application/vnd.pyon+json](https://img.shields.io/badge/MIME-IANA%20Registered-blue.svg)](https://www.iana.org/assignments/media-types/application/vnd.pyon+json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)


**Pyon (Python Object Notation)** is a serialization/deserialization library that extends JSON to natively support complex Python types. It aims to provide a robust and efficient solution for advanced scenarios like Artificial Intelligence, Machine Learning, and heterogeneous data manipulation.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Simplified Interface](#2-simplified-interface)
3. [Supported Types](#3-supported-types)
4. [Installation](#4-installation)
5. [Quick Start](#5-quick-start)
6. [Examples](#6-examples)
7. [Recursion in Encoding and Decoding](#7-recursion-in-encoding-and-decoding)
8. [Decode Behavior and Safety Overview](#8-decode-behavior-and-safety-overview)
9. [JSON Compatibility](#9-json-compatibility)
10. [Project Structure](#10-project-structure)
11. [Encoders](#11-encoders)
12. [Testing](#12-testing)
13. [Roadmap](#13-roadmap)
14. [Media Type (IANA)](#14-media-type-iana)
15. [Additional Documentation](#15-additional-documentation)
16. [Contributing](#16-contributing)
17. [About the Creator](#17-about-the-creator)
18. [License](#18-license)
19. [Project Links](#19-project-links)

---

## 1. Overview

Pyon is a Python library that extends the JSON format to support a broader set of Python-native data types, including sets, tuples, enums, user-defined classes, and structures from libraries such as NumPy and pandas.

It provides a serialization and deserialization mechanism that preserves the structure and type information of supported objects using additional metadata embedded in standard JSON.

Pyon was designed with the following principles:

- **JSON-valid output**: All serialized data is valid JSON and can be parsed back by a Pyon decoder.
- **Type preservation**: Encoded objects retain enough metadata to be accurately reconstructed as their original Python types.
- **Modular architecture**: Support for data types is implemented through independent encoders, allowing structured maintenance and future expansion.

Pyon is suitable for tasks such as storing structured data, saving configurations, exporting Python objects for inspection or reuse, and ensuring deterministic reconstruction across environments — provided that all involved types are supported.

---
<br>

## 2. Simplified Interface

Pyon provides a straightforward interface with four main methods:

- **`encode(obj)`**: Serializes a Python object into a Pyon string.
- **`decode(data)`**: Deserializes a Pyon string into the corresponding Python object.
- **`to_file(obj, file_path)`**: Serializes a Python object and saves the result to a file.
- **`from_file(file_path)`**: Loads data from a file and deserializes it into the corresponding Python object.

Each of these methods automatically detects the data type and applies the appropriate serialization or deserialization logic.
<br>

### Additional options
Additional options are available in the core encoding methods:

| Method         | Description                                           |
|----------------|-------------------------------------------------------|
| `encode(...)`  | Serializes an object to a Pyon string                 |
| `to_file(...)` | Saves a serialized object to disk                     |

These methods accept two optional parameters:

- `enc_protected=True` includes attributes starting with `_` in the serialization.
- `enc_private=True` includes name-mangled attributes starting with `__` in the serialization.

---
<br>

## 3. Supported Types

Pyon supports a broad array of Python types out-of-the-box:
<br/>

**1. Base Types**
- `bool`, `float`, `int`, `str`, `type`, `None`

**2. Numeric Types**
- `complex`, `decimal.Decimal`

**3. Collection Types**
- `bytearray`, `bytes`, `frozenset`, `list`, `set`, `tuple`
- `ChainMap`, `Counter`, `defaultdict`, `deque`, `namedtuple` (collections)

**4. Datetime Types**
- `datetime.date`, `datetime.datetime`, `datetime.time`

**5. Mapping Types**
- `class` (user defined classes), `dataclasses.dataclass`, `dict`, `Enum`

**6. Specialized Types**
- `bitarray.bitarray`, `numpy.ndarray`, `pyon.File`, `uuid.UUID`
- `pandas.DataFrame`, `pandas.Series`

---
<br>

## 4. Installation

Pyon is released on PyPI. You can install the runtime package with:

```bash
pip install pyon-core
```

To install directly from the source repository:

```bash
pip install git+https://github.com/eonflux-ai/pyon.git
```

For local development from a cloned repository, use the project metadata in `pyproject.toml`:

```bash
git clone https://github.com/eonflux-ai/pyon.git
cd Pyon
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev,debug]"
```

The package is distributed as a typed package. The wheel includes `pyon/py.typed`, so type checkers can read the inline annotations directly from the installed package.

---
<br>

## 5. Quick Start

Below are some quick examples to help you get started.

### Basic Serialization and Deserialization

```python
import pyon

# 1. Python Data: Classes, Collections, Dataframes, Numpy arrays, etc...
data = {...}

# 2. One line Encode and Decode...
encoded = pyon.encode(data)
decoded = pyon.decode(encoded)

# 3. One line Encode and Decode to and from File...
pyon.to_file(data, "data.pyon")
decoded = pyon.from_file("data.pyon")
```

---
<br>

## 6. Examples

Pyon provides several usage examples covering supported data types and common serialization scenarios.
These examples are located in the `examples/` directory and provide practical use cases for serialization and deserialization.

Check **[EXAMPLES.md](examples/EXAMPLES.md)** for more information.

---
<br>

## 7. Recursion in Encoding and Decoding

Pyon supports recursive and nested data structures, such as dictionaries containing lists of sets, or custom objects nested within other containers. It is capable of encoding and decoding these compositions while preserving the original structure and supported types.

```python
import pyon

# 1. Test Objects...
example_data = {

    # 1.1 Tuple, Set...
    "tuple-set": ({"abc", "def"}),

    # 1.2 List, Tuple, Set...
    "list-tuple-set": [({"abc", "def"}), ({1, 2}), ({True, False})],

    # 1.3 Dict, List, Tuple, Set...
    "dict-list-tuple-set": {
        "a": [({"abc", "def"}), ({1, 2}), ({True, False})]
    },

    # 1.4 Dict, Dict, List, Tuple, Set...
    "dict-dict-list-tuple-set": {
        "one": {"a": [({"abc", "def"}), ({1, 2}), ({True, False})]},
        "two": {"b": [({"ghi", "jkl"}), ({3.0, 4.0}), ({True, False})]}
    }

}

# 2. One Line encode and decode...
encoded = pyon.encode(example_data)
decoded = pyon.decode(encoded)
```

This capability allows Pyon to represent arbitrarily nested structures without flattening or discarding information, as long as the types involved are supported by the library.

Check **[EXAMPLES.md](examples/EXAMPLES.md)** for more information.

---
<br>

## 8. Decode Behavior and Safety Overview

Pyon was designed to ensure **safe and deterministic reconstruction** of Python objects from `.pyon` files.

The decoding process does **not execute any user-defined code**. No custom methods such as `__init__`, `__post_init__` are triggered.

Instead, object reconstruction follows this predictable flow:

- Type information is parsed from static metadata fields.
- Objects are instantiated using `__new__` or built-in constructors where necessary.
- Attributes are restored via direct assignment — no custom logic is invoked.

This approach ensures that deserialization remains **passive, safe, and transparent** in trusted contexts.

---

### 🔍 Constructor Exceptions

Some supported types — such as `decimal.Decimal`, `datetime`, `pandas.DataFrame`, `numpy.ndarray`, and `File` — require calling their constructors during decoding.

In all such cases, constructors are used in a **controlled and deterministic way**, strictly for data restoration, without invoking arbitrary or user-defined logic.

However, a few types involve additional caveats:

- `defaultdict` may invoke its `default_factory`, which can contain logic.
- `namedtuple` subclasses may define methods or side effects.
- `Enum` can override `__new__`, introducing dynamic behavior.
- `File` content can be manipulated by third parties to inject unsafe payloads.

These types are handled within modules such as `collection_types.py` and `specialized_types.py`, which are documented as **having special decoding behavior**.

---

### 🔐 For Security Details

For a full audit and analysis of risks (including `Enum`, `defaultdict`, and tampering scenarios), see:

**[SECURITY.md](doc/SECURITY.md)**

---
<br>

## 9. JSON Compatibility

Pyon uses standard **JSON syntax** for all its serialized output. The result is a `.pyon` file that can be parsed by any standard JSON parser in terms of structure — but not necessarily understood in terms of semantics.

Although every `.pyon` file is a valid JSON document, it embeds additional metadata (e.g., `__type__`, `__module__`) that is **essential for reconstructing Python objects**. This makes Pyon a **superset of JSON**, not a drop-in replacement.

### 🔁 Encoding Process

When encoding, Pyon:

1. Converts Python objects into a **dictionary structure compatible with JSON syntax**.
2. Adds metadata fields that describe the object’s original type and context.
3. Serializes the resulting dictionary to a JSON string (or file).

The output is a syntactically valid JSON document that retains full information about Python-specific constructs, including:

- Complex types like `tuple`, `set`, `complex`, `datetime`, `Decimal`
- Nested and custom classes
- Type annotations for accurate reconstruction

### 🔄 Decoding Process

When decoding:

1. The `.pyon` file is first parsed using a standard JSON parser (e.g., `json.loads`).
2. Then, Pyon-specific metadata is interpreted to **reconstruct the original object structure and types**.

### 🧩 Compatibility Notes

While the file format conforms to JSON in syntax:

- Generic tools can parse the structure but **will not reconstruct the original Python types** without a Pyon-compatible decoder.
- Do **not** use `.pyon` files as substitutes for `application/json` in systems expecting generic JSON — behavior may be incorrect or undefined.
- The Pyon format is most effective when both encoding and decoding are done using the Pyon library itself.

> ✅ JSON-readable.  
> ❌ Not semantically interoperable without the Pyon specification.

---
<br>

## 10. Project Structure

Here is the current project structure for Pyon:

```text
Pyon/
|-- pyproject.toml                 # Build, package metadata, dependencies, and tool config
|-- README.md                      # Project overview and user-facing instructions
|-- CHANGELOG.md                   # Version history
|-- CONTRIBUTING.md                # Contribution workflow
|-- LICENSE                        # License details
|-- agents/                        # Local agent instructions used by project workflows
|-- doc/                           # Project documentation
|   |-- ROADMAP.md                 # Development roadmap
|   |-- TASKS.md                   # Task breakdown by version
|   |-- VERSION.md                 # Current version details
|   |-- SECURITY.md                # Security model and decode caveats
|   |-- releases/                  # Historical release notes
|   |-- other/                     # Auxiliary audit and registration documents
|-- examples/                      # Executable usage examples and example documentation
|-- pyon/                          # Main source package
|   |-- __init__.py                # Public package exports
|   |-- api.py                     # Public encode/decode file API
|   |-- encoder.py                 # Main encoder orchestration
|   |-- py.typed                   # PEP 561 typed-package marker
|   |-- supported_types.py         # Supported type markers
|   |-- utils.py                   # Utility helpers and constants
|   |-- annotations/               # Export-policy annotations
|   |-- encoders/                  # Type-specific encoders
|   |-- file/                      # File wrapper package
|       |-- api.py                 # File implementation
|       |-- types.py               # Public File typing aliases and TypedDicts
|-- tests/                         # Test suite
|   |-- encoders/                  # Encoder-specific tests
|   |   |-- test_base_types.py
|   |   |-- test_collection_types.py
|   |   |-- test_datetime_types.py
|   |   |-- test_mapping_types.py
|   |   |-- test_numeric_types.py
|   |   |-- test_specialized_types.py
|   |-- test_api.py                # Public API coverage
|   |-- test_file.py               # File wrapper coverage
|   |-- test_typing_contract.py    # Consumer-facing typing contracts
|   |-- test_resilience_contracts.py # Cross-cutting resilience contracts
```

---

### **Key Highlights**

1. **Public Interface**:

   - `pyon/api.py` exposes `encode`, `decode`, `to_file`, and `from_file`.
   - `pyon/encoder.py` coordinates the specialized encoder modules.
   - `pyon/file/api.py` exposes the `File` abstraction through `pyon.File` and `pyon.file.File`.

2. **Packaging and Typing**:

   - `pyproject.toml` is the single source for runtime dependencies, optional development dependencies, package metadata, build configuration, and tool configuration.
   - `pyon/py.typed` marks the package as typed for consumers using Pyright, Pylance, Mypy, or other PEP 561-aware tools.
   - `pyon/file/types.py` defines public typing helpers such as `ExportMode` and `FileDict`.

3. **Encoders Modularization**:

   - The `encoders/` directory contains submodules for handling specific categories of Python data.
   - This keeps the main encoder orchestration small and makes future type support easier to review.

4. **Testing Structure**:

   - The `tests/` directory covers public API behavior, file behavior, typing contracts, and cross-cutting resilience contracts.
   - The `tests/encoders/` directory keeps direct encoder helper and edge-case coverage next to the matching encoder category.
   - `examples/` contains executable examples that are validated during audit workflows.

---
<br>

## 11. Encoders

The **encoders** in Pyon are modularized to handle different data types efficiently. The main `encoder.py` file serves as the public interface for encoding and decoding, while the internal logic is organized into submodules within the `encoders/` directory.

Each submodule is responsible for specific categories of data types, ensuring maintainability and scalability. Below is an overview of the encoders and the types they manage:


| **Encoder**         | **Types**                                                                               |
|---------------------|-----------------------------------------------------------------------------------------|
| `base_types`        | `bool`, `float`, `int`, `str`, `type`, `None`                                           |
| `numeric_types`     | `complex`, `decimal.Decimal`                                                            |
| `collection_types`  | `bytearray`, `bytes`, `frozenset`, `list`, `set`, `tuple`                               |
|                     | `ChainMap`, `Counter`, `defaultdict`, `deque`, `namedtuple` (from collections)          |
| `datetime_types`    | `datetime.date`, `datetime.datetime`, `datetime.time`                                   |
| `mapping_types`     | `class` (user defined classes), `dataclasses.dataclass`, `dict`, `Enum`                 |
| `specialized_types` | `bitarray.bitarray`, `numpy.ndarray`, `pyon.File`, `uuid.UUID`                          |
|                     | `pandas.DataFrame`, `pandas.Series`                                                     |


This modularization simplifies the process of adding support for new data types and ensures that each encoder submodule focuses solely on its designated category of data.

As the building blocks for other types, the base types don't require encoding and decoding.

---
<br>

## 12. Testing

Pyon uses **pytest** for automated testing. The test suite covers:

- Serialization and deserialization for all supported types.
- Validation of valid, invalid, malformed, and null inputs.
- Logging of errors with `caplog` and temporary file handling with `tmp_path`.
- Public API contracts and consumer-facing typing contracts.

To run the primary validation locally:

```bash
cd Pyon
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev,debug]"
.venv\Scripts\python -m pytest --cov=pyon --cov-report=term-missing
.venv\Scripts\python -m pyright
.venv\Scripts\python -m pylint pyon tests
```

The extended audit also uses `mypy`, `ruff`, `bandit`, `radon`, `vulture`, `build`, and the executable examples under `examples/`.

---
<br>

## 13. Roadmap

For detailed plans, phased expansions, and future directions, see the [ROADMAP.md](doc/ROADMAP.md) file.

---
<br>

## 14. Media Type (IANA)

Pyon files use a structured JSON-compatible format and are best identified by the media type:  
`application/vnd.pyon+json`

This follows the IANA convention for custom JSON-based types (`+json`) and is appropriate for files with `.pyon` extension.

This media type is officially registered with IANA and listed in the official registry:  
🔗 [https://www.iana.org/assignments/media-types/media-types.xhtml#application](https://www.iana.org/assignments/media-types/media-types.xhtml#application)

Direct link:  
🔗 [https://www.iana.org/assignments/media-types/application/vnd.pyon+json](https://www.iana.org/assignments/media-types/application/vnd.pyon+json)

---

### Clipboard & Pasteboard Interoperability

**Windows (Clipboard):** Applications should use the **Microsoft-recommended clipboard registration function** when placing or reading Pyon data on the clipboard (e.g., today this is typically done via `RegisterClipboardFormatW`, but the specification intentionally avoids coupling to a specific API name).

**macOS (Pasteboard / UTI):**
- **Uniform Type Identifier (UTI):** `ai.eonflux.pyon`
- **Conforms to:** `public.json`, `public.data`
- **Filename extension:** `.pyon`

These identifiers enable consistent copy-paste and drag-and-drop behavior between desktop applications that handle Pyon objects, without repeating or redefining the media type information already provided in the IANA registration.

---
<br>

## 15. Additional Documentation

- [ROADMAP.md](doc/ROADMAP.md): Detailed plans and future directions for Pyon.  
- [VERSION.md](doc/VERSION.md): Current version details and key features.  
- [TASKS.md](doc/TASKS.md): Progress tracking and specific tasks for each version.
- [PUBLISHING.md](doc/PUBLISHING.md): Standard release, GitHub, and PyPI publication workflow.
- [CHANGELOG.md](./CHANGELOG.md): History of changes between versions.
- [FILE.md](pyon/file/README.md): `File` module documentation.
- [SECURITY.md](doc/SECURITY.md): Analysis of security guarantees and risks.

---
<br>

## 16. Contributing

We will welcome contributions of all kinds:

- **Issues**: Report bugs or suggest enhancements via GitHub issues.  
- **Pull Requests**: Submit patches or new features.  
- **Feedback**: Share your use cases to help guide future development.

Please check our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---
<br>

## 17. About the Creator

Pyon was created by Eduardo Rodrigues, a software engineer with over two decades of experience and a deep interest in science, artificial intelligence, and data structures.

He conducts independent research at **eonflux-ai**, a quiet and evolving initiative dedicated to exploring various aspects of intelligent systems — including machine learning, deep learning, natural language processing, computer vision, expert systems, and generative AI. While not a development hub, eonflux-ai serves as a research environment where ideas are tested, refined, and occasionally shared through open-source tools and publications.

Pyon itself emerged from a simple but critical need encountered during AI research: to serialize and reload complex datasets using minimal code, without compromising safety, clarity, or Python compatibility.

Throughout his career, Eduardo has worked across a range of industries — including finance, healthcare, legal systems, the automotive sector, academia, and independent research — always aiming to design tools that combine conceptual clarity with practical efficiency.

Pyon reflects a commitment to simplicity, default safety, and reproducibility. It is both a personal tool and an open invitation for collaboration.

For contact, feedback, or collaboration:
`eduardo@eonflux.ai`

---
<br>

## 18. License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.

---
<br>

## 19. Project Links

- 🔗 [GitHub Repository](https://github.com/eonflux-ai/pyon)
- 📦 [PyPI Page](https://pypi.org/project/pyon-core/)
- 📄 [IANA Media Type](https://www.iana.org/assignments/media-types/application/vnd.pyon+json)


---
<br>

**Thank you for using Pyon!** 

If you have any questions or suggestions, feel free to open an issue or start a discussion on our GitHub repository.
