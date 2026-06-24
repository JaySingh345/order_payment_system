from fastapi import FastAPI, HTTPException
from temporalio.client import Client
from workflow_service.workflows.order_workflow import OrderWorkflow
from fast_api.schemas import OrderRequest, DeleteInventory, AddInventory
from shared.models import Order
from sqlalchemy.orm import Session
from fastapi import Depends
from database.database import get_db
from database.models import OrderDB, InventoryDB
import uuid


app = FastAPI()

client: Client | None = None


@app.on_event("startup")
async def startup():
    global client
    client = await Client.connect("localhost:7233")


@app.post("/api/orders")
async def create_order(order_request: OrderRequest, db: Session = Depends(get_db)):

    order = Order(
        order_id=0,
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
        id=f"order-{uuid.uuid4()}",
        task_queue="order-task-queue",
    )
    return {"workflow_id": handle.id}


@app.get("/api/orders")
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(OrderDB).all()
    return orders


@app.get("/api/orders/id/{id}")
def get_order_by_order_id(id: int, db: Session = Depends(get_db)):
    product = db.query(OrderDB).filter(OrderDB.order_id == id).first()

    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    return product


@app.get("/api/orders/mail/{mail}")
def get_order_by_mail(mail: str, db: Session = Depends(get_db)):
    product = db.query(OrderDB).filter(OrderDB.email == mail).all()

    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    return product


@app.get("/api/inventory/quantity")
def products_in_inventory(db: Session = Depends(get_db)):
    inventory = db.query(InventoryDB).all()

    return inventory


@app.post("/api/inventory/add")
def add_products_inventory(request: AddInventory, db: Session = Depends(get_db)):
    product = db.query(InventoryDB).filter(
        InventoryDB.product_name == request.product_name
    ).first()

    if product is not None:
        product.quantity += request.quantity
        product.amount = request.amount

    else:
        add_product = InventoryDB(
            product_name=request.product_name,
            quantity=request.quantity,
            amount=request.amount,
        )
        db.add(add_product)
    db.commit()
    db.refresh(product)

    return {
        "messege": "Inventory updated",
        "product name ": product.product_name,
        "quantity": product.quantity,
        "amount": product.amount,
    }


@app.delete("/api/inventory/delete")
def delete_products_inventory_by_product_name(
    request: DeleteInventory, db: Session = Depends(get_db)
):
    product = (
        db.query(InventoryDB)
        .filter(InventoryDB.product_name == request.product_name)
        .first()
    )

    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    if product.quantity < request.quantity:
        raise HTTPException(status_code=400, detail="insufficient quantity avaiable")

    product.quantity -= request.quantity

    if product.quantity == 0:
        db.delete(product)

    db.commit()

    return f"inventory updated successfully \n remaining quantity {product.quantity}"
