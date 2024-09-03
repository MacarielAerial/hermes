from typing import List, Optional
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Session, select

from hermes.connectors.schema import (
    Item,
    ItemCreate,
    Order,
    OrderCreate,
    User,
    UserCreate,
)


def _create_user(session: Session, user_create: UserCreate) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def _get_user(session: Session, user_id: UUID) -> Optional[User]:
    user = session.get(User, user_id)

    return user


def _get_users(session: Session) -> List[User]:
    statement = select(User)
    users = list(session.exec(statement).all())

    return users


def _get_user_by_email(session: Session, email: EmailStr) -> Optional[User]:
    statement = select(User).where(User.email == email)
    user = session.exec(statement).one_or_none()

    return user


def _delete_user(session: Session, user: User) -> User:
    session.delete(user)
    session.commit()

    return user


def _create_item(session: Session, item_create: ItemCreate) -> Item:
    item = Item(**item_create.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)

    return item


def _get_item(session: Session, item_id: UUID) -> Optional[Item]:
    item = session.get(Item, item_id)

    return item


def _get_items(session: Session) -> List[Item]:
    statement = select(Item)
    items = list(session.exec(statement).all())

    return items


def _delete_item(session: Session, item: Item) -> Item:
    session.delete(item)
    session.commit()

    return item


def _create_order(session: Session, order_create: OrderCreate) -> Order:
    order = Order(**order_create.model_dump())
    session.add(order)
    session.commit()
    session.refresh(order)

    return order


def _get_order(session: Session, order_id: UUID) -> Optional[Order]:
    order = session.get(Order, order_id)

    return order


def _get_orders(session: Session) -> List[Order]:
    statement = select(Order)
    orders = list(session.exec(statement).all())

    return orders


def _delete_order(session: Session, order: Order) -> Order:
    session.delete(order)
    session.commit()

    return order
