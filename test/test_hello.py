from dataclasses import dataclass


@dataclass
class t:
    a: int
    b: int


def test_example():
    assert 1 + 1 == 2


def test_typed():
    a: str | int = 1
    b: str | int = 2
    assert a + b == 3


def test_dataclass():
    a = t(1, 2)
    b = t(1, 2)
    assert a == b
