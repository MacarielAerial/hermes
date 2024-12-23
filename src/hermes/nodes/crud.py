from typing import List, Optional, Union
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Session, select

from hermes.connectors.schema import (
    Item,
    ItemCreate,
    BuyOrder,
    BuyOrderCreate,
    ItemType,
    ItemTypeCreate,
    SellOrder,
    SellOrderCreate,
    User,
    UserCreate,
)


def _create_user(session: Session, user_create: UserCreate) -> User:
    user = User.model_validate(user_create)
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

def _create_item_type(session: Session, item_type_create: ItemTypeCreate) -> ItemType:
    item_type = ItemType.model_validate(item_type_create)
    session.add(item_type)
    session.commit()
    session.refresh(item_type)

    return item_type


def _get_item_type(session: Session, item_type_id: UUID) -> Optional[Item]:
    item_type = session.get(ItemType, item_type_id)

    return item_type

def _get_item_type_by_name(session: Session, name: str) -> Optional[Item]:
    statement = select(ItemType).where(ItemType.name == name)
    item_type = session.exec(statement).one_or_none()

    return item_type


def _delete_item_type(session: Session, item_type: ItemType) -> ItemType:
    session.delete(item_type)
    session.commit()

    return item_type

def _create_item(session: Session, item_create: ItemCreate) -> Item:
    item = Item.model_validate(item_create)
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


def _create_buy_order(session: Session, buy_order_create: BuyOrderCreate) -> BuyOrder:
    buy_order = BuyOrder(**buy_order_create.model_dump())
    session.add(buy_order)
    session.commit()
    session.refresh(buy_order)

    return buy_order

def _create_sell_order(session: Session, sell_order_create: SellOrderCreate) -> SellOrder:
    sell_order = SellOrder(**sell_order_create.model_dump())
    session.add(sell_order)
    session.commit()
    session.refresh(sell_order)

    return sell_order

def _get_buy_order(session: Session, buy_order_id: UUID) -> Optional[BuyOrder]:
    buy_order = session.get(BuyOrder, buy_order_id)

    return buy_order

def _get_sell_order(session: Session, sell_order_id: UUID) -> Optional[SellOrder]:
    sell_order = session.get(SellOrder, sell_order_id)

    return sell_order

def _get_all_orders(session: Session) -> List[Union[BuyOrder, SellOrder]]:
    """
    Query both buy and sell orders and return them sorted by creation date.
    """
    buy_orders = session.exec(select(BuyOrder)).all()
    sell_orders = session.exec(select(SellOrder)).all()
    
    # Merge and sort by creation date
    all_orders = buy_orders + sell_orders

    return sorted(all_orders, key=lambda x: x.created_at)

def _delete_buy_order(session: Session, buy_order: BuyOrder) -> BuyOrder:
    session.delete(buy_order)
    session.commit()

    return buy_order

def _delete_sell_order(session: Session, sell_order: SellOrder) -> SellOrder:
    session.delete(sell_order)
    session.commit()

    return sell_order