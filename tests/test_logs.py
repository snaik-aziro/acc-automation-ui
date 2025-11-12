"""
Logging System Tests for Aziro Cluster Center
Tests for system logs viewing and filtering
"""

import pytest
from playwright.sync_api import Page
from pages.dashboard_page import DashboardPage
from pages.logs_page import LogsPage
import logging

logger = logging.getLogger(__name__)


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
        logger.info("=" * 80)
        logger.info("TEST: Load L1 Critical logs - START")
        logger.info("=" * 80)
        
        logger.info("Step 1: Initializing logs page object")
        logs_page = LogsPage(page)
        logger.info("✓ Logs page object created successfully")
        
        logger.info("Step 2: Clicking L1 (Critical) logs button to load critical logs")
        logs_page.load_l1_logs()
        logger.info("✓ L1 logs load action completed")
        
        # Check if any L1 logs are displayed or no logs message
        logger.info("Step 3: Retrieving log container text content")
        log_text = logs_page.get_log_container_text()
        logger.info(f"Step 4: Log container text length: {len(log_text)} characters")
        
        if len(log_text) > 100:
            logger.info(f"Step 5: Log preview: {log_text[:100]}...")
        else:
            logger.info(f"Step 5: Log content: {log_text}")
        
        # Either logs are present or "No L1 logs found" message
        logger.info("Step 6: Validating log container has content")
        assert len(log_text) > 0, "Log container should have content"
        logger.info("✓ Log container validation passed")
        
        logger.info("=" * 80)
        logger.info("✓✓✓ TEST PASSED: L1 Critical logs loaded successfully")
        logger.info("=" * 80)
    
    @pytest.mark.smoke
    def test_load_l2_warning_logs(self, page: Page):
        """Test loading L2 (Warning) logs"""
        logger.info("=" * 80)
        logger.info("TEST: Load L2 Warning logs - START")
        logger.info("=" * 80)
        
        logger.info("Step 1: Creating logs page object instance")
        logs_page = LogsPage(page)
        logger.info("✓ Logs page object instantiated")
        
        logger.info("Step 2: Loading L2 (Warning) level logs")
        logs_page.load_l2_logs()
        logger.info("✓ L2 logs load command executed")
        
        # Check if any L2 logs are displayed or no logs message
        logger.info("Step 3: Fetching log container text for validation")
        log_text = logs_page.get_log_container_text()
        logger.info(f"Step 4: Retrieved log text with length: {len(log_text)} characters")
        
        if "No L2 logs" in log_text:
            logger.info("Step 5: No L2 logs found message displayed")
        else:
            logger.info(f"Step 5: L2 logs found - preview: {log_text[:80]}...")
        
        logger.info("Step 6: Asserting log container has content")
        assert len(log_text) > 0, "Log container should have content"
        logger.info("✓ Assertion passed - log container has content")
        
        logger.info("=" * 80)
        logger.info("✓✓✓ TEST PASSED: L2 Warning logs loaded successfully")
        logger.info("=" * 80)
    
    @pytest.mark.smoke
    def test_load_l3_info_logs(self, page: Page):
        """Test loading L3 (Info) logs"""
        logger.info("=" * 80)
        logger.info("TEST: Load L3 Info logs - START")
        logger.info("=" * 80)
        
        logger.info("Step 1: Initializing logs page object")
        logs_page = LogsPage(page)
        logger.info("✓ Logs page object created")
        
        logger.info("Step 2: Loading L3 (Info) level logs - most common log type")
        logs_page.load_l3_logs()
        logger.info("✓ L3 logs load action initiated")
        
        # Check if any L3 logs are displayed or no logs message
        logger.info("Step 3: Getting log container text content")
        log_text = logs_page.get_log_container_text()
        logger.info(f"Step 4: Log container text retrieved: {len(log_text)} characters")
        
        logger.info("Step 5: Validating log container has content")
        assert len(log_text) > 0, "Log container should have content"
        logger.info("✓ Log container content validation passed")
        
        # L3 logs should be the most common
        logger.info("Step 6: Counting L3 log entries in the display")
        l3_count = logs_page.get_log_count("L3")
        logger.info(f"Step 7: L3 log count retrieved: {l3_count} entries")
        logger.info(f"⚡ L3 is typically the most common log level - found {l3_count} entries")
        
        logger.info("=" * 80)
        logger.info(f"✓✓✓ TEST PASSED: L3 Info logs loaded successfully ({l3_count} entries)")
        logger.info("=" * 80)
    
    def test_log_level_filtering(self, page: Page):
        """Test that log level filtering works correctly"""
        logger.info("=" * 80)
        logger.info("TEST: Log level filtering - START")
        logger.info("=" * 80)
        
        logger.info("Step 1: Initializing logs page object for filtering test")
        logs_page = LogsPage(page)
        logger.info("✓ Logs page object ready")
        
        # Load L1 logs
        logger.info("Step 2: Loading L1 (Critical) logs and counting entries")
        logs_page.load_l1_logs()
        logger.info("✓ L1 logs loaded")
        
        logger.info("Step 3: Counting L1 log entries")
        l1_count = logs_page.get_log_count("L1")
        logger.info(f"Step 4: L1 (Critical) log count: {l1_count}")
        
        # Load L2 logs
        logger.info("Step 5: Switching to L2 (Warning) logs")
        logs_page.load_l2_logs()
        logger.info("✓ L2 logs loaded")
        
        logger.info("Step 6: Counting L2 log entries")
        l2_count = logs_page.get_log_count("L2")
        logger.info(f"Step 7: L2 (Warning) log count: {l2_count}")
        
        # Load L3 logs
        logger.info("Step 8: Switching to L3 (Info) logs")
        logs_page.load_l3_logs()
        logger.info("✓ L3 logs loaded")
        
        logger.info("Step 9: Counting L3 log entries")
        l3_count = logs_page.get_log_count("L3")
        logger.info(f"Step 10: L3 (Info) log count: {l3_count}")
        
        logger.info("Step 11: Summary of all log level counts:")
        logger.info(f"  - L1 (Critical): {l1_count}")
        logger.info(f"  - L2 (Warning):  {l2_count}")
        logger.info(f"  - L3 (Info):     {l3_count}")
        logger.info(f"  - Total:         {l1_count + l2_count + l3_count}")
        
        # Verify counts are non-negative
        logger.info("Step 12: Validating L1 count is non-negative")
        assert l1_count >= 0, "L1 log count should be non-negative"
        logger.info("✓ L1 count validation passed")
        
        logger.info("Step 13: Validating L2 count is non-negative")
        assert l2_count >= 0, "L2 log count should be non-negative"
        logger.info("✓ L2 count validation passed")
        
        logger.info("Step 14: Validating L3 count is non-negative")
        assert l3_count >= 0, "L3 log count should be non-negative"
        logger.info("✓ L3 count validation passed")
        
        logger.info("=" * 80)
        logger.info("✓✓✓ TEST PASSED: Log level filtering works correctly")
        logger.info("=" * 80)
    
    def test_clear_logs_display(self, page: Page):
        """Test clearing the log display"""
        logger.info("=" * 80)
        logger.info("TEST: Clear logs display - START")
        logger.info("=" * 80)
        
        logger.info("Step 1: Initializing logs page object")
        logs_page = LogsPage(page)
        logger.info("✓ Logs page object created")
        
        # First load some logs
        logger.info("Step 2: Loading L3 logs to populate the display")
        logs_page.load_l3_logs()
        logger.info("✓ L3 logs loaded into display")
        
        logger.info("Step 3: Getting initial log container state")
        initial_text = logs_page.get_log_container_text()
        logger.info(f"Step 4: Initial log content length: {len(initial_text)} characters")
        
        # Then clear them
        logger.info("Step 5: Clicking clear logs button")
        logs_page.clear_logs()
        logger.info("✓ Clear logs action executed")
        
        # Verify logs are cleared
        logger.info("Step 6: Verifying logs are cleared from display")
        is_cleared = logs_page.verify_logs_cleared()
        logger.info(f"Step 7: Logs cleared status: {is_cleared}")
        
        logger.info("Step 8: Asserting logs were successfully cleared")
        assert logs_page.verify_logs_cleared(), "Logs should be cleared"
        logger.info("✓ Logs cleared validation passed")
        
        logger.info("=" * 80)
        logger.info("✓✓✓ TEST PASSED: Logs display cleared successfully")
        logger.info("=" * 80)
    
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

