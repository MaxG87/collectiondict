import typing as t
from collections import Counter, deque
from itertools import groupby

import pytest
from hypothesis import given
from hypothesis import strategies as st

from collectiondict import reverse_multimapping
from tests import custom_classes as cc
from tests import hypothesis_utils as hu


def valid_mappings() -> st.SearchStrategy[dict[int, list[int]]]:
    # We take the modulo 13 to provoke reuse of values. This will force the
    # implementation to create collections with multiple keys correctly.
    return st.dictionaries(st.integers(), st.lists(st.integers().map(lambda x: x % 13)))


@given(mapping=valid_mappings(), clct=hu.valid_ordered_collections())
def test_reverse_multimapping_for_ordered_collections(
    mapping: dict[int, list[int]],
    clct: t.Union[
        t.Type[cc.MyList[int]],
        t.Type[cc.MyTuple[int]],
        t.Type[list[int]],
        t.Type[tuple[int, ...]],
    ],
) -> None:
    result = reverse_multimapping(clct, mapping)
    grouped = groupby(
        sorted(
            ((key, val) for key, values in mapping.items() for val in values),
            key=lambda x: x[1],
        ),
        lambda x: x[1],
    )

    expected = {}
    for val, values in grouped:
        expected[val] = Counter(k for k, _ in values)

    assert expected.keys() == result.keys()
    for key, val in expected.items():
        result_ctr = Counter(result[key])
        assert isinstance(result[key], clct)
        assert val == result_ctr


@given(mapping=valid_mappings(), clct=hu.valid_hashing_collections())
def test_reverse_multimapping_for_reordering_robust_collections(
    mapping: dict[int, list[int]],
    clct: t.Union[
        t.Type[Counter[int]],
        t.Type[cc.MyCounter[int]],
        t.Type[cc.MyFrozenset[int]],
        t.Type[cc.MySet[int]],
        t.Type[frozenset[int]],
        t.Type[set[int]],
    ],
) -> None:
    result = reverse_multimapping(clct, mapping)
    grouped = groupby(
        sorted(
            ((key, val) for key, values in mapping.items() for val in values),
            key=lambda x: x[1],
        ),
        lambda x: x[1],
    )
    expected = {}
    for val, values in grouped:
        expected[val] = clct(k for k, _ in values)
    assert result == expected


@given(
    mapping=valid_mappings(),
    invalid_clct=st.sampled_from([dict, deque]),
)
def test_breaks_for_invalid_collections(
    mapping: dict[int, list[int]], invalid_clct: t.Type[t.Any]
) -> None:
    with pytest.raises(AssertionError):
        reverse_multimapping(invalid_clct, mapping)


@given(
    mapping=valid_mappings(),
    invalid_clct=hu.generic_aliases(),
)
def test_breaks_for_generic_aliases(
    mapping: dict[int, list[int]], invalid_clct: t.Type[t.Any]
) -> None:
    with pytest.raises((AssertionError, TypeError)):
        reverse_multimapping(invalid_clct, mapping)


def test_breaks_for_unhashable_values() -> None:
    mapping = {1234: [[1234]]}
    with pytest.raises(TypeError):
        reverse_multimapping(set, mapping)  # type: ignore[arg-type, type-var]
    with pytest.raises(TypeError):
        reverse_multimapping(frozenset, mapping)  # type: ignore[arg-type, type-var]
    with pytest.raises(TypeError):
        reverse_multimapping(cc.MySet, mapping)  # type: ignore[arg-type, type-var]
    with pytest.raises(TypeError):
        reverse_multimapping(cc.MyFrozenset, mapping)  # type: ignore[arg-type, type-var]


@given(
    clct_t=hu.valid_hashing_collections().filter(
        lambda clct_t: not issubclass(clct_t, Counter)
    ),
    mapping=valid_mappings(),
)
def test_roundtrip_with_reordering_robust_collections(
    clct_t: t.Union[
        t.Type[cc.MyFrozenset[t.Any]],
        t.Type[cc.MySet[t.Any]],
        t.Type[frozenset[t.Any]],
        t.Type[set[t.Any]],
    ],
    mapping: dict[int, list[int]],
) -> None:
    start = reverse_multimapping(clct_t, mapping)
    reversed_ = reverse_multimapping(clct_t, start)
    roundtriped = reverse_multimapping(clct_t, reversed_)
    assert start == roundtriped
