from temporalio import activity
from shared.models import Order
import uuid
@activity.defn
async def ship_order(order:Order)-> str:
    print(f"shipping order {order.order_id}")

    tracking_id = f"Track - {uuid.uuid4}"

    return tracking_id
