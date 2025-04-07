# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
and this project adheres to [Semantic Versioning](https://semver.org/).

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
