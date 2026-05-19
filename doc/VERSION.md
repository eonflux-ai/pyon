# Pyon Versioning

## Current Version: 0.2.7-alpha

### Status
Alpha (Stable)

### Overview
This version introduces **Timezone Region (IANA TZDB)** support for temporal types, ensuring **exact round-trip** for `datetime` objects and **pandas` time-based indexes. This resolves reconstruction errors that occurred when pandas required explicit timezone information to rebuild `DatetimeIndex` faithfully. Metadata now includes region, offset, and fold (PEP 495), enabling precise representation of temporal data.

---

### Key Features in 0.2.7-alpha

- ✅ Added storage of **timezone region** (IANA TZDB, e.g., `America/Sao_Paulo`) in encoded temporal objects.
- ✅ Added storage of **UTC offset** (`+HH:MM`) and **fold** (PEP 495) when applicable.
- ✅ Updated decode logic to:
  - Prefer `ZoneInfo(region)` when available.
  - Fallback to fixed offset when region is not found.
  - Safely handle naïve `datetime` before applying `astimezone`.
- ✅ Updated offset parser to correctly accept canonical `+HH:MM`/`-HH:MM` length.
- ✅ Extended support to `time` with timezone metadata.
- ✅ pandas integration:
  - `DatetimeIndex`: serialize and restore with original region, including `freq`.
  - `PeriodIndex`/`TimedeltaIndex`: unchanged.
- ✅ Confirmed backward compatibility: legacy files without region decode without errors.

---

### Tasks Completed for This Version

### ✅ Timezone Region Core
- [x] Encode `datetime` with region, offset, fold
- [x] Decode `datetime` with preference for `ZoneInfo(region)` and fallback
- [x] Handle naïve `datetime` safely
- [x] Accept canonical offset formats (`+HH:MM`, `-HH:MM`)

### ✅ pandas Integration
- [x] `DatetimeIndex`: serialize and restore region + freq
- [x] Ensure round-trip fidelity for Series and DataFrame indexes
- [x] Preserve compatibility with indexes without tz

### ✅ Documentation Updates
- [x] Added notes in `README.md` under **JSON Compatibility** describing TZ metadata
- [x] Updated `SECURITY.md` to clarify controlled use of constructors (`datetime`, pandas)
- [x] Prepared `iana-registration-v2.md` draft reflecting updated semantics

---

### Known Limitations

- Requires IANA TZDB data at runtime for full fidelity; environments without tzdata fall back to fixed offsets.
- No change for `PeriodIndex` and `TimedeltaIndex` (remain without tz support).
- Shared/cyclic references still not supported.
- Binary output and encryption remain pending.
- No built-in support yet for ML-specific tensor types (`torch.Tensor`, `tf.Tensor`, etc.).

---

### Next Steps

The next version will be **0.3.0-alpha**, continuing the roadmap toward extended object graph handling and robust file management. Planned goals:

- 🔐 **Safe Decode Mode**: optional flag to restrict decoding to safe types.
- 📂 **Stream Support**: chunked and line-by-line reading.
- 🌐 **Remote File Access**: fetch and decode directly from HTTP(S).
- ✅ **File Enhancements**: improved metadata, `exists`/`status` checks.
- 🔄 **Export Control**: refine export modes for deterministic behavior.
- 🧪 **Dedicated Testing**: expand coverage of temporal types under TZDB edge cases.
- 📚 **Documentation**: update guides with advanced timezone usage examples.

---

## Versioning Notes

This project follows semantic versioning principles:
- **MAJOR.MINOR.PATCH**
- Pre-release versions are suffixed with `-alpha`, `-beta`, or `-rc`.

For example:
- `0.2.0-alpha`: Added dict keys, hashing, protected/private support.
- `0.2.6-alpha`: Security audit and documentation alignment.
- `0.2.7-alpha`: Timezone region support for exact temporal round-trip.
- `0.3.0-alpha`: Planned support for reference handling and file enhancements.

---

## Feedback and Contribution

This version is considered stable for scenarios requiring precise temporal serialization with timezone fidelity. Feedback and contributions are welcome to refine timezone handling and guide progress toward 1.0.