# Pyon Tasks

This document contains a structured list of tasks organized by version for the development of the Pyon project. Tasks are based on the roadmap and are tied to specific milestones. Use this file to track progress locally in VSCode.

---

## Version 0.1.1-alpha — Internal Refactors

### Core Improvements
- `[x]` Initial encoder modularization and file structure setup
- `[x]` Preliminary support for future extensibility
- `[ ]` Refactor test methods adding tests to all project files
- `[ ]` Create tests for key methods beyond the public API

---

## Version 0.1.2-alpha — Type Serialization

### New Type Support
- `[x]` Add support for Python `Type` objects (`type`, `isinstance`)
- `[x]` Extend internal type detection and handler routing

---

## Version 0.1.3-alpha — PyPI Release

### Packaging
- `[x]` Create `setup.py`, finalize project metadata
- `[x]` First release on [PyPI](https://pypi.org/project/pyon-core/) as `pyon-core`

---

## Version 0.1.4-alpha — DataFrame MultiIndex Support

### Advanced Pandas Support
- `[x]` Full support for `pandas.MultiIndex` in `DataFrame.index` and `DataFrame.columns`
- `[x]` Add modular decode logic via `__decode_columns` and `__decode_index`
- `[x]` Normalize complex labels to JSON-safe types
- `[x]` Integrate recursive encoding for cells with `Timestamp`, `Period`, `Timedelta`, etc.
- `[x]` Add complete test coverage for all known `pandas.Index` types

---

## Version 0.1.5-alpha — Series Support

### Series Enhancements
- `[x]` Implement `_encode_series` and `_decode_series` methods
- `[x]` Support for all `pandas.Index` types on Series
- `[x]` Centralize index reconstruction via `__rebuild_index`
- `[x]` Refactor `_decode_dataframe` to construct objects using full signature (`data=`, `columns=`, `index=`)
- `[x]` Add test suite for `Series`, covering all index combinations

---

## Version 0.2.0-alpha — Arbitrary Dict Keys

### Mapping Flexibility
- `[p]` Support for any hashable type as a dict key (instead of only strings)
- `[ ]` Encode/decode recursive mapping types with mixed key/value types
- `[ ]` Add tests for edge cases: tuples, enums, frozenset, nested keys
- `[ ]` Update encoder routing to handle these during dict traversal

---

## Version 0.3.0-alpha — Shared and Cyclical References

### Shared References
- `[ ]` Create a hash dictionary for shared objects during serialization
- `[ ]` Replace duplicates with unique references in the output
- `[ ]` Restore shared references during deserialization
- `[ ]` Add tests for aliasing scenarios

### Cyclical References
- `[ ]` Detect cycles and inject reference tokens
- `[ ]` Resolve references during decode
- `[ ]` Prevent infinite recursion in cyclical structures

---

## Version 0.4.0-alpha — Binary and Encryption Support

### Binary I/O
- `[ ]` Add `binary=True` to `to_file`, support `gzip`, `lzma`, `zipfile`
- `[ ]` Ensure compatibility with `from_file`
- `[ ]` Write tests for compressed I/O

### Encryption
- `[ ]` Add `encrypt=True` and `password` to `to_file`
- `[ ]` Use `cryptography` for secure AES-based encryption
- `[ ]` Integrate with binary output
- `[ ]` Write tests for encrypted round-trip

---

## Future Versions

### 0.5.0-alpha — Scientific Ecosystem Support
- `[ ]` PyTorch: `torch.Tensor`
- `[ ]` TensorFlow: `tf.Tensor`
- `[ ]` `networkx.Graph`, `scipy.sparse` matrices

### 0.6.0-alpha — ML Integration
- `[ ]` Scikit-learn pipelines with `pickle`/`joblib`
- `[ ]` Serialize ML models in reusable format

### 0.7.0-alpha — Distributed and Streaming Support
- `[ ]` `dask` DataFrames/Arrays
- `[ ]` `xarray` for N-D labeled arrays
- `[ ]` Fallback integration with `pickle`
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
