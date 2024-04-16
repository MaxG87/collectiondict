import typing as t
from collections import Counter

from ._collectiondict import collectiondict

_KeyT = t.TypeVar("_KeyT", bound=t.Hashable)
_HashableValueT = t.TypeVar("_HashableValueT", bound=t.Hashable)


# TODO Currently, the type annotations are not perfect. Due to the limited
# nature of Python's type annotations, it is not possible to specify the correct
# return type for the custom classes. Thus, custom classes are supported but the
# return type is not inferred to be the parent class.


@t.overload
def reverse_mapping(  # pragma: nocover
    clct: t.Type[Counter[_KeyT]],
    mapping: t.Mapping[_KeyT, _HashableValueT],
) -> dict[_HashableValueT, Counter[_KeyT]]: ...


@t.overload
def reverse_mapping(  # pragma: nocover
    clct: t.Type[frozenset[_KeyT]], mapping: t.Mapping[_KeyT, _HashableValueT]
) -> dict[_HashableValueT, frozenset[_KeyT]]: ...


@t.overload
def reverse_mapping(  # pragma: nocover
    clct: t.Type[list[_KeyT]], mapping: t.Mapping[_KeyT, _HashableValueT]
) -> dict[_HashableValueT, list[_KeyT]]: ...


@t.overload
def reverse_mapping(  # pragma: nocover
    clct: t.Type[tuple[_KeyT, ...]], mapping: t.Mapping[_KeyT, _HashableValueT]
) -> dict[_HashableValueT, tuple[_KeyT, ...]]: ...


@t.overload
def reverse_mapping(  # pragma: nocover
    clct: t.Type[set[_KeyT]], mapping: t.Mapping[_KeyT, _HashableValueT]
) -> dict[_HashableValueT, set[_KeyT]]: ...


def reverse_mapping(
    clct: t.Union[
        t.Type[Counter[_KeyT]],
        t.Type[frozenset[_KeyT]],
        t.Type[list[_KeyT]],
        t.Type[set[_KeyT]],
        t.Type[tuple[_KeyT, ...]],
    ],
    mapping: t.Mapping[_KeyT, _HashableValueT],
) -> t.Union[
    dict[_HashableValueT, Counter[_KeyT]],
    dict[_HashableValueT, frozenset[_KeyT]],
    dict[_HashableValueT, list[_KeyT]],
    dict[_HashableValueT, set[_KeyT]],
    dict[_HashableValueT, tuple[_KeyT, ...]],
]:
    """
    Reverse mapping to map from values to keys

    Given a mapping, e.g. a dictionary, from keys to values, this function
    reverses the mapping so it maps from values to keys. The keys are collected
    in a collection specified by `clct`.

    The supported collections are fixed. Only the built-in collections
    `Counter`, `frozenset`, `list`, `set`, and `tuple` as well as their
    subclasses are supported. If an unsupported collection is passed, an
    exception is raised. However, `mypy` will warn about it.

    Due to the limits of Pythons type annotations, it is not possible to
    specify the correct return type for the custom classes. Thus, custom
    classes are supported but the return type is not inferred to be the parent
    class.

    In order to have the best type inference, it is recommended to **cast**
    `clct` to specify the value type. Passing a specialised collection class is
    **not** supported currently. The examples show how to use a cast.

    Examples:
    ---------
    Simple usage using `set`:
    >>> reverse_mapping(set, {1: "foobar", 2: "blablubb", 3: "foobar"})
    {'foobar': {1, 3}, 'blablubb': {2}}

    Usage using `frozenset` and a cast to have the best type inference:
    >>> import typing as t
    >>> clct = t.cast(t.Type[frozenset[int]], frozenset)
    >>> reverse_mapping(clct, {1: "foobar", 2: "blablubb", 3: "foobar"})
    {'foobar': frozenset({1, 3}), 'blablubb': frozenset({2})}
    """

    return collectiondict(clct, ((v, k) for k, v in mapping.items()))
