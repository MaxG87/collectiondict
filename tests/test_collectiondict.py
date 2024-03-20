import typing as t

from collectiondict import collectiondict


def test_basic_functioning() -> None:
    no_values: t.List[t.Tuple[str, int]] = []
    result = collectiondict(list, no_values)
    assert result == {}
