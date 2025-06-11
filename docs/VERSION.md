# Pyon Versioning

## Current Version: 0.2.0-alpha

### Status
Alpha (Mature)

### Overview
This version of Pyon introduces several critical features aimed at enhancing flexibility, introspection, and identification.  
In addition to supporting arbitrary types as dictionary keys, it adds robust hashing utilities and control over class attribute visibility during serialization.  
These enhancements significantly expand Pyon's applicability to object tracking, caching, and structural comparison use cases.

---

### Key Features in 0.2.0-alpha

- ✅ Full support for any hashable type as a dictionary key (not just strings).
- ✅ Recursive serialization of mapping types with mixed key/value structures.
- ✅ New `to_hash()` utility supporting 7 algorithms (`sha256`, `sha512`, `sha3_256`, `sha3_512`, `blake2b`, `md5`, `sha1`) for deterministic hashing.
- ✅ New `to_int()` method for generating a 256-bit stable integer hash from any object.
- ✅ Optional inclusion of protected (`_`) and private (`__`) attributes during serialization using `enc_protected` and `enc_private` flags.
- ✅ Support for complex `Enum` values (e.g., tuples, dicts) in serialization.
- ✅ New `__pyon_post_init__()` hook allows objects to self-reconstruct internal state after deserialization.

---

### Tasks Completed for This Version

- [x] Add support for any type as dictionary key.
- [x] Support recursive encoding/decoding of mixed key/value types in mappings.
- [x] Add `to_hash()` with configurable algorithm.
- [x] Add `to_int()` deterministic integer hash.
- [x] Add `enc_protected` and `enc_private` flags to include non-public attributes.
- [x] Add support for complex `Enum` values.
- [x] Ensure hash behavior is deterministic across platforms and executions.
- [x] Refactor internal hash API into `to_hash()` and `_to_hash()` for separation of concerns.
- [x] Add support for `__pyon_post_init__()` lifecycle hook after object deserialization.

---

### Known Limitations

- Shared and cyclical references are not yet supported.
- Binary output and encryption are pending implementation.
- No support yet for deep ML structures like `torch.Tensor`, `tf.Tensor`, `networkx.Graph`, or `scipy.sparse`.
- Fallback integration with `pickle` not yet available.

---

### Next Steps

The next version will be **0.3.0-alpha**, focused on:

- 🔁 Shared object aliasing and cyclical reference handling.
- 🧠 Preventing infinite recursion during serialization.
- 🧪 Advanced object graph testing.

---

## Versioning Notes

This project follows semantic versioning principles:
- **MAJOR.MINOR.PATCH**
- Pre-release versions are suffixed with `-alpha`, `-beta`, or `-rc`.

For example:
- `0.2.0-alpha`: Current alpha release (dict keys + hashing + protected/private support).
- `0.3.0-alpha`: Next alpha, introducing reference handling for shared/cyclic objects.
- `1.0.0-beta`: First beta release with full core and safety features.
- `1.0.0`: First production-ready release.

---

## Feedback and Contribution

This version is considered stable for all usage scenarios involving JSON-safe and hashable Python structures.  
Feedback and suggestions are welcome to guide the roadmap toward 1.0.
