"""
Base Page Object for Aziro Cluster Center
Contains common methods used across all pages
"""

from playwright.sync_api import Page, expect
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """Base page object with common functionality"""
    
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "http://localhost:8082"
        self.api_url = "http://localhost:5000/api"
    
    def navigate_to(self, url: str = None):
        """Navigate to specified URL or base URL"""
        target_url = url if url else self.base_url
        logger.info(f"Navigating to: {target_url}")
        self.page.goto(target_url, wait_until="domcontentloaded")
    
    def click_element(self, selector: str, timeout: int = 10000):
        """Click an element with logging"""
        logger.info(f"Clicking element: {selector}")
        self.page.click(selector, timeout=timeout)
    
    def fill_input(self, selector: str, value: str, timeout: int = 10000):
        """Fill input field with logging"""
        logger.info(f"Filling '{selector}' with value: {value}")
        self.page.fill(selector, value, timeout=timeout)
    
    def select_option(self, selector: str, value: str, timeout: int = 10000):
        """Select dropdown option with logging"""
        logger.info(f"Selecting '{value}' from '{selector}'")
        self.page.select_option(selector, value, timeout=timeout)
    
    def get_text(self, selector: str, timeout: int = 10000) -> str:
        """Get text content of an element"""
        logger.info(f"Getting text from: {selector}")
        return self.page.text_content(selector, timeout=timeout)
    
    def wait_for_selector(self, selector: str, timeout: int = 10000):
        """Wait for selector to be visible"""
        logger.info(f"Waiting for selector: {selector}")
        self.page.wait_for_selector(selector, timeout=timeout, state="visible")
    
    def is_visible(self, selector: str) -> bool:
        """Check if element is visible"""
        return self.page.is_visible(selector)
    
    def wait_for_alert(self, alert_type: str = "success", timeout: int = 10000):
        """Wait for success or error alert to appear"""
        selector = f".alert.{alert_type}"
        logger.info(f"Waiting for {alert_type} alert")
        self.page.wait_for_selector(selector, timeout=timeout)
        return self.get_text(selector)
    
    def get_alert_message(self, alert_type: str = "success") -> str:
        """Get alert message text"""
        selector = f".alert.{alert_type}"
        if self.is_visible(selector):
            return self.get_text(selector)
        return None
    
    def take_screenshot(self, name: str):
        """Take a screenshot with specified name"""
        screenshot_path = f"reports/screenshots/{name}.png"
        logger.info(f"Taking screenshot: {screenshot_path}")
        self.page.screenshot(path=screenshot_path)
    
    def wait_for_page_load(self):
        """Wait for page to fully load"""
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_load_state("networkidle")

