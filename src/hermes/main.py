from dotenv import load_dotenv

from fastapi import FastAPI

from hermes.nodes.project_logging import default_logging
from hermes.routers.root import router as root_router
from hermes.routers.health_check import router as health_check_router
from hermes.routers.crud import router as crud_user_router


default_logging()
load_dotenv()

app = FastAPI()
app.include_router(root_router)
app.include_router(health_check_router)
app.include_router(crud_user_router)
