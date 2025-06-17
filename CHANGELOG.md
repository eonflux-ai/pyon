# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.2.5-alpha] - 2025-06-16

### Added
- `export_mode` parameter in the `File` class, replacing the previous `fetch` flag. Accepts `"reference"` (default) or `"data"` to control export behavior.
- `load()` method to populate the `content` attribute from the file path or temporary path, if available.
- `unload()` method to discard in-memory content after writing it to a defined path or temporary location.
- `_write_temp()` method to write file content to a temporary file and register its path in `_tmp_path`.
- `temp` property to indicate if a temporary file is currently associated.
- `loaded` property to indicate whether the file content is currently in memory.
- `name`, `extension`, `directory` properties for extracting metadata from the file path.
- `exists` property to check if the file exists on disk.
- Status now with 3 options: `memory`, `filesystem`, and `temp`.
- Support for `__len__()` to return file size in bytes, dynamically computed from either `content` or `path`.
- Support for comparison operators (`__eq__`, `__lt__`, `__le__`, `__gt__`, `__ge__`) based on file size or content identity.
- Enhanced `__repr__` and `__str__` with structured and informative output.
- MIME type `application/vnd.pyon+json` defined and documented for `.pyon` files.
- Modularization: `file.py` moved to `pyon/file/api.py`, and now exposed via `pyon.file` package.
- Dedicated `README.md` for the `file` submodule, with usage, structure, and public interface.

### Changed
- The constructor signature of `File` was updated. It now accepts `path`, `content`, `mime`, and `export_mode`, replacing the older `filepath`, `filename`, `content`, `mime`, and `fetch`.
- `from_dict()` no longer calls `__init__()`; it instantiates objects using `__new__()` and assigns attributes directly, maintaining consistency with Pyon's deserialization constraints.
- `to_dict()` now respects the `export_mode` setting to decide whether or not to include `content`. An optional `encode: bool` argument was added to control base64 encoding.
- MIME type detection logic was moved into a private helper and reorganized to support fallbacks from `path`, `content`, and `name`.
- The `size` property no longer returns an integer. It now returns a formatted string representing the file size using appropriate units (e.g., "3.5 MB"). To obtain the raw size in bytes, use `len(file)` via the newly implemented `__len__()` method.
- Imports across modules updated to reflect the new structure of the `pyon.file` package.

### Removed
- The `fetch` parameter and related logic were removed from the `File` class.
- Attributes `filename`, `_size`, and `get_content()` method were removed or replaced by new properties and helpers.
- Direct exposure of `file.py` was removed; it is now accessed through `pyon.file`.

---

## [0.2.0-alpha] - 2025-06-09

### Added
- New optional parameters `enc_protected` and `enc_private` in `encode()` and `to_file()` to allow serialization of class attributes prefixed with `_` or `__`.
- Support for serializing Enums with complex values (e.g., tuples, dicts), extending beyond primitive types.

### Fixed
- Enums decoding errors with complex values.

---

## [0.1.5-alpha] - 2025-04-07
### Added
- Full support for `pandas.Series`, including all known index types: `Index`, `RangeIndex`, `MultiIndex`, `DatetimeIndex`, `PeriodIndex`, `TimedeltaIndex`, `CategoricalIndex`, `Float64Index`, `Int64Index`, and `UInt64Index`.
- New `_encode_series` method for serializing Series objects with index metadata and name preservation.
- New `_decode_series` method for reconstructing Series using deserialized data and regenerated index.
- Complete test suite covering all index variants within Series, ensuring accurate round-trip serialization and deserialization.

### Changed
- Introduced internal method `__rebuild_index` to centralize index reconstruction for both `DataFrame` and `Series`.
- Refactored `_decode_dataframe` to construct DataFrames directly with `data=`, `columns=`, and `index=` instead of mutating attributes post-creation.
- `__decode_index` now delegates all reconstruction to `__rebuild_index` for consistency.

### Fixed
- Serialization issues for Series with complex or structured index types.
- Improved robustness when handling `Series` elements containing objects like `pandas.Timestamp`, `pandas.Timedelta`, or nested structures.

---

## [0.1.4-alpha] - 2025-04-07
### Added
- Full support for `pandas.MultiIndex` in both `DataFrame.columns` and `DataFrame.index`.
- Modular decode logic introduced via `__decode_columns` and `__decode_index` methods.
- Comprehensive test cases covering all known `pandas.Index` variants, including nested combinations for both index and columns.
- Integration of existing `_encode_as_dict` and `_decode_from_dict` to ensure safe serialization of complex objects within `DataFrame` cells (e.g., `Timestamp`, `Period`, `Timedelta`, nested types).

### Changed
- `_encode_dataframe` now applies normalization to `MultiIndex` structures (columns and index), converting tuples to string representations during serialization.
- Raw records from `DataFrame.to_dict(orient="records")` are now processed recursively to ensure JSON safety.

### Fixed
- Crash caused by tuple-based column or index labels during JSON encoding (`TypeError: keys must be str...`) has been resolved.

---

## [0.1.3-alpha] - 2025-04-23
### Added
- First release on [PyPI](https://pypi.org/project/pyon-core/) as `pyon-core`.

---

## [0.1.2-alpha] - 2025-03-23
### Added
- Support for Python `Type` objects in serialization and deserialization.

---

## [0.1.1-alpha] - 2025-03-22
### Changed
- Internal refactors and preliminary support for future extensibility.

---

## [0.1.0-alpha] - 2025-03-22
### Added
- Initial version with core encoder/decoder logic.
- Support for common Python types and basic pandas objects.
