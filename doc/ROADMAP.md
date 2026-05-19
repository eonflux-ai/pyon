# Pyon Roadmap

This document outlines the future direction of **Pyon**, a serialization and deserialization library that extends JSON to preserve complex Python object semantics.

The roadmap is intentionally directional. Items listed here are not part of the current public contract until they are implemented, tested, documented, and released.

---

## Table of Contents

1. [Roadmap Principles](#1-roadmap-principles)
2. [Object Graph Fidelity](#2-object-graph-fidelity)
3. [Safety and Validation](#3-safety-and-validation)
4. [Storage and File Evolution](#4-storage-and-file-evolution)
5. [Interoperability Profiles and Adapter Registry](#5-interoperability-profiles-and-adapter-registry)
6. [New Types: Phased Expansions](#6-new-types-phased-expansions)
7. [Additional Potential Features](#7-additional-potential-features)
8. [Funded Development](#8-funded-development)
9. [Contributing](#9-contributing)
10. [Related Documents](#10-related-documents)

---

## 1. Roadmap Principles

Pyon's mission is to provide a robust and extensible way to serialize and deserialize Python objects that go beyond standard JSON while preserving transparency and reviewability.

As the project grows, the main goals are:

- Improve correctness, safety, and long-term format stability.
- Preserve a readable JSON-compatible representation wherever practical.
- Support additional data types relevant to AI, data processing, automation, and scientific workflows.
- Keep advanced reconstruction behavior explicit, documented, and testable.
- Avoid treating future interoperability as arbitrary runtime object execution.

---

## 2. Object Graph Fidelity

### Detecting Cyclical References

**Goal**: Prevent infinite recursion when objects reference themselves directly or indirectly.

**Proposed Approach**:

1. Track object identities during serialization.
2. Replace repeated cyclic encounters with reference tokens.
3. Resolve reference tokens during deserialization.

**Benefits**:

- Avoids recursion depth errors.
- Allows deterministic handling of cyclic structures.
- Creates a foundation for richer object graph support.

### Handling Shared References

**Goal**: Preserve scenarios where multiple objects share the same sub-object without forming a cycle.

**Proposed Approach**:

1. Track encountered objects and assign stable reference identifiers.
2. Store repeated references as links instead of duplicate serialized payloads.
3. Restore shared object identity during deserialization when the target runtime supports it.

**Benefits**:

- Reduces output size.
- Preserves aliasing semantics.
- Opens a path toward object archive and storage-oriented workflows.

---

## 3. Safety and Validation

### Safe Decode Mode

**Goal**: Provide a restricted decode mode for untrusted or semi-trusted data.

Potential capabilities:

- Allow-list based type reconstruction.
- Disable reconstruction of types with constructor or runtime caveats.
- Decode unsupported or disallowed types into plain structured data.
- Report rejected types with explicit diagnostics.

### Schema Generation

**Goal**: Generate schemas or schema-like descriptions from Pyon payloads.

Potential uses:

- Validate payloads before decode.
- Document expected result shapes.
- Support interop profiles for other runtimes.
- Improve tooling around versioned serialized data.

---

## 4. Storage and File Evolution

Pyon may evolve beyond individual object serialization toward structured object archives and storage-oriented workflows.

This direction is exploratory and should not be interpreted as a current database contract.

Potential capabilities:

- Store collections of Pyon objects as structured archives.
- Maintain manifests with object metadata, type names, version information, and optional indexes.
- Support chunked or streamed storage for larger payloads.
- Support query-friendly metadata without requiring full object reconstruction.
- Preserve compatibility with the readable Pyon representation where practical.

Initial storage-oriented work should focus on deterministic archive layout and metadata indexing. It should not attempt to replace general-purpose databases in early versions.

### Binary Output and Compression

**Goal**: Provide an option to create compressed Pyon files.

Potential approach:

1. Add an explicit compression option to file output.
2. Use standard compression modules such as `gzip`, `zipfile`, or `lzma`.
3. Preserve the ability to recover the original readable Pyon text after decompression.

### Encryption

**Goal**: Provide optional encryption for serialized output.

Potential approach:

1. Add an explicit encryption option to file output.
2. Use reviewed cryptographic libraries and documented key handling.
3. Keep encryption separate from serialization semantics.

Encryption must be designed carefully and should not be added as a superficial wrapper around sensitive data.

---

## 5. Interoperability Profiles and Adapter Registry

Pyon is currently Python-first. Broader cross-runtime interoperability is a long-term direction, not a current guarantee.

The most practical path is to define explicit interoperability profiles rather than attempting arbitrary object reconstruction across languages.

### Core Interop Profile

A future core interop profile could support:

- `null` / `None`
- booleans
- integers and floats
- strings
- arrays/lists
- maps/objects with string keys
- simple record-like data objects
- datetime-like values through documented metadata

The goal would be to let Java, C#, JavaScript, or other runtimes decode Pyon payloads into maps, records, DTOs, or plain data objects without executing arbitrary constructors.

### Adapter Registry

A future adapter registry could let users define explicit translators for types not covered by the core profile.

Potential adapter responsibilities:

- Detect whether a type tag or metadata shape is supported.
- Convert Pyon payloads into local runtime objects.
- Convert local runtime objects back into Pyon-compatible payloads.
- Fail safely when metadata is missing or unsupported.

This should be designed as an explicit registry, not as unsafe dynamic plugin loading by default.

Example conceptual mappings:

- Python `decimal.Decimal` to Java `BigDecimal` or C# `decimal`.
- Python `uuid.UUID` to Java/C# UUID/GUID equivalents.
- Simple Python data objects to Java records or C# records.
- Domain-specific classes to user-defined DTOs.

### Runtime Bridges

Possible future bridges include:

- Python-to-Java data object exchange.
- Python-to-C# data object exchange.
- Decode-to-map workflows for runtimes without a formal adapter.

Cross-runtime bridges should prioritize simple data objects and explicit adapters before attempting full runtime object reconstruction.

---

## 6. New Types: Phased Expansions

### Phase 1

- **AI/ML Tensors**:
  - PyTorch (`torch.Tensor`)
  - TensorFlow (`tf.Tensor`)
- **Graph Structures**:
  - `networkx.Graph`
- **Sparse Data**:
  - `scipy.sparse` matrices

These data types are useful in machine learning and graph-based workflows, but they require careful handling to avoid fragile or oversized payloads.

### Phase 2

- **scikit-learn Models/Pipelines**:
  - Store model artifacts, estimators, and preprocessing pipelines in a Pyon-friendly format.

Model support should prefer metadata and portable state over unsafe executable reconstruction.

### Phase 3

- **Dask DataFrames/Arrays**:
  - Explore large-scale distributed structures without forcing everything into memory.
- **xarray**:
  - Preserve coordinate metadata and dimension labels.
- **HDF5 Integration**:
  - Explore interoperability with chunked and compressed dataset storage.
- **Iterators/Generators**:
  - Possibly store basic state or configuration, not arbitrary execution state.

---

## 7. Additional Potential Features

Additional exploratory features include:

- APIs and services for web frameworks such as FastAPI or Django.
- Command-line validation and inspection tools.
- Format inspection tools for debugging Pyon payloads.
- Versioned format metadata and migration helpers.
- Public format specification once the payload contracts stabilize.

---

## 8. Funded Development

Some roadmap items, especially cross-runtime interoperability, adapter registries, storage-oriented features, formal specifications, and production hardening, require sustained engineering effort.

If these capabilities have value for your organization, funded development can help prioritize and accelerate them.

For sponsorship or funded development inquiries, contact: `eduardo@eonflux.ai`.

---

## 9. Contributing

We welcome contributions of any kind, including code, documentation, examples, issue reports, and feedback on future directions.

To get involved:

1. Check existing issues to see if your idea or bug has already been reported.
2. Open a new issue with a clear description and practical use case.
3. Submit a pull request with tests and documentation when applicable.
4. Discuss roadmap items before implementing large features.

Please read [CONTRIBUTING.md](../CONTRIBUTING.md) for setup, validation, and pull request guidelines.

---

## 10. Related Documents

For more details on progress and specific tasks, refer to:

- [VERSION.md](VERSION.md): Current version and features.
- [TASKS.md](TASKS.md): Detailed tasks and progress tracking.
- [SECURITY.md](SECURITY.md): Decode safety model and caveats.
- [PUBLISHING.md](PUBLISHING.md): Release and publication workflow.

---

Thank you for supporting Pyon. For questions, suggestions, or to share your use case, feel free to open an issue or start a discussion in the GitHub repository.
