import typing as t
from collections import Counter, deque
from itertools import groupby

import pytest
from hypothesis import given
from hypothesis import strategies as st

from collectiondict import reverse_mapping
from tests import custom_classes as cc
from tests import hypothesis_utils as hu


def valid_mappings() -> st.SearchStrategy[dict[int, int]]:
    return st.dictionaries(st.integers(), st.integers())


@given(mapping=valid_mappings(), clct=hu.valid_ordered_collections())
def test_reverse_mapping_for_ordered_collections(
    mapping: dict[int, int],
    clct: t.Union[
        t.Type[cc.MyList[int]],
        t.Type[cc.MyTuple[int]],
        t.Type[list[int]],
        t.Type[tuple[int, ...]],
    ],
) -> None:
    result = reverse_mapping(clct, mapping)
    grouped = groupby(sorted(mapping.items(), key=lambda x: x[1]), key=lambda x: x[1])
    expected = {}
    for key, values in grouped:
        expected[key] = clct(key for key, _ in values)
    assert result == expected


@given(mapping=valid_mappings(), clct=hu.valid_hashing_collections())
def test_reverse_mapping_for_reordering_robust_collections(
    mapping: dict[int, int],
    clct: t.Union[
        t.Type[Counter[int]],
        t.Type[cc.MyCounter[int]],
        t.Type[cc.MyFrozenset[int]],
        t.Type[cc.MySet[int]],
        t.Type[frozenset[int]],
        t.Type[set[int]],
    ],
) -> None:
    result = reverse_mapping(clct, mapping)
    grouped = groupby(sorted(mapping.items(), key=lambda x: x[1]), key=lambda x: x[1])
    expected = {}
    for key, values in grouped:
        expected[key] = clct(key for key, _ in values)
    assert result == expected


@given(
    mapping=valid_mappings(),
    invalid_clct=st.sampled_from([dict, list[int], deque]),
)
def test_breaks_for_invalid_collections(
    mapping: dict[int, int], invalid_clct: t.Type[t.Any]
) -> None:
    with pytest.raises(AssertionError):
        reverse_mapping(invalid_clct, mapping)


def test_breaks_for_unhashable_values() -> None:
    mapping = {1234: [1234]}
    with pytest.raises(TypeError):
        reverse_mapping(set, mapping)  # type: ignore[arg-type, type-var]
    with pytest.raises(TypeError):
        reverse_mapping(frozenset, mapping)  # type: ignore[arg-type, type-var]
    with pytest.raises(TypeError):
        reverse_mapping(cc.MySet, mapping)  # type: ignore[arg-type, type-var]
    with pytest.raises(TypeError):
        reverse_mapping(cc.MyFrozenset, mapping)  # type: ignore[arg-type, type-var]
