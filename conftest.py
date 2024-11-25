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
@pytest.fixture(autouse=True)
def add_selenium_log(request):
    driver = request.node.funcargs.get("driver")
    if driver:
        # Adding browser logs to report
        for entry in driver.get_log('browser'):
            request.node.user_properties.append(("browser_log", entry))