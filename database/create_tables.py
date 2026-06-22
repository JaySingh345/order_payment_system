from database.database import engine
from database.models import OrderDB

Base = OrderDB.metadata

Base.create_all(bind=engine)

print("Tables created")