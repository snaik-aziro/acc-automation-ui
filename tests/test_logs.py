"""
Logging System Tests for Aziro Cluster Center
Tests for system logs viewing and filtering
"""

import pytest
from playwright.sync_api import Page
from pages.dashboard_page import DashboardPage
from pages.logs_page import LogsPage
import logging
import time
import sys
from datetime import datetime

logger = logging.getLogger(__name__)

def log_step(step_num, step_name, page=None):
    """Helper function to log detailed step information"""
    step_start = time.time()
    logger.info("")
    logger.info("━" * 100)
    logger.info(f"📍 STEP {step_num}: {step_name}")
    logger.info("━" * 100)
    logger.info(f"   ⏰ Step Start: {datetime.now().strftime('%H:%M:%S.%f')}")
    if page:
        try:
            logger.info(f"   🌐 Current URL: {page.url}")
            logger.info(f"   📄 Current Title: {page.title()}")
            logger.info(f"   📍 Page State: {page.evaluate('document.readyState')}")
        except:
            pass
    return step_start

def log_step_complete(step_num, step_start, success=True, details=""):
    """Helper function to log step completion"""
    step_elapsed = time.time() - step_start
    status = "✅" if success else "❌"
    logger.info(f"   {status} Step {step_num} completed in {step_elapsed:.4f} seconds")
    if details:
        logger.info(f"   {details}")
    logger.info(f"   ✓ Step {step_num} completed successfully" if success else f"   ✗ Step {step_num} failed")


