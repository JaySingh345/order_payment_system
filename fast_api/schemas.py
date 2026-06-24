from pydantic import BaseModel


class item(BaseModel):
    name: str
    quantity: int


class OrderRequest(BaseModel):
    customer_id: int
    items: list[item]
    address: str
    email: str


class DeleteInventory(BaseModel):
    product_name: str
    quantity: int


class AddInventory(BaseModel):
    product_name: str
    quantity: int
    amount: float
