"""
Aziro Cluster Center - UI Automation Test Configuration
Pytest fixtures and configuration for Playwright tests
"""

import pytest
import logging
from playwright.sync_api import Page, Browser, BrowserContext
from datetime import datetime
import os

# Configure logging to file
import sys
from pathlib import Path

# Create logs directory
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Generate log filename with timestamp
log_filename = logs_dir / f"test_execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Configure file handler with detailed formatting
file_handler = logging.FileHandler(log_filename, mode='w', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(
    '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s() - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(file_formatter)

# Configure console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Configure root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

logger = logging.getLogger(__name__)
logger.info(f"Logging configured. Log file: {log_filename}")
logger.info(f"Log file will contain detailed execution logs for all test cases")
logger.info(f"Target log file size: 2 MB")


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
    logger.debug(f"conftest.page() - Creating new page for test")
    logger.debug(f"conftest.page() - Browser context type: {type(context).__name__}")
    logger.debug(f"conftest.page() - Browser context ID: {id(context)}")
    page = context.new_page()
    logger.debug(f"conftest.page() - Page object created")
    logger.debug(f"conftest.page() - Page object type: {type(page).__name__}")
    logger.debug(f"conftest.page() - Page object ID: {id(page)}")
    logger.debug(f"conftest.page() - Initial page URL: {page.url}")
    logger.debug(f"conftest.page() - Initial page title: {page.title()}")
    logger.debug(f"conftest.page() - Page viewport: {page.viewport_size}")
    
    # Log console messages with extensive details
    def log_console(msg):
        logger.debug(f"conftest.page() - Browser Console Event Received")
        logger.debug(f"conftest.page() - Console Message Type: {msg.type}")
        logger.debug(f"conftest.page() - Console Message Text: {msg.text}")
        logger.debug(f"conftest.page() - Console Message Location: {msg.location}")
        logger.debug(f"conftest.page() - Console Message Args Count: {len(msg.args)}")
        for idx, arg in enumerate(msg.args):
            try:
                arg_value = arg.json_value()
                logger.debug(f"conftest.page() - Console Arg {idx}: {arg_value}")
            except:
                logger.debug(f"conftest.page() - Console Arg {idx}: [Could not serialize]")
        logger.info(f"Browser Console [{msg.type}]: {msg.text}")
    
    page.on("console", log_console)
    
    # Log page errors with extensive details
    def log_page_error(err):
        logger.debug(f"conftest.page() - Page Error Event Received")
        logger.debug(f"conftest.page() - Error Type: {type(err).__name__}")
        logger.debug(f"conftest.page() - Error Message: {str(err)}")
        logger.debug(f"conftest.page() - Error String Representation: {repr(err)}")
        logger.error(f"Page Error: {err}")
    
    page.on("pageerror", log_page_error)
    
    # Log failed requests with extensive details
    def log_failed_request(request):
        logger.debug(f"conftest.page() - Failed Request Event Received")
        logger.debug(f"conftest.page() - Request URL: {request.url}")
        logger.debug(f"conftest.page() - Request Method: {request.method}")
        logger.debug(f"conftest.page() - Request Headers: {request.headers}")
        logger.debug(f"conftest.page() - Request Failure: {request.failure}")
        logger.debug(f"conftest.page() - Request Resource Type: {request.resource_type}")
        logger.debug(f"conftest.page() - Request Post Data: {request.post_data}")
        logger.warning(f"Failed Request: {request.url} - {request.failure}")
    
    page.on("requestfailed", log_failed_request)
    
    # Log all requests with extensive details
    def log_request(request):
        logger.debug(f"conftest.page() - Request Event Received")
        logger.debug(f"conftest.page() - Request URL: {request.url}")
        logger.debug(f"conftest.page() - Request Method: {request.method}")
        logger.debug(f"conftest.page() - Request Resource Type: {request.resource_type}")
        logger.debug(f"conftest.page() - Request Headers: {request.headers}")
        logger.debug(f"conftest.page() - Request Post Data: {request.post_data}")
        logger.debug(f"conftest.page() - Request Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        logger.debug(f"Request initiated: {request.method} {request.url}")
    
    page.on("request", log_request)
    
    # Log all responses with extensive details
    def log_response(response):
        logger.debug(f"conftest.page() - Response Event Received")
        logger.debug(f"conftest.page() - Response URL: {response.url}")
        logger.debug(f"conftest.page() - Response Status: {response.status}")
        logger.debug(f"conftest.page() - Response Status Text: {response.status_text}")
        logger.debug(f"conftest.page() - Response Headers: {response.headers}")
        logger.debug(f"conftest.page() - Response Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        try:
            body_size = len(response.body()) if response.ok else 0
            logger.debug(f"conftest.page() - Response Body Size: {body_size} bytes")
        except:
            logger.debug(f"conftest.page() - Could not get response body size")
        logger.debug(f"Response received: {response.status} {response.status_text} for {response.url}")
    
    page.on("response", log_response)
    
    # Log dialog events
    def log_dialog(dialog):
        logger.debug(f"conftest.page() - Dialog Event Received")
        logger.debug(f"conftest.page() - Dialog Type: {dialog.type}")
        logger.debug(f"conftest.page() - Dialog Message: {dialog.message}")
        logger.debug(f"conftest.page() - Dialog Default Value: {dialog.default_value}")
        logger.info(f"Browser Dialog [{dialog.type}]: {dialog.message}")
        dialog.dismiss()
    
    page.on("dialog", log_dialog)
    
    logger.info(f"Created new page for test")
    logger.debug(f"conftest.page() - Page fixture setup complete")
    yield page
    
    logger.debug(f"conftest.page() - Test completed, closing page")
    logger.debug(f"conftest.page() - Final page URL: {page.url}")
    logger.debug(f"conftest.page() - Final page title: {page.title()}")
    logger.info(f"Closing page after test")
    page.close()
    logger.debug(f"conftest.page() - Page closed successfully")


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
    import platform
    import os
    try:
        import psutil
        PSUTIL_AVAILABLE = True
    except ImportError:
        PSUTIL_AVAILABLE = False
        logger.debug(f"conftest.log_test_info() - psutil not available, skipping system metrics")
    
    test_name = request.node.name
    
    # Log extensive system information
    logger.debug(f"conftest.log_test_info() - Test fixture called")
    logger.debug(f"conftest.log_test_info() - Test name: {test_name}")
    logger.debug(f"conftest.log_test_info() - Test node ID: {request.node.nodeid}")
    logger.debug(f"conftest.log_test_info() - Test file: {request.node.fspath}")
    logger.debug(f"conftest.log_test_info() - Test function: {request.node.function}")
    logger.debug(f"conftest.log_test_info() - System Information:")
    logger.debug(f"conftest.log_test_info() -   Platform: {platform.platform()}")
    logger.debug(f"conftest.log_test_info() -   System: {platform.system()}")
    logger.debug(f"conftest.log_test_info() -   Release: {platform.release()}")
    logger.debug(f"conftest.log_test_info() -   Version: {platform.version()}")
    logger.debug(f"conftest.log_test_info() -   Machine: {platform.machine()}")
    logger.debug(f"conftest.log_test_info() -   Processor: {platform.processor()}")
    logger.debug(f"conftest.log_test_info() -   Python Version: {platform.python_version()}")
    logger.debug(f"conftest.log_test_info() -   Python Implementation: {platform.python_implementation()}")
    logger.debug(f"conftest.log_test_info() -   Python Compiler: {platform.python_compiler()}")
    if PSUTIL_AVAILABLE:
        try:
            logger.debug(f"conftest.log_test_info() -   CPU Count: {psutil.cpu_count()}")
            logger.debug(f"conftest.log_test_info() -   CPU Percent: {psutil.cpu_percent(interval=0.1)}%")
            logger.debug(f"conftest.log_test_info() -   Memory Total: {psutil.virtual_memory().total / (1024**3):.2f} GB")
            logger.debug(f"conftest.log_test_info() -   Memory Available: {psutil.virtual_memory().available / (1024**3):.2f} GB")
            logger.debug(f"conftest.log_test_info() -   Memory Used: {psutil.virtual_memory().used / (1024**3):.2f} GB")
            logger.debug(f"conftest.log_test_info() -   Memory Percent: {psutil.virtual_memory().percent}%")
            logger.debug(f"conftest.log_test_info() -   Process ID: {os.getpid()}")
            process = psutil.Process(os.getpid())
            logger.debug(f"conftest.log_test_info() -   Process Memory: {process.memory_info().rss / (1024**2):.2f} MB")
            logger.debug(f"conftest.log_test_info() -   Process CPU Percent: {process.cpu_percent(interval=0.1)}%")
        except Exception as e:
            logger.debug(f"conftest.log_test_info() -   Could not get system info: {e}")
    else:
        logger.debug(f"conftest.log_test_info() -   psutil not available, using basic system info")
        logger.debug(f"conftest.log_test_info() -   Process ID: {os.getpid()}")
    logger.debug(f"conftest.log_test_info() - Environment Variables:")
    for key in ['PATH', 'HOME', 'USER', 'SHELL', 'LANG', 'TZ']:
        if key in os.environ:
            logger.debug(f"conftest.log_test_info() -   {key}: {os.environ[key]}")
    
    # Extract feature from markers
    feature = "General"
    markers_list = []
    for marker in request.node.iter_markers():
        markers_list.append(marker.name)
        if marker.name in ['dashboard', 'vm_management', 'logs']:
            feature = marker.name.replace('_', ' ').title()
    logger.debug(f"conftest.log_test_info() - Test markers: {markers_list}")
    logger.debug(f"conftest.log_test_info() - Extracted feature: {feature}")
    
    # Get test number from session
    if not hasattr(request.session, 'test_counter'):
        request.session.test_counter = 0
    request.session.test_counter += 1
    logger.debug(f"conftest.log_test_info() - Test counter: {request.session.test_counter}")
    
    # Print test start
    logger.debug(f"conftest.log_test_info() - Calling reporter.print_test_start()")
    reporter.print_test_start(test_name, feature, request.session.test_counter)
    logger.debug(f"conftest.log_test_info() - Test start logged")
    
    yield
    
    # Log test completion information
    logger.debug(f"conftest.log_test_info() - Test execution completed")
    logger.debug(f"conftest.log_test_info() - Checking test result")
    
    # Print test end based on test result
    if hasattr(request.node, 'rep_call'):
        logger.debug(f"conftest.log_test_info() - Test result available")
        logger.debug(f"conftest.log_test_info() - Test passed: {request.node.rep_call.passed}")
        logger.debug(f"conftest.log_test_info() - Test failed: {request.node.rep_call.failed}")
        logger.debug(f"conftest.log_test_info() - Test skipped: {request.node.rep_call.skipped}")
        if request.node.rep_call.passed:
            logger.debug(f"conftest.log_test_info() - Logging test pass")
            reporter.print_test_end("pass", "Test completed successfully")
        elif request.node.rep_call.failed:
            logger.debug(f"conftest.log_test_info() - Logging test failure")
            logger.debug(f"conftest.log_test_info() - Failure details: {str(request.node.rep_call.longrepr)}")
            reporter.print_test_end("fail", str(request.node.rep_call.longrepr))
        elif request.node.rep_call.skipped:
            logger.debug(f"conftest.log_test_info() - Logging test skip")
            reporter.print_test_end("skip", "Test was skipped")
    else:
        logger.debug(f"conftest.log_test_info() - No test result available, assuming pass")
        reporter.print_test_end("pass")
    
    # Log final system state
    if PSUTIL_AVAILABLE:
        try:
            logger.debug(f"conftest.log_test_info() - Final System State:")
            logger.debug(f"conftest.log_test_info() -   CPU Percent: {psutil.cpu_percent(interval=0.1)}%")
            logger.debug(f"conftest.log_test_info() -   Memory Used: {psutil.virtual_memory().used / (1024**3):.2f} GB")
            logger.debug(f"conftest.log_test_info() -   Memory Percent: {psutil.virtual_memory().percent}%")
            process = psutil.Process(os.getpid())
            logger.debug(f"conftest.log_test_info() -   Process Memory: {process.memory_info().rss / (1024**2):.2f} MB")
        except Exception as e:
            logger.debug(f"conftest.log_test_info() -   Could not get final system state: {e}")
    else:
        logger.debug(f"conftest.log_test_info() - Final System State: psutil not available")
    
    logger.debug(f"conftest.log_test_info() - Test fixture teardown complete")


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
    # Note: allure-results directory removed to avoid greenlet dependency
    # os.makedirs("reports/allure-results", exist_ok=True)
    
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
    import platform
    import os
    
    # Session start - extensive logging
    logger.debug(f"conftest.session_setup_teardown() - Session setup started")
    logger.debug(f"conftest.session_setup_teardown() - Session start timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
    logger.debug(f"conftest.session_setup_teardown() - Python version: {platform.python_version()}")
    logger.debug(f"conftest.session_setup_teardown() - Platform: {platform.platform()}")
    logger.debug(f"conftest.session_setup_teardown() - Working directory: {os.getcwd()}")
    logger.debug(f"conftest.session_setup_teardown() - Process ID: {os.getpid()}")
    logger.debug(f"conftest.session_setup_teardown() - Base URL: {BASE_URL}")
    logger.debug(f"conftest.session_setup_teardown() - API URL: {API_URL}")
    logger.debug(f"conftest.session_setup_teardown() - Log file location: {log_filename}")
    logger.debug(f"conftest.session_setup_teardown() - Target log file size: 2 MB")
    
    reporter.print_header(
        "🧪 AZIRO CLUSTER CENTER - UI AUTOMATION SUITE",
        "Comprehensive End-to-End Testing"
    )
    reporter.print_info(f"Base URL: {BASE_URL}")
    reporter.print_info(f"API URL: {API_URL}")
    reporter.print_info(f"Browser: Chromium (Headed Mode)")
    reporter.print_separator()
    
    session_start = time.time()
    logger.debug(f"conftest.session_setup_teardown() - Session start time recorded: {session_start}")
    logger.info(f"Test session started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Log file: {log_filename}")
    logger.info(f"Target log file size: 2 MB")
    
    yield
    
    # Session end - extensive logging
    session_duration = time.time() - session_start
    logger.debug(f"conftest.session_setup_teardown() - Session teardown started")
    logger.debug(f"conftest.session_setup_teardown() - Session end timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
    logger.debug(f"conftest.session_setup_teardown() - Session duration: {session_duration:.4f} seconds")
    logger.debug(f"conftest.session_setup_teardown() - Session duration formatted: {session_duration / 60:.2f} minutes")
    
    # Get test statistics from session
    passed = request.session.testscollected - request.session.testsfailed
    failed = request.session.testsfailed
    skipped = 0  # Can be enhanced to track skipped tests
    
    logger.debug(f"conftest.session_setup_teardown() - Test statistics:")
    logger.debug(f"conftest.session_setup_teardown() -   Tests collected: {request.session.testscollected}")
    logger.debug(f"conftest.session_setup_teardown() -   Tests passed: {passed}")
    logger.debug(f"conftest.session_setup_teardown() -   Tests failed: {failed}")
    logger.debug(f"conftest.session_setup_teardown() -   Tests skipped: {skipped}")
    logger.debug(f"conftest.session_setup_teardown() -   Pass rate: {(passed / request.session.testscollected * 100) if request.session.testscollected > 0 else 0:.2f}%")
    
    # Check log file size
    try:
        if log_filename.exists():
            log_file_size = log_filename.stat().st_size
            log_file_size_mb = log_file_size / (1024 * 1024)
            logger.debug(f"conftest.session_setup_teardown() - Log file size: {log_file_size} bytes ({log_file_size_mb:.2f} MB)")
            logger.debug(f"conftest.session_setup_teardown() - Log file path: {log_filename.absolute()}")
            logger.info(f"Log file generated: {log_filename} ({log_file_size_mb:.2f} MB)")
        else:
            logger.debug(f"conftest.session_setup_teardown() - Log file does not exist")
    except Exception as e:
        logger.debug(f"conftest.session_setup_teardown() - Could not check log file size: {e}")
    
    reporter.print_final_summary(passed, failed, skipped, session_duration)
    logger.debug(f"conftest.session_setup_teardown() - Session teardown complete")

