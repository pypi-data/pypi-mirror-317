"""
Wrappers for useful packages, debug tools, etc.
"""

import logging
import warnings
from typing import Any

logger = logging.getLogger(__name__)
__all__ = ["DodgeFolder", "DuckLike"]


class DodgeFolder:
    """
    A container class with dodging capabilities:
    - Dynamically creates new instances for missing attributes.
    - Always stores attribute values as strings.
    - Flattens its structure when iterated over.

    Example:
        dog = DodgeFolder()
        dog.know.v1.host = "s1"
        dog.know.v1.user = "s2"
        dog.cont = "more 10"
        dog_to_save = list(dog)
    """

    def __init__(self):
        self._data = {}

    def __getattr__(self, name):
        if name not in self._data:
            self._data[name] = DodgeFolder()
        return self._data[name]

    def __setattr__(self, name, value):
        if name == "_data":
            super().__setattr__(name, value)
        else:
            self._data[name] = str(value)

    def __iter__(self):
        return iter(self._flatten(self))

    def _flatten(self, obj, parent_key=""):
        items = []
        for key, value in obj._data.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, DodgeFolder):
                items.extend(value._flatten(value, new_key))
            else:
                items.append([f"{new_key}", value])
        return items


class DuckLike:
    """
    See everything as a duck.

    DuckLike represents a collection of attribute names from an instance or class,
    excluding private or protected members (names starting with `_`).

    This class supports "duck subtraction" using the `-` operator, allowing intuitive
    comparison of attribute sets between two DuckLike instances.

    Example:
        A = DuckLike(complex_router)
        B = DuckLike(simple_router)
        diff = A - B
        print(diff)  # Outputs a list of attribute names in A but not in B
    """

    def __init__(self, instance_or_class: Any) -> None:
        # Collect all non-private attribute names
        self.names: list[str] = [
            name for name in dir(instance_or_class) if not name.startswith("_")
        ]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.names!r})"

    def __sub__(self, other: "DuckLike") -> list[str]:
        """
        Perform "duck subtraction" to find names unique to this DuckLike instance.
        """
        if not isinstance(other, DuckLike):
            raise TypeError("Subtraction is only supported between DuckLike instances.")
        return [name for name in self.names if name not in other.names]

    @classmethod
    def from_args(cls, *args):
        """
        Build a DuckLike instance using a list of attribute or method names.
        """
        duck_instance = cls.__new__(cls)  # Create without invoking __init__
        duck_instance.names = [name for name in args if not name.startswith("_")]
        return duck_instance
