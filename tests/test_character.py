
import httpx
from ares.models.character.character import Character


def test():
    example = Character.random_character()
    char = Character.model_validate(example)
    resp = httpx.post("http://127.0.0.1:8000/v1/characters/", json=char.model_dump())
    print(resp)
    print(resp.content)

def test_list():
    resp = httpx.get("http://127.0.0.1:8000/v1/characters/")
    print(resp.json())