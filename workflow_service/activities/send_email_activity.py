from temporalio import activity
from shared.models import Order

@activity.defn
async def send_email(order:Order,tracking_id:str) -> None:
    print(f"sending mail to {order.email}")
    print(f"tracking id - {tracking_id}")
    
