from temporalio import activity
from shared.models import Order
import uuid


@activity.defn
async def ship_order(order: Order) -> str:

    tracking_id = f"Track - {uuid.uuid4()}"
    print(f"Order {order.order_id} shipped with tracking ID: {tracking_id}")

    return tracking_id
