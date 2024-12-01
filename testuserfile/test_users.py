def test_valid_users(mongodb_compass_seed):
    db = mongodb_compass_seed  # Connect to the seeded MongoDB db
    valid_users = list(db["users"].find({"is_valid": True}))
    assert len(valid_users) == 1, "Expected 1 valid users."

def test_invalid_users(mongodb_compass_seed):
    db = mongodb_compass_seed
    invalid_users = list(db["users"].find({"is_valid": False}))
    assert len(invalid_users) == 1, "Expected 1 invalid users."
