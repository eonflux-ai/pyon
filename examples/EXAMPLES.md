# Examples

Pyon includes a set of examples to demonstrate its capabilities in handling different data types and scenarios.  
These examples are located in the `examples/` directory and provide practical use cases for serialization and deserialization.

---

## Table of Contents

1. [Simple to Use](#1-simple-to-use)
2. [Encoding and Decoding to and from String](#2-encoding-and-decoding-to-and-from-string)
    - [Number Types](#number-types)
    - [Custom Types](#custom-types)
    - [Collection Types](#collection-types)
    - [Mapping Types](#mapping-types)
    - [Pandas and Numpy](#pandas-and-numpy)
    - [File Wrapper](#file-wrapper)
    - [All Types: One by One](#all-types-one-by-one)
    - [All Types: All at Once](#all-types-all-at-once)
3. [Encoding and Decoding to and from File](#3-encoding-and-decoding-to-and-from-file)
    - [File: Collection Types](#file-collection-types)
    - [File: All Types](#file-all-types)
4. [Encoding and Decoding Nested Types](#4-encoding-and-decoding-nested-types)
    - [Nested: Base Types](#nested-base-types)
    - [Nested: Complex Types](#nested-complex-types)
---

## 1. Simple to Use
Pyon is simple to use, offering a straightforward one-liner interface with just four intuitive methods: \
`encode`, `decode`, `to_file`, `from_file`.

```python
import pyon

# 1. Python Data: Classes, Collections, Dataframes, Numpy arrays, etc...
data = {...}

# 2. One line Encode and Decode...
encoded = pyon.encode(data)
decoded = pyon.decode(encoded)

# 3. One line Encode and Decode to and from File...
pyon.to_file(data, "data.pyon")
decoded = pyon.from_file("data.pyon")
```

Whether you're serializing or deserializing Python objects, Pyon makes it effortless and efficient!

## 2. Encoding and Decoding to and from String

### Number Types
**[e01_number_types.py](e01_number_types.py)** \
This example shows pyon encoding and decoding numeric types.

```python
from decimal import Decimal
import pyon

# 1. Test Objects...
example_data = {

    # 1.1 Testing numeric types...
    "int": 42,
    "float": 3.14,
    "complex": 2 + 3j,
    "decimal": Decimal("123.456")

}

# 2. Iterate over the dictionary, encoding and decoding each item...
for key, value in example_data.items():

    # 1.1 Display the type...
    print('\n----------------')
    print(f"Type: {key}\n")

    # 1.2 Perform encoding and decoding...
    encoded = pyon.encode(value)
    decoded = pyon.decode(encoded)

    # 1.3 Print the results...
    print(f"Original: {value}")
    print(f" Decoded: {decoded}")
    print(f" Encoded: {encoded}")
    print('----------------\n')    
```

### Custom Types
**[e02_custom_types.py](e02_custom_types.py)** \
This example shows pyon encoding and decoding custom types.

```python
from dataclasses import dataclass
from enum import Enum
import pyon

# 1. Enum for Testing...
class Color(Enum):
    """
    Enum representing basic cat colors.
    """
    BLACK = 1
    WHITE = 2
    BROWN = 3
    ORANGE = 3

# 2. Test Class...
class Cat:
    """ Class representing a cat. """
    # 1.1 ...
    def __init__(self, name, color):
        self.name = name
        self.color = color

# 3. Dataclass for Testing...
@dataclass
class Person:
    """ Dataclass representing a person. """
    name: str
    age: int

# 4. Test Objects...
example_data = {

    # 1.1 Testing enumeration...
    "enum": Color.BLACK,

    # 1.2 Testing custom classes...
    "class": Cat("Malbec", Color.ORANGE),
    "dataclass": Person("John", 30)

}

# 5. Iterate over the dictionary, encoding and decoding each item...
for key, value in example_data.items():

    # 1.1 Display the type...
    print('\n----------------')
    print(f"Type: {key}\n")

    # 1.2 Perform encoding and decoding...
    encoded = pyon.encode(value)
    decoded = pyon.decode(encoded)

    # 1.3 Print the results...
    print(f"Original: {value}")
    print(f" Decoded: {decoded}")
    print(f" Encoded: {encoded}")
    print('----------------\n')        
```

### Collection Types
**[e03_collection_types.py](e03_collection_types.py)** \
This example shows pyon encoding and decoding for collection types.

```python
from collections import deque, namedtuple
from enum import Enum
import pyon

# 1. Enum for Testing...
class Color(Enum):
    """ Enum representing basic colors. """
    RED = 1
    GREEN = 2
    BLUE = 3

# 2. Namedtuple for Testing...
XData = namedtuple('XData', ['field1', 'field2'])

# 3. Test Objects...
example_data = {

    # 1.1 Testing collection types...
    "list": [1, 2, 3, 4],
    "set": {Color.RED, Color.GREEN, Color.BLUE},
    "frozenset": frozenset([5.1, 6.2, 7.3]),
    "deque": deque(["a", "b", "c"]),
    "tuple": (1, "two", 3.0),
    "namedtuple": XData("value1", 123)

}

# 4. Iterate over the dictionary, encoding and decoding each item...
for key, value in example_data.items():

    # 1.1 Display the type...
    print('\n----------------')
    print(f"Type: {key}\n")

    # 1.2 Perform encoding and decoding...
    encoded = pyon.encode(value)
    decoded = pyon.decode(encoded)

    # 1.3 Print the results...
    print(f"Original: {value}")
    print(f" Decoded: {decoded}")
    print(f" Encoded: {encoded}")
    print('----------------\n')        
```

### Mapping Types
**[e04_mapping_types.py](e04_mapping_types.py)** \
This example shows pyon encoding and decoding for mapping types.

```python
from dataclasses import dataclass
from collections import defaultdict, ChainMap, Counter
from enum import Enum
import pyon

# 1. Enum for Testing...
class Color(Enum):
    """ Enum representing basic colors. """
    RED = 1
    GREEN = 2
    BLUE = 3

# 2. Dataclass for Testing...
@dataclass
class Person:
    """ Dataclass representing a person. """
    name: str
    age: int

# 3. Test Objects...
example_data = {

    # 1.1 Testing mapping types...
    "dict": {
        "x": Person("John", 10),
        "y": Person("Paul", 20),
        "z": Person("Michael", 30),
    },
    "defaultdict": defaultdict(int, a=1, b=2),
    "chainmap": ChainMap(
        {"r": Color.RED, "g": Color.GREEN, "b": Color.BLUE},
        {"w": Person("William", 20), "c": Person("Charles", 25)}
    ),
    "counter": Counter({"x": 10, "y": 20})

}

# 4. Iterate over the dictionary, encoding and decoding each item...
for key, value in example_data.items():

    # 1.1 Display the type...
    print('\n----------------')
    print(f"Type: {key}\n")

    # 1.2 Perform encoding and decoding...
    encoded = pyon.encode(value)
    decoded = pyon.decode(encoded)

    # 1.3 Print the results...
    print(f"Original: {value}")
    print(f" Decoded: {decoded}")
    print(f" Encoded: {encoded}")
    print('----------------\n')
```

### Pandas and Numpy
**[e05_pandas_numpy.py](e05_pandas_numpy.py)** \
This example shows pyon encoding and decoding for pandas dataframe and numpy arrays.

```python
import pandas as pd
import numpy as np
import pyon

# 1. Test Objects...
example_data = {

    # 1.1 Numpy Array...
    "np.ndarray": np.array([[1, 2, 3], [4, 5, 6]]),

    # 1.2 Pandas Dataframe...
    "pd.DataFrame": pd.DataFrame(
        {"col1": [1, 2], "col2": ["a", "b"]}
    )

}

# 2. Iterate over the dictionary, encoding and decoding each item...
for key, value in example_data.items():

    # 1.1 Display the type...
    print('\n----------------')
    print(f"Type: {key}\n")

    # 1.2 Perform encoding and decoding...
    encoded = pyon.encode(value)
    decoded = pyon.decode(encoded)

    # 1.3 Print the results...
    print(f"Original:\n{value}\n")
    print(f" Decoded:\n{decoded}\n")
    print(f" Encoded: {encoded}")
    print('----------------\n')       
```

### File Wrapper
**[e06_file_wrapper.py](e06_file_wrapper.py)** \
This example shows pyon encoding and decoding for files.

```python
import pyon
from pyon import File

FILE_PATH = "./data/img.jpg"

# 1. Test Objects...
example_data = {

    # 1.1 File Reference: Does not fetch the data. Just saves filesystem references.
    "File-1": File(FILE_PATH),

    # 1.2 File Data: Fetchs the data and encodes it.
    "File-2": File(FILE_PATH, fetch=True)

}

# 2. Iterate over the dictionary, encoding and decoding each item...
for key, value in example_data.items():

    # 1.1 Display the type...
    print('\n----------------')
    print(f"Type: {key}\n")

    # 1.2 Perform encoding and decoding...
    encoded = pyon.encode(value)
    decoded = pyon.decode(encoded)

    # 1.3 Print the results...
    print(f"Original: {value}")
    print(f" Decoded: {decoded}")
    print(f" Encoded: {encoded}")
    print('----------------\n')
```

### All Types: One by One
**[e07_data_types_one.py](e07_data_types_one.py)**  
This example showcases Pyon's ability to encode and decode a wide variety of Python data types. Each type is tested individually to ensure proper serialization and deserialization. The types covered include:

   - **Basic types**: `str`, `int`, `float`, `NoneType`.
   - **Boolean types**: `True`, `False`.
   - **Numeric types**: `complex`, `Decimal`.
   - **Enumerations**: `enum`.
   - **Date and time types**: `date`, `datetime`, `time`.
   - **Collection types**: `list`, `set`, `frozenset`, `deque`, `tuple`, `namedtuple`.
   - **Binary types**: `bytes`, `bitarray`, `bytearray`.
   - **Mapping types**: `dict`, `defaultdict`, `ChainMap`, `Counter`.
   - **Specialized types**: `uuid`, `np.ndarray`, `pd.DataFrame`.
   - **Custom classes**: `dataclass`, user-defined classes.
   - **File representation**: Using `File` object for file handling.

```python
# 1. Data...
example_data = {

    # 1.1 Testing basic data types...
    "str": "Hello, World!",
    "int": 42,
    "float": 3.14,
    "NoneType": None,

    # 1.2 Testing boolean types...
    "bool (False)": False,
    "bool (True)": True,

    # 1.3 Testing numeric types...
    "complex": 2 + 3j,
    "decimal": Decimal("123.456"),    

    # 1.4 Testing enumeration...
    "enum": Color.RED,

    # 1.5 Testing date and time types...
    "date": date.today(),
    "datetime": datetime.now(),
    "time": time(14, 30, 15),

    # 1.6 Testing collection types...
    "list": [1, 2, 3, 4],
    "set": {1, 2, 3},
    "frozenset": frozenset([1, 2, 3]),
    "deque": deque(["a", "b", "c"]),
    "tuple": (1, "two", 3.0),
    "namedtuple": XData("value1", 123),

    # 1.7 Testing binary types...
    "bytes": b"hello",
    "bitarray": bitarray.bitarray("1101"),
    "bytearray": bytearray([65, 66, 67]),

    # 1.8 Testing mapping types...
    "dict": {"a": 1, "b": 2, "c": 3},
    "defaultdict": defaultdict(int, a=1, b=2),
    "chainmap": ChainMap({"key1": "value1"}, {"key2": "value2"}),
    "counter": Counter({"x": 10, "y": 20}),

    # 1.9 Testing specialized types...
    "uuid": uuid4(),
    "np.ndarray": np.array([[1, 2, 3], [4, 5, 6]]),
    "pd.DataFrame": pd.DataFrame(
        {"col1": [1, 2], "col2": ["a", "b"]}
    ),

    # 1.10 Testing custom classes...
    "class": Cat("Malbec", 6),
    "dataclass": Person("John", 30),

    # 1.11 Testing files...
    "File": File(
        "D:/Desenv/Source/Python/src/metrics/Pyon/tests/data/img.jpg"
    )

}
```

This example demonstrates how Pyon can handle both simple and complex nested data structures while maintaining readability and reliability.

### All Types: All at Once
**[e08_data_types_all.py](e08_data_types_all.py)**  
This example demonstrates encoding all supported types simultaneously. \
This example verifies that the encoded and decoded data maintain integrity by comparing the hash values of the original and deserialized data. It demonstrates Pyon's robustness in handling diverse data structures effectively.

---

## 3. Encoding and Decoding to and from File

### File: Collection Types
**[e09_file_collection.py](e09_file_collection.py)** \
This example shows pyon encoding and decoding collections using File output.

```python
from collections import deque, namedtuple
from enum import Enum
import os
import pyon

# 1. Enum for Testing...
class Color(Enum):
    """ Enum representing basic colors. """
    RED = 1
    GREEN = 2
    BLUE = 3

# 2. Namedtuple for Testing...
XData = namedtuple('XData', ['field1', 'field2'])

# 3. Test Objects...
example_data = {

    # 1.1 Testing collection types...
    "list": [1, 2, 3, 4],
    "set": {Color.RED, Color.GREEN, Color.BLUE},
    "frozenset": frozenset([5.1, 6.2, 7.3]),
    "deque": deque(["a", "b", "c"]),
    "tuple": (1, "two", 3.0),
    "namedtuple": XData("value1", 123)

}

FILE = "./data.pyon"

# 4. Encodes to File and Decodes from File...
pyon.to_file(example_data, FILE)
decoded = pyon.from_file(FILE)

# 5. Iterate over the dictionary, encoding and decoding each item...
for key, value in example_data.items():

    # 1.1 Display the type...
    print('\n----------------')
    print(f"Type: {key}\n")

    # 1.2 Print the results...
    print(f"Original: {value}")
    print(f" Decoded: {decoded[key]}")
    print('----------------\n')

# 6. Excludes temp file...
if os.path.exists(FILE):
    os.remove(FILE)
```

### File: All Types
**[e10_file_data_types.py](e10_file_data_types.py)**  
This example demonstrates encoding all supported types simultaneously using File output.

---

## 4. Encoding and Decoding Nested Types

Pyon excels at handling recursive data structures seamlessly. Whether your data includes deeply nested dictionaries, lists, or custom objects, Pyon ensures accurate serialization and deserialization across all levels.

### Nested: Base Types
**[e11_nested_base_types.py](e11_nested_base_types.py)** \
This example shows pyon encoding and decoding nested base types.

```python
import pyon

# 1. Test Objects...
example_data = {

    # 1.1 Tuple, Set...
    "tuple-set-1": ({"abc", "def"}),
    "tuple-set-2": ({1, 2}),
    "tuple-set-3": ({1.1, 2.2}),
    "tuple-set-4": ({True, False}),

    # 1.2 List, Tuple, Set...
    "list-tuple-set-1": [({"abc", "def"}), ({1, 2}), ({True, False})],
    "list-tuple-set-2": [({"ghi", "jkl"}), ({3.0, 4.0}), ({True, False})],

    # 1.3 Dict, List, Tuple, Set...
    "dict-list-tuple-set": {
        "a": [({"abc", "def"}), ({1, 2}), ({True, False})],
        "b": [({"ghi", "jkl"}), ({3.0, 4.0}), ({True, False})],
    },

    # 1.4 Dict, Dict, Dict, List, Tuple, Set...
    "dict-dict-dict-list-tuple-set": {
        "top": {
            "one": {"a": [({"abc", "def"}), ({1, 2}), ({True, False})]},
            "two": {"b": [({"ghi", "jkl"}), ({3.0, 4.0}), ({True, False})]}
        },
        "down": {
            "three": {"c": [({"mno", "pqr"}), ({3, 4}), ({True, False})]},
            "four": {"d": [({"stu", "vwx"}), ({5.0, 6.0}), ({True, False})]}
        }
    }

}

# 2. Iterate over the dictionary, encoding and decoding each item...
for key, value in example_data.items():

    # 1.1 Display the type...
    print('\n----------------')
    print(f"Type: {key}\n")

    # 1.2 Perform encoding and decoding...
    encoded = pyon.encode(value)
    decoded = pyon.decode(encoded)

    # 1.3 Print the results...
    print(f"Original: {value}")
    print(f" Decoded: {decoded}")
    print('----------------\n')
```

### Nested: Complex Types
**[e12_nested_complex_types.py](e12_nested_complex_types.py)** \
This example shows pyon encoding and decoding nested complex types.

```python
from dataclasses import dataclass
from enum import Enum
import pyon

# 1. Enum for Testing...
class Color(Enum):
    """ Enum representing basic colors. """
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4
    ORANGE = 5
    BROWN = 6
    BLACK = 7
    WHITE = 8

# 2. Dataclass for Testing...
@dataclass
class Person:
    """ Dataclass representing a person. """

    # 1.1 ...
    name: str
    age: int
    height: float
    is_student: bool
    hobbies: tuple
    favorite_numbers: set
    favorite_colors: list
    pets: dict

    # 1.2 ...
    def __repr__(self):
        return f"({Person}):({self.name}):({self.age})"

    # 1.3 ...
    def __hash__(self):
        return hash(self.__repr__())

# 3. Test Class...
class Pet:
    """ Class representing a Pet. """

    # 1.1 ...
    def __init__(self, p_type, name, color):
        self.p_type = p_type
        self.name = name
        self.color = color

    # 1.2 Repr output...
    def __repr__(self):
        return f"({Pet}):({self.p_type}):({self.name}):({self.color})"

# 4. Persons...
p1 = Person(
    "Alice", 30, 1.65, False, ("reading", "paiting"), {1, 9}, [Color.RED, Color.YELLOW],
    {
        "cat": [Pet("cat", "Malbeck", Color.ORANGE), Pet("cat", "Yuki", Color.WHITE)],
        "dog": [Pet("dog", "Lync", Color.WHITE), Pet("dog", "Nemo", Color.BROWN)],
    }
)

p2 = Person(
    "Bob", 25, 1.80, True, ("gaming", "cycling"), {7, 13}, [Color.BLACK, Color.WHITE],
    {
        "dog": [Pet("dog", "Zync", Color.BLACK)]
    }
)

p3 = Person(
    "Charlie", 40, 1.75, False, ("hiking", "photography"), {1, 13}, [Color.BLACK, Color.WHITE],
    {"dog": None, "cat": None}
)

# 4. Test Objects...
example_data = {

    # 1.1 Tuple, Set...
    "tuple-list": ({p1, p2}),

    # 1.2 List, Tuple, Set...
    "list-tuple-set": [({p1, p2}), ({p3})],

    # 1.3 Dict, List, Tuple, Set...
    "dict-list-tuple-set": {
        "a": [({p1}), ({p2})],
        "b": [({p3})]
    },

    # 1.4 Dict, Dict, Dict, List, Tuple, Set...
    "dict-dict-dict-list-tuple-set": {
        "top": {
            "one": {"a": [({p1, p2})]}
        },
        "down": {
            "three": {"b": [({p3})]}
        }
    }

}

# 5. Iterate over the dictionary, encoding and decoding each item...
for key, value in example_data.items():

    # 1.1 Display the type...
    print('\n----------------')
    print(f"Type: {key}\n")

    # 1.2 Perform encoding and decoding...
    encoded = pyon.encode(value)
    decoded = pyon.decode(encoded)

    # 1.3 Print the results...
    print(f"Original: {value}")
    print(f" Decoded: {decoded}")
    print('----------------\n')
```

Pyon's recursive encoding and decoding provide a reliable way to handle arbitrarily complex structures, making it ideal for advanced use cases like configuration management, AI/ML pipelines, or hierarchical datasets.


---
<br>

**Thank you for using Pyon!** 

If you have any questions or suggestions, feel free to open an issue or start a discussion on our GitHub repository.
