"""
Aziro Cluster Center - UI Automation Test Configuration
Pytest fixtures and configuration for Playwright tests
"""

import pytest
import logging
from playwright.sync_api import Page, Browser, BrowserContext
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Application URLs
BASE_URL = os.getenv("BASE_URL", "http://localhost:8082")
API_URL = os.getenv("API_URL", "http://localhost:5000/api")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Configure browser context with custom settings
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "en-US",
        "timezone_id": "America/New_York",
        "permissions": [],
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """
    Create a new page for each test with enhanced logging
    """
    page = context.new_page()
    
    # Log console messages
    page.on("console", lambda msg: logger.info(f"Browser Console [{msg.type}]: {msg.text}"))
    
    # Log page errors
    page.on("pageerror", lambda err: logger.error(f"Page Error: {err}"))
    
    # Log failed requests
    page.on("requestfailed", lambda request: 
            logger.warning(f"Failed Request: {request.url} - {request.failure}"))
    
    logger.info(f"Created new page for test")
    yield page
    
    logger.info(f"Closing page after test")
    page.close()


@pytest.fixture(scope="function")
def dashboard_page(page: Page):
    """
    Navigate to the dashboard and wait for it to load
    """
    logger.info(f"Navigating to: {BASE_URL}")
    page.goto(BASE_URL, wait_until="domcontentloaded")
    
    # Wait for the dashboard to be ready
    page.wait_for_selector('[data-testid="dashboard-tab"]', timeout=10000)
    logger.info("Dashboard loaded successfully")
    
    return page


@pytest.fixture(scope="function", autouse=True)
def log_test_info(request):
    """
    Log test information before and after each test with decorations
    """
    from utils.test_reporter import reporter
    
    test_name = request.node.name
    
    # Extract feature from markers
    feature = "General"
    for marker in request.node.iter_markers():
        if marker.name in ['dashboard', 'vm_management', 'logs']:
            feature = marker.name.replace('_', ' ').title()
            break
    
    # Get test number from session
    if not hasattr(request.session, 'test_counter'):
        request.session.test_counter = 0
    request.session.test_counter += 1
    
    # Print test start
    reporter.print_test_start(test_name, feature, request.session.test_counter)
    
    yield
    
    # Print test end based on test result
    if hasattr(request.node, 'rep_call'):
        if request.node.rep_call.passed:
            reporter.print_test_end("pass", "Test completed successfully")
        elif request.node.rep_call.failed:
            reporter.print_test_end("fail", str(request.node.rep_call.longrepr))
        elif request.node.rep_call.skipped:
            reporter.print_test_end("skip", "Test was skipped")
    else:
        reporter.print_test_end("pass")


@pytest.fixture(scope="function")
def screenshot_on_failure(request, page: Page):
    """
    Take screenshot on test failure
    """
    yield
    
    if request.node.rep_call.failed:
        # Create screenshots directory if it doesn't exist
        screenshots_dir = "reports/screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Generate screenshot filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name.replace(" ", "_").replace("[", "_").replace("]", "_")
        screenshot_path = f"{screenshots_dir}/{test_name}_{timestamp}.png"
        
        # Take screenshot
        page.screenshot(path=screenshot_path)
        logger.error(f"Test failed. Screenshot saved: {screenshot_path}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Make test result available to fixtures
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_configure(config):
    """
    Configure pytest with custom settings
    """
    # Create reports directory
    os.makedirs("reports", exist_ok=True)
    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("reports/allure-results", exist_ok=True)
    
    logger.info("Pytest configuration completed")
    logger.info(f"Base URL: {BASE_URL}")
    logger.info(f"API URL: {API_URL}")


@pytest.fixture(scope="session", autouse=True)
def session_setup_teardown(request):
    """
    Setup and teardown for the entire test session
    """
    from utils.test_reporter import reporter
    import time
    
    # Session start
    reporter.print_header(
        "🧪 AZIRO CLUSTER CENTER - UI AUTOMATION SUITE",
        "Comprehensive End-to-End Testing"
    )
    reporter.print_info(f"Base URL: {BASE_URL}")
    reporter.print_info(f"API URL: {API_URL}")
    reporter.print_info(f"Browser: Chromium (Headed Mode)")
    reporter.print_separator()
    
    session_start = time.time()
    
    yield
    
    # Session end
    session_duration = time.time() - session_start
    
    # Get test statistics from session
    passed = request.session.testscollected - request.session.testsfailed
    failed = request.session.testsfailed
    skipped = 0  # Can be enhanced to track skipped tests
    
    reporter.print_final_summary(passed, failed, skipped, session_duration)

