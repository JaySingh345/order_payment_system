from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

engine = create_engine("postgresql://postgres:root@localhost:5432/order_payment_db")

session = sessionmaker(autocommit = False,autoflush = False,bind = engine)

Base = declarative_base()

def get_db():
    db =session()
    try:
        yield db
    finally:
        db.close()

        