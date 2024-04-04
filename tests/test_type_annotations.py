import sys
import typing as t
from collections import Counter

from collectiondict import collectiondict
from tests import custom_classes as cc

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


def test_type_inference_for_set() -> None:
    test_data = [("a", 1), ("b", 2), ("c", 3)]
    clct = t.cast(t.Type[set[int]], set)
    result = collectiondict(clct, iterable=test_data)
    assert_type(test_data, list[tuple[str, int]])
    assert_type(result, dict[str, set[int]])


def test_type_inference_for_tuple() -> None:
    test_data = [("a", 1), ("b", 2), ("c", 3)]
    clct = t.cast(t.Type[tuple[int, ...]], tuple)
    result = collectiondict(clct, iterable=test_data)
    assert_type(test_data, list[tuple[str, int]])
    assert_type(result, dict[str, tuple[int, ...]])


def test_type_inference_for_frozenset() -> None:
    test_data = [("a", 1), ("b", 2), ("c", 3)]
    clct = t.cast(t.Type[frozenset[int]], frozenset)
    result = collectiondict(clct, iterable=test_data)
    assert_type(test_data, list[tuple[str, int]])
    assert_type(result, dict[str, frozenset[int]])


def test_type_inference_for_Counter() -> None:
    test_data = [("a", 1), ("b", 2), ("c", 3)]
    clct = t.cast(t.Type[Counter[int]], Counter)
    result = collectiondict(clct, iterable=test_data)
    assert_type(test_data, list[tuple[str, int]])
    assert_type(result, dict[str, Counter[int]])


def test_type_inference_for_MyList() -> None:
    test_data = [("a", 1), ("b", 2), ("c", 3)]
    clct = t.cast(t.Type[cc.MyList[int]], cc.MyList)
    result = collectiondict(clct, iterable=test_data)
    assert_type(test_data, list[tuple[str, int]])
    assert_type(result, dict[str, list[int]])


def test_type_inference_for_MySet() -> None:
    test_data = [("a", 1), ("b", 2), ("c", 3)]
    clct = t.cast(t.Type[cc.MySet[int]], cc.MySet)
    result = collectiondict(clct, iterable=test_data)
    assert_type(test_data, list[tuple[str, int]])
    assert_type(result, dict[str, set[int]])


def test_type_inference_for_MyTuple() -> None:
    test_data = [("a", 1), ("b", 2), ("c", 3)]
    clct = t.cast(t.Type[cc.MyTuple[int]], cc.MyTuple)
    result = collectiondict(clct, iterable=test_data)
    assert_type(test_data, list[tuple[str, int]])
    assert_type(result, dict[str, tuple[int, ...]])


def test_type_inference_for_MyFrozenset() -> None:
    test_data = [("a", 1), ("b", 2), ("c", 3)]
    clct = t.cast(t.Type[cc.MyFrozenset[int]], cc.MyFrozenset)
    result = collectiondict(clct, iterable=test_data)
    assert_type(test_data, list[tuple[str, int]])
    assert_type(result, dict[str, frozenset[int]])


def test_type_inference_for_MyCounter() -> None:
    test_data = [("a", 1), ("b", 2), ("c", 3)]
    clct = t.cast(t.Type[cc.MyCounter[int]], cc.MyCounter)
    result = collectiondict(clct, iterable=test_data)
    assert_type(test_data, list[tuple[str, int]])
    assert_type(result, dict[str, Counter[int]])
