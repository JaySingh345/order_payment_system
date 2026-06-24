import smtplib
import os
from dotenv import load_dotenv
from temporalio import activity
from shared.models import Order

load_dotenv()


@activity.defn
async def send_email(
    order: Order, tracking_id: str, transaction_id: str, order_id: int
) -> None:
    print("step 6")
    sender_mail = os.getenv("EMAIL_USER")
    sender_pass = os.getenv("EMAIL_PASS")
    reciever_mail = order.email
    if sender_pass is None or sender_mail is None:
        raise ValueError("EMAIL_USER or EMAIL_PASS is not set")

    Subject = "Order purchase completed"

    items_message = ""

    for item in order.items:
        items_message += f"- {item['name']} x {item['quantity']}\n"

    message = f"Order ID: {order_id} \n Customer ID:{order.customer_id} \n Amount: {order.amount} \n items and quantity: {items_message} \n Delivery Address: {order.address} \n Transaction ID: {transaction_id} \n tracking ID: {tracking_id} "

    text = f"Subject:{Subject} \n\n {message}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender_mail, sender_pass)
    server.sendmail(sender_mail, reciever_mail, text)

    print(f"Email has been sent to {reciever_mail}")
