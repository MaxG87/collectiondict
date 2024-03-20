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


def collectiondict(
    clct: t.Union[
        t.Type[list[_ValueT]], t.Type[set[_ValueT]], t.Type[frozenset[_ValueT]]
    ],
    iterable: t.Iterable[tuple[_KeyT, _ValueT]],
) -> t.Union[
    dict[_KeyT, list[_ValueT]],
    dict[_KeyT, set[_ValueT]],
    dict[_KeyT, frozenset[_ValueT]],
]:
    if issubclass(clct, list):
        return _collectiondict_for_lists(clct, iterable)
    elif issubclass(clct, set):
        return _collectiondict_for_sets(clct, iterable)
    elif issubclass(clct, frozenset):
        return _collectiondict_for_frozensets(clct, iterable)
    else:
        # Due to compatiblity with Python 3.9 and 3.10, we cannot use
        # t.assert_never here. That would be preferable, though.
        raise AssertionError("unreachable")  # type: ignore[unreachable, unused-ignore]


def _collectiondict_for_lists(
    clct: t.Type[list[_ValueT]],
    iterable: t.Iterable[tuple[_KeyT, _ValueT]],
) -> dict[_KeyT, list[_ValueT]]:
    ret: dict[_KeyT, list[_ValueT]] = {}
    for key, val in iterable:
        try:
            ret[key].append(val)
        except KeyError:
            ret[key] = [val]
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
            ret[key] = {val}
    return ret


def _collectiondict_for_frozensets(
    clct: t.Type[frozenset[_HashableValueT]],
    iterable: t.Iterable[tuple[_KeyT, _HashableValueT]],
) -> dict[_KeyT, frozenset[_HashableValueT]]:
    ret: dict[_KeyT, frozenset[_HashableValueT]] = {}
    for key, val in iterable:
        try:
            fs = ret[key]
            ret[key] = fs.union([val])
        except KeyError:
            ret[key] = frozenset([val])
    return ret
