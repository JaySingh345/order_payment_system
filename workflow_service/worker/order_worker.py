import asyncio
from temporalio.client import Client
from workflow_service.workflows.order_workflow import OrderWorkflow

from workflow_service.activities.process_payment_activity import process_payment
from workflow_service.activities.reserve_inventory_activity import reserve_inventory
from workflow_service.activities.send_email_activity import send_email
from workflow_service.activities.ship_order_activity import ship_order
from workflow_service.activities.validate_order_activity import validate_order

from temporalio.worker import Worker

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue = "order-task-queue",
        workflows = [OrderWorkflow],
        activities = [process_payment,reserve_inventory,send_email,ship_order,validate_order]
    )
    print("worker started")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())

