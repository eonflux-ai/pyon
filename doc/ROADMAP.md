# Pyon Roadmap

This document outlines the future direction of **Pyon**, a serialization/deserialization library extending JSON to handle complex Python objects. Here, we detail planned features, optimizations, and phased expansions of supported data types.

---

## Table of Contents

1. [Introduction](#introduction)  
2. [Detecting Cyclical References](#detecting-cyclical-references)  
3. [Handling Shared References](#handling-shared-references)  
4. [New Types: Phased Expansions](#new-types-phased-expansions)  
   - [Phase 1](#phase-1)  
   - [Phase-2](#phase-2)  
   - [Phase-3](#phase-3)  
5. [Binary Output](#binary-output)  
6. [Encryption](#encryption)  
7. [Additional Potential Features](#additional-potential-features)  
8. [Contributing](#contributing)  
9. [Related Documents](#related-documents)  

---

## 1. Introduction

Pyon’s mission is to provide a robust and extensible way to serialize and deserialize Python objects that go beyond standard JSON. As the project grows, we aim to:

- Improve performance and memory usage.  
- Support additional data types critical for AI/ML and data processing.  
- Enhance usability and reliability in production environments.

This roadmap describes major features and improvements that the community and core developers consider high-priority for upcoming releases.

---

## 2. Detecting Cyclical References

**Goal**: Prevent infinite recursion and streamline memory usage when objects reference themselves (directly or indirectly).

- **Why It Matters**: In Python, it’s relatively easy to create data structures that loop back onto themselves. For example, a linked list or a self-referencing node.  
- **Proposed Approach**:  
  1. Implement a reference tracker that records object identities (e.g., `id(obj)`) as they’re serialized.  
  2. If the serializer encounters an already-seen object, it replaces it with a reference token (instead of attempting to serialize it again).  
  3. During deserialization, the reference tokens are resolved to re-create the cyclical structure.  
- **Benefits**:  
  - Avoids recursion depth errors and infinite loops.  
  - Ensures consistent, repeatable serialization of cyclical objects.

---

## 3. Handling Shared References

**Goal**: Optimize scenarios where multiple objects share the **same** sub-object but do **not** form a cycle.

- **Use Case**:  
  - A single instance of `A` is referenced by many instances of `B` in a collection.  
  - Currently, each `B` might cause a redundant copy of `A` in the serialized output.  
- **Proposed Solution**:  
  - Maintain a dictionary (e.g., `{(type, hash): object}`) that tracks encountered objects and their unique hashes.  
  - When the same object appears again, store only a reference to the hash, not the full serialization.  
  - During deserialization, replace those references with the original object from the dictionary.  
- **Benefits**:  
  - Reduces output size significantly.  
  - Preserves the concept of shared data (multiple pointers to the same object).

---

## 4. Binary Output

**Goal**: Provide an option to create a compressed, binary file in the `to_file` method.  

**Use Case**:  
- Pyon outputs are text-based, potentially large JSON-like structures.  
- Compressing them can significantly reduce file size while preserving the human-readable format (once decompressed).

**Proposed Approach**:  
1. Add a parameter to `to_file` (e.g., `binary=True` or `compression=True`).  
2. Use Python’s standard compression modules (e.g., `gzip`, `zipfile`, or `lzma`) to compress the serialized string.  
3. The user can decompress the file to retrieve the original, readable Pyon text—preserving both compactness and human-friendliness.

**Benefits**:  
- Substantially smaller output files for large datasets.  
- Straightforward implementation using built-in compression libraries.  
- Maintains readability and interoperability by allowing simple decompression to restore the original Pyon format.

---

## 5. Encryption

**Goal**: Provide an option to encrypt a Pyon output file with a password, ensuring secure serialization and deserialization.

**Use Case**:  
- Protect sensitive data serialized by Pyon with encryption, similar to how tools like WinRAR or ZIP offer password protection.

**Proposed Approach**:  
1. Add a parameter to `to_file` (e.g., `encrypt=True` and `password='your-password'`).  
2. Use Python libraries such as `gzip`, `zipfile`, or `lzma` in combination with encryption modules (e.g., `cryptography` or built-in alternatives) to encrypt the serialized data.
3. The file can only be decrypted with the same password, ensuring security during storage or transmission.

**Benefits**:  
- Adds a layer of security to serialized data.  
- Prevents unauthorized access to sensitive or proprietary information.  
- Integrates seamlessly with the existing `to_file` and `from_file` methods.

---

## 6. New Types: Phased Expansions

Below is our plan for expanding the range of types that **Pyon** supports. We’ve split this into **three phases** based on priority and complexity.

### Phase 1

- **AI/ML Tensors**:  
  - **PyTorch** (`torch.Tensor`)  
  - **TensorFlow** (`tf.Tensor`)  
- **Graph Structures**: `networkx.Graph`  
- **Sparse Data**: `scipy.sparse` matrices  

*Rationale*: These data types are essential in machine learning and graph-based applications, providing immediate value to a wide range of users.

### Phase 2

- **scikit-learn Models/Pipelines**  
  - Store model artifacts (estimators, preprocessing pipelines) in a Pyon-friendly format.

*Rationale*: scikit-learn remains one of the most popular machine learning libraries, so supporting its models will broaden Pyon’s appeal in production and research environments.

### Phase 3

- **Dask DataFrames/Arrays**  
  - Extend Pyon for large-scale, distributed data structures without forcing everything into memory.  
- **xarray (Labeled Multidimensional Data)**  
  - Preserve coordinate metadata and dimension labels, crucial for scientific data.  
- **HDF5 Integration**  
  - Explore interoperability with chunked and compressed dataset storage.  
- **Iterators/Generators (Limited Support)**  
  - Possibly store basic state or configurations (though full generator state is complex).

*Rationale*: Phase 3 focuses on large data handling, advanced scientific use cases, and bridging gaps with existing Python serialization practices.

---

## 7. Additional Potential Features

Beyond the main roadmap items, we’re exploring:

- **Schema Generation**: Automatic creation of schemas to validate Pyon-serialized data.  
- **APIs and Services**: Tools to integrate Pyon directly with web frameworks (e.g., FastAPI, Django).  
- **Plugin Architecture**: A standardized way for the community to contribute custom serializers for new data types.

---

## 8. Contributing

We welcome contributions of any kind—whether it’s code, documentation, or simply feedback on new features. To get involved:

1. **Check Existing Issues**: See if your idea or bug has already been reported.  
2. **Open a New Issue**: Share details about new feature requests or bugs.  
3. **Submit a Pull Request**: Fork the repo and propose your changes.  
4. **Discuss & Collaborate**: Join our community discussions to help shape the roadmap.

Please read our [CONTRIBUTING.md](CONTRIBUTING.md) (if available) for detailed guidelines.

---

## 9. Related Documents

For more details on progress and specific tasks, refer to:
- [VERSION.md](VERSION.md): Current version and features.
- [TASKS.md](TASKS.md): Detailed tasks and progress tracking.

---
\
**Thank you for supporting Pyon!**  
For questions, suggestions, or to share your use case, feel free to open an issue or start a discussion in our GitHub repository.
