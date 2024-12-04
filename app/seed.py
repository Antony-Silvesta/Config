from db import connect_db
def seed_database():
    """Create a collection and insert seed data."""
    db = connect_db()
    try:
        collection = db["users"]
        collection.insert_many
            
        print("Seed data inserted successfully.")
    except Exception as e:
        print(f"Error seeding database: {e}")
if __name__ == "__main__":
    seed_database()