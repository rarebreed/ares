from abc import abstractmethod
from dataclasses import dataclass
from enum import IntEnum
import operator
from typing import Any, Callable, Protocol, overload


class Numeric(Protocol):

    @abstractmethod
    def __add__(self, other: int | float) -> "Numeric":
        raise NotImplementedError

    @abstractmethod
    def __sub__(self, other: int | float) -> "Numeric":
        raise NotImplementedError

    @abstractmethod
    def __mul__(self, other: int) -> "Numeric":
        raise NotImplementedError


class RangedAttribute(IntEnum):
    Weak = 0
    Poor = 1
    Average = 2
    Good = 3
    Outstanding = 4
    Excellent = 5


@dataclass
class Attribute(Numeric):
    value: RangedAttribute

    def _op(self, op: Callable[[Any, Any], Any], other: int | float):
        match other:
            case int(i):
                result: int = op(self.value.value, i)
                return Attribute(value=RangedAttribute(check(result)))
            case float(f):
                res: float = op(self.value.value, f)
                return Attribute(value=RangedAttribute(int(check(res))))

    def __add__(self, other: int | float):
        return self._op(operator.add, other)

    def __sub__(self, other: int | float):
        return self._op(operator.sub, other)

    def __mul__(self, other: int | float):
        return self._op(operator.mul, other)


@overload
def check(res: int) -> int:
    return check(res)


@overload
def check(res: float) -> float:
    return check(res)


def check(res: int | float) -> int | float:
    if res < 0.0:
        res = 0 if isinstance(res, int) else 0.0
    if res > 5.0:
        res = 5 if isinstance(res, int) else 5.0
    return res
