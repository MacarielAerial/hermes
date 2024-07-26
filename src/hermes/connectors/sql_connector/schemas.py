from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, NonNegativeFloat, NonNegativeInt

#
# Enum
#

class Currency(str, Enum):
    GBP = 'GBP'

class OrderType(str, Enum):
    BUY = 'BUY'
    SELL = 'SELL'

class TokenType(str, Enum):
    bearer = 'bearer'

#
# Pydantic Classes
#


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

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
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int

class Item(ItemInDBBase):
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
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int

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
    model_config = ConfigDict(from_attributes=True)
    
    id: int

class OrderItem(OrderItemInDBBase):
    order: Order
    item: Optional[Item] = None  # Item can be NULL for buy orders

# TODO: Replace below with JWT token setup for user login

class Token(BaseModel):
    access_token: str
    token_type: str
