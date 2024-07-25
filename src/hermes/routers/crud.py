from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from hermes.nodes.schema import RegisterRequest, RegisterResponse, UserItemsResponse, UsersResponse, UserResponse
from hermes.nodes.crud import create_user, get_user_by_email, get_users, get_user, create_user_item
from hermes.connectors.sql_connector import models
from hermes.connectors.sql_connector import schemas
from hermes.connectors.sql_connector.database import engine, SessionLocal


# TODO: Use alembic to sync declarative code change with underlying sql tables
models.Base.metadata.drop_all(engine)
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
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> UsersResponse:
    users = get_users(db, skip=skip, limit=limit)

    return UsersResponse(message=f'Returned list of users:\n{users}')

@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def read_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(message=f'Found user {db_user}')

@router.post("/users/{user_id}/items/", status_code=status.HTTP_200_OK)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
) -> UserItemsResponse:
    db_user = get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} does not exist.")
    item = create_user_item(db=db, item=item, user_id=user_id)

    return UserItemsResponse(message=f'Item {item.id} has been created')
