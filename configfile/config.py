import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
MONGO_URI = "mongodb://127.0.0.1:27017/"  # MongoDB URI
DATABASE_NAME = "sampleupload"  # Your database name
USER_COLLECTION = "users"  # Your collection name
def setup_mongodb():
    # Retrieve MongoDB URI from environment variable if set
    mongo_uri = os.getenv("MONGO_URI", MONGO_URI)
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')  # Ping to check connection
        print("MongoDB connected successfully!")
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        exit(1)
    # Set up test data (example)
    db = client.get_database(DATABASE_NAME)  # Use your actual database
    collection = db.get_collection(USER_COLLECTION)  # Use your collection
  # Example: Insert some test documents
    sample_data = [
       {
            "username": "",
            "first_name": "admin",
            "last_name": "admin",
            "password": "demo",
            "mode_2fa": "Off",
            "groups": ["Admin"],
            "rights": "Admin",
            "notes": {"info": "this 'notes' field exists only for this default admin user", "p": "donttrustyou"},
            "vec_2fa": None,  # Corrected null to None
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/",
            "is_valid": False,
            "expected_error": "success",
        },
        
        {
            "username": "demo",
            "first_name": "admin",
            "last_name": "admin",
            "password": "",
            "mode_2fa": "Off",
            "groups": ["Admin"],
            "rights": "Admin",
            "notes": {"info": "this 'notes' field exists only for this default admin user", "p": "donttrustyou"},
            "vec_2fa": None,  # Corrected null to None
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/",
            "is_valid": False,
            "expected_error": "Wrong credentials",
        },
        {
            "username": "demo",
            "first_name": "admin",
            "last_name": "admin",
            "password": "demo",
            "mode_2fa": "Off",
            "groups": ["Admin"],
            "rights": "Admin",
            "notes": {
                "info": "this 'notes' field exists only for this default admin user",
                "p": "donttrustyou"
            },
            "vec_2fa": None,  # Corrected null to None
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/",
            "is_valid": True,
            "expected_error": "success",
        }










    ]
    collection.insert_many(sample_data)
    print(f"Test data inserted into {db.name}.{collection.name}")
if __name__ == "__main__":
    setup_mongodb()
