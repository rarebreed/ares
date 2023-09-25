
import httpx
from ares.models.character.character import Character, example_character


def test():
    example = example_character()
    char = Character.model_validate(example)
    resp = httpx.post("http://127.0.0.1:8000/v1/characters/", json=char.model_dump())
    print(resp)
    print(resp.content)