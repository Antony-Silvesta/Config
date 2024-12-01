import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from homeobjects.test_login import LoginPage
from pymongo import MongoClient

# Fixture for MongoDB client connection
@pytest.fixture(scope="module")
def mongo_client():
    client = MongoClient("mongodb://127.0.0.1:27017/")  # MongoDB URI
    db = client["sampleupload"]  # Database name
    users_collection = db["users"]  # Collection name
    yield users_collection
    client.close()  # Close MongoDB connection after tests
    print("MongoDB client connection closed.")

# Fixture for Selenium WebDriver
@pytest.fixture(scope="module")
def driver():
    # Set up Chrome options for headless mode
    options = Options()
    options.add_argument("--headless")  # Headless mode for testing without a GUI
    options.add_argument("--disable-gpu")  # Disable GPU for headless mode
    options.add_argument("--window-size=1920x1080")  # Optional: Set window size
    
    # Set up the service for ChromeDriver
    service = Service(ChromeDriverManager().install())
    
    # Initialize Chrome WebDriver with the headless options
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
    print("Browser closed.")

# Test function to check login with valid users
def test_login_with_valid_users(driver, mongo_client):
    valid_users = list(mongo_client.find({"is_valid": True}))
    assert valid_users, "No valid users found in the database!"  # Will fail if no valid users found

    print(f"Valid users: {valid_users}")  # Debugging: Print valid users to verify the result

    for index, user_details in enumerate(valid_users):
        required_keys = ["username", "password", "baseurl"]
        
        # Ensure all necessary keys are present
        if not all(key in user_details for key in required_keys):
            print("Skipping login due to missing keys:", user_details)
            continue  # Skip this user if required keys are missing

        username = user_details["username"]
        password = user_details["password"]
        base_url = user_details["baseurl"]

        # Print the username and password being tested
        print(f"Testing login for Username: '{username}' with Password: '{password}'")

        # Navigate to the base URL
        try:
            driver.get(base_url)
            print("Navigated to:", base_url)
        except Exception as e:
            print("Error navigating to base URL:", e)
            continue  # Skip this user if navigation fails

        # Instantiate the LoginPage object and perform login
        lg = LoginPage(driver)
        lg.setUsername(username)  # Enter the username
        lg.setPassword(password)  # Enter the password
        lg.clickLogin()
        time.sleep(5)
