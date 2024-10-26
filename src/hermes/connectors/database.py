import logging
import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()
logger = logging.getLogger(__name__)

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_DB = os.environ["POSTGRES_DB"]
SQL_DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres/{POSTGRES_DB}"
)

engine = create_engine(SQL_DATABASE_URL)


# TODO: Use alembic to sync declarative code change with underlying sql tables
def init_sql() -> None:
    logger.info("Initialising SQL schemas")
    SQLModel.metadata.create_all(bind=engine)


def truncate_sql() -> None:
    logger.info("Truncating SQL database to zero")
    SQLModel.metadata.drop_all(bind=engine)
