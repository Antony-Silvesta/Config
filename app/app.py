from db import connect_db
def list_entries():
    """List all entries in the collection."""
    db = connect_db()
    try:
        
        collection = db["users"]  # Updated collection 
        entries = collection.find()
        for entry in entries:
            print(entry)
    except Exception as e:
        print(f"Error listing entries: {e}")
if __name__ == "__main__":
    list_entries()