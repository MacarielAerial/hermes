from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum, DateTime
from sqlalchemy.orm import relationship

from hermes.connectors.sql_connector.database import Base
from hermes.connectors.sql_connector.schemas import Currency, OrderType


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)

    items = relationship("Item", back_populates="user")
    orders = relationship("Order", back_populates="user")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(255), index=True)
    quantity = Column(Integer)

    user = relationship("User", back_populates="items")
    order_items = relationship("OrderItem", back_populates="item")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_type = Column(Enum(OrderType))
    order_date = Column(DateTime)
    quantity = Column(Integer)
    price = Column(Float)
    currency = Column(Enum(Currency))

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    item_id = Column(Integer, ForeignKey('items.id'))

    order = relationship('Order', back_populates='order_items')
    item = relationship('Item', back_populates='order_items')
