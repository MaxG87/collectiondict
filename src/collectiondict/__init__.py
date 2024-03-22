import typing as t

_T = t.TypeVar("_T")
_CollectionT = t.Generic[_T]
_KeyT = t.TypeVar("_KeyT", bound=t.Hashable)
_ValueT = t.TypeVar("_ValueT")
_HashableValueT = t.TypeVar("_HashableValueT", bound=t.Hashable)


@t.overload
def collectiondict(  # pragma: nocover
    clct: t.Type[list[_ValueT]], iterable: t.Iterable[tuple[_KeyT, _ValueT]]
) -> dict[_KeyT, list[_ValueT]]: ...


@t.overload
def collectiondict(  # pragma: nocover
    clct: t.Type[set[_HashableValueT]],
    iterable: t.Iterable[tuple[_KeyT, _HashableValueT]],
) -> dict[_KeyT, set[_HashableValueT]]: ...


@t.overload
def collectiondict(  # pragma: nocover
    clct: t.Type[frozenset[_HashableValueT]],
    iterable: t.Iterable[tuple[_KeyT, _HashableValueT]],
) -> dict[_KeyT, frozenset[_HashableValueT]]: ...


@t.overload
def collectiondict(  # pragma: nocover
    clct: t.Type[tuple[_ValueT, ...]], iterable: t.Iterable[tuple[_KeyT, _ValueT]]
) -> dict[_KeyT, tuple[_ValueT, ...]]: ...


def collectiondict(
    clct: t.Union[
        t.Type[list[_ValueT]],
        t.Type[set[_ValueT]],
        t.Type[frozenset[_ValueT]],
        t.Type[tuple[_ValueT, ...]],
    ],
    iterable: t.Iterable[tuple[_KeyT, _ValueT]],
) -> t.Union[
    dict[_KeyT, list[_ValueT]],
    dict[_KeyT, set[_ValueT]],
    dict[_KeyT, frozenset[_ValueT]],
    dict[_KeyT, tuple[_ValueT, ...]],
]:
    """
    Create dictionaries that collect values into collections

    Given any stream of key-value tuples, this function creates a
    multi-dictionary which maps all values to the corresponding key. Thus,
    `collectiondict(clct, stream)` is similar to `dict(stream)` but does not
    discard values.

    The implementation tries to be memory efficient and performant. Therefore,
    it is possible to use it on extremely large streams, as long as the end
    result fits in memory. Thus, if a list of the stream consumes more than
    half of the available memory, `collectiondict` can still be used.
    Furthermore, for deduplicating collections, e.g. `set`, the stream could
    exceed available memory, as long as the key-value pairs do not. One of the
    examples covers this scenario.

    The supported collections are fixed. Only the built-in collections
    `frozenset`, `list`, `set`, and `tuple` as well as their subclasses are
    supported. If a unsupported collection is passed, an exception is raised.
    However, `mypy` will warn about it.


    Examples:
    ---------
    Simple usage using `set`:
    >>> collectiondict(set, [("a", 1), ("b", 2), ("a", 3)])
    {'a': {1, 3}, 'b': {2}}

    Scenario that might exceed memory:
    >>> N=1000  # could be humongous, e.g. 10**20
    >>> collectiondict(set, [(str(n%2), n%3) for n in range(N)])
    {'0': {0, 1, 2}, '1': {0, 1, 2}}
    """

    if issubclass(clct, list):
        return _collectiondict_for_lists(clct, iterable)
    elif issubclass(clct, set):
        return _collectiondict_for_sets(clct, iterable)
    elif issubclass(clct, frozenset):
        return _collectiondict_for_frozensets(clct, iterable)
    elif issubclass(clct, tuple):
        return _collectiondict_for_tuple(clct, iterable)
    else:
        # Due to compatiblity with Python 3.9 and 3.10, we cannot use
        # t.assert_never here. That would be preferable, though.
        raise AssertionError("Invalid collection type passed!")  # type: ignore[unreachable, unused-ignore]


def _collectiondict_for_lists(
    clct: t.Type[list[_ValueT]],
    iterable: t.Iterable[tuple[_KeyT, _ValueT]],
) -> dict[_KeyT, list[_ValueT]]:
    ret: dict[_KeyT, list[_ValueT]] = {}
    for key, val in iterable:
        try:
            ret[key].append(val)
        except KeyError:
            ret[key] = clct([val])
    return ret


def _collectiondict_for_sets(
    clct: t.Type[set[_HashableValueT]],
    iterable: t.Iterable[tuple[_KeyT, _HashableValueT]],
) -> dict[_KeyT, set[_HashableValueT]]:
    ret: dict[_KeyT, set[_HashableValueT]] = {}
    for key, val in iterable:
        try:
            ret[key].add(val)
        except KeyError:
            ret[key] = clct([val])
    return ret


def _collectiondict_for_frozensets(
    clct: t.Type[frozenset[_HashableValueT]],
    iterable: t.Iterable[tuple[_KeyT, _HashableValueT]],
) -> dict[_KeyT, frozenset[_HashableValueT]]:
    # TODO: One could cosider to create collectiondict of `set` first and to
    # transform all sets to frozensets later on. That would require some
    # justification, e.g. benchmarks.
    ret: dict[_KeyT, frozenset[_HashableValueT]] = {}
    for key, val in iterable:
        try:
            fs = ret[key]
            if val not in fs:
                new_fs = fs.union([val])
                ret[key] = new_fs if clct == frozenset else clct(new_fs)
        except KeyError:
            ret[key] = clct([val])
    return ret


def _collectiondict_for_tuple(
    clct: t.Type[tuple[_ValueT, ...]],
    iterable: t.Iterable[tuple[_KeyT, _ValueT]],
) -> dict[_KeyT, tuple[_ValueT, ...]]:
    # TODO: One could cosider to create collectiondict of `list` first and to
    # transform all lists to tuples later on. That would require some
    # justification, e.g. benchmarks.
    ret: dict[_KeyT, tuple[_ValueT, ...]] = {}
    for key, val in iterable:
        try:
            tup = ret[key]
            ret[key] = clct([*tup, val])
        except KeyError:
            ret[key] = clct([val])
    return ret
