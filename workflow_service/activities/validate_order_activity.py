from temporalio import activity
from shared.models import Order
@activity.defn
async def validate_order(order:Order) -> bool:
    print(f"validating order {order.order_id}")

    if order.amount <= 0:
        return False
    
    if len(order.items) == 0:
        return False
    
    return True 
    