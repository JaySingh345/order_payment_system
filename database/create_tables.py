from database.database import engine
from database.models import OrderDB,InventoryDB

OrderDB.metadata.create_all(bind=engine)

InventoryDB.metadata.create_all(bind=engine)
print("Tables created")
