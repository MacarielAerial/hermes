import uuid
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import (
    ConfigDict, 
    EmailStr, 
    NonNegativeInt,
    model_validator
)
from sqlmodel import Field, Relationship, SQLModel, Index

class Currency(str, Enum):
    GBP = "GBP"

class OrderType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStatus(str, Enum):
    OPEN = "open"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"

#
# User
#

class UserBase(SQLModel):
    email: EmailStr = Field(index=True)

class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    items: List["Item"] = Relationship(back_populates="user")
    buy_orders: List["BuyOrder"] = Relationship(back_populates="user")
    sell_orders: List["SellOrder"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    pass

class UserPublic(UserBase):
    id: UUID

#
# Item Type
#

class ItemTypeBase(SQLModel):
    name: str = Field(index=True)

class ItemType(ItemTypeBase, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
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

class Item(ItemBase, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user_id: UUID = Field(foreign_key="user.id")
    item_type_id: UUID = Field(foreign_key="itemtype.id")

    user: User = Relationship(back_populates="items")
    item_type: ItemType = Relationship(back_populates="items")
    sell_order: Optional["SellOrder"] = Relationship(back_populates="item")

class ItemCreate(ItemBase):
    user_id: UUID
    item_type_id: UUID

class ItemPublic(ItemBase):
    id: UUID

#
# Order Base (Not a table, just shared fields)
#

class OrderBase(SQLModel):
    order_type: OrderType
    order_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    price: Decimal = Field(max_digits=18, decimal_places=8)
    quantity: NonNegativeInt
    remaining_quantity: NonNegativeInt
    currency: Currency
    status: OrderStatus = Field(default=OrderStatus.OPEN, index=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    matched_order_id: Optional[UUID] = None

    @model_validator(mode='after')
    def validate_remaining_quantity(self) -> 'OrderBase':
        if self.remaining_quantity > self.quantity:
            raise ValueError("remaining_quantity cannot be greater than quantity")
        return self

#
# Buy Order
#

class BuyOrder(OrderBase, table=True):
    model_config = ConfigDict(use_enum_values=True)
    __table_args__ = (
        Index("idx_buy_order_item_status_price", "item_type_id", "status", "price"),
    )

    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    item_type_id: UUID = Field(foreign_key="itemtype.id")
    user_id: UUID = Field(foreign_key="user.id")

    user: User = Relationship(back_populates="buy_orders")
    item_type: ItemType = Relationship(back_populates="buy_orders")
    trades_as_buyer: List["Trade"] = Relationship(back_populates="buy_order")

class BuyOrderCreate(OrderBase):
    item_type_id: UUID

#
# Sell Order
#

class SellOrder(OrderBase, table=True):
    model_config = ConfigDict(use_enum_values=True)
    __table_args__ = (
        Index("idx_sell_order_item_status_price", "item_id", "status", "price"),
    )

    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    item_id: UUID = Field(foreign_key="item.id")
    user_id: UUID = Field(foreign_key="user.id")

    user: User = Relationship(back_populates="sell_orders")
    item: Item = Relationship(back_populates="sell_order")
    trades_as_seller: List["Trade"] = Relationship(back_populates="sell_order")

class SellOrderCreate(OrderBase):
    item_id: UUID

#
# Trade
#

class TradeBase(SQLModel):
    executed_price: Decimal = Field(max_digits=18, decimal_places=8)
    executed_quantity: NonNegativeInt
    executed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Trade(TradeBase, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
 
    buy_order_id: UUID = Field(foreign_key="buyorder.id")
    sell_order_id: UUID = Field(foreign_key="sellorder.id")
 
    buy_order: BuyOrder = Relationship(back_populates="trades_as_buyer")
    sell_order: SellOrder = Relationship(back_populates="trades_as_seller")

class TradeCreate(TradeBase):
    buy_order_id: UUID
    sell_order_id: UUID
