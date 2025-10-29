"""
Logs Page Object for Aziro Cluster Center
Handles all system logs interactions
"""

from playwright.sync_api import Page
from pages.base_page import BasePage
import logging
import time

logger = logging.getLogger(__name__)


class LogsPage(BasePage):
    """Logs page object for system logs management"""
    
    # Log controls
    L1_LOGS_BUTTON = '[data-testid="l1-logs-button"]'
    L2_LOGS_BUTTON = '[data-testid="l2-logs-button"]'
    L3_LOGS_BUTTON = '[data-testid="l3-logs-button"]'
    CLEAR_LOGS_BUTTON = '[data-testid="clear-logs-button"]'
    
    # Log container
    LOG_CONTAINER = '[data-testid="log-container"]'
    LOG_ENTRY = '.log-entry'
    LOG_ENTRY_L1 = '.log-entry.L1'
    LOG_ENTRY_L2 = '.log-entry.L2'
    LOG_ENTRY_L3 = '.log-entry.L3'
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def load_l1_logs(self):
        """Load L1 (Critical) logs"""
        logger.info("Loading L1 Critical logs")
        self.click_element(self.L1_LOGS_BUTTON)
        time.sleep(3)  # Wait for logs to load
        logger.info("L1 logs loaded")
    
    def load_l2_logs(self):
        """Load L2 (Warning) logs"""
        logger.info("Loading L2 Warning logs")
        self.click_element(self.L2_LOGS_BUTTON)
        time.sleep(3)  # Wait for logs to load
        logger.info("L2 logs loaded")
    
    def load_l3_logs(self):
        """Load L3 (Info) logs"""
        logger.info("Loading L3 Info logs")
        self.click_element(self.L3_LOGS_BUTTON)
        time.sleep(3)  # Wait for logs to load
        logger.info("L3 logs loaded")
    
    def clear_logs(self):
        """Clear the log display"""
        logger.info("Clearing log display")
        self.click_element(self.CLEAR_LOGS_BUTTON)
        time.sleep(1)
    
    def get_log_count(self, level: str = None) -> int:
        """
        Get count of log entries
        
        Args:
            level: Optional log level (L1, L2, L3). If None, counts all logs.
        """
        if level:
            selector = f'.log-entry.{level}'
            count = self.page.locator(selector).count()
            logger.info(f"{level} log count: {count}")
        else:
            count = self.page.locator(self.LOG_ENTRY).count()
            logger.info(f"Total log count: {count}")
        
        return count
    
    def get_log_entries(self, level: str = None) -> list:
        """
        Get log entries as list
        
        Args:
            level: Optional log level (L1, L2, L3). If None, gets all logs.
        """
        if level:
            selector = f'.log-entry.{level}'
        else:
            selector = self.LOG_ENTRY
        
        entries = self.page.locator(selector).all()
        log_texts = [entry.text_content() for entry in entries]
        
        logger.info(f"Retrieved {len(log_texts)} log entries")
        return log_texts
    
    def verify_log_level_displayed(self, level: str) -> bool:
        """
        Verify that logs of a specific level are displayed
        
        Args:
            level: Log level to verify (L1, L2, L3)
        """
        selector = f'.log-entry.{level}'
        count = self.page.locator(selector).count()
        
        result = count > 0
        logger.info(f"Log level {level} displayed: {result} (count: {count})")
        return result
    
    def get_log_container_text(self) -> str:
        """Get the text content of the log container"""
        return self.get_text(self.LOG_CONTAINER)
    
    def verify_logs_cleared(self) -> bool:
        """Verify that logs display has been cleared"""
        text = self.get_log_container_text()
        result = "cleared" in text.lower() or self.get_log_count() == 0
        logger.info(f"Logs cleared verification: {result}")
        return result
    
    def search_log_for_text(self, search_text: str, level: str = None) -> bool:
        """
        Search for specific text in log entries
        
        Args:
            search_text: Text to search for
            level: Optional log level to search in
        """
        logger.info(f"Searching for text: '{search_text}' in logs")
        entries = self.get_log_entries(level)
        
        for entry in entries:
            if search_text.lower() in entry.lower():
                logger.info(f"Found text in log entry: {entry[:100]}")
                return True
        
        logger.info(f"Text '{search_text}' not found in logs")
        return False

