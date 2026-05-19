# --------------------------------------------------------------------------------------------- #
""" Pyon: Export Policy Annotations """
# --------------------------------------------------------------------------------------------- #

from typing import Any, Callable, TypeVar

# --------------------------------------------------------------------------------------------- #

T = TypeVar("T", bound=type)

# --------------------------------------------------------------------------------------------- #


def export(private: bool = False, protected: bool = False) -> Callable[[T], T]:
    """
    Decorator to define export flags for Pyon serialization.

    Args:
        private (bool): Export private attributes (e.g., __attr) if True.
        protected (bool): Export protected attributes (e.g., _attr) if True.
    """

    # 1. Wrapper that sets export attributes...
    def wrapper(cls: T) -> T:

        # 1.1 Set export flags...
        setattr(cls, "__pyon_export_private__", private)
        setattr(cls, "__pyon_export_protected__", protected)

        # 1.2 Return class unchanged...
        return cls

    # 2. Return wrapper...
    return wrapper


# --------------------------------------------------------------------------------------------- #


def get_export_flags(obj: Any) -> tuple[bool, bool]:
    """
    Retrieves the export policy for a given object's class.

    Args:
        obj (Any): The object whose export flags are to be read.

    Returns:
        Tuple[bool, bool]: A tuple (private_flag, protected_flag).

    Raises:
        ValueError: If flags are present but not of type bool.
    """

    # 1. Class reference...
    cls = obj.__class__

    # 2. Get attributes with fallback...
    private = getattr(cls, '__pyon_export_private__', False)
    protected = getattr(cls, '__pyon_export_protected__', False)

    # 3. Validate types...
    if not isinstance(private, bool) or not isinstance(protected, bool):
        raise ValueError(f"Invalid Pyon export flags in class '{cls.__name__}'")

    # 4. Return flags...
    return private, protected


# --------------------------------------------------------------------------------------------- #
