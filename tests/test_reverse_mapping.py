import typing as t
from itertools import groupby

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
