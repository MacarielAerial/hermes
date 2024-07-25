from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: EmailStr

class RegisterResponse(BaseModel):
    message: str

class UsersResponse(BaseModel):
    message: str

class UserResponse(BaseModel):
    message: str

class UserItemsResponse(BaseModel):
    message: str
