from temporalio import activity
from shared.models import Order
import uuid

@activity.defn
async def process_payment(order:Order) -> str:

    print(f"processing payment of {order.order_id}")

    transaction_id = str(uuid.uuid4())

    return transaction_id