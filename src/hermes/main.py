from typing import AsyncGenerator
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from fastapi import FastAPI

from hermes.nodes.project_logging import default_logging
from hermes.connectors.sql_connector.database import init_sql, truncate_sql
from hermes.routers.root import router as root_router
from hermes.routers.health_check import router as health_check_router
from hermes.routers.crud import router as crud_user_router
from hermes.routers.auth import router as auth_router


default_logging()
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    init_sql()
    yield
    # Only used in development because it deletes all the data
    truncate_sql()

app = FastAPI(lifespan=lifespan)
app.include_router(root_router)
app.include_router(health_check_router)
app.include_router(crud_user_router)
app.include_router(auth_router)
