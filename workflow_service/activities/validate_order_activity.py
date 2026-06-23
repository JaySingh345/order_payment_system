from temporalio import activity
from shared.models import Order
from database.models import InventoryDB
from database.database import SessionLocal


@activity.defn
async def validate_order(order: Order) -> bool:

    print("valedating order", order.order_id)
    db = SessionLocal()
    try:
        for items in order.items:
            print("checking item", items)
            product = (
                db.query(InventoryDB)
                .filter(InventoryDB.product_name == items["name"])
                .first()
            )

            print("product =", product)

            if product is None:
                print(f"{items['name']} product do not exist")
                return False

            if product.quantity < items["quantity"]:
                print(f"{product.product_name} insufficient quantity")
                return False

            print("validation completed")
        return True

    finally:
        db.close()
