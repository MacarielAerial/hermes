from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI

from hermes.connectors.sql_connector.database import init_sql, truncate_sql
from hermes.nodes.project_logging import default_logging
from hermes.routers.crud import router as crud_router
from hermes.routers.health_check import router as health_check_router
from hermes.routers.root import router as root_router

load_dotenv()
default_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    init_sql()
    yield
    # Only used in development because it deletes all the data
    truncate_sql()


app = FastAPI(lifespan=lifespan)
app.include_router(root_router)
app.include_router(health_check_router)
app.include_router(crud_router)
