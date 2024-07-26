import os
import logging

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
logger = logging.getLogger(__name__)

POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_DB = os.environ['POSTGRES_DB']
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres/{POSTGRES_DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# TODO: Use alembic to sync declarative code change with underlying sql tables
def init_sql() -> None:
    logger.info('Initialising SQL schemas')
    Base.metadata.create_all(bind=engine)

def truncate_sql() -> None:
    logger.info('Truncating SQL database to zero')
    Base.metadata.drop_all(bind=engine)
