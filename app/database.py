import databases
import sqlalchemy
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

vehicles_table = sqlalchemy.Table(
    "vehicles",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("marca", sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column("localidad", sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column("aspirante", sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)