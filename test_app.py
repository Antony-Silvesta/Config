import pytest
from pymongo import MongoClient

@pytest.fixture
def mongodb_client():
    client = MongoClient("mongodb://localhost:27017")
    yield client
    client.close()

def test_mongodb_connection(mongodb_client):
    db = mongodb_client.sampleupload
    db.test_collection.insert_one({"key": "value"})
    assert db.test_collection.find_one({"key": "value"}) is not None
