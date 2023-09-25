
from pathlib import Path
import duckdb as dd
from duckdb import DuckDBPyConnection
from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn

from ares.models.character.character import Character, init_char_pq_path
import pyarrow as pa

app = FastAPI()

# Paths for databases
ares_dir =Path(__file__).parent.parent

# Create or open the database our service will use
def init_db(db_name: str = "ares.db", test=True) -> DuckDBPyConnection:
    if not Path(db_name).exists():
        conn = dd.connect(db_name)
        init_df = conn.read_parquet(f"{init_char_pq_path}")
        conn.execute("CREATE TABLE char_db as SELECT * FROM init_df")
    else:
        conn = dd.connect(db_name)
        print(conn.sql("SHOW ALL TABLES"))
        print(conn.sql("SELECT * FROM char_db"))


    def new_record():
        example = Character.random_character()
        schema = Character.arrow_schema()
        tbl = pa.Table.from_pylist([example.model_dump()], schema=schema)
        sql_cmd = f"INSERT INTO char_db SELECT * FROM tbl RETURNING *"
        print(sql_cmd)
        df = conn.sql(sql_cmd)
        print(df)

    if test:
        new_record()
    return conn

conn = init_db(test=False)

# /v1/characters
char_ept = "/v1/characters/"

@app.get(f"{char_ept}parquet")
async def get_parquet() -> FileResponse:
    df = conn.sql("SELECT * FROM char_db")
    pq_path = Path("parquet/saved.parquet")
    if pq_path.exists():
        pq_path.unlink()
    pq_path.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet("parquet/saved.parquet", compression="snappy")
    return FileResponse(pq_path)


# Create 
@app.post(char_ept)
async def post_character(char: Character) -> Character:
    model = char.model_dump()
    print(model)
    tbl = pa.Table.from_pylist([model], schema=Character.arrow_schema())
    sql_cmd = f"INSERT INTO char_db SELECT * FROM tbl RETURNING *"
    df = conn.sql(sql_cmd)
    print(df)
    return char


@app.get(f"{char_ept}{{uid}}")
async def get_character(uid: str) -> Character:
    # FIXME: SQL injection.
    sql_cmd = f"SELECT * FROM char_db WHERE uid = '{uid}'"
    df = conn.sql(sql_cmd)
    batch = df.to_arrow_table()
    data = batch.to_pylist()[0]
    # Due to pyarrow being a column oriented data type, it will be [("1HSword", 10)] instead of {"1HSword": 10}
    data["skills"] = {name: lvl for name, lvl in data["skills"]}
    char = Character.model_validate(data)
    return char


@app.get(char_ept)
async def get_characters() -> list[Character]:
    df = conn.sql("SELECT * FROM char_db")
    batch = df.to_arrow_table()
    data = batch.to_pylist()
    chars: list[Character] = []
    for d in data:
        d["skills"] = {name: lvl for name, lvl in d["skills"]}
        chars.append(Character.model_validate(d))
    return chars

if __name__ == "__main__":
    uvicorn.run(app, host ="0.0.0.0", port=8000)
