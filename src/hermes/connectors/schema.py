import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import ConfigDict, EmailStr, NonNegativeFloat, NonNegativeInt
from sqlmodel import Field, Relationship, SQLModel

class Currency(str, Enum):
    GBP = "GBP"

class OrderType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

#
# User
#

class UserBase(SQLModel):
    email: EmailStr = Field(index=True)

class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    items: List["Item"] = Relationship(back_populates="user")
    orders: List["Order"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    pass

#
# Item Type
#

class ItemTypeBase(SQLModel):
    name: str = Field(index=True)

class ItemType(ItemTypeBase, table=True):
    id: Optional[UUID] = Field(default=uuid.uuid4, primary_key=True)
    
    items: List["Item"] = Relationship(back_populates="item_type")
    buy_orders: List["BuyOrder"] = Relationship(back_populates="item_type")

class ItemTypeCreate(ItemTypeBase):
    pass

#
# Item
#

class ItemBase(SQLModel):
    name: str = Field(index=True)
    quantity: NonNegativeInt

    user_id: UUID = Field(foreign_key="user.id")
    item_type_id: UUID = Field(foreign_key="usertype.id")

class Item(ItemBase, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    user: User = Relationship(back_populates="items")
    item_type: ItemType = Relationship(back_populates="items")
    sell_order: Optional["SellOrder"] = Relationship(back_populates="item")

class ItemCreate(ItemBase):
    pass

#
# Order
#

class OrderBase(SQLModel):
    model_config = ConfigDict(use_enum_values=True)

    order_type: OrderType
    order_date: datetime
    price: float
    quantity: int
    currency: Currency

    user_id: UUID = Field(foreign_key="user.id")

class Order(OrderBase, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    user: User = Relationship(back_populates="orders")

class OrderCreate(OrderBase):
    pass

#
# Buy Order
#

class BuyOrderBase(OrderBase):
    item_type_id: int = Field(foreign_key="itemtype.id")

class BuyOrder(BuyOrderBase, table=True):
    item_type: ItemType = Relationship(back_populates="buy_orders")

class BuyOrderCreate(BuyOrderBase):
    pass

#
# Sell Order
#

class SellOrderBase(OrderBase):
    item_id: int = Field(foreign_key="item.id")

class SellOrder(SellOrderBase, table=True):
    item: Item = Relationship(back_populates="sell_order")

class SellOrderCreate(SellOrderBase):
    pass
