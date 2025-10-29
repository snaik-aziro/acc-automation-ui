"""
Dashboard Tests for Aziro Cluster Center
Tests for dashboard functionality and metrics display
"""

import pytest
from playwright.sync_api import Page, expect
from pages.dashboard_page import DashboardPage
import logging

logger = logging.getLogger(__name__)


@pytest.mark.dashboard
@pytest.mark.smoke
class TestDashboard:
    """Test suite for Dashboard functionality"""
    
    def test_dashboard_loads_successfully(self, page: Page):
        """Test that dashboard loads with all expected elements"""
        logger.info("TEST: Dashboard loads successfully")
        
        # Initialize page object
        dashboard = DashboardPage(page)
        dashboard.load_dashboard()
        
        # Verify dashboard loaded
        assert dashboard.verify_dashboard_loaded(), "Dashboard did not load properly"
        
        # Verify page title
        title = dashboard.get_page_title()
        assert "Aziro Cluster Center" in title, f"Expected title to contain 'Aziro Cluster Center', got: {title}"
        
        # Verify page description
        description = dashboard.get_page_description()
        assert "Enterprise-grade" in description, "Page description not found"
        
        logger.info("✓ Dashboard loaded successfully")
    
    def test_dashboard_displays_metrics(self, page: Page):
        """Test that dashboard displays all metric cards"""
        logger.info("TEST: Dashboard displays metrics")
        
        dashboard = DashboardPage(page)
        dashboard.load_dashboard()
        
        # Get all metrics
        total_vms = dashboard.get_total_vms_count()
        running_vms = dashboard.get_running_vms_count()
        cpu_usage = dashboard.get_system_cpu_usage()
        memory_usage = dashboard.get_system_memory_usage()
        
        # Verify metrics are numbers/percentages
        assert isinstance(total_vms, int), "Total VMs should be an integer"
        assert isinstance(running_vms, int), "Running VMs should be an integer"
        assert "%" in cpu_usage, "CPU usage should be a percentage"
        assert "%" in memory_usage, "Memory usage should be a percentage"
        
        # Verify running VMs <= total VMs
        assert running_vms <= total_vms, f"Running VMs ({running_vms}) should not exceed Total VMs ({total_vms})"
        
        logger.info(f"✓ Metrics: Total VMs={total_vms}, Running={running_vms}, CPU={cpu_usage}, Memory={memory_usage}")
    
    def test_tab_navigation_works(self, page: Page):
        """Test that tab navigation works correctly"""
        logger.info("TEST: Tab navigation works")
        
        dashboard = DashboardPage(page)
        dashboard.load_dashboard()
        
        # Test Dashboard tab (should be active by default)
        assert dashboard.is_tab_active(dashboard.TAB_DASHBOARD), "Dashboard tab should be active by default"
        
        # Navigate to VMs tab
        dashboard.click_vms_tab()
        assert dashboard.is_visible(dashboard.VMS_CONTENT), "VMs content should be visible"
        assert dashboard.is_tab_active(dashboard.TAB_VMS), "VMs tab should be active"
        
        # Navigate to Create tab
        dashboard.click_create_tab()
        assert dashboard.is_visible(dashboard.CREATE_CONTENT), "Create content should be visible"
        assert dashboard.is_tab_active(dashboard.TAB_CREATE), "Create tab should be active"
        
        # Navigate to Logs tab
        dashboard.click_logs_tab()
        assert dashboard.is_visible(dashboard.LOGS_CONTENT), "Logs content should be visible"
        assert dashboard.is_tab_active(dashboard.TAB_LOGS), "Logs tab should be active"
        
        # Navigate back to Dashboard tab
        dashboard.click_dashboard_tab()
        assert dashboard.is_visible(dashboard.DASHBOARD_CONTENT), "Dashboard content should be visible"
        assert dashboard.is_tab_active(dashboard.TAB_DASHBOARD), "Dashboard tab should be active"
        
        logger.info("✓ Tab navigation works correctly")
    
    def test_dashboard_header_content(self, page: Page):
        """Test dashboard header displays correct branding"""
        logger.info("TEST: Dashboard header content")
        
        dashboard = DashboardPage(page)
        dashboard.load_dashboard()
        
        # Check header elements
        header_title = dashboard.get_page_title()
        assert "🏢" in header_title, "Header should contain building emoji"
        assert "Aziro Cluster Center" in header_title, "Header should contain application name"
        
        header_desc = dashboard.get_page_description()
        assert len(header_desc) > 0, "Header description should not be empty"
        assert "virtual machine" in header_desc.lower(), "Description should mention virtual machines"
        
        logger.info("✓ Dashboard header content is correct")
    
    @pytest.mark.slow
    def test_dashboard_metrics_are_numeric(self, page: Page):
        """Test that dashboard metrics contain valid numeric values"""
        logger.info("TEST: Dashboard metrics are numeric")
        
        dashboard = DashboardPage(page)
        dashboard.load_dashboard()
        
        # Verify total VMs is non-negative
        total_vms = dashboard.get_total_vms_count()
        assert total_vms >= 0, "Total VMs should be non-negative"
        
        # Verify running VMs is non-negative
        running_vms = dashboard.get_running_vms_count()
        assert running_vms >= 0, "Running VMs should be non-negative"
        
        # Verify CPU usage is a valid percentage
        cpu_text = dashboard.get_system_cpu_usage()
        cpu_value = int(cpu_text.replace("%", ""))
        assert 0 <= cpu_value <= 100, f"CPU usage should be between 0-100%, got {cpu_value}%"
        
        # Verify memory usage is a valid percentage
        memory_text = dashboard.get_system_memory_usage()
        memory_value = int(memory_text.replace("%", ""))
        assert 0 <= memory_value <= 100, f"Memory usage should be between 0-100%, got {memory_value}%"
        
        logger.info("✓ All dashboard metrics are valid numeric values")

