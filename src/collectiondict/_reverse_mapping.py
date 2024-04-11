import typing as t

from ._collectiondict import collectiondict

_KeyT = t.TypeVar("_KeyT", bound=t.Hashable)
_ValueT = t.TypeVar("_ValueT")
_HashableValueT = t.TypeVar("_HashableValueT", bound=t.Hashable)


@t.overload
def reverse_mapping(  # pragma: nocover
    clct: t.Type[list[_KeyT]], mapping: t.Mapping[_KeyT, _HashableValueT]
) -> dict[_HashableValueT, list[_KeyT]]: ...


@t.overload
def reverse_mapping(  # pragma: nocover
    clct: t.Type[tuple[_KeyT, ...]], mapping: t.Mapping[_KeyT, _HashableValueT]
) -> dict[_HashableValueT, tuple[_KeyT, ...]]: ...


def reverse_mapping(
    clct: t.Union[
        t.Type[list[_KeyT]],
        t.Type[tuple[_KeyT, ...]],
    ],
    mapping: t.Mapping[_KeyT, _HashableValueT],
) -> t.Union[
    dict[_HashableValueT, list[_KeyT]],
    dict[_HashableValueT, tuple[_KeyT, ...]],
]:
    return collectiondict(clct, ((v, k) for k, v in mapping.items()))
