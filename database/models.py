from sqlalchemy import Column, Integer, JSON, Float, String
from database.database import Base


class OrderDB(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    items = Column(JSON, nullable=False)
    address = Column(String, nullable=False)
    email = Column(String, nullable=False)
    status = Column(String, default="CREATED")
    transaction_id = Column(String, unique=True)
    tracking_id = Column(String, unique=True)


class InventoryDB(Base):
    __tablename__ = "inventory"

    product_name = Column(String, primary_key=True)
    quantity = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