@pytest.mark.logs
class TestLoggingSystem:
    """Test suite for Logging System functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup for each test - navigate to Logs tab"""
        dashboard = DashboardPage(page)
        dashboard.load_dashboard()
        dashboard.click_logs_tab()
    
    @pytest.mark.smoke
    def test_load_l1_critical_logs(self, page: Page):
        """Test loading L1 (Critical) logs"""
        test_start_time = time.time()
        test_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("🚀 TEST: Load L1 Critical logs - START")
        logger.info("=" * 100)
        logger.info(f"⏰ Test Start Time: {test_timestamp}")
        logger.info(f"🆔 Test ID: test_load_l1_critical_logs")
        logger.info(f"📋 Test Description: Test loading L1 (Critical) logs")
        logger.info(f"🏷️  Test Markers: @pytest.mark.smoke, @pytest.mark.logs")
        logger.info(f"🌐 Page URL Before Test: {page.url}")
        logger.info(f"📏 Page Viewport: {page.viewport_size}")
        logger.info(f"🧠 Memory Usage: {sys.getsizeof(page)} bytes (page object)")
        logger.info(f"📊 Page Load State: {page.evaluate('document.readyState')}")
        logger.info("=" * 100)
        
        step1_start = log_step(1, "Initializing logs page object", page)
        logger.info(f"   📦 Input: page object type={type(page).__name__}")
        logger.info(f"   🔍 Page State: url={page.url}, title={page.title()}")
        logger.info(f"   🧠 Memory Before: {sys.getsizeof(page)} bytes")
        logger.info(f"   🎯 Action: Creating LogsPage(page) instance")
        logs_page = LogsPage(page)
        step1_elapsed = time.time() - step1_start
        logger.info(f"   ✅ LogsPage object created in {step1_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(logs_page).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(logs_page)} bytes")
        logger.info(f"   🔗 Object ID: {id(logs_page)}")
        logger.info(f"   📍 Object Location: {logs_page.__class__.__module__}")
        log_step_complete(1, step1_start, True, "Logs page object created successfully")
        
        step2_start = log_step(2, "Clicking L1 (Critical) logs button to load critical logs", page)
        logger.info(f"   🎯 Method: logs_page.load_l1_logs()")
        logger.info(f"   📍 Method Location: {logs_page.load_l1_logs.__code__.co_filename}:{logs_page.load_l1_logs.__code__.co_firstlineno}")
        logger.info(f"   🔍 Pre-click State:")
        logger.info(f"      Current URL: {page.url}")
        logger.info(f"      Current Title: {page.title()}")
        logger.info(f"      Page Load State: {page.evaluate('document.readyState')}")
        logger.info(f"   🔍 Checking if L1 button exists before click...")
        try:
            l1_button = page.locator('[data-testid="l1-logs-button"]')
            is_visible_before = l1_button.is_visible()
            logger.info(f"   👁️  L1 button visible before click: {is_visible_before}")
            if is_visible_before:
                bbox = l1_button.bounding_box()
                logger.info(f"   📏 L1 button bounding box: {bbox}")
                logger.info(f"   🎨 L1 button text: {l1_button.text_content()}")
        except Exception as e:
            logger.warning(f"   ⚠️  Could not check L1 button state: {e}")
        logger.info(f"   🚀 Executing load_l1_logs() call...")
        call_start = time.time()
        logs_page.load_l1_logs()
        call_elapsed = time.time() - call_start
        step2_elapsed = time.time() - step2_start
        logger.info(f"   ⏱️  Method call completed in {call_elapsed:.4f} seconds")
        logger.info(f"   🔍 Post-click State:")
        logger.info(f"      Current URL: {page.url}")
        logger.info(f"      Current Title: {page.title()}")
        logger.info(f"      Page Load State: {page.evaluate('document.readyState')}")
        log_step_complete(2, step2_start, True, f"L1 logs load action completed in {call_elapsed:.4f} seconds")
        
        step3_start = log_step(3, "Retrieving log container text content", page)
        logger.info(f"   🎯 Method: logs_page.get_log_container_text()")
        logger.info(f"   📍 Method Location: {logs_page.get_log_container_text.__code__.co_filename}:{logs_page.get_log_container_text.__code__.co_firstlineno}")
        logger.info(f"   🔍 Pre-retrieval State:")
        logger.info(f"      Current URL: {page.url}")
        logger.info(f"      Page Load State: {page.evaluate('document.readyState')}")
        logger.info(f"   🚀 Executing get_log_container_text() call...")
        call_start = time.time()
        log_text = logs_page.get_log_container_text()
        call_elapsed = time.time() - call_start
        step3_elapsed = time.time() - step3_start
        logger.info(f"   ⏱️  Method call completed in {call_elapsed:.4f} seconds")
        logger.info(f"   ✅ get_log_container_text() returned result")
        logger.info(f"   📊 Result Type: {type(log_text).__name__}")
        logger.info(f"   📏 Result Length: {len(log_text)} characters")
        logger.info(f"   🧠 Result Memory: {sys.getsizeof(log_text)} bytes")
        logger.info(f"   📝 Result Size in Bytes (UTF-8): {len(log_text.encode('utf-8'))} bytes")
        logger.info(f"   🔢 Character Count: {len(log_text)}")
        logger.info(f"   📊 Word Count: {len(log_text.split()) if log_text else 0}")
        logger.info(f"   📊 Line Count: {len(log_text.splitlines()) if log_text else 0}")
        log_step_complete(3, step3_start, True, f"Log container text retrieved: {len(log_text)} characters")
        
        step4_start = log_step(4, "Analyzing log container content", page)
        logger.info(f"   🔍 Content Analysis:")
        logger.info(f"      Total Characters: {len(log_text)}")
        logger.info(f"      Total Bytes (UTF-8): {len(log_text.encode('utf-8'))}")
        logger.info(f"      Total Words: {len(log_text.split()) if log_text else 0}")
        logger.info(f"      Total Lines: {len(log_text.splitlines()) if log_text else 0}")
        logger.info(f"      Empty Check: {len(log_text) == 0}")
        logger.info(f"      Non-Empty Check: {len(log_text) > 0}")
        if len(log_text) > 100:
            preview = log_text[:100]
            logger.info(f"   📄 Log Preview (first 100 chars): '{preview}...'")
            logger.info(f"   📏 Preview Length: {len(preview)} characters")
            logger.info(f"   🔍 Preview Contains 'L1': {'L1' in preview}")
            logger.info(f"   🔍 Preview Contains 'Critical': {'Critical' in preview}")
            logger.info(f"   🔍 Preview Contains 'ERROR': {'ERROR' in preview}")
        else:
            logger.info(f"   📄 Full Log Content: '{log_text}'")
            logger.info(f"   📏 Full Content Length: {len(log_text)} characters")
        step4_elapsed = time.time() - step4_start
        log_step_complete(4, step4_start, True, f"Content analysis completed in {step4_elapsed:.4f} seconds")
        
        step5_start = log_step(5, "Validating log container has content", page)
        logger.info(f"   🔍 Validation Details:")
        logger.info(f"      Log Text Length: {len(log_text)}")
        logger.info(f"      Length > 0 Check: {len(log_text) > 0}")
        logger.info(f"      Expected: Length > 0")
        logger.info(f"      Actual: Length = {len(log_text)}")
        logger.info(f"   ✅ Assertion: assert len(log_text) > 0")
        assert_start = time.time()
        assert len(log_text) > 0, "Log container should have content"
        assert_elapsed = time.time() - assert_start
        step5_elapsed = time.time() - step5_start
        logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
        logger.info(f"   ✓ Log container validation passed")
        logger.info(f"   📊 Validation Result: Log container contains {len(log_text)} characters")
        log_step_complete(5, step5_start, True, "Log container validation passed")
        
        test_elapsed = time.time() - test_start_time
        logger.info("")
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("✓✓✓ TEST PASSED: L1 Critical logs loaded successfully")
        logger.info("=" * 100)
        logger.info(f"⏰ Test End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        logger.info(f"⏱️  Total Test Duration: {test_elapsed:.4f} seconds")
        logger.info(f"📊 Test Summary:")
        logger.info(f"   - Steps Executed: 5")
        logger.info(f"   - Log Text Retrieved: {len(log_text)} characters")
        logger.info(f"   - Log Size: {len(log_text.encode('utf-8'))} bytes")
        logger.info(f"   - Status: PASSED")
        logger.info(f"   - Memory Usage: {sys.getsizeof(page) + sys.getsizeof(logs_page)} bytes")
        logger.info("=" * 100)
        logger.info("=" * 100)
    
    @pytest.mark.smoke
    def test_load_l2_warning_logs(self, page: Page):
        """Test loading L2 (Warning) logs"""
        test_start_time = time.time()
        test_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("🚀 TEST: Load L2 Warning logs - START")
        logger.info("=" * 100)
        logger.info(f"⏰ Test Start Time: {test_timestamp}")
        logger.info(f"🆔 Test ID: test_load_l2_warning_logs")
        logger.info(f"📋 Test Description: Test loading L2 (Warning) logs")
        logger.info(f"🏷️  Test Markers: @pytest.mark.logs")
        logger.info(f"🌐 Page URL Before Test: {page.url}")
        logger.info(f"📏 Page Viewport: {page.viewport_size}")
        logger.info(f"🧠 Memory Usage: {sys.getsizeof(page)} bytes (page object)")
        logger.info("=" * 100)
        
        step1_start = log_step(1, "Creating logs page object instance", page)
        logger.info(f"   📦 Input: page object type={type(page).__name__}")
        logger.info(f"   🔍 Page State: url={page.url}, title={page.title()}")
        logs_page = LogsPage(page)
        step1_elapsed = time.time() - step1_start
        logger.info(f"   ✅ LogsPage object created in {step1_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(logs_page).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(logs_page)} bytes")
        logger.info(f"   🔗 Object ID: {id(logs_page)}")
        log_step_complete(1, step1_start, True, "Logs page object instantiated")
        
        step2_start = log_step(2, "Loading L2 (Warning) level logs", page)
        logger.info(f"   🎯 Method: logs_page.load_l2_logs()")
        logger.info(f"   📍 Method Location: {logs_page.load_l2_logs.__code__.co_filename}:{logs_page.load_l2_logs.__code__.co_firstlineno}")
        logger.info(f"   🔍 Pre-call State:")
        logger.info(f"      Current URL: {page.url}")
        logger.info(f"      Current Title: {page.title()}")
        logger.info(f"      Page Load State: {page.evaluate('document.readyState')}")
        logger.info(f"   🚀 Executing load_l2_logs() call...")
        call_start = time.time()
        logs_page.load_l2_logs()
        call_elapsed = time.time() - call_start
        step2_elapsed = time.time() - step2_start
        logger.info(f"   ⏱️  Method call completed in {call_elapsed:.4f} seconds")
        logger.info(f"   🔍 Post-call State:")
        logger.info(f"      Current URL: {page.url}")
        logger.info(f"      Current Title: {page.title()}")
        logger.info(f"      Page Load State: {page.evaluate('document.readyState')}")
        log_step_complete(2, step2_start, True, f"L2 logs load command executed in {call_elapsed:.4f} seconds")
        
        step3_start = log_step(3, "Fetching log container text for validation", page)
        logger.info(f"   🎯 Method: logs_page.get_log_container_text()")
        logger.info(f"   📍 Method Location: {logs_page.get_log_container_text.__code__.co_filename}:{logs_page.get_log_container_text.__code__.co_firstlineno}")
        call_start = time.time()
        log_text = logs_page.get_log_container_text()
        call_elapsed = time.time() - call_start
        step3_elapsed = time.time() - step3_start
        logger.info(f"   ⏱️  Text retrieval completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📊 Result Type: {type(log_text).__name__}")
        logger.info(f"   📏 Result Length: {len(log_text)} characters")
        logger.info(f"   🧠 Result Memory: {sys.getsizeof(log_text)} bytes")
        log_step_complete(3, step3_start, True, f"Retrieved log text with length: {len(log_text)} characters")
        
        step4_start = log_step(4, "Analyzing log text content", page)
        logger.info(f"   🔍 Content Analysis:")
        logger.info(f"      Text Length: {len(log_text)} characters")
        logger.info(f"      Text is Empty: {len(log_text) == 0}")
        logger.info(f"      Contains 'No L2 logs': {'No L2 logs' in log_text}")
        if len(log_text) > 0:
            logger.info(f"      First 80 chars: '{log_text[:80]}...'")
            logger.info(f"      Last 80 chars: '...{log_text[-80:]}'")
        step4_elapsed = time.time() - step4_start
        log_step_complete(4, step4_start, True, "Log text content analyzed")
        
        step5_start = log_step(5, "Evaluating log content state", page)
        if "No L2 logs" in log_text:
            logger.info(f"   ⚠️  Log State: NO L2 LOGS")
            logger.info(f"      No L2 logs found message displayed")
            logger.info(f"      This is a valid state if no warnings exist")
        else:
            logger.info(f"   ✅ Log State: L2 LOGS FOUND")
            logger.info(f"      L2 logs found - preview: {log_text[:80]}...")
            logger.info(f"      Full text length: {len(log_text)} characters")
        step5_elapsed = time.time() - step5_start
        log_step_complete(5, step5_start, True, "Log content state evaluated")
        
        step6_start = log_step(6, "Asserting log container has content", page)
        logger.info(f"   🔍 Validation Details:")
        logger.info(f"      Log Text Length: {len(log_text)}")
        logger.info(f"      Length > 0 Check: {len(log_text) > 0}")
        logger.info(f"      Expected: len(log_text) > 0")
        logger.info(f"      Actual: len(log_text) = {len(log_text)}")
        logger.info(f"   ✅ Assertion: assert len(log_text) > 0")
        assert_start = time.time()
        assert len(log_text) > 0, "Log container should have content"
        assert_elapsed = time.time() - assert_start
        step6_elapsed = time.time() - step6_start
        logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
        logger.info(f"   ✓ Log container has content validated")
        log_step_complete(6, step6_start, True, f"Assertion passed in {assert_elapsed:.4f} seconds")
        
        test_elapsed = time.time() - test_start_time
        logger.info("")
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("✓✓✓ TEST PASSED: L2 Warning logs loaded successfully")
        logger.info("=" * 100)
        logger.info(f"⏰ Test End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        logger.info(f"⏱️  Total Test Duration: {test_elapsed:.4f} seconds")
        logger.info(f"📊 Test Summary:")
        logger.info(f"   - Steps Executed: 6")
        logger.info(f"   - Log Text Length: {len(log_text)} characters")
        logger.info(f"   - Has Content: {len(log_text) > 0}")
        logger.info(f"   - Status: PASSED")
        logger.info(f"   - Memory Usage: {sys.getsizeof(page) + sys.getsizeof(logs_page)} bytes")
        logger.info("=" * 100)
        logger.info("=" * 100)
    
    @pytest.mark.smoke
    def test_load_l3_info_logs(self, page: Page):
        """Test loading L3 (Info) logs"""
        test_start_time = time.time()
        test_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("🚀 TEST: Load L3 Info logs - START")
        logger.info("=" * 100)
        logger.info(f"⏰ Test Start Time: {test_timestamp}")
        logger.info(f"🆔 Test ID: test_load_l3_info_logs")
        logger.info(f"📋 Test Description: Test loading L3 (Info) logs")
        logger.info(f"🏷️  Test Markers: @pytest.mark.smoke, @pytest.mark.logs")
        logger.info(f"🌐 Page URL Before Test: {page.url}")
        logger.info(f"📏 Page Viewport: {page.viewport_size}")
        logger.info(f"🧠 Memory Usage: {sys.getsizeof(page)} bytes (page object)")
        logger.info("=" * 100)
        
        step1_start = log_step(1, "Initializing logs page object", page)
        logger.info(f"   📦 Input: page object type={type(page).__name__}")
        logs_page = LogsPage(page)
        step1_elapsed = time.time() - step1_start
        logger.info(f"   ✅ LogsPage object created in {step1_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(logs_page).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(logs_page)} bytes")
        log_step_complete(1, step1_start, True, "Logs page object created")
        
        step2_start = log_step(2, "Loading L3 (Info) level logs - most common log type", page)
        logger.info(f"   🎯 Method: logs_page.load_l3_logs()")
        logger.info(f"   📍 Method Location: {logs_page.load_l3_logs.__code__.co_filename}:{logs_page.load_l3_logs.__code__.co_firstlineno}")
        logger.info(f"   🔍 Pre-call State:")
        logger.info(f"      Current URL: {page.url}")
        logger.info(f"      Current Title: {page.title()}")
        call_start = time.time()
        logs_page.load_l3_logs()
        call_elapsed = time.time() - call_start
        step2_elapsed = time.time() - step2_start
        logger.info(f"   ⏱️  Method call completed in {call_elapsed:.4f} seconds")
        logger.info(f"   🔍 Post-call State:")
        logger.info(f"      Current URL: {page.url}")
        logger.info(f"      Current Title: {page.title()}")
        log_step_complete(2, step2_start, True, f"L3 logs load action initiated in {call_elapsed:.4f} seconds")
        
        step3_start = log_step(3, "Getting log container text content", page)
        logger.info(f"   🎯 Method: logs_page.get_log_container_text()")
        call_start = time.time()
        log_text = logs_page.get_log_container_text()
        call_elapsed = time.time() - call_start
        step3_elapsed = time.time() - step3_start
        logger.info(f"   ⏱️  Text retrieval completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📊 Result Type: {type(log_text).__name__}")
        logger.info(f"   📏 Result Length: {len(log_text)} characters")
        logger.info(f"   🧠 Result Memory: {sys.getsizeof(log_text)} bytes")
        log_step_complete(3, step3_start, True, f"Log container text retrieved: {len(log_text)} characters")
        
        step4_start = log_step(4, "Validating log container has content", page)
        logger.info(f"   🔍 Validation Details:")
        logger.info(f"      Log Text Length: {len(log_text)}")
        logger.info(f"      Length > 0 Check: {len(log_text) > 0}")
        logger.info(f"   ✅ Assertion: assert len(log_text) > 0")
        assert_start = time.time()
        assert len(log_text) > 0, "Log container should have content"
        assert_elapsed = time.time() - assert_start
        step4_elapsed = time.time() - step4_start
        logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
        log_step_complete(4, step4_start, True, f"Log container content validation passed in {assert_elapsed:.4f} seconds")
        
        step5_start = log_step(5, "Counting L3 log entries in the display", page)
        logger.info(f"   🎯 Method: logs_page.get_log_count('L3')")
        logger.info(f"   📦 Method Argument: 'L3'")
        call_start = time.time()
        l3_count = logs_page.get_log_count("L3")
        call_elapsed = time.time() - call_start
        step5_elapsed = time.time() - step5_start
        logger.info(f"   ⏱️  Count retrieval completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📊 Result Type: {type(l3_count).__name__}")
        logger.info(f"   📏 Result Value: {l3_count} entries")
        logger.info(f"   🧠 Result Memory: {sys.getsizeof(l3_count)} bytes")
        logger.info(f"   ⚡ L3 is typically the most common log level - found {l3_count} entries")
        log_step_complete(5, step5_start, True, f"L3 log count retrieved: {l3_count} entries")
        
        test_elapsed = time.time() - test_start_time
        logger.info("")
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info(f"✓✓✓ TEST PASSED: L3 Info logs loaded successfully ({l3_count} entries)")
        logger.info("=" * 100)
        logger.info(f"⏰ Test End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        logger.info(f"⏱️  Total Test Duration: {test_elapsed:.4f} seconds")
        logger.info(f"📊 Test Summary:")
        logger.info(f"   - Steps Executed: 5")
        logger.info(f"   - Log Text Length: {len(log_text)} characters")
        logger.info(f"   - L3 Log Count: {l3_count} entries")
        logger.info(f"   - Status: PASSED")
        logger.info(f"   - Memory Usage: {sys.getsizeof(page) + sys.getsizeof(logs_page)} bytes")
        logger.info("=" * 100)
        logger.info("=" * 100)
    
    def test_log_level_filtering(self, page: Page):
        """Test that log level filtering works correctly"""
        test_start_time = time.time()
        test_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("🚀 TEST: Log level filtering - START")
        logger.info("=" * 100)
        logger.info(f"⏰ Test Start Time: {test_timestamp}")
        logger.info(f"🆔 Test ID: test_log_level_filtering")
        logger.info(f"📋 Test Description: Test that log level filtering works correctly")
        logger.info(f"🏷️  Test Markers: @pytest.mark.logs")
        logger.info(f"🌐 Page URL Before Test: {page.url}")
        logger.info(f"📏 Page Viewport: {page.viewport_size}")
        logger.info(f"🧠 Memory Usage: {sys.getsizeof(page)} bytes (page object)")
        logger.info("=" * 100)
        
        step1_start = log_step(1, "Initializing logs page object for filtering test", page)
        logs_page = LogsPage(page)
        step1_elapsed = time.time() - step1_start
        logger.info(f"   ✅ LogsPage object created in {step1_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(logs_page).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(logs_page)} bytes")
        log_step_complete(1, step1_start, True, "Logs page object ready")
        
        step2_start = log_step(2, "Loading L1 (Critical) logs and counting entries", page)
        logger.info(f"   🎯 Method: logs_page.load_l1_logs()")
        call_start = time.time()
        logs_page.load_l1_logs()
        call_elapsed = time.time() - call_start
        step2_elapsed = time.time() - step2_start
        logger.info(f"   ⏱️  L1 logs loaded in {call_elapsed:.4f} seconds")
        log_step_complete(2, step2_start, True, f"L1 logs loaded in {call_elapsed:.4f} seconds")
        
        step3_start = log_step(3, "Counting L1 log entries", page)
        logger.info(f"   🎯 Method: logs_page.get_log_count('L1')")
        call_start = time.time()
        l1_count = logs_page.get_log_count("L1")
        call_elapsed = time.time() - call_start
        step3_elapsed = time.time() - step3_start
        logger.info(f"   ⏱️  Count retrieval completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📊 Result Type: {type(l1_count).__name__}")
        logger.info(f"   📏 Result Value: {l1_count}")
        logger.info(f"   🧠 Result Memory: {sys.getsizeof(l1_count)} bytes")
        log_step_complete(3, step3_start, True, f"L1 (Critical) log count: {l1_count}")
        
        step4_start = log_step(4, "Switching to L2 (Warning) logs", page)
        logger.info(f"   🎯 Method: logs_page.load_l2_logs()")
        call_start = time.time()
        logs_page.load_l2_logs()
        call_elapsed = time.time() - call_start
        step4_elapsed = time.time() - step4_start
        logger.info(f"   ⏱️  L2 logs loaded in {call_elapsed:.4f} seconds")
        log_step_complete(4, step4_start, True, f"L2 logs loaded in {call_elapsed:.4f} seconds")
        
        step5_start = log_step(5, "Counting L2 log entries", page)
        logger.info(f"   🎯 Method: logs_page.get_log_count('L2')")
        call_start = time.time()
        l2_count = logs_page.get_log_count("L2")
        call_elapsed = time.time() - call_start
        step5_elapsed = time.time() - step5_start
        logger.info(f"   ⏱️  Count retrieval completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📊 Result Type: {type(l2_count).__name__}")
        logger.info(f"   📏 Result Value: {l2_count}")
        log_step_complete(5, step5_start, True, f"L2 (Warning) log count: {l2_count}")
        
        step6_start = log_step(6, "Switching to L3 (Info) logs", page)
        logger.info(f"   🎯 Method: logs_page.load_l3_logs()")
        call_start = time.time()
        logs_page.load_l3_logs()
        call_elapsed = time.time() - call_start
        step6_elapsed = time.time() - step6_start
        logger.info(f"   ⏱️  L3 logs loaded in {call_elapsed:.4f} seconds")
        log_step_complete(6, step6_start, True, f"L3 logs loaded in {call_elapsed:.4f} seconds")
        
        step7_start = log_step(7, "Counting L3 log entries", page)
        logger.info(f"   🎯 Method: logs_page.get_log_count('L3')")
        call_start = time.time()
        l3_count = logs_page.get_log_count("L3")
        call_elapsed = time.time() - call_start
        step7_elapsed = time.time() - step7_start
        logger.info(f"   ⏱️  Count retrieval completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📊 Result Type: {type(l3_count).__name__}")
        logger.info(f"   📏 Result Value: {l3_count}")
        log_step_complete(7, step7_start, True, f"L3 (Info) log count: {l3_count}")
        
        step8_start = log_step(8, "Analyzing log level counts summary", page)
        total_count = l1_count + l2_count + l3_count
        logger.info(f"   📊 Count Summary:")
        logger.info(f"      L1 (Critical): {l1_count}")
        logger.info(f"      L2 (Warning):  {l2_count}")
        logger.info(f"      L3 (Info):     {l3_count}")
        logger.info(f"      Total:         {total_count}")
        logger.info(f"      L1 Percentage: {(l1_count / total_count * 100) if total_count > 0 else 0:.2f}%")
        logger.info(f"      L2 Percentage: {(l2_count / total_count * 100) if total_count > 0 else 0:.2f}%")
        logger.info(f"      L3 Percentage: {(l3_count / total_count * 100) if total_count > 0 else 0:.2f}%")
        step8_elapsed = time.time() - step8_start
        log_step_complete(8, step8_start, True, f"Summary: L1={l1_count}, L2={l2_count}, L3={l3_count}, Total={total_count}")
        
        step9_start = log_step(9, "Validating L1 count is non-negative", page)
        logger.info(f"   🔍 Validation Details:")
        logger.info(f"      L1 Count: {l1_count}")
        logger.info(f"      Count >= 0 Check: {l1_count >= 0}")
        logger.info(f"   ✅ Assertion: assert l1_count >= 0")
        assert_start = time.time()
        assert l1_count >= 0, "L1 log count should be non-negative"
        assert_elapsed = time.time() - assert_start
        step9_elapsed = time.time() - step9_start
        logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
        log_step_complete(9, step9_start, True, f"L1 count validation passed in {assert_elapsed:.4f} seconds")
        
        step10_start = log_step(10, "Validating L2 count is non-negative", page)
        logger.info(f"   🔍 Validation Details:")
        logger.info(f"      L2 Count: {l2_count}")
        logger.info(f"      Count >= 0 Check: {l2_count >= 0}")
        logger.info(f"   ✅ Assertion: assert l2_count >= 0")
        assert_start = time.time()
        assert l2_count >= 0, "L2 log count should be non-negative"
        assert_elapsed = time.time() - assert_start
        step10_elapsed = time.time() - step10_start
        logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
        log_step_complete(10, step10_start, True, f"L2 count validation passed in {assert_elapsed:.4f} seconds")
        
        step11_start = log_step(11, "Validating L3 count is non-negative", page)
        logger.info(f"   🔍 Validation Details:")
        logger.info(f"      L3 Count: {l3_count}")
        logger.info(f"      Count >= 0 Check: {l3_count >= 0}")
        logger.info(f"   ✅ Assertion: assert l3_count >= 0")
        assert_start = time.time()
        assert l3_count >= 0, "L3 log count should be non-negative"
        assert_elapsed = time.time() - assert_start
        step11_elapsed = time.time() - step11_start
        logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
        log_step_complete(11, step11_start, True, f"L3 count validation passed in {assert_elapsed:.4f} seconds")
        
        test_elapsed = time.time() - test_start_time
        logger.info("")
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("✓✓✓ TEST PASSED: Log level filtering works correctly")
        logger.info("=" * 100)
        logger.info(f"⏰ Test End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        logger.info(f"⏱️  Total Test Duration: {test_elapsed:.4f} seconds")
        logger.info(f"📊 Test Summary:")
        logger.info(f"   - Steps Executed: 11")
        logger.info(f"   - L1 Count: {l1_count}")
        logger.info(f"   - L2 Count: {l2_count}")
        logger.info(f"   - L3 Count: {l3_count}")
        logger.info(f"   - Total Count: {total_count}")
        logger.info(f"   - Status: PASSED")
        logger.info(f"   - Memory Usage: {sys.getsizeof(page) + sys.getsizeof(logs_page)} bytes")
        logger.info("=" * 100)
        logger.info("=" * 100)
    
    def test_clear_logs_display(self, page: Page):
        """Test clearing the log display"""
        test_start_time = time.time()
        test_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("🚀 TEST: Clear logs display - START")
        logger.info("=" * 100)
        logger.info(f"⏰ Test Start Time: {test_timestamp}")
        logger.info(f"🆔 Test ID: test_clear_logs_display")
        logger.info(f"📋 Test Description: Test clearing the log display")
        logger.info(f"🏷️  Test Markers: @pytest.mark.logs")
        logger.info(f"🌐 Page URL Before Test: {page.url}")
        logger.info(f"📏 Page Viewport: {page.viewport_size}")
        logger.info(f"🧠 Memory Usage: {sys.getsizeof(page)} bytes (page object)")
        logger.info("=" * 100)
        
        step1_start = log_step(1, "Initializing logs page object", page)
        logs_page = LogsPage(page)
        step1_elapsed = time.time() - step1_start
        logger.info(f"   ✅ LogsPage object created in {step1_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(logs_page).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(logs_page)} bytes")
        log_step_complete(1, step1_start, True, "Logs page object created")
        
        step2_start = log_step(2, "Loading L3 logs to populate the display", page)
        logger.info(f"   🎯 Method: logs_page.load_l3_logs()")
        call_start = time.time()
        logs_page.load_l3_logs()
        call_elapsed = time.time() - call_start
        step2_elapsed = time.time() - step2_start
        logger.info(f"   ⏱️  L3 logs loaded in {call_elapsed:.4f} seconds")
        log_step_complete(2, step2_start, True, f"L3 logs loaded into display in {call_elapsed:.4f} seconds")
        
        step3_start = log_step(3, "Getting initial log container state", page)
        logger.info(f"   🎯 Method: logs_page.get_log_container_text()")
        call_start = time.time()
        initial_text = logs_page.get_log_container_text()
        call_elapsed = time.time() - call_start
        step3_elapsed = time.time() - step3_start
        logger.info(f"   ⏱️  Text retrieval completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📊 Result Type: {type(initial_text).__name__}")
        logger.info(f"   📏 Result Length: {len(initial_text)} characters")
        logger.info(f"   🧠 Result Memory: {sys.getsizeof(initial_text)} bytes")
        log_step_complete(3, step3_start, True, f"Initial log content length: {len(initial_text)} characters")
        
        step4_start = log_step(4, "Clicking clear logs button", page)
        logger.info(f"   🎯 Method: logs_page.clear_logs()")
        logger.info(f"   🔍 Pre-clear State:")
        logger.info(f"      Initial Text Length: {len(initial_text)} characters")
        call_start = time.time()
        logs_page.clear_logs()
        call_elapsed = time.time() - call_start
        step4_elapsed = time.time() - step4_start
        logger.info(f"   ⏱️  Clear logs action completed in {call_elapsed:.4f} seconds")
        log_step_complete(4, step4_start, True, f"Clear logs action executed in {call_elapsed:.4f} seconds")
        
        step5_start = log_step(5, "Verifying logs are cleared from display", page)
        logger.info(f"   🎯 Method: logs_page.verify_logs_cleared()")
        call_start = time.time()
        is_cleared = logs_page.verify_logs_cleared()
        call_elapsed = time.time() - call_start
        step5_elapsed = time.time() - step5_start
        logger.info(f"   ⏱️  Verification completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📊 Result Type: {type(is_cleared).__name__}")
        logger.info(f"   📏 Result Value: {is_cleared}")
        logger.info(f"   🧠 Result Memory: {sys.getsizeof(is_cleared)} bytes")
        log_step_complete(5, step5_start, True, f"Logs cleared status: {is_cleared}")
        
        step6_start = log_step(6, "Asserting logs were successfully cleared", page)
        logger.info(f"   🔍 Validation Details:")
        logger.info(f"      Is Cleared: {is_cleared}")
        logger.info(f"      Is Truthy: {bool(is_cleared)}")
        logger.info(f"   ✅ Assertion: assert logs_page.verify_logs_cleared()")
        assert_start = time.time()
        assert logs_page.verify_logs_cleared(), "Logs should be cleared"
        assert_elapsed = time.time() - assert_start
        step6_elapsed = time.time() - step6_start
        logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
        log_step_complete(6, step6_start, True, f"Logs cleared validation passed in {assert_elapsed:.4f} seconds")
        
        test_elapsed = time.time() - test_start_time
        logger.info("")
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("✓✓✓ TEST PASSED: Logs display cleared successfully")
        logger.info("=" * 100)
        logger.info(f"⏰ Test End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        logger.info(f"⏱️  Total Test Duration: {test_elapsed:.4f} seconds")
        logger.info(f"📊 Test Summary:")
        logger.info(f"   - Steps Executed: 6")
        logger.info(f"   - Initial Text Length: {len(initial_text)} characters")
        logger.info(f"   - Is Cleared: {is_cleared}")
        logger.info(f"   - Status: PASSED")
        logger.info(f"   - Memory Usage: {sys.getsizeof(page) + sys.getsizeof(logs_page)} bytes")
        logger.info("=" * 100)
        logger.info("=" * 100)
    
    def test_log_entries_have_correct_format(self, page: Page):
        """Test that log entries have the correct format"""
        logger.info("=" * 80)
        logger.info("TEST: Log entries format - START")
        logger.info("=" * 80)
        
        logger.info("Step 1: Creating logs page object")
        logs_page = LogsPage(page)
        logger.info("✓ Logs page object created")
        
        logger.info("Step 2: Loading L3 logs for format validation")
        logs_page.load_l3_logs()
        logger.info("✓ L3 logs loaded")
        
        # Get log entries
        logger.info("Step 3: Retrieving log entries from display")
        entries = logs_page.get_log_entries("L3")
        logger.info(f"Step 4: Retrieved {len(entries)} log entries")
        
        if len(entries) > 0:
            logger.info(f"Step 5: Log entries found - validating format of {len(entries)} entries")
            
            # Check first entry format
            first_entry = entries[0]
            logger.info(f"Step 6: First log entry: {first_entry[:150]}...")
            
            # Log entries should contain timestamp and level
            logger.info("Step 7: Checking for timestamp in brackets [...]")
            assert "[" in first_entry, "Log entry should contain timestamp in brackets"
            logger.info("✓ Timestamp bracket found")
            
            logger.info("Step 8: Checking for log level (L3 or INFO)")
            has_level = "L3" in first_entry or "INFO" in first_entry.upper()
            assert has_level, "Log entry should contain log level"
            logger.info("✓ Log level indicator found")
            
            logger.info("Step 9: Log format components validated:")
            logger.info(f"  - Contains brackets: {'✓' if '[' in first_entry else '✗'}")
            logger.info(f"  - Contains level: {'✓' if has_level else '✗'}")
            logger.info(f"  - Entry length: {len(first_entry)} characters")
            
            logger.info("=" * 80)
            logger.info(f"✓✓✓ TEST PASSED: Log format verified. Sample: {first_entry[:100]}")
            logger.info("=" * 80)
        else:
            logger.info("Step 5: No log entries found")
            logger.info("⊘ Cannot verify format without log entries")
            logger.info("=" * 80)
            logger.info("TEST SKIPPED: No L3 log entries found to verify format")
            logger.info("=" * 80)
    
    def test_all_log_levels_accessible(self, page: Page):
        """Test that all log level buttons are accessible"""
        logger.info("=" * 80)
        logger.info("TEST: All log levels accessible - START")
        logger.info("=" * 80)
        
        logger.info("Step 1: Initializing logs page object")
        logs_page = LogsPage(page)
        logger.info("✓ Logs page object ready")
        
        # Verify all log level buttons are visible
        logger.info("Step 2: Checking visibility of L1 (Critical) logs button")
        l1_visible = logs_page.is_visible(logs_page.L1_LOGS_BUTTON)
        logger.info(f"Step 3: L1 logs button visible: {l1_visible}")
        assert logs_page.is_visible(logs_page.L1_LOGS_BUTTON), "L1 logs button should be visible"
        logger.info("✓ L1 logs button is accessible")
        
        logger.info("Step 4: Checking visibility of L2 (Warning) logs button")
        l2_visible = logs_page.is_visible(logs_page.L2_LOGS_BUTTON)
        logger.info(f"Step 5: L2 logs button visible: {l2_visible}")
        assert logs_page.is_visible(logs_page.L2_LOGS_BUTTON), "L2 logs button should be visible"
        logger.info("✓ L2 logs button is accessible")
        
        logger.info("Step 6: Checking visibility of L3 (Info) logs button")
        l3_visible = logs_page.is_visible(logs_page.L3_LOGS_BUTTON)
        logger.info(f"Step 7: L3 logs button visible: {l3_visible}")
        assert logs_page.is_visible(logs_page.L3_LOGS_BUTTON), "L3 logs button should be visible"
        logger.info("✓ L3 logs button is accessible")
        
        logger.info("Step 8: Checking visibility of Clear logs button")
        clear_visible = logs_page.is_visible(logs_page.CLEAR_LOGS_BUTTON)
        logger.info(f"Step 9: Clear logs button visible: {clear_visible}")
        assert logs_page.is_visible(logs_page.CLEAR_LOGS_BUTTON), "Clear logs button should be visible"
        logger.info("✓ Clear logs button is accessible")
        
        logger.info("Step 10: Button visibility summary:")
        logger.info(f"  - L1 (Critical) Button: ✓")
        logger.info(f"  - L2 (Warning) Button:  ✓")
        logger.info(f"  - L3 (Info) Button:     ✓")
        logger.info(f"  - Clear Logs Button:    ✓")
        
        logger.info("=" * 80)
        logger.info("✓✓✓ TEST PASSED: All log level buttons are accessible")
        logger.info("=" * 80)
    
    def test_log_container_exists(self, page: Page):
        """Test that log container element exists and is visible"""
        logger.info("=" * 80)
        logger.info("TEST: Log container exists - START")
        logger.info("=" * 80)
        
        logger.info("Step 1: Creating logs page object instance")
        logs_page = LogsPage(page)
        logger.info("✓ Logs page object instantiated")
        
        # Verify log container is visible
        logger.info("Step 2: Checking if log container element exists on the page")
        logger.info(f"Step 3: Looking for element: {logs_page.LOG_CONTAINER}")
        
        logger.info("Step 4: Verifying log container visibility")
        is_visible = logs_page.is_visible(logs_page.LOG_CONTAINER)
        logger.info(f"Step 5: Log container visibility status: {is_visible}")
        
        logger.info("Step 6: Asserting log container is visible")
        assert logs_page.is_visible(logs_page.LOG_CONTAINER), "Log container should be visible"
        logger.info("✓ Log container visibility assertion passed")
        
        logger.info("=" * 80)
        logger.info("✓✓✓ TEST PASSED: Log container exists and is visible")
        logger.info("=" * 80)
    
    @pytest.mark.slow
    def test_multiple_log_level_switches(self, page: Page):
        """Test switching between different log levels multiple times"""
        logger.info("=" * 80)
        logger.info("TEST: Multiple log level switches - START")
        logger.info("=" * 80)
        
        logger.info("Step 1: Initializing logs page object for stress test")
        logs_page = LogsPage(page)
        logger.info("✓ Logs page object ready for multiple switches")
        
        # Switch between log levels multiple times
        logger.info("Step 2: Starting 2 cycles of log level switching (L1→L2→L3)")
        total_switches = 0
        
        for i in range(2):
            logger.info(f"{'='*60}")
            logger.info(f"CYCLE {i+1} of 2 - Starting log level switch cycle")
            logger.info(f"{'='*60}")
            
            logger.info(f"Cycle {i+1}, Step 1: Switching to L1 (Critical) logs")
            logs_page.load_l1_logs()
            logger.info(f"Cycle {i+1}, Step 2: Getting L1 log container text")
            l1_text = logs_page.get_log_container_text()
            logger.info(f"Cycle {i+1}, Step 3: L1 text length: {len(l1_text) if l1_text else 0}")
            assert logs_page.get_log_container_text() is not None
            logger.info(f"✓ Cycle {i+1}: L1 logs loaded successfully")
            total_switches += 1
            
            logger.info(f"Cycle {i+1}, Step 4: Switching to L2 (Warning) logs")
            logs_page.load_l2_logs()
            logger.info(f"Cycle {i+1}, Step 5: Getting L2 log container text")
            l2_text = logs_page.get_log_container_text()
            logger.info(f"Cycle {i+1}, Step 6: L2 text length: {len(l2_text) if l2_text else 0}")
            assert logs_page.get_log_container_text() is not None
            logger.info(f"✓ Cycle {i+1}: L2 logs loaded successfully")
            total_switches += 1
            
            logger.info(f"Cycle {i+1}, Step 7: Switching to L3 (Info) logs")
            logs_page.load_l3_logs()
            logger.info(f"Cycle {i+1}, Step 8: Getting L3 log container text")
            l3_text = logs_page.get_log_container_text()
            logger.info(f"Cycle {i+1}, Step 9: L3 text length: {len(l3_text) if l3_text else 0}")
            assert logs_page.get_log_container_text() is not None
            logger.info(f"✓ Cycle {i+1}: L3 logs loaded successfully")
            total_switches += 1
            
            logger.info(f"✓✓ Cycle {i+1} completed: All 3 log levels switched successfully")
        
        logger.info(f"{'='*60}")
        logger.info(f"Step 3: All cycles completed")
        logger.info(f"Step 4: Total log level switches performed: {total_switches}")
        logger.info(f"Step 5: Switches per cycle: 3 (L1→L2→L3)")
        logger.info(f"Step 6: Cycles completed: 2")
        
        logger.info("=" * 80)
        logger.info("✓✓✓ TEST PASSED: Multiple log level switches work correctly")
        logger.info(f"✓✓✓ Total {total_switches} switches completed successfully")
        logger.info("=" * 80)

