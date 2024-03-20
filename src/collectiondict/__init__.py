import typing as t

_T = t.TypeVar("_T")
_CollectionT = t.Generic[_T]
_KeyT = t.TypeVar("_KeyT", bound=t.Hashable)
_ValueT = t.TypeVar("_ValueT")


@t.overload
def collectiondict(  # pragma: nocover
    clct: t.Type[list[_ValueT]], iterable: t.Iterable[tuple[_KeyT, _ValueT]]
) -> dict[_KeyT, list[_ValueT]]: ...


@t.overload
def collectiondict(  # pragma: nocover
    clct: t.Type[set[_ValueT]], iterable: t.Iterable[tuple[_KeyT, _ValueT]]
) -> dict[_KeyT, set[_ValueT]]: ...


def collectiondict(
    clct: t.Type[list[_ValueT]] | t.Type[set[_ValueT]],
    iterable: t.Iterable[tuple[_KeyT, _ValueT]],
) -> dict[_KeyT, list[_ValueT]] | dict[_KeyT, set[_ValueT]]:

    if issubclass(clct, list):
        return _collectiondict_for_lists(clct, iterable)
    elif issubclass(clct, set):
        return _collectiondict_for_sets(clct, iterable)
    else:
        t.assert_never(clct)


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
    clct: t.Type[set[_ValueT]],
    iterable: t.Iterable[tuple[_KeyT, _ValueT]],
) -> dict[_KeyT, set[_ValueT]]:
    ret: dict[_KeyT, set[_ValueT]] = {}
    for key, val in iterable:
        try:
            ret[key].add(val)
        except KeyError:
            ret[key] = {val}
    return ret
