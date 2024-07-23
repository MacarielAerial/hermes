from sqlalchemy import Column, Integer, String

from hermes.connectors.sql_connector.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
