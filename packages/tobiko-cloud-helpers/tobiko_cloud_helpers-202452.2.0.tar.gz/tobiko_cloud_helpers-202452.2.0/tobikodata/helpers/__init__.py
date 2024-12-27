from __future__ import annotations

import sys
import typing as t
from collections.abc import Collection

T = t.TypeVar("T")


def seq_get(seq: t.Sequence[T], index: int) -> t.Optional[T]:
    """Returns the value in `seq` at position `index`, or `None` if `index` is out of bounds."""
    try:
        return seq[index]
    except IndexError:
        return None


@t.overload
def ensure_list(value: t.Collection[T]) -> t.List[T]: ...


@t.overload
def ensure_list(value: T) -> t.List[T]: ...


def ensure_list(value: t.Union[T, t.Collection[T]]) -> t.List[T]:
    """
    Ensures that a value is a list, otherwise casts or wraps it into one.

    Args:
        value: The value of interest.

    Returns:
        The value cast as a list if it's a list or a tuple, or else the value wrapped in a list.
    """
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)

    return [t.cast(T, value)]


@t.overload
def ensure_collection(value: t.Collection[T]) -> t.Collection[T]: ...


@t.overload
def ensure_collection(value: T) -> t.Collection[T]: ...


def ensure_collection(value: t.Union[T, t.Collection[T]]) -> t.Collection[T]:
    """
    Ensures that a value is a collection (excluding `str` and `bytes`), otherwise wraps it into a list.

    Args:
        value: The value of interest.

    Returns:
        The value if it's a collection, or else the value wrapped in a list.
    """
    if value is None:
        return []

    if isinstance(value, Collection) and not isinstance(value, (str, bytes)):
        return value

    return [t.cast(T, value)]


def first(it: t.Iterable[T]) -> T:
    """Returns the first element from an iterable (useful for sets)."""
    return next(i for i in it)


def major_minor_patch_dev(version: str) -> t.Tuple[int, int, int, int]:
    """Returns a tuple of the major.minor.patch.dev (dev is optional) for a version string (major.minor.patch-devXXX)."""
    version = version.split("+")[0]
    version_parts = version.split(".")
    # Check for legacy major.minor.patch.devXX format
    if len(version_parts) not in (3, 4):
        raise ValueError(f"Invalid version: {version}")
    if len(version_parts) == 4:
        major, minor, patch, dev = version_parts
        dev = dev.replace("dev", "")
    else:
        major, minor, patch = version_parts[0:3]
        dev_info = patch.split("-")
        if len(dev_info) == 1:
            patch, dev = patch, sys.maxsize  # type: ignore
        else:
            patch, dev = dev_info  # type: ignore
            dev = dev.replace("dev", "")  # type: ignore
    return t.cast(
        t.Tuple[int, int, int, int],
        tuple(int(part) for part in [major, minor, patch, dev]),  # type: ignore
    )


def urljoin(*args: str) -> str:
    from urllib.parse import urljoin

    if not args:
        return ""

    if len(args) == 1:
        return args[0]
    base = args[0]
    for part in args[1:]:
        if base:
            base = base.rstrip("/") + "/"
            part = part.lstrip("/")
        base = urljoin(base, part)

    return base
