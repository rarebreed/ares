
from pathlib import Path
from random import randint, random
from typing import Iterable
from uuid import uuid4

import pyarrow as pa
from pydantic import BaseModel

init_char_db_path = Path(__file__).parent.parent.parent / "db/characters/character_init.json"
init_char_pq_path = Path(__file__).parent.parent.parent / "db/characters/character_init.parquet"

def die(num: int, size: int = 20):
    def pool():
        for i in range(num):
            yield randint(1, size)
    return pool

def best_of(pool: list[int], amount: int):
    pool_size = len(pool)
    if amount > pool_size:
        amount = pool_size
    start_from = pool_size - amount
    return sorted(pool)[start_from:]

class Character(BaseModel):
    uid: str
    player: str
    player_id: str
    force: int
    speed: int
    kinesthesia: int
    wit: int
    insight: int
    discipline: int
    height: float
    weight: float
    skills: dict[str, int]


def example_character() -> "Character":
    pool = die(3, 6)
    return Character(
        uid=str(uuid4()),
        player="Sean Toner",
        player_id=str(uuid4()),
        force=sum(best_of(list(pool()), 3)),
        speed=sum(best_of(list(pool()), 3)),
        kinesthesia=sum(best_of(list(pool()), 3)),
        wit=sum(best_of(list(pool()), 3)),
        insight=sum(best_of(list(pool()), 3)),
        discipline=sum(best_of(list(pool()), 3)),
        height=50.0 + random() * 50,
        weight=60 + random() * 40,
        skills={
            "1HSword": sum(best_of(list(pool()), 3))
        }
    )

def save_json(char: Character, db_path: Path | None = None):
    if db_path is None:
        db_path = init_char_db_path
    with open(db_path, "wa") as json_f:
        json_f.write(char.model_dump_json() + "\n")


def arrow_schema():
    return pa.schema([
        ("uid", pa.string()),
        ('player', pa.string()),
        ("player_id", pa.string()),
        ("force", pa.int64()),
        ("speed", pa.int64()),
        ("kinesthesia", pa.int64()),
        ("wit", pa.int64()),
        ("insight", pa.int64()),
        ("discipline", pa.int64()),
        ("height", pa.float64()),
        ("weight", pa.float64()),
        ("skills", pa.map_(pa.string(), pa.int64()))
    ])

def init_json():
    example = example_character()
    if init_char_db_path.exists():
        print(f"{init_char_db_path}")
    with open(init_char_db_path, "w") as json_f:
        json_f.write(example.model_dump_json() + "\n")

def init_parquet():
    example = example_character()
    tbl = pa.Table.from_pylist([example.model_dump()], schema=arrow_schema())
    import pyarrow.parquet as pq
    pq.write_table(tbl, f"{init_char_pq_path}")


if __name__ == "__main__":
    init_parquet()