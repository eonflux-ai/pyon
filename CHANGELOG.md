# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.2.0-alpha] - 2025-06-09

### Added
- Support for hashing via `to_hash(obj, algorithm='sha256')`, with selectable algorithms: `sha256`, `sha512`, `sha3_256`, `sha3_512`, `blake2b`, `md5`, and `sha1`.
- New method `to_int(obj)` that generates a deterministic 256-bit integer identifier based on the SHA-256 hash of the serialized object, even for non-hashable types like `dict` and `set`.
- New optional parameters `enc_protected` and `enc_private` in `encode()` to allow serialization of class attributes prefixed with `_` or `__`.
- Support for serializing Enums with complex values (e.g., tuples, dicts), extending beyond primitive types.
- Support for `__pyon_post_init__()` method to finalize object reconstruction after decoding.

### Changed
- Internal hash API split into `to_hash()` and `_to_hash()` to improve maintainability.

### Fixed
- Ensured deterministic behavior in all supported hashing algorithms for identical object states across machines and executions.

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
