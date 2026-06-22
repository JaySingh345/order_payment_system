import asyncio
from temporalio.client import Client
from workflow_service.workflows.order_workflow import OrderWorkflow
from shared.models import Order


async def main():
    client = await Client.connect("localhost:7233")

    order = Order(
        order_id=1,
        customer_id=101,
        amount=150.00,
        items=[{"product_id": 1, "quantity": 2}, {"product_id": 2, "quantity": 2}],
        address="Noida",
        email="john@example.com",
    )
    result = await client.execute_workflow(
        OrderWorkflow.run,
        order,
        id=f"order-{order.order_id}",
        task_queue="order-task-queue",
    )
    print(result)


asyncio.run(main())
