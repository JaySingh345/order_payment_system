from pydantic import BaseModel


class item(BaseModel):
    name: str
    quantity: int


class OrderRequest(BaseModel):
    items: list[item]
    address: str


class DeleteInventory(BaseModel):
    product_name: str
    quantity: int


class AddInventory(BaseModel):
    product_name: str
    quantity: int
    amount: float

class RegisterUser(BaseModel):
    name: str
    email: str
    password:str

class LoginUser(BaseModel):
    email: str
    password: str
