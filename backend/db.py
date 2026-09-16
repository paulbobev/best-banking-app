import os
from motor.motor_asyncio import AsyncIOMotorClient

# Set MONGO_URI to the MongoDB Atlas connection string in the runtime environment.
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Initialize asynchronous MongoDB Atlas client
client = AsyncIOMotorClient(MONGO_URI)
db = client["banking_db"]

# Document Collections
users_collection = db["users"]
accounts_collection = db["accounts"]
transactions_collection = db["transactions"]


async def init_db():
    """Optional startup check to verify MongoDB Atlas connectivity."""
    try:
        await client.admin.command("ping")
        print("Successfully connected to MongoDB Cloud Atlas!")
    except Exception as e:
        print(f"MongoDB Connection Error: {e}")