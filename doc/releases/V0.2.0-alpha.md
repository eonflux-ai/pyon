# Pyon Versioning

## Current Version: 0.2.0-alpha

### Status
Alpha (Mature)

### Overview

A significant structural evolution of Pyon. Allows supported pyon types as dictionary keys — a major step beyond string-only mappings — adding enhanced flexibility for object introspection.\
This release also improves support for encoding and decoding user-defined classes, including optional serialization of protected and private attributes.\
The internal system now correctly handles complex `Enum` values, including those based on tuples or dictionaries.\
Although still in alpha, this version is stable for use cases involving complex but acyclic Python supported structures and JSON-safe types.


---

### Key Features in 0.2.0-alpha

- ✅ Allow any pyon supported type be used as a dict key (instead of only strings).
- ✅ Encode/decode recursive mapping types with mixed key/value types.
- ✅ Add support for optional inclusion of protected attributes (`_`) via `enc_protected=True`.
- ✅ Add support for optional inclusion of private attributes (`__`) via `enc_private=True`.
- ✅ Support for serializing Enums with complex values (e.g., tuples, dicts).

---

### Tasks Completed for This Version

- [x] Add support for any type as dictionary key.
- [x] Support recursive encoding/decoding of mixed key/value types in mappings.
- [x] Add `enc_protected` and `enc_private` flags to include non-public attributes.
- [x] Add support for complex `Enum` values.

---

### Known Limitations

- Shared and cyclical references are not yet supported.
- Binary output and encryption are pending implementation.
- No support yet for deep ML structures like `torch.Tensor`, `tf.Tensor`, `networkx.Graph`, or `scipy.sparse`.

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
