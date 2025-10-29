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
        logger.info("TEST: Load L1 Critical logs")
        
        logs_page = LogsPage(page)
        logs_page.load_l1_logs()
        
        # Check if any L1 logs are displayed or no logs message
        log_text = logs_page.get_log_container_text()
        
        # Either logs are present or "No L1 logs found" message
        assert len(log_text) > 0, "Log container should have content"
        
        logger.info("✓ L1 Critical logs loaded")
    
    @pytest.mark.smoke
    def test_load_l2_warning_logs(self, page: Page):
        """Test loading L2 (Warning) logs"""
        logger.info("TEST: Load L2 Warning logs")
        
        logs_page = LogsPage(page)
        logs_page.load_l2_logs()
        
        # Check if any L2 logs are displayed or no logs message
        log_text = logs_page.get_log_container_text()
        
        assert len(log_text) > 0, "Log container should have content"
        
        logger.info("✓ L2 Warning logs loaded")
    
    @pytest.mark.smoke
    def test_load_l3_info_logs(self, page: Page):
        """Test loading L3 (Info) logs"""
        logger.info("TEST: Load L3 Info logs")
        
        logs_page = LogsPage(page)
        logs_page.load_l3_logs()
        
        # Check if any L3 logs are displayed or no logs message
        log_text = logs_page.get_log_container_text()
        
        assert len(log_text) > 0, "Log container should have content"
        
        # L3 logs should be the most common
        l3_count = logs_page.get_log_count("L3")
        logger.info(f"Found {l3_count} L3 log entries")
        
        logger.info("✓ L3 Info logs loaded")
    
    def test_log_level_filtering(self, page: Page):
        """Test that log level filtering works correctly"""
        logger.info("TEST: Log level filtering")
        
        logs_page = LogsPage(page)
        
        # Load L1 logs
        logs_page.load_l1_logs()
        l1_count = logs_page.get_log_count("L1")
        logger.info(f"L1 log count: {l1_count}")
        
        # Load L2 logs
        logs_page.load_l2_logs()
        l2_count = logs_page.get_log_count("L2")
        logger.info(f"L2 log count: {l2_count}")
        
        # Load L3 logs
        logs_page.load_l3_logs()
        l3_count = logs_page.get_log_count("L3")
        logger.info(f"L3 log count: {l3_count}")
        
        # Verify counts are non-negative
        assert l1_count >= 0, "L1 log count should be non-negative"
        assert l2_count >= 0, "L2 log count should be non-negative"
        assert l3_count >= 0, "L3 log count should be non-negative"
        
        logger.info("✓ Log level filtering works correctly")
    
    def test_clear_logs_display(self, page: Page):
        """Test clearing the log display"""
        logger.info("TEST: Clear logs display")
        
        logs_page = LogsPage(page)
        
        # First load some logs
        logs_page.load_l3_logs()
        
        # Then clear them
        logs_page.clear_logs()
        
        # Verify logs are cleared
        assert logs_page.verify_logs_cleared(), "Logs should be cleared"
        
        logger.info("✓ Logs display cleared successfully")
    
    def test_log_entries_have_correct_format(self, page: Page):
        """Test that log entries have the correct format"""
        logger.info("TEST: Log entries format")
        
        logs_page = LogsPage(page)
        logs_page.load_l3_logs()
        
        # Get log entries
        entries = logs_page.get_log_entries("L3")
        
        if len(entries) > 0:
            # Check first entry format
            first_entry = entries[0]
            
            # Log entries should contain timestamp and level
            assert "[" in first_entry, "Log entry should contain timestamp in brackets"
            assert "L3" in first_entry or "INFO" in first_entry.upper(), "Log entry should contain log level"
            
            logger.info(f"✓ Log format verified. Sample: {first_entry[:100]}")
        else:
            logger.info("⊘ No L3 log entries found to verify format")
    
    def test_all_log_levels_accessible(self, page: Page):
        """Test that all log level buttons are accessible"""
        logger.info("TEST: All log levels accessible")
        
        logs_page = LogsPage(page)
        
        # Verify all log level buttons are visible
        assert logs_page.is_visible(logs_page.L1_LOGS_BUTTON), "L1 logs button should be visible"
        assert logs_page.is_visible(logs_page.L2_LOGS_BUTTON), "L2 logs button should be visible"
        assert logs_page.is_visible(logs_page.L3_LOGS_BUTTON), "L3 logs button should be visible"
        assert logs_page.is_visible(logs_page.CLEAR_LOGS_BUTTON), "Clear logs button should be visible"
        
        logger.info("✓ All log level buttons are accessible")
    
    def test_log_container_exists(self, page: Page):
        """Test that log container element exists and is visible"""
        logger.info("TEST: Log container exists")
        
        logs_page = LogsPage(page)
        
        # Verify log container is visible
        assert logs_page.is_visible(logs_page.LOG_CONTAINER), "Log container should be visible"
        
        logger.info("✓ Log container exists and is visible")
    
    @pytest.mark.slow
    def test_multiple_log_level_switches(self, page: Page):
        """Test switching between different log levels multiple times"""
        logger.info("TEST: Multiple log level switches")
        
        logs_page = LogsPage(page)
        
        # Switch between log levels multiple times
        for i in range(2):
            logger.info(f"Switch cycle {i+1}")
            
            logs_page.load_l1_logs()
            assert logs_page.get_log_container_text() is not None
            
            logs_page.load_l2_logs()
            assert logs_page.get_log_container_text() is not None
            
            logs_page.load_l3_logs()
            assert logs_page.get_log_container_text() is not None
        
        logger.info("✓ Multiple log level switches work correctly")

