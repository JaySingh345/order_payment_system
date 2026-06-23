from temporalio import activity
from shared.models import Order
from database.models import InventoryDB
from database.database import SessionLocal


@activity.defn
async def reserve_inventory(order: Order) -> bool:
    db = SessionLocal()
    try:
        for item in order.items:
            product = (
                db.query(InventoryDB)
                .filter(InventoryDB.product_name == item["name"])
                .first()
            )
            assert product is not None
            product.quantity -= item["quantity"]
            print(f"Inventory reserved for the order {item['name']}")

        db.commit()
        return True

    finally:
        db.close
