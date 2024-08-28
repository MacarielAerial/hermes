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
