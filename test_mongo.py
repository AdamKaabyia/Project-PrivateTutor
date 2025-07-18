import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_CLUSTER = os.getenv("DB_CLUSTER")
DB_NAME = os.getenv("DB_NAME")

uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_CLUSTER}/{DB_NAME}?retryWrites=true&w=majority"
print("MongoDB URI being used:")
print(uri)

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    db = client[DB_NAME]
    collection = db["test_connection"]

    result = collection.insert_one({"message": "Hello MongoDB!"})
    print("✅ Successfully inserted test document:", result.inserted_id)
except Exception as e:
    print("❌ Connection failed:", str(e))

