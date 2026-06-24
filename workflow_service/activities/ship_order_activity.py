from temporalio import activity
from shared.models import Order
import uuid


@activity.defn
async def ship_order(order: Order) -> str:

    print("step 4")

    tracking_id = f"Track - {uuid.uuid4()}"
    print(f"shipping the order Tracking ID: {tracking_id}")

    return tracking_id
