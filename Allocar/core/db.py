import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# Get MongoDB credentials from environment variables
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]

async def init_db():
    await db['employees'].create_index([("email", 1)], unique=True)
    await db['employees'].create_index([("employee_id", 1)], unique=True)   
    await db['vehicles'].create_index([("vehicle_id", 1)], unique=True)
    await db['allocations'].create_index([("allocation_id", 1)], unique=True)
    pass
init_db()
def get_database():
    return db
