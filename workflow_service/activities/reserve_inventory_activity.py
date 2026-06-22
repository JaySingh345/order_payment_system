from temporalio import activity
from shared.models import Order

@activity.defn
async def reserve_inventory(order:Order) -> bool:
    print(f"reserve inventory for order {order.order_id}")

    return True