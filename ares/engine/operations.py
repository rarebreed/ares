
from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Final, Literal, Protocol, TypeAlias


class Numerical(Protocol):
    value: "Numerical"

    @abstractmethod
    def __add__(self, other: int | float, /) -> "Numerical":
        ...

    # @abstractmethod
    # def __sub__(self, other: "Numerical", /) -> "Numerical":
    #     ...
    
    # @abstractmethod
    # def __mul__(self, other: "Numerical", /) -> "Numerical":
    #     ...
    
    # @abstractmethod
    # def __gt__(self, other: "Numerical") -> bool:
    #     ...


Ratings: TypeAlias = Literal["Weak", "Poor", "Average", "Good", "Superb", "Excellent"]

@dataclass
class Range:
    value: Ratings
    mapping: ClassVar[list[tuple[Ratings, int]]] = [
        ("Weak", 0),
        ("Poor", 1),
        ("Average", 2),
        ("Good", 2),
        ("Superb", 3),
        ("Excellent", 4)
    ]

    def __add__(self, other: int | float) -> "Range":
        res = self.mapping[self.value] + other
    
def check_add(rhs: Numerical, x: int):
    return rhs + x