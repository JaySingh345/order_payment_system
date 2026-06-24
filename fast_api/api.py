from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from temporalio.client import Client
from workflow_service.workflows.order_workflow import OrderWorkflow
from fast_api.schemas import OrderRequest, DeleteInventory, AddInventory,RegisterUser
from sqlalchemy.orm import Session
from fastapi import Depends
from database.database import get_db
from database.models import OrderDB, InventoryDB , CustomerDB
import uuid
from auth.hashing import hash_password,verify_password
from auth.token import create_access_token
from auth.oauth import get_current_user
from shared.models import Order

app = FastAPI()

client: Client | None = None


@app.on_event("startup")
async def startup():
    global client
    client = await Client.connect("localhost:7233")

@app.post("/register")
def register(
        request: RegisterUser,
        db: Session = Depends(get_db)
):
    


    user = CustomerDB(
        name=request.name,
        email=request.email,
        password=hash_password(request.password)
    )

    db.add(user)
    db.commit()

    return {"message": "Registered"}

@app.post("/login")
def login(
        request: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):

    user = (
        db.query(CustomerDB)
        .filter(CustomerDB.email == request.username)
        .first()
    )

    if user is None:
        raise HTTPException(status_code=401,detail = "invalid credentials")

    if not verify_password(
            request.password,
            user.password):
        raise HTTPException(401)

    token = create_access_token(
        user.customer_id
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.post("/api/orders")
async def create_order(order_request: OrderRequest, db: Session = Depends(get_db),current_user: CustomerDB = Depends(get_current_user)):

    order = Order(
        order_id=0,
        customer_id=current_user.customer_id,
        amount=0,
        items=[item.model_dump() for item in order_request.items],
        address=order_request.address,
        email=current_user.email,
    )

    assert client is not None
    handle = await client.start_workflow(
        OrderWorkflow.run,
        order,
        id=f"order-{uuid.uuid4()}",
        task_queue="order-task-queue",
    )
    return {"workflow_id": handle.id}

@app.get("/api/orders/users")
def get_user_orders(
    current_user: CustomerDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    orders = db.query(OrderDB).filter(OrderDB.customer_id == current_user.customer_id).all() 
    return orders


@app.get("/api/orders")
def get_all_orders(
    db: Session = Depends(get_db),
    current_user: CustomerDB = Depends(get_current_user)
    ):
    orders = db.query(OrderDB).all()
    return orders


@app.get("/api/orders/id/{id}")
def get_order_by_order_id(id: int, db: Session = Depends(get_db),current_user: CustomerDB = Depends(get_current_user)):
    product = db.query(OrderDB).filter(OrderDB.order_id == id).first()

    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    return product


@app.get("/api/orders/mail/{mail}")
def get_order_by_mail(mail: str, db: Session = Depends(get_db),current_user: CustomerDB = Depends(get_current_user)):
    product = db.query(OrderDB).filter(OrderDB.email == mail).all()

    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    return product


@app.get("/api/inventory/quantity")
def products_in_inventory(db: Session = Depends(get_db),current_user: CustomerDB = Depends(get_current_user)):
    inventory = db.query(InventoryDB).all()

    return inventory


@app.post("/api/inventory/add")
def add_products_inventory(request: AddInventory, db: Session = Depends(get_db),current_user: CustomerDB = Depends(get_current_user)):
    product = (
        db.query(InventoryDB)
        .filter(InventoryDB.product_name == request.product_name)
        .first()
    )

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
    request: DeleteInventory, db: Session = Depends(get_db),current_user: CustomerDB = Depends(get_current_user)
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
