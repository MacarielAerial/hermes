import logging
from typing import Iterable
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from hermes.connectors.sql_connector.database import engine
from hermes.connectors.schema import ItemCreate, OrderCreate, UserCreate
from hermes.nodes.crud import (
    _create_item,
    _create_user,
    _delete_item,
    _delete_user,
    _get_item,
    _get_user,
    _get_user_by_email,
    _get_users,
    _create_order
)
from hermes.nodes.schema import (
    CreateItemResponse,
    CreateOrderResponse,
    CreateUserResponse,
    DeleteItemResponse,
    DeleteUserResponse,
    GetItemResponse,
    GetUserResponse,
    GetUsersResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter()


def get_session() -> Iterable[Session]:
    with Session(engine) as session:
        yield session


@router.post("/create-user", status_code=status.HTTP_201_CREATED)
def create_user(
    user_create: UserCreate, session: Session = Depends(get_session)
) -> CreateUserResponse:
    user = _get_user_by_email(session, user_create.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with the following data already exists: {user.model_dump()}",
        )

    user = _create_user(session, user_create=user_create)

    return CreateUserResponse(
        message=f"The following user is created:\n{user.model_dump()}"
    )


@router.get("/get-user/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: UUID, session: Session = Depends(get_session)) -> GetUserResponse:
    user = _get_user(session, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return GetUserResponse(message=f"Got the following user:\n{user.model_dump()}")


@router.get("/get-users", status_code=status.HTTP_200_OK)
def get_users(session: Session = Depends(get_session)) -> GetUsersResponse:
    users = _get_users(session)

    return GetUsersResponse(
        message=f"Here are all users in the database:\n{[user.model_dump() for user in users]}"
    )


@router.post("/delete-user/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
    user_id: UUID, session: Session = Depends(get_session)
) -> DeleteUserResponse:
    # Identify the user first
    user = _get_user(session, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # User still exists in memory but is gone in the database
    user = _delete_user(session, user)

    return DeleteUserResponse(
        message=f"Deleted the following user:\n{user.model_dump()}"
    )


@router.post("/create-item/{user_id}", status_code=status.HTTP_201_CREATED)
def create_item(
    user_id: UUID, item_create: ItemCreate, session: Session = Depends(get_session)
) -> CreateItemResponse:
    # Check the user exists
    user = _get_user(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with the following ID: {user_id}",
        )

    # Attach the user to the item
    item_create.user_id = user.id

    # Create the item
    item = _create_item(session, item_create)

    return CreateItemResponse(
        message=f"The following item is created:\n{item.model_dump()} for the following user:\n{item.user.model_dump()}"
    )


@router.get("/get-item/{item_id}", status_code=status.HTTP_200_OK)
def get_item(item_id: UUID, session: Session = Depends(get_session)) -> GetItemResponse:
    # Check the item exists
    item = _get_item(session, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return GetItemResponse(message=f"Got the following item:\n{item.model_dump()}")


@router.post("/delete-item/{item_id}", status_code=status.HTTP_200_OK)
def delete_item(
    item_id: UUID, session: Session = Depends(get_session)
) -> DeleteItemResponse:
    # Identify the item first
    item = _get_item(session, item_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Item still exists in memory but is gone in the database
    item = _delete_item(session, item)

    return DeleteItemResponse(
        message=f"Deleted the following item:\n{item.model_dump()}"
    )

@router.post("/create-order/{user_id}", status_code=status.HTTP_201_CREATED)
def create_order(
    user_id: UUID, order_create: OrderCreate, session: Session = Depends(get_session)
) -> CreateOrderResponse:
    # Check the user exists
    user = _get_user(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with the following ID: {user_id}",
        )

    # Attach the user to the order
    order_create.user_id = user.id

    # Create the order
    order = _create_order(session, order_create)

    return CreateOrderResponse(
        message=f"The following order is created:\n{order.model_dump()} for the following user:\n{order.user.model_dump()}"
    )
