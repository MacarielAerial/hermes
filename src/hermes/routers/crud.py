from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from hermes.nodes.schema import RegisterRequest, RegisterResponse
from hermes.nodes.crud import create_user, get_user_by_email, get_users
from hermes.connectors.sql_connector import models
from hermes.connectors.sql_connector import schemas
from hermes.connectors.sql_connector.database import engine, SessionLocal


# TODO: Use alembic to sync declarative code change with underlying sql tables
# models.Base.metadata.drop_all(engine)
models.Base.metadata.create_all(bind=engine)
def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
router = APIRouter()

@router.post("/register/", status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> RegisterResponse:
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db=db, user=user)

    return RegisterResponse(message=f'User {user.id} has been created')



@router.get("/users/", status_code=status.HTTP_200_OK)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)

    return users
