from fastapi import FastAPI,HTTPException
from temporalio.client import Client
from workflow_service.workflows.order_workflow import OrderWorkflow
from fast_api.schemas import OrderRequest
from shared.models import Order
from sqlalchemy.orm import Session
from fastapi import Depends
from database.database import get_db
from database.models import OrderDB

app = FastAPI()

client: Client | None = None


@app.on_event("startup")
async def startup():
    global client
    client = await Client.connect("localhost:7233")


@app.post("/api/orders")
async def create_order(order_request: OrderRequest, db: Session = Depends(get_db)):

    order = Order(
        order_id=order_request.order_id,
        customer_id=order_request.customer_id,
        amount=0,
        items=[item.model_dump() for item in order_request.items],
        address=order_request.address,
        email=order_request.email,
    )
    
    assert client is not None
    handle = await client.start_workflow(
        OrderWorkflow.run,
        order,
        id=f"order-{order.order_id}",
        task_queue="order-task-queue",
    )
    return {"workflow_id": handle.id}


@app.get("/api/orders")
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(OrderDB).all()
    print(orders)
    return orders

@app.get("/api/orders/id/{id}")
def get_order_by_order_id(id : int,db: Session = Depends(get_db)):
    product = db.query(OrderDB).filter(OrderDB.order_id == id).first()
    
    if not product:
        raise HTTPException (status_code= 404, detail = "product not found")
    
    return product


@app.get("/api/orders/mail/{mail}")
def get_order_by_mail(mail : str,db: Session = Depends(get_db)):
    product = db.query(OrderDB).filter(OrderDB.email == mail).all()
    
    if not product:
        raise HTTPException (status_code= 404, detail = "product not found")
    
    # total_product = ""
    # for items in product:
    #     total_product += product

    return product
