# Pyon Versioning

## Current Version: 0.2.6-alpha

### Status
Alpha (Stable)

### Overview

This version focuses on auditing the Pyon decoding pipeline and updating all documentation to reflect the results of this security review.  
A dedicated `SECURITY.md` file was added to provide a detailed description of the decoding guarantees, constructor-based risks, and recommended practices.  
The `README.md` was revised to improve the clarity and accuracy of sections related to decoding behavior and JSON compatibility, ensuring alignment with the actual implementation and the MIME type specification.

This release solidifies Pyon’s security model for deserialization and lays the groundwork for future `safe_mode` and field validation features.

---

### Key Features in 0.2.6-alpha

- ✅ Conducted and documented a full decode pipeline audit.
- ✅ Created `SECURITY.md` with detailed explanations of deserialization behavior and constructor usage.
- ✅ Rewrote section 8 ("Decode Without Execution") of `README.md` to reflect audited guarantees.
- ✅ Rewrote section 9 ("JSON Compatibility") to clarify the distinction between structural and semantic JSON compatibility.
- ✅ Integrated constructor-based exception table into `README.md`, detailing safe and partially safe decoding types.
- ✅ Documented limitations and risks of decoding external `.pyon` files.
- ✅ Planned future improvements such as `safe_mode`, allow-lists, and validation hooks.

---

### Tasks Completed for This Version

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

### Known Limitations

- Shared and cyclical references are not yet supported.
- Binary output and encryption are pending implementation.
- No support yet for deep ML structures like `torch.Tensor`, `tf.Tensor`, `networkx.Graph`, or `scipy.sparse`.

---

### Next Steps

The next version will be **0.3.0-alpha**, focused on extending the `File` interface and preparing it for general-purpose file management.

Key goals include:

- 🔐 **Safe Decode Mode**: Add support for a `safe_mode` flag in `decode()` to restrict decoding to a whitelist of known-safe types.
- 📂 **Stream Support**: Implement chunked and line-by-line reading via `stream()` and `to_stream()` interfaces.
- 🌐 **Remote File Access**: Introduce `from_url()` to create `File` instances directly from HTTP(S) sources.
- ✅ **Existence and Status Checks**: Expand metadata and introspection via properties like `exists`, `status`, and `is_loaded`.
- 🔄 **Export Control**: Continue refining the `export_mode` mechanism to ensure predictable serialization behavior.
- 🧪 **Dedicated Testing**: Isolate `pyon.file` tests to its own suite, ensuring maintainability and clarity.
- 📚 **Module Documentation**: Expand the `README.md` of `pyon.file` to reflect upcoming additions, with code samples and guidelines.

These changes aim to make the `File` class a self-contained and expressive abstraction for both serialized and disk-based content, without deviating from Pyon's core principles: deterministic behavior, secure deserialization, and clear object boundaries.

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
