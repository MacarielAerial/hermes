import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import ConfigDict, EmailStr, NonNegativeFloat, NonNegativeInt
from sqlmodel import Field, Relationship, SQLModel

#
# Enum
#


class Currency(str, Enum):
    GBP = "GBP"


class OrderType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


#
# Pydantic Classes
#


class UserBase(SQLModel):
    email: EmailStr = Field(index=True)


class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    items: List["Item"] = Relationship(back_populates="user")
    orders: List["Order"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    pass


class ItemBase(SQLModel):
    name: str = Field(index=True)
    quantity: NonNegativeInt

    user_id: Optional[UUID] = Field(foreign_key="user.id", default=None)
    order_id: Optional[UUID] = Field(foreign_key="order.id", default=None)


class Item(ItemBase, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    user: User = Relationship(back_populates="items")
    order: "Order" = Relationship(back_populates="items")


class ItemCreate(ItemBase):
    pass


class OrderBase(SQLModel):
    model_config = ConfigDict(use_enum_values=True)  # type: ignore[assignment]

    order_type: OrderType
    order_date: datetime
    quantity: NonNegativeInt
    price: NonNegativeFloat
    currency: Currency

    user_id: UUID = Field(foreign_key="user.id")


class Order(OrderBase, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    items: List[Item] = Relationship(back_populates="order")
    user: User = Relationship(back_populates="orders")


class OrderCreate(OrderBase):
    pass
