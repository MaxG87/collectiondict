import typing as t
from itertools import groupby

from hypothesis import given
from hypothesis import strategies as st

from collectiondict import collectiondict

_KeyT = t.TypeVar("_KeyT", bound=t.Hashable)
_ValueT = t.TypeVar("_ValueT")


@given(
    ref_dict=st.dictionaries(st.integers(), st.integers()),
    clct=st.sampled_from([list]),
)
def test_dict_to_one_element_collections(
    ref_dict: dict[_KeyT, _ValueT], clct: t.Type[list[_ValueT]]
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
    for key in result:
        result_values = sorted(result[key])
        expected_values = sorted(expected[key])  # type: ignore[type-var]
        assert result_values == expected_values
