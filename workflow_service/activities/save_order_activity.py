from temporalio import activity 
from shared.models import Order
from database.database import SessionLocal
from database.models import OrderDB
@activity.defn
async  def save_order(order:Order,transaction_id:str,tracking_id:str):
    db = SessionLocal()
    try:
        db_order = OrderDB(
            order_id=order.order_id,
            customer_id=order.customer_id,
            amount=order.amount,
            items=order.items,
            address=order.address,
            email=order.email,
            status="COMPLETED",
            transaction_id = transaction_id,
            tracking_id = tracking_id
        )

        db.add(db_order)
        db.commit()
    finally:
        db.close()