from abc import ABC

from pydantic import BaseModel


class Attribute(ABC, BaseModel):
    name: str
    value: int
