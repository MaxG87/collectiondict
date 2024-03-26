import sys
import typing as t

from collectiondict import collectiondict

if sys.version_info >= (3, 11):
    from typing import assert_type
else:
    _T = t.TypeVar("_T")

    def assert_type(val: _T, type_: t.Any) -> _T:
        return val


def test_type_inference_for_list() -> None:
    test_data = [("a", 1), ("b", 2), ("c", 3)]
    clct = t.cast(t.Type[list[int]], list)
    result = collectiondict(clct, iterable=test_data)
    assert_type(test_data, list[tuple[str, int]])
    assert_type(result, dict[str, list[int]])
