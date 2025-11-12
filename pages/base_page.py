"""
Base Page Object for Aziro Cluster Center
Contains common methods used across all pages
"""

from playwright.sync_api import Page, expect
import logging
import time
import sys
from datetime import datetime

logger = logging.getLogger(__name__)


class BasePage:
    """Base page object with common functionality"""
    
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "http://localhost:8082"
        self.api_url = "http://localhost:5000/api"
        logger.debug(f"BasePage.__init__() - Initializing BasePage object")
        logger.debug(f"BasePage.__init__() - Page object type: {type(page).__name__}")
        logger.debug(f"BasePage.__init__() - Page object ID: {id(page)}")
        logger.debug(f"BasePage.__init__() - Base URL: {self.base_url}")
        logger.debug(f"BasePage.__init__() - API URL: {self.api_url}")
        logger.debug(f"BasePage.__init__() - Current page URL: {page.url}")
        logger.debug(f"BasePage.__init__() - Current page title: {page.title()}")
        logger.debug(f"BasePage.__init__() - Page viewport size: {page.viewport_size}")
        logger.debug(f"BasePage.__init__() - Memory usage (self): {sys.getsizeof(self)} bytes")
        logger.debug(f"BasePage.__init__() - Memory usage (page): {sys.getsizeof(page)} bytes")
        logger.info(f"BasePage initialized successfully")
    
    def navigate_to(self, url: str = None):
        """Navigate to specified URL or base URL"""
        start_time = time.time()
        target_url = url if url else self.base_url
        logger.debug(f"BasePage.navigate_to() - Method called")
        logger.debug(f"BasePage.navigate_to() - Input URL parameter: {url}")
        logger.debug(f"BasePage.navigate_to() - Resolved target URL: {target_url}")
        logger.debug(f"BasePage.navigate_to() - Current page URL before navigation: {self.page.url}")
        logger.debug(f"BasePage.navigate_to() - Current page title before navigation: {self.page.title()}")
        logger.debug(f"BasePage.navigate_to() - Page ready state before navigation: {self.page.evaluate('document.readyState')}")
        logger.info(f"Navigating to: {target_url}")
        logger.debug(f"BasePage.navigate_to() - Calling page.goto() with wait_until='domcontentloaded'")
        nav_start = time.time()
        self.page.goto(target_url, wait_until="domcontentloaded")
        nav_elapsed = time.time() - nav_start
        total_elapsed = time.time() - start_time
        logger.debug(f"BasePage.navigate_to() - Navigation completed in {nav_elapsed:.4f} seconds")
        logger.debug(f"BasePage.navigate_to() - Total method execution time: {total_elapsed:.4f} seconds")
        logger.debug(f"BasePage.navigate_to() - New page URL after navigation: {self.page.url}")
        logger.debug(f"BasePage.navigate_to() - New page title after navigation: {self.page.title()}")
        logger.debug(f"BasePage.navigate_to() - Page ready state after navigation: {self.page.evaluate('document.readyState')}")
        logger.info(f"Navigation completed successfully in {nav_elapsed:.4f} seconds")
    
    def click_element(self, selector: str, timeout: int = 10000):
        """Click an element with extensive logging"""
        start_time = time.time()
        logger.debug(f"BasePage.click_element() - Method called")
        logger.debug(f"BasePage.click_element() - Selector: {selector}")
        logger.debug(f"BasePage.click_element() - Timeout: {timeout}ms")
        logger.debug(f"BasePage.click_element() - Current page URL: {self.page.url}")
        logger.debug(f"BasePage.click_element() - Current page title: {self.page.title()}")
        logger.debug(f"BasePage.click_element() - Checking if element exists before click")
        try:
            element = self.page.locator(selector)
            logger.debug(f"BasePage.click_element() - Element locator created successfully")
            logger.debug(f"BasePage.click_element() - Element count: {element.count()}")
            if element.count() > 0:
                logger.debug(f"BasePage.click_element() - Element is present in DOM")
                logger.debug(f"BasePage.click_element() - Element visibility: {element.is_visible()}")
                logger.debug(f"BasePage.click_element() - Element enabled state: {element.is_enabled()}")
                try:
                    bbox = element.bounding_box()
                    logger.debug(f"BasePage.click_element() - Element bounding box: {bbox}")
                except:
                    logger.debug(f"BasePage.click_element() - Could not get bounding box")
        except Exception as e:
            logger.debug(f"BasePage.click_element() - Error checking element: {e}")
        logger.info(f"Clicking element: {selector}")
        click_start = time.time()
        self.page.click(selector, timeout=timeout)
        click_elapsed = time.time() - click_start
        total_elapsed = time.time() - start_time
        logger.debug(f"BasePage.click_element() - Click action completed in {click_elapsed:.4f} seconds")
        logger.debug(f"BasePage.click_element() - Total method execution time: {total_elapsed:.4f} seconds")
        logger.debug(f"BasePage.click_element() - Page URL after click: {self.page.url}")
        logger.debug(f"BasePage.click_element() - Page title after click: {self.page.title()}")
        logger.info(f"Element clicked successfully in {click_elapsed:.4f} seconds")
    
    def fill_input(self, selector: str, value: str, timeout: int = 10000):
        """Fill input field with extensive logging"""
        start_time = time.time()
        logger.debug(f"BasePage.fill_input() - Method called")
        logger.debug(f"BasePage.fill_input() - Selector: {selector}")
        logger.debug(f"BasePage.fill_input() - Value type: {type(value).__name__}")
        logger.debug(f"BasePage.fill_input() - Value length: {len(str(value))} characters")
        logger.debug(f"BasePage.fill_input() - Value content: {value}")
        logger.debug(f"BasePage.fill_input() - Timeout: {timeout}ms")
        logger.debug(f"BasePage.fill_input() - Memory usage of value: {sys.getsizeof(value)} bytes")
        logger.debug(f"BasePage.fill_input() - Current page URL: {self.page.url}")
        try:
            element = self.page.locator(selector)
            logger.debug(f"BasePage.fill_input() - Element locator created")
            logger.debug(f"BasePage.fill_input() - Element count: {element.count()}")
            if element.count() > 0:
                logger.debug(f"BasePage.fill_input() - Getting current input value before fill")
                try:
                    current_value = element.input_value()
                    logger.debug(f"BasePage.fill_input() - Current input value: {current_value}")
                    logger.debug(f"BasePage.fill_input() - Current value length: {len(current_value)} characters")
                except:
                    logger.debug(f"BasePage.fill_input() - Could not get current input value")
        except Exception as e:
            logger.debug(f"BasePage.fill_input() - Error checking element: {e}")
        logger.info(f"Filling '{selector}' with value: {value}")
        fill_start = time.time()
        self.page.fill(selector, value, timeout=timeout)
        fill_elapsed = time.time() - fill_start
        total_elapsed = time.time() - start_time
        logger.debug(f"BasePage.fill_input() - Fill action completed in {fill_elapsed:.4f} seconds")
        logger.debug(f"BasePage.fill_input() - Total method execution time: {total_elapsed:.4f} seconds")
        try:
            new_value = self.page.locator(selector).input_value()
            logger.debug(f"BasePage.fill_input() - New input value after fill: {new_value}")
            logger.debug(f"BasePage.fill_input() - New value length: {len(new_value)} characters")
            logger.debug(f"BasePage.fill_input() - Value match: {new_value == str(value)}")
        except:
            logger.debug(f"BasePage.fill_input() - Could not verify new input value")
        logger.info(f"Input filled successfully in {fill_elapsed:.4f} seconds")
    
    def select_option(self, selector: str, value: str, timeout: int = 10000):
        """Select dropdown option with extensive logging"""
        start_time = time.time()
        logger.debug(f"BasePage.select_option() - Method called")
        logger.debug(f"BasePage.select_option() - Selector: {selector}")
        logger.debug(f"BasePage.select_option() - Option value: {value}")
        logger.debug(f"BasePage.select_option() - Value type: {type(value).__name__}")
        logger.debug(f"BasePage.select_option() - Timeout: {timeout}ms")
        logger.debug(f"BasePage.select_option() - Current page URL: {self.page.url}")
        try:
            select_element = self.page.locator(selector)
            logger.debug(f"BasePage.select_option() - Select element locator created")
            logger.debug(f"BasePage.select_option() - Select element count: {select_element.count()}")
            if select_element.count() > 0:
                logger.debug(f"BasePage.select_option() - Getting all available options")
                try:
                    options = select_element.locator("option").all()
                    logger.debug(f"BasePage.select_option() - Total options found: {len(options)}")
                    option_values = []
                    for idx, opt in enumerate(options):
                        opt_value = opt.get_attribute("value")
                        opt_text = opt.text_content()
                        option_values.append(f"Option {idx}: value='{opt_value}', text='{opt_text}'")
                        logger.debug(f"BasePage.select_option() - {option_values[-1]}")
                    logger.debug(f"BasePage.select_option() - Available option values: {[opt.get_attribute('value') for opt in options]}")
                    logger.debug(f"BasePage.select_option() - Target value '{value}' in options: {value in [opt.get_attribute('value') for opt in options]}")
                except Exception as e:
                    logger.debug(f"BasePage.select_option() - Error getting options: {e}")
                try:
                    current_value = select_element.input_value()
                    logger.debug(f"BasePage.select_option() - Current selected value: {current_value}")
                except:
                    logger.debug(f"BasePage.select_option() - Could not get current selected value")
        except Exception as e:
            logger.debug(f"BasePage.select_option() - Error checking select element: {e}")
        logger.info(f"Selecting '{value}' from '{selector}'")
        select_start = time.time()
        self.page.select_option(selector, value, timeout=timeout)
        select_elapsed = time.time() - select_start
        total_elapsed = time.time() - start_time
        logger.debug(f"BasePage.select_option() - Select action completed in {select_elapsed:.4f} seconds")
        logger.debug(f"BasePage.select_option() - Total method execution time: {total_elapsed:.4f} seconds")
        try:
            new_value = self.page.locator(selector).input_value()
            logger.debug(f"BasePage.select_option() - New selected value after selection: {new_value}")
            logger.debug(f"BasePage.select_option() - Selection match: {new_value == value}")
        except:
            logger.debug(f"BasePage.select_option() - Could not verify new selected value")
        logger.info(f"Option selected successfully in {select_elapsed:.4f} seconds")
    
    def get_text(self, selector: str, timeout: int = 10000) -> str:
        """Get text content of an element with extensive logging"""
        start_time = time.time()
        logger.debug(f"BasePage.get_text() - Method called")
        logger.debug(f"BasePage.get_text() - Selector: {selector}")
        logger.debug(f"BasePage.get_text() - Timeout: {timeout}ms")
        logger.debug(f"BasePage.get_text() - Current page URL: {self.page.url}")
        try:
            element = self.page.locator(selector)
            logger.debug(f"BasePage.get_text() - Element locator created")
            logger.debug(f"BasePage.get_text() - Element count: {element.count()}")
            if element.count() > 0:
                logger.debug(f"BasePage.get_text() - Element visibility: {element.is_visible()}")
        except Exception as e:
            logger.debug(f"BasePage.get_text() - Error checking element: {e}")
        logger.info(f"Getting text from: {selector}")
        get_start = time.time()
        text_content = self.page.text_content(selector, timeout=timeout)
        get_elapsed = time.time() - get_start
        total_elapsed = time.time() - start_time
        logger.debug(f"BasePage.get_text() - Text retrieval completed in {get_elapsed:.4f} seconds")
        logger.debug(f"BasePage.get_text() - Total method execution time: {total_elapsed:.4f} seconds")
        logger.debug(f"BasePage.get_text() - Text content type: {type(text_content).__name__}")
        logger.debug(f"BasePage.get_text() - Text content length: {len(text_content) if text_content else 0} characters")
        logger.debug(f"BasePage.get_text() - Text content memory: {sys.getsizeof(text_content) if text_content else 0} bytes")
        if text_content:
            preview = text_content[:100] + "..." if len(text_content) > 100 else text_content
            logger.debug(f"BasePage.get_text() - Text content preview: {preview}")
        logger.info(f"Text retrieved successfully: {len(text_content) if text_content else 0} characters")
        return text_content
    
    def wait_for_selector(self, selector: str, timeout: int = 10000):
        """Wait for selector to be visible with extensive logging"""
        start_time = time.time()
        logger.debug(f"BasePage.wait_for_selector() - Method called")
        logger.debug(f"BasePage.wait_for_selector() - Selector: {selector}")
        logger.debug(f"BasePage.wait_for_selector() - Timeout: {timeout}ms")
        logger.debug(f"BasePage.wait_for_selector() - Wait state: visible")
        logger.debug(f"BasePage.wait_for_selector() - Current page URL: {self.page.url}")
        logger.debug(f"BasePage.wait_for_selector() - Current page title: {self.page.title()}")
        logger.debug(f"BasePage.wait_for_selector() - Page ready state: {self.page.evaluate('document.readyState')}")
        logger.info(f"Waiting for selector: {selector}")
        wait_start = time.time()
        self.page.wait_for_selector(selector, timeout=timeout, state="visible")
        wait_elapsed = time.time() - wait_start
        total_elapsed = time.time() - start_time
        logger.debug(f"BasePage.wait_for_selector() - Wait completed in {wait_elapsed:.4f} seconds")
        logger.debug(f"BasePage.wait_for_selector() - Total method execution time: {total_elapsed:.4f} seconds")
        try:
            element = self.page.locator(selector)
            logger.debug(f"BasePage.wait_for_selector() - Element is now visible: {element.is_visible()}")
            logger.debug(f"BasePage.wait_for_selector() - Element count: {element.count()}")
        except:
            logger.debug(f"BasePage.wait_for_selector() - Could not verify element state")
        logger.info(f"Selector found and visible after {wait_elapsed:.4f} seconds")
    
    def is_visible(self, selector: str) -> bool:
        """Check if element is visible with extensive logging"""
        start_time = time.time()
        logger.debug(f"BasePage.is_visible() - Method called")
        logger.debug(f"BasePage.is_visible() - Selector: {selector}")
        logger.debug(f"BasePage.is_visible() - Current page URL: {self.page.url}")
        check_start = time.time()
        is_vis = self.page.is_visible(selector)
        check_elapsed = time.time() - check_start
        total_elapsed = time.time() - start_time
        logger.debug(f"BasePage.is_visible() - Visibility check completed in {check_elapsed:.4f} seconds")
        logger.debug(f"BasePage.is_visible() - Total method execution time: {total_elapsed:.4f} seconds")
        logger.debug(f"BasePage.is_visible() - Element visibility result: {is_vis}")
        logger.debug(f"BasePage.is_visible() - Result type: {type(is_vis).__name__}")
        logger.info(f"Element visibility check: {is_vis}")
        return is_vis
    
    def wait_for_alert(self, alert_type: str = "success", timeout: int = 10000):
        """Wait for success or error alert to appear with extensive logging"""
        start_time = time.time()
        logger.debug(f"BasePage.wait_for_alert() - Method called")
        logger.debug(f"BasePage.wait_for_alert() - Alert type: {alert_type}")
        logger.debug(f"BasePage.wait_for_alert() - Timeout: {timeout}ms")
        selector = f".alert.{alert_type}"
        logger.debug(f"BasePage.wait_for_alert() - Alert selector: {selector}")
        logger.debug(f"BasePage.wait_for_alert() - Current page URL: {self.page.url}")
        logger.info(f"Waiting for {alert_type} alert")
        wait_start = time.time()
        self.page.wait_for_selector(selector, timeout=timeout)
        wait_elapsed = time.time() - wait_start
        logger.debug(f"BasePage.wait_for_alert() - Alert appeared after {wait_elapsed:.4f} seconds")
        text_start = time.time()
        alert_text = self.get_text(selector)
        text_elapsed = time.time() - text_start
        total_elapsed = time.time() - start_time
        logger.debug(f"BasePage.wait_for_alert() - Text retrieval completed in {text_elapsed:.4f} seconds")
        logger.debug(f"BasePage.wait_for_alert() - Total method execution time: {total_elapsed:.4f} seconds")
        logger.debug(f"BasePage.wait_for_alert() - Alert text: {alert_text}")
        logger.debug(f"BasePage.wait_for_alert() - Alert text length: {len(alert_text) if alert_text else 0} characters")
        logger.info(f"Alert appeared and text retrieved: {alert_text}")
        return alert_text
    
    def get_alert_message(self, alert_type: str = "success") -> str:
        """Get alert message text with extensive logging"""
        start_time = time.time()
        logger.debug(f"BasePage.get_alert_message() - Method called")
        logger.debug(f"BasePage.get_alert_message() - Alert type: {alert_type}")
        selector = f".alert.{alert_type}"
        logger.debug(f"BasePage.get_alert_message() - Alert selector: {selector}")
        logger.debug(f"BasePage.get_alert_message() - Checking visibility")
        visibility_start = time.time()
        is_vis = self.is_visible(selector)
        visibility_elapsed = time.time() - visibility_start
        logger.debug(f"BasePage.get_alert_message() - Visibility check completed in {visibility_elapsed:.4f} seconds")
        logger.debug(f"BasePage.get_alert_message() - Alert is visible: {is_vis}")
        if is_vis:
            text_start = time.time()
            alert_text = self.get_text(selector)
            text_elapsed = time.time() - text_start
            total_elapsed = time.time() - start_time
            logger.debug(f"BasePage.get_alert_message() - Text retrieval completed in {text_elapsed:.4f} seconds")
            logger.debug(f"BasePage.get_alert_message() - Total method execution time: {total_elapsed:.4f} seconds")
            logger.debug(f"BasePage.get_alert_message() - Alert message: {alert_text}")
            logger.info(f"Alert message retrieved: {alert_text}")
            return alert_text
        else:
            total_elapsed = time.time() - start_time
            logger.debug(f"BasePage.get_alert_message() - Total method execution time: {total_elapsed:.4f} seconds")
            logger.debug(f"BasePage.get_alert_message() - Alert not visible, returning None")
            logger.info(f"Alert not visible")
            return None
    
    def take_screenshot(self, name: str):
        """Take a screenshot with extensive logging"""
        start_time = time.time()
        logger.debug(f"BasePage.take_screenshot() - Method called")
        logger.debug(f"BasePage.take_screenshot() - Screenshot name: {name}")
        screenshot_path = f"reports/screenshots/{name}.png"
        logger.debug(f"BasePage.take_screenshot() - Screenshot path: {screenshot_path}")
        logger.debug(f"BasePage.take_screenshot() - Current page URL: {self.page.url}")
        logger.debug(f"BasePage.take_screenshot() - Current page title: {self.page.title()}")
        logger.debug(f"BasePage.take_screenshot() - Page viewport: {self.page.viewport_size}")
        logger.info(f"Taking screenshot: {screenshot_path}")
        screenshot_start = time.time()
        self.page.screenshot(path=screenshot_path)
        screenshot_elapsed = time.time() - screenshot_start
        total_elapsed = time.time() - start_time
        logger.debug(f"BasePage.take_screenshot() - Screenshot captured in {screenshot_elapsed:.4f} seconds")
        logger.debug(f"BasePage.take_screenshot() - Total method execution time: {total_elapsed:.4f} seconds")
        logger.info(f"Screenshot saved successfully in {screenshot_elapsed:.4f} seconds")
    
    def wait_for_page_load(self):
        """Wait for page to fully load with extensive logging"""
        start_time = time.time()
        logger.debug(f"BasePage.wait_for_page_load() - Method called")
        logger.debug(f"BasePage.wait_for_page_load() - Current page URL: {self.page.url}")
        logger.debug(f"BasePage.wait_for_page_load() - Current page title: {self.page.title()}")
        logger.debug(f"BasePage.wait_for_page_load() - Page ready state before wait: {self.page.evaluate('document.readyState')}")
        logger.info(f"Waiting for page to load (domcontentloaded)")
        dom_start = time.time()
        self.page.wait_for_load_state("domcontentloaded")
        dom_elapsed = time.time() - dom_start
        logger.debug(f"BasePage.wait_for_page_load() - DOM content loaded in {dom_elapsed:.4f} seconds")
        logger.info(f"Waiting for page to load (networkidle)")
        network_start = time.time()
        self.page.wait_for_load_state("networkidle")
        network_elapsed = time.time() - network_start
        total_elapsed = time.time() - start_time
        logger.debug(f"BasePage.wait_for_page_load() - Network idle in {network_elapsed:.4f} seconds")
        logger.debug(f"BasePage.wait_for_page_load() - Total method execution time: {total_elapsed:.4f} seconds")
        logger.debug(f"BasePage.wait_for_page_load() - Page ready state after wait: {self.page.evaluate('document.readyState')}")
        logger.info(f"Page load completed in {total_elapsed:.4f} seconds (DOM: {dom_elapsed:.4f}s, Network: {network_elapsed:.4f}s)")

