import typing as t

_T = t.TypeVar("_T")
_CollectionT = t.Generic[_T]
_KeyT = t.TypeVar("_KeyT", bound=t.Hashable)
_ValueT = t.TypeVar("_ValueT")


def collectiondict(
    clct: t.Type[list[_ValueT]], iterable: t.Iterable[tuple[_KeyT, _ValueT]]
) -> dict[_KeyT, list[_ValueT]]:
    ret: dict[_KeyT, list[_ValueT]] = {}
    for key, val in iterable:
        try:
            ret[key].append(val)
        except KeyError:
            ret[key] = [val]
    return ret
