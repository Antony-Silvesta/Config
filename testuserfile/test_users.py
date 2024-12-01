import pytest

# MongoDB connection fixture
@pytest.fixture(scope="module")
def mongodb_compass_seed():
    from pymongo import MongoClient
    client = MongoClient("mongodb://127.0.0.1:27017/")  # Update this URI as necessary
    db = client["sampleupload"]  # Your MongoDB database name
    return db

# Test for valid users
def test_valid_users(mongodb_compass_seed):
    db = mongodb_compass_seed
    valid_users = list(db["users"].find({"is_valid": True}))
    assert len(valid_users) == 1, "Expected 1 valid user."
