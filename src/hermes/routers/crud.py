import logging
from typing import Iterable, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from hermes.connectors.database import engine
from hermes.connectors.schema import ItemCreate, BuyOrderCreate, ItemPublic, SellOrderCreate, UserCreate, UserPublic
from hermes.nodes.crud import (
    _get_item_type,
    _create_item,
    _get_item,
    _delete_item,
    _create_user,
    _get_user,
    _get_user_by_email,
    _get_users,
    _delete_user,
    _create_buy_order,
    _get_buy_order,
    _delete_buy_order,
    _create_sell_order,
    _get_sell_order,
    _delete_sell_order
)
from hermes.nodes.schema import (
    CreateOrderResponse,
    DeleteOrderResponse,
    GetOrderResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter()


def get_session() -> Iterable[Session]:
    with Session(engine) as session:
        yield session


@router.post("/create-user", status_code=status.HTTP_201_CREATED)
def create_user(
    user_create: UserCreate, session: Session = Depends(get_session)
) -> UserPublic:
    user = _get_user_by_email(session, user_create.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with the following data already exists: {user.model_dump()}",
        )

    user = _create_user(session, user_create=user_create)

    return UserPublic.model_validate(user)


@router.get("/get-user/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: UUID, session: Session = Depends(get_session)) -> UserPublic:
    user = _get_user(session, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return UserPublic.model_validate(user)


@router.get("/get-users", status_code=status.HTTP_200_OK)
def get_users(session: Session = Depends(get_session)) -> List[UserPublic]:
    users = _get_users(session)

    return [UserPublic.model_validate(user) for user in users]


@router.post("/delete-user/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
    user_id: UUID, session: Session = Depends(get_session)
) -> UserPublic:
    # Identify the user first
    user = _get_user(session, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # User still exists in memory but is gone in the database
    user = _delete_user(session, user)

    return UserPublic.model_validate(user)


@router.post("/create-item/{user_id}/{item_type_id}/{quantity}", status_code=status.HTTP_201_CREATED)
def create_item(
    user_id: UUID, item_type_id: UUID, quantity: int, session: Session = Depends(get_session)
) -> ItemPublic:
    # Check the user exists
    user = _get_user(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with the following ID: {user_id}",
        )

    # Check the item type exists
    item_type = _get_item_type(session=session, item_type_id=item_type_id)
    if item_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item type not found with the following ID: {item_type}"
        )

    # Create the item
    item_create = ItemCreate(name=item_type.name, quantity=quantity, user_id=user.id, item_type_id=item_type.id)
    item = _create_item(session, item_create)

    return ItemPublic.model_validate(item)


@router.get("/get-item/{item_id}", status_code=status.HTTP_200_OK)
def get_item(item_id: UUID, session: Session = Depends(get_session)) -> ItemPublic:
    # Check the item exists
    item = _get_item(session, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return ItemPublic.model_validate(item)


@router.post("/delete-item/{item_id}", status_code=status.HTTP_200_OK)
def delete_item(
    item_id: UUID, session: Session = Depends(get_session)
) -> ItemPublic:
    # Identify the item first
    item = _get_item(session, item_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Item still exists in memory but is gone in the database
    item = _delete_item(session, item)

    return ItemPublic.model_validate(item)

@router.post("/create-buy-order/{user_id}", status_code=status.HTTP_201_CREATED)
def create_buy_order(
    user_id: UUID, buy_order_create: BuyOrderCreate, session: Session = Depends(get_session)
) -> CreateOrderResponse:
    # Check the user exists
    user = _get_user(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with the following ID: {user_id}",
        )

    # Attach the user to the order
    buy_order_create.user_id = user.id

    # Create the order
    buy_order = _create_buy_order(session, buy_order_create)

    return CreateOrderResponse(
        message=f"The following order is created:\n{buy_order.model_dump()} for the following user:\n{buy_order.user.model_dump()}"
    )

@router.post("/create-sell-order/{user_id}", status_code=status.HTTP_201_CREATED)
def create_sell_order(
    user_id: UUID, sell_order_create: SellOrderCreate, session: Session = Depends(get_session)
) -> CreateOrderResponse:
    # Check the user exists
    user = _get_user(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with the following ID: {user_id}",
        )

    # Attach the user to the order
    sell_order_create.user_id = user.id

    # Create the order
    sell_order = _create_sell_order(session, sell_order_create)

    return CreateOrderResponse(
        message=f"The following order is created:\n{sell_order.model_dump()} for the following user:\n{sell_order.user.model_dump()}"
    )

@router.get("/get-buy-order/{buy_order_id}", status_code=status.HTTP_200_OK)
def get_buy_order(
    buy_order_id: UUID, session: Session = Depends(get_session)
) -> GetOrderResponse:
    # Check the order exists
    buy_order = _get_buy_order(session=session, buy_order_id=buy_order_id)

    if buy_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return GetOrderResponse(message=f"Got the following order:\n{buy_order.model_dump()}")

@router.get("/get-sell-order/{sell_order_id}", status_code=status.HTTP_200_OK)
def get_sell_order(
    sell_order_id: UUID, session: Session = Depends(get_session)
) -> GetOrderResponse:
    # Check the order exists
    sell_order = _get_sell_order(session=session, sell_order_id=sell_order_id)

    if sell_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return GetOrderResponse(message=f"Got the following order:\n{sell_order.model_dump()}")


@router.post("/delete-buy-order/{buy_order_id}", status_code=status.HTTP_200_OK)
def delete_buy_order(
    buy_order_id: UUID, session: Session = Depends(get_session)
) -> DeleteOrderResponse:
    # Identify the order first
    buy_order = _get_buy_order(session, buy_order_id)

    if buy_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    # Order still exists in memory but is gone in the database
    buy_order = _delete_buy_order(session, buy_order)

    return DeleteOrderResponse(
        message=f"Deleted the following order:\n{buy_order.model_dump()}"
    )

@router.post("/delete-sell-order/{sell_order_id}", status_code=status.HTTP_200_OK)
def delete_sell_order(
    sell_order_id: UUID, session: Session = Depends(get_session)
) -> DeleteOrderResponse:
    # Identify the order first
    sell_order = _get_buy_order(session, sell_order_id)

    if sell_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    # Order still exists in memory but is gone in the database
    sell_order = _delete_sell_order(session, sell_order)

    return DeleteOrderResponse(
        message=f"Deleted the following order:\n{sell_order.model_dump()}"
    )