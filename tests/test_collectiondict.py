import typing as t
from itertools import groupby

import pytest
from hypothesis import given
from hypothesis import strategies as st

from collectiondict import collectiondict

_KeyT = t.TypeVar("_KeyT", bound=t.Hashable)
_ValueT = t.TypeVar("_ValueT")


@given(
    ref_dict=st.dictionaries(st.integers(), st.integers()),
    clct=st.sampled_from([list, set, frozenset]),
)
def test_dict_to_one_element_collections(
    ref_dict: dict[_KeyT, _ValueT],
    clct: t.Union[
        t.Type[list[_ValueT]], t.Type[set[_ValueT]], t.Type[frozenset[_ValueT]]
    ],
) -> None:
    expected = [(key, clct([val])) for key, val in ref_dict.items()]
    result = list(collectiondict(clct, ref_dict.items()).items())
    assert result == expected


@given(
    stream=st.lists(st.tuples(st.integers(), st.integers())),
)
def test_to_collectiondict_for_lists(stream: list[tuple[_KeyT, _ValueT]]) -> None:
    # This uses a very naive implementation to generate the expected result.
    # The actual implementation will use a slightly more clever implemenation
    # that uses less memory.

    # For some reason, `groupby` reorders elements sometimes. Therefore, the
    # comparision has to be more complicated.

    sorted_pairs = sorted(stream)
    grouped_by_key = groupby(sorted_pairs, lambda tup: tup[0])
    expected = {
        key: [val for _, val in key_and_val] for key, key_and_val in grouped_by_key
    }
    result = collectiondict(list, stream)

    assert result.keys() == expected.keys()
    assert all(isinstance(clct, list) for clct in result.values())
    for key in result:
        result_values = sorted(result[key])
        expected_values = sorted(expected[key])  # type: ignore[type-var]
        assert result_values == expected_values


@given(
    clct_t=st.sampled_from([set, frozenset]),
    stream=st.lists(st.tuples(st.integers(), st.integers())),
)
def test_to_collectiondict_for_reordering_robust_collections(
    clct_t: t.Union[t.Type[set[_ValueT]], t.Type[frozenset[_ValueT]]],
    stream: list[tuple[_KeyT, _ValueT]],
) -> None:
    # This uses a very naive implementation to generate the expected result.
    # The actual implementation will use a slightly more clever implemenation
    # that uses less memory.

    # For some reason, `groupby` reorders elements sometimes. Therefore, the
    # comparision has to be more complicated.

    sorted_pairs = sorted(stream)
    grouped_by_key = groupby(sorted_pairs, lambda tup: tup[0])
    expected = {
        key: {kv[1] for kv in key_and_val} for key, key_and_val in grouped_by_key
    }
    result = collectiondict(clct_t, stream)
    assert all(isinstance(clct, clct_t) for clct in result.values())
    assert result == expected


def test_breaks_for_unhashable_values_with_sets() -> None:
    # These should raise type errors. However, `mypy` does not support that in
    # full generality: https://github.com/python/typeshed/issues/3884.
    # This test exists as a marker and playground.
    stream: list[tuple[int, list[int]]] = [(1234, [1234])]
    with pytest.raises(TypeError):
        collectiondict(set, stream)
    with pytest.raises(TypeError):
        collectiondict(frozenset, stream)
