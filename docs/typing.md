# Annotations

Pyslvs sources and API are following PEP 484 (Type Hints) rules.

There are some things still need to declare
since Python is a weak typing language and
some developer are not familiar with static typing rules.

In a "duck typing" or "static duck typing"
(just like [Rust](https://www.rust-lang.org/))
language, the "operators" in code block needs to defined.
For example, "a" must be "addable" in following function:

```python
def add(a, b):
    return a + b
```

So a "prototype" will represented as:

```python
from typing import Protocol

class Add(Protocol):
    def __add__(self, other):
        ...  # No implementation here (and shouldn't be)

def add(a: Add, b):
    return a + b
```

And the same works are acting on "copyable", "callable", "appendable" objects.
They are calling specific methods or magic methods
and the methods should be implemented.

We use a lot of "protocols" instead of traditional object orientation design (like below),
since Python is a dynamic duck typing language.

```python
from typing import List

def iterate_over(it: List[int]) -> None:
    """How about other containers?"""
    for k in it:
        ...
```

```python
from typing import Iterable

def iterate_over(it: Iterable[int]) -> None:
    """An "iterable" object with __iter__ magic method."""
    for k in it:
        ...
```

We need to mark up the usage of the object prototypes, instead of its implementation.

In Python, a lot of "prototypes" are already defined in "typing" module.
See PEP 484 or MyPy documentation to get more information.

## Standard Containers

The annotation usages of standard containers in Pyslvs.

| | Mutable | Immutable | Implementation |
|:---:|:-------:|:---------:|:--------------:|
| Chain like | `List[T]` | `Sequence[T]`, `Tuple[T, ...]` | `list`, `tuple` |
| Mapping like | `Dict[K, V]` | `Mapping[K, V]` | `dict` |
| Set like | `Set[T]` | `FrozenSet[T]` | `set`, `frozenset` |

Although mutable containers has a `copy` method, but when they are marked as
immutable, please use the builtin `copy.copy` function instead.

```python
from typing import Mapping
from copy import copy

old_dict: Mapping[int, int] = {}
new_dict = copy(old_dict)
```
