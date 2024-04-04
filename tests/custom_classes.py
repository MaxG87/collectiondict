import typing as t
from collections import Counter

_KeyT = t.TypeVar("_KeyT", bound=t.Hashable)
_ValueT = t.TypeVar("_ValueT")


class MyCounter(Counter[_ValueT]):
    pass


class MyFrozenset(frozenset[_ValueT]):
    pass


class MyList(list[_ValueT]):
    pass


class MySet(set[_ValueT]):
    pass


class MyTuple(tuple[_ValueT, ...]):
    pass
