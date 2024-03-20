import typing as t

_T = t.TypeVar("_T")
_CollectionT = t.Generic[_T]
_KeyT = t.TypeVar("_KeyT", bound=t.Hashable)
_ValueT = t.TypeVar("_ValueT")


def collectiondict(
    clct: t.Type[t.List[_ValueT]], iterable: t.Iterable[t.Tuple[_KeyT, _ValueT]]
) -> dict[_KeyT, t.List[_ValueT]]:
    return {}
