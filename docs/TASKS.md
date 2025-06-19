# Pyon Tasks

This document contains a structured list of tasks organized by version for the development of the Pyon project. Tasks are based on the roadmap and are tied to specific milestones. Use this file to track progress locally in VSCode.

---

## Version 0.2.6-alpha — Decode Audit & Security Documentation

### ✅ Decode Pipeline Audit
- [x] Conduct full audit of the decoding logic across all modules
- [x] Identify and categorize all types that invoke constructors
- [x] Confirm passive behavior of `__new__` + direct attribute assignment
- [x] Validate that no user-defined methods (`__init__`, `from_json`, etc.) are invoked
- [x] Classify modules as fully conformant or with documented caveats

### ✅ SECURITY.md Creation
- [x] Create dedicated `SECURITY.md` with full security overview
- [x] Document constructor-based exceptions with detailed table
- [x] Highlight risks related to external or tampered `.pyon` files
- [x] Recommend best practices for secure decoding

### ✅ README.md Updates
- [x] Revise section on **Decode Without Execution** to reflect audit findings
- [x] Add summary of constructor-based exceptions, with link to `SECURITY.md`
- [x] Update section on **JSON Compatibility** to clarify that Pyon is not a drop-in JSON replacement
- [x] Add MIME type information and its implications for tooling

### ✅ Documentation Cleanup
- [x] Standardize terminology: decoding, deserialization, constructor-based logic
- [x] Include links to `SECURITY.md` in relevant sections (Decode, JSON Compatibility)
- [x] Cross-link audit data from `decode-pipeline--2025-06-18.md` where appropriate
- [x] Ensure consistency between `README.md`, `SECURITY.md`, and MIME registration notes

---

## Version 0.2.5-alpha — Enhanced File Handling

### ✅ File Object Refactor
- [x] Replace `fetch` with `export_mode: Literal["reference", "data"]`
- [x] Redesign constructor interface to accept `path`, `content`, `mime`, and `export_mode`
- [x] Use `__new__` in `from_dict()` to bypass `__init__`, preserving deserialization neutrality
- [x] Update `to_dict()` to include content only when `export_mode == "data"`

### ✅ Temporary File Support
- [x] Add `_write_temp()` to write content to a temporary file
- [x] Add `_tmp_path` tracking for temporary file location
- [x] Update `load()` to prioritize loading from temporary file if present
- [x] Add `unload()` method to discard memory content and persist to file or temp location

### ✅ Interface Improvements
- [x] Add `__len__()` to return raw byte size
- [x] Redefine `size` to return formatted size string (e.g., "3.1 MB")
- [x] Add `name`, `extension`, `directory` properties
- [x] Add `loaded` and `temp` state properties
- [x] Implement comparison operators: `__eq__`, `__lt__`, `__le__`, `__gt__`, `__ge__`

### ✅ MIME Type and IANA Registration
- [x] Define MIME type as `application/vnd.pyon+json`
- [x] Add section to README specifying MIME type and usage
- [x] Prepare full registration form for IANA media type registry
- [x] Archive registration info in `docs/other/iana-registration.md`

### ✅ Modularization and Isolation
- [x] Create `pyon.file` as its own module directory
- [x] Move implementation from `file.py` to `pyon/file/api.py`
- [x] Create `pyon/file/__init__.py` to expose `File` from `api`
- [x] Ensure `from pyon.file import File` works as expected
- [x] Refactor imports across project to reflect new structure

### ✅ Documentation Bootstrap
- [x] Create standalone `README.md` for `pyon/file` submodule
- [x] Include version badge, GitHub links, license, and summary
- [x] Document current public interface of `File` (pre-refactor)
- [x] Provide example usage consistent with Pyon serialization
- [x] Plan for migration to future interface (0.3.x)

---

## Version 0.2.0-alpha — Arbitrary Dict Keys

### Mapping Flexibility
- `[x]` Allow any pyon supported type be used as a dict key (instead of only strings)
- `[x]` Encode/decode recursive mapping types with mixed key/value types

