from pydantic import BaseModel

class item(BaseModel):
    name : str
    quantity : int

class OrderRequest(BaseModel):
    order_id:int
    customer_id:int
    amount:float
    items:list[item]
    address:str
    email:str
