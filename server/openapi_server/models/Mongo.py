import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


class MongoDatabase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDatabase, cls).__new__(cls)

            DB_USER = os.getenv("DB_USER")
            DB_PASSWORD = os.getenv("DB_PASSWORD")
            DB_CLUSTER = os.getenv("DB_CLUSTER")
            DB_NAME = os.getenv("DB_NAME")

            if not all([DB_USER, DB_PASSWORD, DB_CLUSTER, DB_NAME]):
                raise EnvironmentError("Missing required environment variables.")
            MONGO_URI = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_CLUSTER}/{DB_NAME}?retryWrites=true&w=majority"
            print("URI:", MONGO_URI)
            cls._instance.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            cls._instance.db = cls._instance.client[DB_NAME]
            print("Connected to MongoDB successfully.")
        return cls._instance

    def get_collection(self, collection_name):
        return self.db[collection_name]


def validate_object_id():

    return None