from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import CustomerDB
from auth.token import SECRET_KEY,ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        customer_id = payload.get("customer_id")
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if customer_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    user = (
        db.query(CustomerDB)
        .filter(CustomerDB.customer_id == customer_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return user