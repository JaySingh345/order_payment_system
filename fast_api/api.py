from fastapi import FastAPI
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

@app.post("/orders")
async def create_order(order_request: OrderRequest,db:Session = Depends(get_db)):

    order = Order(
        order_id= order_request.order_id,
        customer_id=order_request.customer_id,
        amount=order_request.amount,
        items=[item.model_dump() for item in order_request.items],
        address=order_request.address,
        email=order_request.email
    )
    db_order = OrderDB(
        order_id = order.order_id,
        customer_id = order.customer_id,
        amount = order.amount,
        items = order.items,
        address = order.address,
        email = order.email,
        status="CREATED"
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    assert client is not None
    print("Before start_workflow")
    handle = await client.start_workflow(
        OrderWorkflow.run,
        order,
        id=f"order-{order.order_id}",
        task_queue="order-task-queue"
    )
    print("After start_workflow")
    return{
        "db_order": db_order.order_id,
        "workflow_id" : handle.id
    }

@app.get("/orders")
def get_all_orders(db: Session = Depends(get_db)):
    orders =  db.query(OrderDB).all()
    print(orders)
    return orders
