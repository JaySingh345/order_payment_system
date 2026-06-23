from temporalio import activity
from shared.models import Order
import uuid
from database.database import SessionLocal
from database.models import InventoryDB


@activity.defn
async def process_payment(order: Order):
    db = SessionLocal()
    try:
        total_amount = 0
        for items in order.items:
            product = (
                db.query(InventoryDB)
                .filter(InventoryDB.product_name == items["name"])
                .first()
            )

            if product is not None:
                total_amount += product.amount * items["quantity"]

        order.amount = total_amount
    finally:
        db.close()

    transaction_id = str(uuid.uuid4())

    return transaction_id, total_amount
