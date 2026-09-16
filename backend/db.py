import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Retrieve the MongoDB connection string from the runtime environment.
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Initialize standard synchronous PyMongo client
client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
db = client["banking_db"]

# Document Collections
users_collection = db["users"]
accounts_collection = db["accounts"]
transactions_collection = db["transactions"]


def init_db():
    """Startup check to verify MongoDB Atlas connectivity synchronously."""
    try:
        # Send a ping to confirm a successful connection
        client.admin.command("ping")
        print("Successfully connected to MongoDB Cloud Atlas (Sync)!")
    except Exception as e:
        print(f"MongoDB Connection Error: {e}")