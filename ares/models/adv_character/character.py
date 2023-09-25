
from abc import ABC
from typing import Literal, TypeAlias
from pydantic import BaseModel

from ares.models.characteristic import Attribute

class Character(BaseModel):
    attributes: list[Attribute]
