
from pathlib import Path
from random import randint, random
from uuid import uuid4

import pyarrow as pa
from pydantic import BaseModel
init_char_pq_path = Path(__file__).parent.parent.parent / "db/characters/character_init.parquet"

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

    @staticmethod
    def random_character() -> "Character":
        pool = die(4, 6)
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
                "1HSword": sum(best_of(list(pool()), 3)),
                "Climbing": sum(best_of(list(pool()), 3))
            }
        )

    @staticmethod
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

def init_parquet():
    """Used to create an initial seed
    """
    example = Character.random_character()
    tbl = pa.Table.from_pylist([example.model_dump()], schema=Character.arrow_schema())
    import pyarrow.parquet as pq
    pq.write_table(tbl, f"{init_char_pq_path}")


if __name__ == "__main__":
    init_parquet()