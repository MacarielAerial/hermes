from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, EmailStr, NonNegativeFloat, NonNegativeInt


class Currency(str, Enum):
    GBP = 'GBP'

class OrderType(str, Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True

class User(UserInDBBase):
    items: List[Item] = []
    orders: List[Order] = []

class ItemBase(BaseModel):
    name: str
    quantity: NonNegativeInt

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class ItemInDBBase(ItemBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class Item(ItemInDBBase):
    user: User
    order_items: List[OrderItem]


class OrderBase(BaseModel):
    order_type: OrderType
    order_date: datetime
    quantity: NonNegativeInt
    price: NonNegativeFloat
    currency: Currency

class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    pass

class OrderInDBBase(OrderBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class Order(OrderInDBBase):
    user: User
    order_items: List[OrderItem]

class OrderItemBase(BaseModel):
    order_id: int
    item_id: Optional[int]  # Item can be NULL for buy orders

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(OrderItemBase):
    pass

class OrderItemInDBBase(OrderItemBase):
    id: int

    class Config:
        orm_mode = True

class OrderItem(OrderItemInDBBase):
    order: Order
    item: Optional[Item] = None  # Item can be NULL for buy orders