### Attribute Visibility Control
- `[x]` Add support for optional inclusion of protected attributes (`_`) via `enc_protected=True`
- `[x]` Add support for optional inclusion of private attributes (`__`) via `enc_private=True`

### Enum Enhancements
- `[x]` Support for serializing Enums with complex values (e.g., tuples, dicts)

---

## Version 0.1.5-alpha — Series Support

### Series Enhancements
- `[x]` Implement `_encode_series` and `_decode_series` methods
- `[x]` Support for all `pandas.Index` types on Series
- `[x]` Centralize index reconstruction via `__rebuild_index`
- `[x]` Refactor `_decode_dataframe` to construct objects using full signature (`data=`, `columns=`, `index=`)
- `[x]` Add test suite for `Series`, covering all index combinations

---

## Version 0.1.4-alpha — DataFrame MultiIndex Support

### Advanced Pandas Support
- `[x]` Full support for `pandas.MultiIndex` in `DataFrame.index` and `DataFrame.columns`
- `[x]` Add modular decode logic via `__decode_columns` and `__decode_index`
- `[x]` Normalize complex labels to JSON-safe types
- `[x]` Integrate recursive encoding for cells with `Timestamp`, `Period`, `Timedelta`, etc.
- `[x]` Add complete test coverage for all known `pandas.Index` types

---

## Version 0.1.3-alpha — PyPI Release

### Packaging
- `[x]` Create `setup.py`, finalize project metadata
- `[x]` First release on [PyPI](https://pypi.org/project/pyon-core/) as `pyon-core`

---

## Version 0.1.2-alpha — Type Serialization

### New Type Support
- `[x]` Add support for Python `Type` objects (`type`, `isinstance`)
- `[x]` Extend internal type detection and handler routing

---

## Version 0.1.1-alpha — Internal Refactors

### Core Improvements
- `[x]` Initial encoder modularization and file structure setup
- `[x]` Preliminary support for future extensibility
- `[ ]` Refactor test methods adding tests to all project files
- `[ ]` Create tests for key methods beyond the public API

---

## Future Versions

### Version 0.3.0-alpha — Shared and Cyclical References

#### Shared References
- `[ ]` Create a hash dictionary for shared objects during serialization
- `[ ]` Replace duplicates with unique references in the output
- `[ ]` Restore shared references during deserialization
- `[ ]` Add tests for aliasing scenarios

#### Cyclical References
- `[ ]` Detect cycles and inject reference tokens
- `[ ]` Resolve references during decode
- `[ ]` Prevent infinite recursion in cyclical structures

---

### Version 0.4.0-alpha — Binary and Encryption Support

#### Binary I/O
- `[ ]` Add `binary=True` to `to_file`, support `gzip`, `lzma`, `zipfile`
- `[ ]` Ensure compatibility with `from_file`
- `[ ]` Write tests for compressed I/O

#### Encryption
- `[ ]` Add `encrypt=True` and `password` to `to_file`
- `[ ]` Use `cryptography` for secure AES-based encryption
- `[ ]` Integrate with binary output
- `[ ]` Write tests for encrypted round-trip

---

### 0.5.0-alpha — Scientific Ecosystem Support
- `[ ]` PyTorch: `torch.Tensor`
- `[ ]` TensorFlow: `tf.Tensor`
- `[ ]` `networkx.Graph`, `scipy.sparse` matrices

### 0.6.0-alpha — ML Integration
- `[ ]` Serialize ML models in reusable format

### 0.7.0-alpha — Distributed and Streaming Support
- `[ ]` `dask` DataFrames/Arrays
- `[ ]` `xarray` for N-D labeled arrays
- `[ ]` Support for generators/iterators

---

## Notes

- Each task is associated with a specific category or feature.
- Use the markers to track progress:
  - `[ ]` Pending task
  - `[p]` In-progress task
  - `[x]` Completed task
- This file is meant for local tracking during development.
- In GitHub, tasks will be converted into issues/milestones for collaboration.
