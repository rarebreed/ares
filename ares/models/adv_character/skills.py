

from ares.models.adv_character.attribute import PrimaryAttribute
from ares.models.characteristic import Attribute


class Skill(Attribute):
    related_attrs: list[PrimaryAttribute]
    dependent_skills: list["Skill"]
    dependent_attrs: list[PrimaryAttribute]