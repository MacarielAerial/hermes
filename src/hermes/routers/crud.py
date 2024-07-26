from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from hermes.nodes.schema import ItemsResponse, RegisterResponse, UserItemResponse, UsersResponse, UserResponse
from hermes.nodes.crud import create_user, get_user_by_email, get_users, get_user, create_user_item, get_items
from hermes.connectors.sql_connector import schemas
from hermes.connectors.sql_connector.database import SessionLocal


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
router = APIRouter()

@router.post("/register/", status_code=status.HTTP_201_CREATED)
def register_user(user_create: schemas.UserCreate, db: Session = Depends(get_db)) -> RegisterResponse:
    db_user = get_user_by_email(db, email=user_create.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = create_user(db=db, user_create=user_create)

    return RegisterResponse(message='User has been created', db_user=db_user)

@router.get("/users/", status_code=status.HTTP_200_OK)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> UsersResponse:
    db_users = get_users(db, skip=skip, limit=limit)

    return UsersResponse(message=f'Found {len(db_users)} user/users', db_users=db_users)

@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def read_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(message='Found user', db_user=db_user)

@router.post("/users/{user_id}/items/", status_code=status.HTTP_201_CREATED)
def create_item_for_user(
    user_id: int, item_create: schemas.ItemCreate, db: Session = Depends(get_db)
) -> UserItemResponse:
    db_user = get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} does not exist.")
    db_item = create_user_item(db=db, item_create=item_create, user_id=user_id)
    
    return UserItemResponse(message='Created an item for a user', db_item=db_item)

@router.get("/items/", status_code=status.HTTP_200_OK)
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> ItemsResponse:
    db_items = get_items(db, skip=skip, limit=limit)

    return ItemsResponse(message=f'Found {len(db_items)} items', db_items=db_items)
