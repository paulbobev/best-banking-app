import os
from pymongo import MongoClient, ReturnDocument
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
counters_collection = db["counters"]




def init_db():
    """Startup check to verify MongoDB Atlas connectivity synchronously."""
    try:
        # Send a ping to confirm a successful connection
        client.admin.command("ping")
        print("Successfully connected to MongoDB Cloud Atlas (Sync)!")
    except Exception as e:
        print(f"MongoDB Connection Error: {e}")
        
def get_next_id(sequence_name: str) -> int:
  doc = counters_collection.find_one_and_update(
      {"_id": sequence_name},
      {"$inc": {"seq": 1}},
      upsert=True,
      return_document=ReturnDocument.AFTER)
  if doc is None:
    raise RuntimeError(f"Failed to generate sequence ID for '{sequence_name}'.")
  return int(doc["seq"])