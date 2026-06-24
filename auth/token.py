import os
from jose import jwt 
from dotenv import load_dotenv
from datetime import timedelta,datetime

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(customer_id: int):

    payload = {
        "customer_id" : customer_id,
        "exp" : datetime.utcnow() + timedelta(hours=1)
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )