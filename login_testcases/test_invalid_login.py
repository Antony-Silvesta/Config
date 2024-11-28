import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from homeobjects.test_login import LoginPage
from pymongo import MongoClient
import logging

# Set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Fixture for Selenium WebDriver setup
@pytest.fixture(scope="class")
def setup_driver():
    # Set up Chrome options for headless mode
    options = Options()
    options.add_argument("--headless")  # Enable headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--window-size=1920x1080")  # Optional: 
    
    # Set up the service for ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
    logger.info("Browser closed.")

# Fixture for fetching invalid users from MongoDB
@pytest.fixture(scope="class")
def invalid_users():
    client = MongoClient("mongodb://127.0.0.1:27017/")  # Update this URI as necessary
    db = client["sampleupload"]  # Use your actual database name
    users_collection = db["users"]  # Use your actual collection name
    logger.info("Connected to MongoDB and fetched users collection.")

    # Fetch users with invalid details
    invalid_user_details = list(users_collection.find({"is_valid": False}))
    logger.info(f"Invalid user details fetched: {invalid_user_details}")

    if not invalid_user_details:
        raise Exception("No invalid user details found in the database!")

    yield invalid_user_details
    client.close()
    logger.info("MongoDB client connection closed.")

@pytest.mark.usefixtures("setup_driver")
class TestInvalidLogin:
    def test_login_with_invalid_users(self, setup_driver, invalid_users):
        logger.info(f"Invalid users fetched for testing: {invalid_users}")
        
        for index, user_details in enumerate(invalid_users):
            logger.debug(f"Index: {index}, User details: {user_details}")

            required_keys = ["username", "password", "baseurl", "expected_error"]

            # Ensure all necessary keys are present
            if not all(key in user_details for key in required_keys):
                logger.warning(f"Skipping login due to missing keys: {user_details}")
                pytest.skip(f"Skipping due to missing keys: {user_details}")

            username = user_details["username"]
            password = user_details["password"]
            base_url = user_details["baseurl"]
            expected_error = user_details["expected_error"]

            logger.info(f"Testing login for Username: '{username}' with Password: '{password}', Expected error: '{expected_error}'")

           

            # Navigate to the base URL
            try:
                setup_driver.get(base_url)
                logger.info(f"Navigated to: {base_url}")
            except Exception as e:
                logger.error(f"Error navigating to base URL: {e}")
                pytest.skip(f"Skipping due to navigation error: {e}")

            # Instantiate the LoginPage object and attempt login
            lg = LoginPage(setup_driver)
            lg.setUsername(username)
            lg.setPassword(password)
            lg.clickLogin()
            actual_error = lg.actualError()

            # Assert that the actual error matches the expected error
            assert expected_error == actual_error, (
                f"Failed for Username: '{username}' with Password: '{password}', "
                f"Expected: {expected_error}, Got: {actual_error}"
            )
