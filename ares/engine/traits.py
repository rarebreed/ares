from typing import Protocol


class Trait[T](Protocol):
    name: str  # name of the trait, eg "strength"
    value: T