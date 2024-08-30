from pydantic import BaseModel

#
# CRUD
#


class CreateUserResponse(BaseModel):
    message: str


class GetUserResponse(BaseModel):
    message: str


class GetUsersResponse(BaseModel):
    message: str


class DeleteUserResponse(BaseModel):
    message: str


class CreateItemResponse(BaseModel):
    message: str


class GetItemResponse(BaseModel):
    message: str


class DeleteItemResponse(BaseModel):
    message: str
