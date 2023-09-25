"""The primary Attributes of a character are defined here.

These are the innate characterists all characters have.  Unlike skills which are learned, Attributes are intrinsic and
are used to modify skills"""

from abc import ABC
from typing import Literal, TypeAlias

from pydantic import BaseModel

from ares.models.characteristic import Attribute


PhysicalPcAttributes: TypeAlias = Literal[
    "force",  # physical strength
    "speed",  # physical speed
    "dexterity",   # limb coordination (think surgeon or artist)
    "kinesthesia", # whole body agility (think acrobat, dancer, martial artist)
]

MentalPcAttributes: TypeAlias = Literal[
    "wit",         # ability to reason and think
    "creativity",  # creativity and being able to think outside the box
    "insight",     # wisdom and foresight
    "discipline",  # mental fortitude
]


class PrimaryAttribute(Attribute):
    name: PhysicalPcAttributes | MentalPcAttributes

class SecondaryAttribute(Attribute):
    name: Literal["height", "weight"]