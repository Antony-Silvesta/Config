import pytest

# Hook for adding additional information in the HTML report
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    if call.when == 'call' and call.excinfo is not None:
        # Add a screenshot if a test fails
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_path = f"screenshots/{item.name}.png"
            driver.save_screenshot(screenshot_path)
            pytest_html = item.config.pluginmanager.getplugin('html')
            extra = getattr(item, 'extra', [])
            extra.append(pytest_html.extras.image(screenshot_path))
            item.extra = extra

# Fixture for adding browser logs to report
@pytest.fixture(autouse=True)
def add_selenium_log(request):
    driver = request.node.funcargs.get("driver")
    if driver:
        # Adding browser logs to report
        for entry in driver.get_log('browser'):
            request.node.user_properties.append(("browser_log", entry))

# Hook for adding the --db command-line option to pytest
def pytest_addoption(parser):
    parser.addoption(
        "--db", action="store", default="sampleupload", help="Database to use (default: sampleupload)"
    )

# Fixture to access the --db option
@pytest.fixture
def db(request):
    return request.config.getoption("--db")
