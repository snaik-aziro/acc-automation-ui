"""
Dashboard Page Object for Aziro Cluster Center
Handles all dashboard-related interactions
"""

from playwright.sync_api import Page
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class DashboardPage(BasePage):
    """Dashboard page object with all dashboard interactions"""
    
    # Page elements
    HEADER_TITLE = ".header h1"
    HEADER_DESCRIPTION = ".header p"
    
    # Tab navigation
    TAB_DASHBOARD = '[data-testid="dashboard-tab"]'
    TAB_VMS = '[data-testid="vms-tab"]'
    TAB_CREATE = '[data-testid="create-tab"]'
    TAB_LOGS = '[data-testid="logs-tab"]'
    
    # Dashboard metrics
    TOTAL_VMS_VALUE = '[data-testid="total-vms-value"]'
    RUNNING_VMS_VALUE = '[data-testid="running-vms-value"]'
    SYSTEM_CPU_VALUE = '[data-testid="system-cpu-value"]'
    SYSTEM_MEMORY_VALUE = '[data-testid="system-memory-value"]'
    
    # Tab content areas
    DASHBOARD_CONTENT = '[data-testid="dashboard-content"]'
    VMS_CONTENT = '[data-testid="vms-content"]'
    CREATE_CONTENT = '[data-testid="create-content"]'
    LOGS_CONTENT = '[data-testid="logs-content"]'
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def load_dashboard(self):
        """Navigate to dashboard and wait for it to load"""
        logger.info("Loading dashboard")
        self.navigate_to()
        self.wait_for_selector(self.TAB_DASHBOARD)
        logger.info("Dashboard loaded successfully")
    
    def get_page_title(self) -> str:
        """Get the page title from header"""
        return self.get_text(self.HEADER_TITLE)
    
    def get_page_description(self) -> str:
        """Get the page description from header"""
        return self.get_text(self.HEADER_DESCRIPTION)
    
    def click_dashboard_tab(self):
        """Click on Dashboard tab"""
        logger.info("Clicking Dashboard tab")
        self.click_element(self.TAB_DASHBOARD)
        self.wait_for_selector(self.DASHBOARD_CONTENT)
    
    def click_vms_tab(self):
        """Click on Virtual Machines tab"""
        logger.info("Clicking VMs tab")
        self.click_element(self.TAB_VMS)
        self.wait_for_selector(self.VMS_CONTENT)
    
    def click_create_tab(self):
        """Click on Create VM tab"""
        logger.info("Clicking Create VM tab")
        self.click_element(self.TAB_CREATE)
        self.wait_for_selector(self.CREATE_CONTENT)
    
    def click_logs_tab(self):
        """Click on System Logs tab"""
        logger.info("Clicking Logs tab")
        self.click_element(self.TAB_LOGS)
        self.wait_for_selector(self.LOGS_CONTENT)
    
    def get_total_vms_count(self) -> int:
        """Get total VMs count from dashboard"""
        text = self.get_text(self.TOTAL_VMS_VALUE)
        logger.info(f"Total VMs: {text}")
        return int(text)
    
    def get_running_vms_count(self) -> int:
        """Get running VMs count from dashboard"""
        text = self.get_text(self.RUNNING_VMS_VALUE)
        logger.info(f"Running VMs: {text}")
        return int(text)
    
    def get_system_cpu_usage(self) -> str:
        """Get system CPU usage from dashboard"""
        text = self.get_text(self.SYSTEM_CPU_VALUE)
        logger.info(f"System CPU: {text}")
        return text
    
    def get_system_memory_usage(self) -> str:
        """Get system memory usage from dashboard"""
        text = self.get_text(self.SYSTEM_MEMORY_VALUE)
        logger.info(f"System Memory: {text}")
        return text
    
    def verify_dashboard_loaded(self) -> bool:
        """Verify dashboard has loaded properly"""
        logger.info("Verifying dashboard loaded")
        
        # Check if key elements are visible
        checks = [
            self.is_visible(self.HEADER_TITLE),
            self.is_visible(self.TAB_DASHBOARD),
            self.is_visible(self.TOTAL_VMS_VALUE),
            self.is_visible(self.RUNNING_VMS_VALUE),
            self.is_visible(self.SYSTEM_CPU_VALUE),
            self.is_visible(self.SYSTEM_MEMORY_VALUE)
        ]
        
        result = all(checks)
        logger.info(f"Dashboard verification: {'PASSED' if result else 'FAILED'}")
        return result
    
    def is_tab_active(self, tab_selector: str) -> bool:
        """Check if a tab is currently active"""
        element = self.page.locator(tab_selector)
        classes = element.get_attribute("class")
        return "active" in classes

