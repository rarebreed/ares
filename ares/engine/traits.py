
from typing import Protocol

from ares.engine.operations import Numeric


class Trait[T: Numeric](Protocol):
    name: str  # name of the trait, eg "strength"
    value: T

    def cost(self) -> float:
        """Determine the cost of purchasing the Trait's value

        Returns
        -------
        float
            the cost or worth of the Trait's value
        """
        ...


class Attribute:
    ...
