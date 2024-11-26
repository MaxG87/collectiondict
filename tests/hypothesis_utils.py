import typing as t
from collections import Counter

from hypothesis import strategies as st

from tests import custom_classes as cc

_KeyT = t.TypeVar("_KeyT", bound=t.Hashable)
_ValueT = t.TypeVar("_ValueT")


def valid_streams() -> st.SearchStrategy[list[tuple[_KeyT, _ValueT]]]:
    return st.lists(st.tuples(st.integers(), st.integers()))


def valid_collections() -> st.SearchStrategy[t.Type[t.Any]]:
    return st.sampled_from(
        [
            list,
            set,
            frozenset,
            tuple,
            Counter,
            cc.MyCounter,
            cc.MyFrozenset,
            cc.MyList,
            cc.MySet,
            cc.MyTuple,
        ]
    )


def valid_ordered_collections() -> st.SearchStrategy[t.Type[t.Any]]:
    return st.sampled_from([list, tuple, cc.MyList, cc.MyTuple])


def valid_hashing_collections() -> st.SearchStrategy[t.Type[t.Any]]:
    return st.sampled_from(
        [set, frozenset, cc.MyFrozenset, cc.MySet, cc.MyCounter, Counter]
    )


def generic_aliases() -> st.SearchStrategy[t.Type[t.Any]]:
    return st.sampled_from(
        [
            list[bool],
            list[int],
            list[str],
            set[bool],
            set[float],
            set[int],
            tuple[bool, ...],
            tuple[int, ...],
            tuple[str, ...],
        ]
    )
