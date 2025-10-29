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
    Log test information before and after each test
    """
    test_name = request.node.name
    logger.info(f"\n{'='*80}")
    logger.info(f"Starting Test: {test_name}")
    logger.info(f"{'='*80}\n")
    
    yield
    
    logger.info(f"\n{'='*80}")
    logger.info(f"Completed Test: {test_name}")
    logger.info(f"{'='*80}\n")


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
def session_setup_teardown():
    """
    Setup and teardown for the entire test session
    """
    logger.info("="*100)
    logger.info("Starting Aziro Cluster Center UI Automation Test Suite")
    logger.info("="*100)
    
    yield
    
    logger.info("="*100)
    logger.info("Completed Aziro Cluster Center UI Automation Test Suite")
    logger.info("="*100)

