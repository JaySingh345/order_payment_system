from datetime import timedelta
from temporalio import workflow


from shared.models import Order

from workflow_service.activities.validate_order_activity import validate_order
from workflow_service.activities.reserve_inventory_activity import reserve_inventory
from workflow_service.activities.process_payment_activity import process_payment
from workflow_service.activities.ship_order_activity import ship_order
from workflow_service.activities.send_email_activity import send_email
from workflow_service.activities.save_order_activity import save_order

from temporalio.common import RetryPolicy


@workflow.defn
class OrderWorkflow:
    def __init__(self):
        self.order_approved = False

    @workflow.signal
    def approve_order(self):
        self.order_approved = True

    async def execute(self, activity, *args):
        return await workflow.execute_activity(
            activity,
            args=args,
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=5),
                backoff_coefficient=2.0,
                maximum_interval=timedelta(seconds=10),
                maximum_attempts=5,
            ),
        )

    @workflow.run
    async def run(self, order: Order):

        if not await self.execute(validate_order, order):
            return "Order validation failed"

        await workflow.wait_condition(lambda: self.order_approved)

        transaction_id, amount = await self.execute(process_payment, order)

        order.amount = amount
        if not await self.execute(reserve_inventory, order):
            return "Inventory unavailable"

        tracking_id = await self.execute(ship_order, order)

        order_id = await self.execute(save_order, order, transaction_id, tracking_id)

        await self.execute(send_email, order, tracking_id, transaction_id, order_id)

        return {
            "status": "completed",
            "order_id": order_id,
            "transaction_id": transaction_id,
            "tracking_id": tracking_id,
        }
