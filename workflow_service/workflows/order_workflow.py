from datetime import timedelta
from temporalio import workflow


from shared.models import Order

from workflow_service.activities.validate_order_activity import validate_order
from workflow_service.activities.reserve_inventory_activity import reserve_inventory
from workflow_service.activities.process_payment_activity import process_payment
from workflow_service.activities.ship_order_activity import ship_order
from workflow_service.activities.send_email_activity import send_email


@workflow.defn
class OrderWorkflow:
    
    async def execute(self, activity, *args):
        return await workflow.execute_activity(
            activity,
            args=args,
            start_to_close_timeout=timedelta(seconds=10),
        )

    @workflow.run
    async def run(self, order: Order):

        if not await self.execute(validate_order, order):
            return "Order validation failed"

        if not await self.execute(reserve_inventory, order):
            return "Inventory unavailable"
        
        await workflow.sleep(timedelta(seconds=30))

        transaction_id = await self.execute(
            process_payment,
            order
        )

        tracking_id = await self.execute(
            ship_order,
            order
        )

        await self.execute(
            send_email,
            order,
            tracking_id
        )

        return {
            "status": "completed",
            "transaction_id": transaction_id,
            "tracking_id": tracking_id,
        }