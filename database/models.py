from sqlalchemy import Column,Integer,JSON,Float,String
from database.database import Base

class OrderDB(Base):
    __tablename__ = "orders"
    order_id = Column(Integer,primary_key = True)
    customer_id = Column(Integer, unique = True)
    amount = Column(Float,nullable = False)
    items = Column(JSON,nullable = False)
    address = Column(String,nullable = False)
    email = Column(String,nullable = False)
    status = Column(String,default="CREATED")