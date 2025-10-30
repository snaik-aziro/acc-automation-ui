"""
Dashboard Tests for Aziro Cluster Center
Tests for dashboard functionality and metrics display
"""

import pytest
from playwright.sync_api import Page, expect
from pages.dashboard_page import DashboardPage
from utils.test_reporter import reporter
import logging

logger = logging.getLogger(__name__)


@pytest.mark.dashboard
@pytest.mark.smoke
class TestDashboard:
    """Test suite for Dashboard functionality"""
    
    def test_dashboard_loads_successfully(self, page: Page):
        """Test that dashboard loads with all expected elements"""
        
        # Step 1: Initialize page object
        reporter.print_test_step(1, "Initialize Dashboard Page Object", "running")
        dashboard = DashboardPage(page)
        reporter.print_test_step(1, "Initialize Dashboard Page Object", "pass")
        
        # Step 2: Load dashboard
        reporter.print_test_step(2, "Navigate to Dashboard URL", "running")
        dashboard.load_dashboard()
        reporter.print_test_step(2, "Navigate to Dashboard URL", "pass")
        
        # Step 3: Verify dashboard loaded
        reporter.print_test_step(3, "Verify Dashboard Elements Loaded", "running")
        is_loaded = dashboard.verify_dashboard_loaded()
        reporter.print_assertion(
            "Dashboard loaded successfully",
            "True",
            str(is_loaded),
            is_loaded
        )
        assert is_loaded, "Dashboard did not load properly"
        reporter.print_test_step(3, "Verify Dashboard Elements Loaded", "pass")
        
        # Step 4: Verify page title
        reporter.print_test_step(4, "Verify Page Title", "running")
        title = dashboard.get_page_title()
        title_check = "Aziro Cluster Center" in title
        reporter.print_assertion(
            "Page title contains 'Aziro Cluster Center'",
            "Aziro Cluster Center in title",
            title,
            title_check
        )
        assert title_check, f"Expected title to contain 'Aziro Cluster Center', got: {title}"
        reporter.print_test_step(4, "Verify Page Title", "pass")
        
        # Step 5: Verify page description
        reporter.print_test_step(5, "Verify Page Description", "running")
        description = dashboard.get_page_description()
        desc_check = "Enterprise-grade" in description
        reporter.print_assertion(
            "Description contains 'Enterprise-grade'",
            "Enterprise-grade in description",
            description,
            desc_check
        )
        assert desc_check, "Page description not found"
        reporter.print_test_step(5, "Verify Page Description", "pass")
        
        reporter.print_success("Dashboard loaded and verified successfully!")
    
    def test_dashboard_displays_metrics(self, page: Page):
        """Test that dashboard displays all metric cards"""
        
        # Step 1: Initialize and load dashboard
        reporter.print_test_step(1, "Initialize Dashboard and Load", "running")
        dashboard = DashboardPage(page)
        dashboard.load_dashboard()
        reporter.print_test_step(1, "Initialize Dashboard and Load", "pass")
        
        # Step 2: Get Total VMs metric
        reporter.print_test_step(2, "Get Total VMs Count", "running")
        total_vms = dashboard.get_total_vms_count()
        reporter.print_info(f"Total VMs: {total_vms}")
        reporter.print_assertion("Total VMs is integer", "int type", type(total_vms).__name__, isinstance(total_vms, int))
        assert isinstance(total_vms, int), "Total VMs should be an integer"
        reporter.print_test_step(2, "Get Total VMs Count", "pass")
        
        # Step 3: Get Running VMs metric
        reporter.print_test_step(3, "Get Running VMs Count", "running")
        running_vms = dashboard.get_running_vms_count()
        reporter.print_info(f"Running VMs: {running_vms}")
        reporter.print_assertion("Running VMs is integer", "int type", type(running_vms).__name__, isinstance(running_vms, int))
        assert isinstance(running_vms, int), "Running VMs should be an integer"
        reporter.print_test_step(3, "Get Running VMs Count", "pass")
        
        # Step 4: Get CPU Usage metric
        reporter.print_test_step(4, "Get System CPU Usage", "running")
        cpu_usage = dashboard.get_system_cpu_usage()
        reporter.print_info(f"CPU Usage: {cpu_usage}")
        cpu_check = "%" in cpu_usage
        reporter.print_assertion("CPU usage is percentage", "contains %", cpu_usage, cpu_check)
        assert cpu_check, "CPU usage should be a percentage"
        reporter.print_test_step(4, "Get System CPU Usage", "pass")
        
        # Step 5: Get Memory Usage metric
        reporter.print_test_step(5, "Get System Memory Usage", "running")
        memory_usage = dashboard.get_system_memory_usage()
        reporter.print_info(f"Memory Usage: {memory_usage}")
        memory_check = "%" in memory_usage
        reporter.print_assertion("Memory usage is percentage", "contains %", memory_usage, memory_check)
        assert memory_check, "Memory usage should be a percentage"
        reporter.print_test_step(5, "Get System Memory Usage", "pass")
        
        # Step 6: Verify logical constraint
        reporter.print_test_step(6, "Verify Running VMs <= Total VMs", "running")
        constraint_check = running_vms <= total_vms
        reporter.print_assertion(
            "Running VMs should not exceed Total VMs",
            f"Running ({running_vms}) <= Total ({total_vms})",
            f"{running_vms} <= {total_vms}",
            constraint_check
        )
        assert constraint_check, f"Running VMs ({running_vms}) should not exceed Total VMs ({total_vms})"
        reporter.print_test_step(6, "Verify Running VMs <= Total VMs", "pass")
        
        reporter.print_success(f"All metrics verified! Total={total_vms}, Running={running_vms}, CPU={cpu_usage}, Memory={memory_usage}")
    
    def test_tab_navigation_works(self, page: Page):
        """Test that tab navigation works correctly"""
        
        # Step 1: Initialize and verify default tab
        reporter.print_test_step(1, "Initialize Dashboard and Check Default Tab", "running")
        dashboard = DashboardPage(page)
        dashboard.load_dashboard()
        default_active = dashboard.is_tab_active(dashboard.TAB_DASHBOARD)
        reporter.print_assertion("Dashboard tab is active by default", "True", str(default_active), default_active)
        assert default_active, "Dashboard tab should be active by default"
        reporter.print_test_step(1, "Initialize Dashboard and Check Default Tab", "pass")
        
        # Step 2: Navigate to VMs tab
        reporter.print_test_step(2, "Navigate to VMs Tab", "running")
        dashboard.click_vms_tab()
        vms_visible = dashboard.is_visible(dashboard.VMS_CONTENT)
        vms_active = dashboard.is_tab_active(dashboard.TAB_VMS)
        reporter.print_assertion("VMs content visible", "True", str(vms_visible), vms_visible)
        reporter.print_assertion("VMs tab active", "True", str(vms_active), vms_active)
        assert vms_visible and vms_active
        reporter.print_test_step(2, "Navigate to VMs Tab", "pass")
        
        # Step 3: Navigate to Create tab
        reporter.print_test_step(3, "Navigate to Create VM Tab", "running")
        dashboard.click_create_tab()
        create_visible = dashboard.is_visible(dashboard.CREATE_CONTENT)
        create_active = dashboard.is_tab_active(dashboard.TAB_CREATE)
        reporter.print_assertion("Create content visible", "True", str(create_visible), create_visible)
        reporter.print_assertion("Create tab active", "True", str(create_active), create_active)
        assert create_visible and create_active
        reporter.print_test_step(3, "Navigate to Create VM Tab", "pass")
        
        # Step 4: Navigate to Logs tab
        reporter.print_test_step(4, "Navigate to Logs Tab", "running")
        dashboard.click_logs_tab()
        logs_visible = dashboard.is_visible(dashboard.LOGS_CONTENT)
        logs_active = dashboard.is_tab_active(dashboard.TAB_LOGS)
        reporter.print_assertion("Logs content visible", "True", str(logs_visible), logs_visible)
        reporter.print_assertion("Logs tab active", "True", str(logs_active), logs_active)
        assert logs_visible and logs_active
        reporter.print_test_step(4, "Navigate to Logs Tab", "pass")
        
        # Step 5: Navigate back to Dashboard tab
        reporter.print_test_step(5, "Navigate Back to Dashboard Tab", "running")
        dashboard.click_dashboard_tab()
        dash_visible = dashboard.is_visible(dashboard.DASHBOARD_CONTENT)
        dash_active = dashboard.is_tab_active(dashboard.TAB_DASHBOARD)
        reporter.print_assertion("Dashboard content visible", "True", str(dash_visible), dash_visible)
        reporter.print_assertion("Dashboard tab active", "True", str(dash_active), dash_active)
        assert dash_visible and dash_active
        reporter.print_test_step(5, "Navigate Back to Dashboard Tab", "pass")
        
        reporter.print_success("All tab navigation verified successfully!")
    
    def test_dashboard_header_content(self, page: Page):
        """Test dashboard header displays correct branding"""
        
        # Step 1: Load dashboard
        reporter.print_test_step(1, "Load Dashboard Page", "running")
        dashboard = DashboardPage(page)
        dashboard.load_dashboard()
        reporter.print_test_step(1, "Load Dashboard Page", "pass")
        
        # Step 2: Verify header title
        reporter.print_test_step(2, "Verify Header Title", "running")
        header_title = dashboard.get_page_title()
        reporter.print_info(f"Header Title: {header_title}")
        
        emoji_check = "🏢" in header_title
        reporter.print_assertion("Header contains building emoji", "🏢 present", header_title, emoji_check)
        assert emoji_check, "Header should contain building emoji"
        
        name_check = "Aziro Cluster Center" in header_title
        reporter.print_assertion("Header contains app name", "Aziro Cluster Center present", header_title, name_check)
        assert name_check, "Header should contain application name"
        reporter.print_test_step(2, "Verify Header Title", "pass")
        
        # Step 3: Verify header description
        reporter.print_test_step(3, "Verify Header Description", "running")
        header_desc = dashboard.get_page_description()
        reporter.print_info(f"Header Description: {header_desc[:50]}...")
        
        not_empty = len(header_desc) > 0
        reporter.print_assertion("Description not empty", "length > 0", str(len(header_desc)), not_empty)
        assert not_empty, "Header description should not be empty"
        
        vm_mentioned = "virtual machine" in header_desc.lower()
        reporter.print_assertion("Description mentions VMs", "virtual machine in text", "found" if vm_mentioned else "not found", vm_mentioned)
        assert vm_mentioned, "Description should mention virtual machines"
        reporter.print_test_step(3, "Verify Header Description", "pass")
        
        reporter.print_success("Dashboard header branding verified!")
    
    @pytest.mark.slow
    def test_dashboard_metrics_are_numeric(self, page: Page):
        """Test that dashboard metrics contain valid numeric values"""
        
        # Step 1: Load dashboard
        reporter.print_test_step(1, "Load Dashboard for Metrics Validation", "running")
        dashboard = DashboardPage(page)
        dashboard.load_dashboard()
        reporter.print_test_step(1, "Load Dashboard for Metrics Validation", "pass")
        
        # Step 2: Validate Total VMs count
        reporter.print_test_step(2, "Validate Total VMs is Non-Negative", "running")
        total_vms = dashboard.get_total_vms_count()
        total_check = total_vms >= 0
        reporter.print_assertion("Total VMs >= 0", "non-negative", str(total_vms), total_check)
        assert total_check, "Total VMs should be non-negative"
        reporter.print_test_step(2, "Validate Total VMs is Non-Negative", "pass")
        
        # Step 3: Validate Running VMs count
        reporter.print_test_step(3, "Validate Running VMs is Non-Negative", "running")
        running_vms = dashboard.get_running_vms_count()
        running_check = running_vms >= 0
        reporter.print_assertion("Running VMs >= 0", "non-negative", str(running_vms), running_check)
        assert running_check, "Running VMs should be non-negative"
        reporter.print_test_step(3, "Validate Running VMs is Non-Negative", "pass")
        
        # Step 4: Validate CPU usage percentage
        reporter.print_test_step(4, "Validate CPU Usage Percentage (0-100%)", "running")
        cpu_text = dashboard.get_system_cpu_usage()
        cpu_value = int(cpu_text.replace("%", ""))
        reporter.print_info(f"CPU Usage Value: {cpu_value}%")
        cpu_range = 0 <= cpu_value <= 100
        reporter.print_assertion("CPU in range 0-100%", "0 <= value <= 100", str(cpu_value), cpu_range)
        assert cpu_range, f"CPU usage should be between 0-100%, got {cpu_value}%"
        reporter.print_test_step(4, "Validate CPU Usage Percentage (0-100%)", "pass")
        
        # Step 5: Validate Memory usage percentage
        reporter.print_test_step(5, "Validate Memory Usage Percentage (0-100%)", "running")
        memory_text = dashboard.get_system_memory_usage()
        memory_value = int(memory_text.replace("%", ""))
        reporter.print_info(f"Memory Usage Value: {memory_value}%")
        memory_range = 0 <= memory_value <= 100
        reporter.print_assertion("Memory in range 0-100%", "0 <= value <= 100", str(memory_value), memory_range)
        assert memory_range, f"Memory usage should be between 0-100%, got {memory_value}%"
        reporter.print_test_step(5, "Validate Memory Usage Percentage (0-100%)", "pass")
        
        reporter.print_success(f"All metrics validated! Total VMs={total_vms}, Running={running_vms}, CPU={cpu_value}%, Memory={memory_value}%")

