
from pathlib import Path
import duckdb as dd
from fastapi import FastAPI
import uvicorn

from ares.models.character.character import Character, arrow_schema, example_character, init_char_pq_path
import pyarrow as pa

app = FastAPI()

# Paths for databases
ares_dir =Path(__file__).parent.parent  

# Create or open the database our service will use
if not Path("ares.db").exists():
    conn = dd.connect("ares.db")
    init_df = conn.read_parquet(f"{init_char_pq_path}")
    conn.execute("CREATE TABLE char_db as SELECT * FROM init_df")
    # conn.register("chats_db", chat_msg_table = conn.read_json(f"{chat_msg_table_path}"))
else:
    conn = dd.connect("ares.db")
    print(conn.sql("SHOW ALL TABLES"))
    print(conn.sql("SELECT * FROM char_db"))
    tbl = conn.table("char_db")


def testing():
    example = example_character()
    schema = arrow_schema()
    tbl = pa.Table.from_pylist([example.model_dump()], schema=schema)
    sql_cmd = f"INSERT INTO char_db SELECT * FROM tbl RETURNING *"
    print(sql_cmd)
    df = conn.sql(sql_cmd)
    print(df)

testing()

# /v1/characters
char_ept = "/v1/characters/"


# Create 
@app.post(char_ept)
async def post_character(char: Character):
    model = char.model_dump()
    print(model)
    schema = arrow_schema()
    tbl = pa.Table.from_pylist([model], schema=schema)
    sql_cmd = f"INSERT INTO char_db SELECT * FROM tbl RETURNING *"
    print(sql_cmd)
    df = conn.sql(sql_cmd)
    print(df)


@app.get(f"{char_ept}/{{uid}}")
async def get_character(uid: str):
    sql_cmd = f"SELECT * FROM char_db WHERE uid = '{uid}'"
    df = conn.sql(sql_cmd)
    batch = df.to_arrow_table()
    data = batch.to_pylist()[0]
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
