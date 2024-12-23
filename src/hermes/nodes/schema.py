from pydantic import BaseModel

#
# CRUD
#

class CreateOrderResponse(BaseModel):
    message: str


class GetOrderResponse(BaseModel):
    message: str


class DeleteOrderResponse(BaseModel):
    message: str
