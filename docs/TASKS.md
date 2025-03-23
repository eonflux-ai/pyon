# Pyon Tasks

This document contains a structured list of tasks organized by version for the development of the Pyon project. Tasks are based on the roadmap and are tied to specific milestones. Use this file to track progress locally in VSCode.

---

## Version 0.1.1-alpha

### Improved testing

- [ ] Refactor test methods adding tests to all project files.
- [ ] Create tests for key methods beyond the public api.
- [ ] Test the contents of generated pyon files.
- [ ] Test recursive encode/decode of nested objects.

---

## Version 0.2.0-alpha

### Handle Shared References

- [ ] Create a hash dictionary for shared objects during serialization.
- [ ] Replace duplicates with unique references in the output.
- [ ] Implement logic to restore shared references during deserialization.
- [ ] Add tests to validate shared object scenarios.

### Detect Cyclical References

- [ ] Implement a reference tracker to detect cyclical objects.
- [ ] Replace cycles with reference tokens during serialization.
- [ ] Resolve reference tokens during deserialization.
- [ ] Write tests to ensure cyclical objects are correctly reconstructed.

---

## Version 0.3.0-alpha

### Handle Shared References

- [ ] Create a hash dictionary for shared objects during serialization.
- [ ] Replace duplicates with unique references in the output.
- [ ] Implement logic to restore shared references during deserialization.
- [ ] Add tests to validate shared object scenarios.

### Detect Cyclical References

- [ ] Implement a reference tracker to detect cyclical objects.
- [ ] Replace cycles with reference tokens during serialization.
- [ ] Resolve reference tokens during deserialization.
- [ ] Write tests to ensure cyclical objects are correctly reconstructed.

---

## Version 0.4.0-alpha

### Binary Output Support

- [ ] Add `binary=True` parameter to the `to_file` method.
- [ ] Implement compression using `gzip`, `zipfile`, or `lzma`.
- [ ] Ensure compatibility with the `from_file` method.
- [ ] Write tests to verify compression and decompression.
- [ ] Update documentation in the README.

### Encryption

- [ ] Add `encrypt=True` and `password='your-password'` parameters to the `to_file` method.
- [ ] Implement encryption logic using `cryptography` or alternatives.
- [ ] Ensure encryption works with compression.
- [ ] Implement decryption logic in the `from_file` method.
- [ ] Add tests to verify encryption and data integrity.
- [ ] Update documentation in the README.

---

## Future Versions:

### Phase 1: 0.5.0-alpha

- [ ] Add support for PyTorch tensors (`torch.Tensor`).
- [ ] Add support for TensorFlow tensors (`tf.Tensor`).
- [ ] Implement support for `networkx.Graph` graphs.
- [ ] Add support for `scipy.sparse` matrices.
- [ ] Write tests for all new types.

### Phase 2: 0.6.0-alpha

- [ ] Integrate scikit-learn models/pipelines with support for `pickle` or `joblib`.
- [ ] Implement storage of ML pipelines in a Pyon-compatible format.
- [ ] Add tests to ensure compatibility with scikit-learn.

### Phase 3: 0.7.0-alpha

- [ ] Add support for Dask structures (`DataFrame`, `Array`).
- [ ] Implement support for `xarray` (multidimensional data).
- [ ] Explore integration with HDF5 for chunked and compressed datasets.
- [ ] Add optional support for `pickle`/`joblib` as a fallback.
- [ ] Implement basic logic to serialize iterators and generators.
- [ ] Write tests for all added types.

---

## Notes

- Each task is associated with a specific category or feature.
- Use the markers to track progress:
  - `[ ]` Pending task
  - `[p]` In-progress task
  - `[x]` Completed task
- Use this file to track progress locally.
- When the project is migrated to GitHub, convert these tasks into issues for collaboration.
