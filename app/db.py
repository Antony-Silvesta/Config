from pymongo import MongoClient
import os
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "sampleupload"
COLLECTION_NAME = "users"
def connect_db():
    """Connect to MongoDB and return the database object."""
    try:
        client = MongoClient(MONGO_URI)
        print("Connected to MongoDB")
        return client[DB_NAME][COLLECTION_NAME]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        exit(1)