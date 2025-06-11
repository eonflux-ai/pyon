# Pyon Versioning

## Current Version: 0.1.5-alpha

### Status
Alpha (Mature)

### Overview
This version of Pyon delivers major improvements in the support for `pandas` structures, completing the serialization logic for `DataFrame` and introducing robust support for `Series`. It also includes architectural refactors that improve maintainability and consistency across specialized encoders.

The project remains in the alpha phase, but is nearing functional maturity. The next milestone will focus on expanding support for dynamic dictionary keys and testing object graphs (shared and cyclic references).

---

### Key Features in 0.1.5-alpha

- ✅ Full support for `pandas.Series`, including all standard and advanced index types.
- ✅ Full support for `pandas.MultiIndex` in `DataFrame.columns` and `DataFrame.index`.
- ✅ All `DataFrame` and `Series` index types now normalized to ensure JSON compatibility.
- ✅ Encoded data cells (from `to_dict(orient="records")`) are now recursively encoded using Pyon’s full logic.
- ✅ Modularized decoding: separated methods for handling columns and indexes (`__decode_columns`, `__decode_index`).
- ✅ Centralized index reconstruction via `__rebuild_index`, used by both `DataFrame` and `Series`.
- ✅ Cleaned up `DataFrame` decoding by constructing directly from `data`, `columns`, and `index`.

---

### Tasks Completed for This Version

- [x] Add `_encode_series` and `_decode_series` methods.
- [x] Add test coverage for `Series` with all index types.
- [x] Modularize and refactor index decoding logic (`__rebuild_index`).
- [x] Convert DataFrame decoding to direct object creation.
- [x] Add `MultiIndex` support for both `columns` and `index`.
- [x] Normalize all label structures for JSON-safe serialization.

---

### Known Limitations

- Dicts still only accept `str` keys.
- Cyclical references are not yet supported.
- Shared object references are not optimized.
- Binary output and encryption are pending.
- No support yet for tensors, graphs, or advanced ML structures.

---

### Next Steps

The next version will be **0.2.0-alpha**, focused on:

- 🔓 Full support for any type of object as dictionary keys.
- ✅ Finalize and test already implemented dictionary key generalization.
- 🧪 Add test coverage for advanced dict key types (e.g., `tuple`, `UUID`, `datetime`).
- 🚀 Publish this as the first major release candidate after full validation.

---

## Versioning Notes

This project follows semantic versioning principles:
- **MAJOR.MINOR.PATCH**
- Pre-release versions are suffixed with `-alpha`, `-beta`, or `-rc`.

For example:
- `0.1.5-alpha`: Current alpha release (Series + DataFrame refinements).
- `0.2.0-alpha`: Next alpha, supporting generic dictionary keys.
- `1.0.0-beta`: First beta release with full core and safety features.
- `1.0.0`: First production-ready release.

---

## Feedback and Contribution

This version is considered stable for most usage scenarios involving supported types.  
Feedback and contribution are welcome to guide the roadmap and push Pyon toward its 1.0 release.
