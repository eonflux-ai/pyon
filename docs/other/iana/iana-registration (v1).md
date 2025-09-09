# Media Type Registration: application/vnd.pyon+json

This document contains the complete registration information submitted for the custom media type `application/vnd.pyon+json`, used by the Pyon serialization format.

---

## General Information

**Type Name:** `application`

**Subtype Name:** `vnd.pyon+json`

**Required Parameters:**
```
N/A
```

**Optional Parameters:**
```
N/A
```

**Encoding Considerations:**
```
binary
```
**Notes:**
```
The format is based on JSON but may include base64-encoded binary content. Encoding is declared as "binary" to accommodate line lengths and characters beyond the 7-bit ASCII range.
```

**Security Considerations:**
```
This media type does not contain active or executable content. Pyon files consist of JSON-compatible structures with additional metadata used to reconstruct Python objects. During decoding, Pyon performs no code execution and does not invoke constructors, methods, or evaluation routines. Object attributes are restored via direct assignment only.

The information stored in Pyon files may contain sensitive data depending on the use case, but the format itself does not provide encryption or integrity verification. Implementers are expected to use external mechanisms such as TLS for transport security, or file-level encryption if confidentiality is required.

The media type is based on JSON, and inherits the general security considerations applicable to `application/json`, including risks associated with large or deeply nested documents.

Pyon does not use compression, containers, or references to external resources.
```

**Interoperability Considerations:**
```
Pyon files are based on JSON syntax but are not fully interoperable with standard JSON parsers. Although the structure conforms to JSON, the semantics depend on type annotations (such as `__type__`) and conventions specific to the Pyon format.

Generic JSON tools may parse the structure but will not correctly interpret or reconstruct the original Python objects without awareness of Pyon-specific metadata. As such, Pyon should not be used as a drop-in replacement for `application/json` in systems expecting pure JSON.

Compatibility is best ensured by using libraries that support the Pyon specification.
```

**Published Specification:**
```
The format is described in the public README available at:
https://github.com/eonflux-ai/pyon/blob/main/README.md
```

**Applications That Use This Media Type:**
```
The Pyon media type is used by the Pyon library (https://github.com/eonflux-ai/pyon) to serialize and deserialize Python objects, including complex types such as NumPy arrays, pandas DataFrames, and custom classes. It is intended for applications that require structured and type-preserving serialization for use in machine learning, data pipelines, configuration management, and object persistence.
```

**Fragment Identifier Considerations:**
```
No fragment identification mechanism is defined for this media type.
```

**Restrictions on Usage:**
```
There are no known restrictions on usage.
```

**Provisional Registration:**
```
No
```

---

## Additional Information

**Deprecated alias names:**
```
N/A
```

**Magic numbers:**
```
N/A
```

**File extension(s):**
```
.pyon
```

**Macintosh file type codes:**
```
N/A
```

**Object Identifiers or OIDs:**
```
N/A
```

**Intended Usage:**
```
COMMON
```

**Additional Information:**
```
The media type is intended for general-purpose use in applications that require structured and type-preserving serialization of Python objects. It is not tied to a specific protocol or platform.
```

---

## Contact Information

**Contact Name:** Eduardo Rodrigues  
**Contact Email:** eduardo@eonflux.ai  
**Author/Change Controller:** Eduardo Rodrigues (eonflux.ai)

**Other Information & Comments:**
```
This media type is defined and maintained by the Pyon project, developed by Eduardo Rodrigues under the eonflux.ai organization. The format can be used in data science and machine learning pipelines for object serialization. Public source code and documentation are available at https://github.com/eonflux-ai/pyon.
```
