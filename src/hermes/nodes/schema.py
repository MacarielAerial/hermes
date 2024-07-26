from typing import List
from pydantic import BaseModel

from hermes.connectors.sql_connector.schemas import TokenType, User, Item

#
# CRUD
#

class RegisterResponse(BaseModel):
    message: str
    db_user: User

class UsersResponse(BaseModel):
    message: str
    db_users: List[User]

class UserResponse(BaseModel):
    message: str
    db_user: User

class UserItemResponse(BaseModel):
    message: str
    db_item: Item

class ItemsResponse(BaseModel):
    message: str
    db_items: List[Item]

#
# Login
#

class LoginResponse(BaseModel):
    access_token: str
    token_type: TokenType
