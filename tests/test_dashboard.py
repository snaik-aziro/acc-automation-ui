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
        logger.info("=" * 80)
        logger.info("TEST: Dashboard loads successfully - START")
        logger.info("=" * 80)
        
        # Step 1: Initialize page object
        logger.info("Step 1: Initializing Dashboard Page Object")
        reporter.print_test_step(1, "Initialize Dashboard Page Object", "running")
        dashboard = DashboardPage(page)
        logger.info("✓ Dashboard page object created successfully")
        reporter.print_test_step(1, "Initialize Dashboard Page Object", "pass")
        
        # Step 2: Load dashboard
        logger.info("Step 2: Navigating to Dashboard URL")
        reporter.print_test_step(2, "Navigate to Dashboard URL", "running")
        dashboard.load_dashboard()
        logger.info("✓ Dashboard URL navigation completed")
        reporter.print_test_step(2, "Navigate to Dashboard URL", "pass")
        
        # Step 3: Verify dashboard loaded
        logger.info("Step 3: Verifying dashboard elements are loaded")
        reporter.print_test_step(3, "Verify Dashboard Elements Loaded", "running")
        is_loaded = dashboard.verify_dashboard_loaded()
        logger.info(f"Step 4: Dashboard loaded status: {is_loaded}")
        reporter.print_assertion(
            "Dashboard loaded successfully",
            "True",
            str(is_loaded),
            is_loaded
        )
        logger.info("Step 5: Asserting dashboard loaded successfully")
        assert is_loaded, "Dashboard did not load properly"
        logger.info("✓ Dashboard loaded assertion passed")
        reporter.print_test_step(3, "Verify Dashboard Elements Loaded", "pass")
        
        # Step 4: Verify page title
        logger.info("Step 6: Retrieving page title")
        reporter.print_test_step(4, "Verify Page Title", "running")
        title = dashboard.get_page_title()
        logger.info(f"Step 7: Page title retrieved: '{title}'")
        title_check = "Aziro Cluster Center" in title
        logger.info(f"Step 8: Title check result: {title_check}")
        reporter.print_assertion(
            "Page title contains 'Aziro Cluster Center'",
            "Aziro Cluster Center in title",
            title,
            title_check
        )
        logger.info("Step 9: Asserting 'Aziro Cluster Center' is in title")
        assert title_check, f"Expected title to contain 'Aziro Cluster Center', got: {title}"
        logger.info("✓ Page title validation passed")
        reporter.print_test_step(4, "Verify Page Title", "pass")
        
        # Step 5: Verify page description
        logger.info("Step 10: Retrieving page description")
        reporter.print_test_step(5, "Verify Page Description", "running")
        description = dashboard.get_page_description()
        logger.info(f"Step 11: Page description retrieved: '{description[:80]}...'")
        desc_check = "Enterprise-grade" in description
        logger.info(f"Step 12: Description contains 'Enterprise-grade': {desc_check}")
        reporter.print_assertion(
            "Description contains 'Enterprise-grade'",
            "Enterprise-grade in description",
            description,
            desc_check
        )
        logger.info("Step 13: Asserting description contains 'Enterprise-grade'")
        assert desc_check, "Page description not found"
        logger.info("✓ Page description validation passed")
        reporter.print_test_step(5, "Verify Page Description", "pass")
        
        logger.info("=" * 80)
        logger.info("✓✓✓ TEST PASSED: Dashboard loaded and verified successfully!")
        logger.info("=" * 80)
        reporter.print_success("Dashboard loaded and verified successfully!")
    
    def test_dashboard_displays_metrics(self, page: Page):
        """Test that dashboard displays all metric cards"""
        logger.info("=" * 80)
        logger.info("TEST: Dashboard displays metrics - START")
        logger.info("=" * 80)
        
        # Step 1: Initialize and load dashboard
        logger.info("Step 1: Initializing dashboard and loading page")
        reporter.print_test_step(1, "Initialize Dashboard and Load", "running")
        dashboard = DashboardPage(page)
        dashboard.load_dashboard()
        logger.info("✓ Dashboard initialized and loaded")
        reporter.print_test_step(1, "Initialize Dashboard and Load", "pass")
        
        # Step 2: Get Total VMs metric
        logger.info("Step 2: Retrieving Total VMs metric from dashboard")
        reporter.print_test_step(2, "Get Total VMs Count", "running")
        total_vms = dashboard.get_total_vms_count()
        logger.info(f"Step 3: Total VMs count: {total_vms}")
        reporter.print_info(f"Total VMs: {total_vms}")
        logger.info(f"Step 4: Total VMs type: {type(total_vms).__name__}")
        reporter.print_assertion("Total VMs is integer", "int type", type(total_vms).__name__, isinstance(total_vms, int))
        logger.info("Step 5: Validating Total VMs is an integer")
        assert isinstance(total_vms, int), "Total VMs should be an integer"
        logger.info("✓ Total VMs metric validated")
        reporter.print_test_step(2, "Get Total VMs Count", "pass")
        
        # Step 3: Get Running VMs metric
        logger.info("Step 6: Retrieving Running VMs metric from dashboard")
        reporter.print_test_step(3, "Get Running VMs Count", "running")
        running_vms = dashboard.get_running_vms_count()
        logger.info(f"Step 7: Running VMs count: {running_vms}")
        reporter.print_info(f"Running VMs: {running_vms}")
        logger.info(f"Step 8: Running VMs type: {type(running_vms).__name__}")
        reporter.print_assertion("Running VMs is integer", "int type", type(running_vms).__name__, isinstance(running_vms, int))
        logger.info("Step 9: Validating Running VMs is an integer")
        assert isinstance(running_vms, int), "Running VMs should be an integer"
        logger.info("✓ Running VMs metric validated")
        reporter.print_test_step(3, "Get Running VMs Count", "pass")
        
        # Step 4: Get CPU Usage metric
        logger.info("Step 10: Retrieving System CPU Usage metric")
        reporter.print_test_step(4, "Get System CPU Usage", "running")
        cpu_usage = dashboard.get_system_cpu_usage()
        logger.info(f"Step 11: CPU Usage value: {cpu_usage}")
        reporter.print_info(f"CPU Usage: {cpu_usage}")
        cpu_check = "%" in cpu_usage
        logger.info(f"Step 12: CPU usage contains '%': {cpu_check}")
        reporter.print_assertion("CPU usage is percentage", "contains %", cpu_usage, cpu_check)
        logger.info("Step 13: Asserting CPU usage is a percentage")
        assert cpu_check, "CPU usage should be a percentage"
        logger.info("✓ CPU usage metric validated")
        reporter.print_test_step(4, "Get System CPU Usage", "pass")
        
        # Step 5: Get Memory Usage metric
        logger.info("Step 14: Retrieving System Memory Usage metric")
        reporter.print_test_step(5, "Get System Memory Usage", "running")
        memory_usage = dashboard.get_system_memory_usage()
        logger.info(f"Step 15: Memory Usage value: {memory_usage}")
        reporter.print_info(f"Memory Usage: {memory_usage}")
        memory_check = "%" in memory_usage
        logger.info(f"Step 16: Memory usage contains '%': {memory_check}")
        reporter.print_assertion("Memory usage is percentage", "contains %", memory_usage, memory_check)
        logger.info("Step 17: Asserting Memory usage is a percentage")
        assert memory_check, "Memory usage should be a percentage"
        logger.info("✓ Memory usage metric validated")
        reporter.print_test_step(5, "Get System Memory Usage", "pass")
        
        # Step 6: Verify logical constraint
        logger.info("Step 18: Verifying logical constraint: Running VMs <= Total VMs")
        reporter.print_test_step(6, "Verify Running VMs <= Total VMs", "running")
        constraint_check = running_vms <= total_vms
        logger.info(f"Step 19: Constraint check: {running_vms} <= {total_vms} = {constraint_check}")
        reporter.print_assertion(
            "Running VMs should not exceed Total VMs",
            f"Running ({running_vms}) <= Total ({total_vms})",
            f"{running_vms} <= {total_vms}",
            constraint_check
        )
        logger.info("Step 20: Asserting logical constraint")
        assert constraint_check, f"Running VMs ({running_vms}) should not exceed Total VMs ({total_vms})"
        logger.info("✓ Logical constraint validated")
        reporter.print_test_step(6, "Verify Running VMs <= Total VMs", "pass")
        
        logger.info("Step 21: Metrics Summary:")
        logger.info(f"  - Total VMs:    {total_vms}")
        logger.info(f"  - Running VMs:  {running_vms}")
        logger.info(f"  - CPU Usage:    {cpu_usage}")
        logger.info(f"  - Memory Usage: {memory_usage}")
        
        logger.info("=" * 80)
        logger.info(f"✓✓✓ TEST PASSED: All metrics verified successfully!")
        logger.info("=" * 80)
        reporter.print_success(f"All metrics verified! Total={total_vms}, Running={running_vms}, CPU={cpu_usage}, Memory={memory_usage}")
    
    def test_tab_navigation_works(self, page: Page):
        """Test that tab navigation works correctly"""
        logger.info("=" * 80)
        logger.info("TEST: Tab navigation works - START")
        logger.info("=" * 80)
        
        # Step 1: Initialize and verify default tab
        logger.info("Step 1: Initializing dashboard and checking default tab")
        reporter.print_test_step(1, "Initialize Dashboard and Check Default Tab", "running")
        dashboard = DashboardPage(page)
        dashboard.load_dashboard()
        logger.info("✓ Dashboard loaded")
        
        logger.info("Step 2: Checking if Dashboard tab is active by default")
        default_active = dashboard.is_tab_active(dashboard.TAB_DASHBOARD)
        logger.info(f"Step 3: Dashboard tab active status: {default_active}")
        reporter.print_assertion("Dashboard tab is active by default", "True", str(default_active), default_active)
        assert default_active, "Dashboard tab should be active by default"
        logger.info("✓ Dashboard is the default active tab")
        reporter.print_test_step(1, "Initialize Dashboard and Check Default Tab", "pass")
        
        # Step 2: Navigate to VMs tab
        logger.info("Step 4: Navigating to VMs tab")
        reporter.print_test_step(2, "Navigate to VMs Tab", "running")
        dashboard.click_vms_tab()
        logger.info("✓ VMs tab clicked")
        
        logger.info("Step 5: Verifying VMs content is visible")
        vms_visible = dashboard.is_visible(dashboard.VMS_CONTENT)
        logger.info(f"Step 6: VMs content visible: {vms_visible}")
        
        logger.info("Step 7: Verifying VMs tab is active")
        vms_active = dashboard.is_tab_active(dashboard.TAB_VMS)
        logger.info(f"Step 8: VMs tab active: {vms_active}")
        
        reporter.print_assertion("VMs content visible", "True", str(vms_visible), vms_visible)
        reporter.print_assertion("VMs tab active", "True", str(vms_active), vms_active)
        assert vms_visible and vms_active
        logger.info("✓✓ VMs tab navigation successful")
        reporter.print_test_step(2, "Navigate to VMs Tab", "pass")
        
        # Step 3: Navigate to Create tab
        logger.info("Step 9: Navigating to Create VM tab")
        reporter.print_test_step(3, "Navigate to Create VM Tab", "running")
        dashboard.click_create_tab()
        logger.info("✓ Create tab clicked")
        
        logger.info("Step 10: Verifying Create content is visible")
        create_visible = dashboard.is_visible(dashboard.CREATE_CONTENT)
        logger.info(f"Step 11: Create content visible: {create_visible}")
        
        logger.info("Step 12: Verifying Create tab is active")
        create_active = dashboard.is_tab_active(dashboard.TAB_CREATE)
        logger.info(f"Step 13: Create tab active: {create_active}")
        
        reporter.print_assertion("Create content visible", "True", str(create_visible), create_visible)
        reporter.print_assertion("Create tab active", "True", str(create_active), create_active)
        assert create_visible and create_active
        logger.info("✓✓ Create tab navigation successful")
        reporter.print_test_step(3, "Navigate to Create VM Tab", "pass")
        
        # Step 4: Navigate to Logs tab
        logger.info("Step 14: Navigating to Logs tab")
        reporter.print_test_step(4, "Navigate to Logs Tab", "running")
        dashboard.click_logs_tab()
        logger.info("✓ Logs tab clicked")
        
        logger.info("Step 15: Verifying Logs content is visible")
        logs_visible = dashboard.is_visible(dashboard.LOGS_CONTENT)
        logger.info(f"Step 16: Logs content visible: {logs_visible}")
        
        logger.info("Step 17: Verifying Logs tab is active")
        logs_active = dashboard.is_tab_active(dashboard.TAB_LOGS)
        logger.info(f"Step 18: Logs tab active: {logs_active}")
        
        reporter.print_assertion("Logs content visible", "True", str(logs_visible), logs_visible)
        reporter.print_assertion("Logs tab active", "True", str(logs_active), logs_active)
        assert logs_visible and logs_active
        logger.info("✓✓ Logs tab navigation successful")
        reporter.print_test_step(4, "Navigate to Logs Tab", "pass")
        
        # Step 5: Navigate back to Dashboard tab
        logger.info("Step 19: Navigating back to Dashboard tab")
        reporter.print_test_step(5, "Navigate Back to Dashboard Tab", "running")
        dashboard.click_dashboard_tab()
        logger.info("✓ Dashboard tab clicked")
        
        logger.info("Step 20: Verifying Dashboard content is visible")
        dash_visible = dashboard.is_visible(dashboard.DASHBOARD_CONTENT)
        logger.info(f"Step 21: Dashboard content visible: {dash_visible}")
        
        logger.info("Step 22: Verifying Dashboard tab is active")
        dash_active = dashboard.is_tab_active(dashboard.TAB_DASHBOARD)
        logger.info(f"Step 23: Dashboard tab active: {dash_active}")
        
        reporter.print_assertion("Dashboard content visible", "True", str(dash_visible), dash_visible)
        reporter.print_assertion("Dashboard tab active", "True", str(dash_active), dash_active)
        assert dash_visible and dash_active
        logger.info("✓✓ Dashboard tab navigation successful")
        reporter.print_test_step(5, "Navigate Back to Dashboard Tab", "pass")
        
        logger.info("Step 24: Navigation summary - All 4 tabs tested:")
        logger.info("  ✓ Dashboard → VMs → Create → Logs → Dashboard")
        logger.info("=" * 80)
        logger.info("✓✓✓ TEST PASSED: All tab navigation verified successfully!")
        logger.info("=" * 80)
        reporter.print_success("All tab navigation verified successfully!")
    
    def test_dashboard_header_content(self, page: Page):
        """Test dashboard header displays correct branding"""
        logger.info("=" * 80)
        logger.info("TEST: Dashboard header content - START")
        logger.info("=" * 80)
        
        # Step 1: Load dashboard
        logger.info("Step 1: Loading dashboard page")
        reporter.print_test_step(1, "Load Dashboard Page", "running")
        dashboard = DashboardPage(page)
        dashboard.load_dashboard()
        logger.info("✓ Dashboard page loaded successfully")
        reporter.print_test_step(1, "Load Dashboard Page", "pass")
        
        # Step 2: Verify header title
        logger.info("Step 2: Verifying header title content")
        reporter.print_test_step(2, "Verify Header Title", "running")
        header_title = dashboard.get_page_title()
        logger.info(f"Step 3: Header title retrieved: '{header_title}'")
        reporter.print_info(f"Header Title: {header_title}")
        
        logger.info("Step 4: Checking if header contains building emoji 🏢")
        emoji_check = "🏢" in header_title
        logger.info(f"Step 5: Building emoji present: {emoji_check}")
        reporter.print_assertion("Header contains building emoji", "🏢 present", header_title, emoji_check)
        assert emoji_check, "Header should contain building emoji"
        logger.info("✓ Building emoji verified in header")
        
        logger.info("Step 6: Checking if header contains 'Aziro Cluster Center'")
        name_check = "Aziro Cluster Center" in header_title
        logger.info(f"Step 7: Application name present: {name_check}")
        reporter.print_assertion("Header contains app name", "Aziro Cluster Center present", header_title, name_check)
        assert name_check, "Header should contain application name"
        logger.info("✓ Application name verified in header")
        reporter.print_test_step(2, "Verify Header Title", "pass")
        
        # Step 3: Verify header description
        logger.info("Step 8: Verifying header description")
        reporter.print_test_step(3, "Verify Header Description", "running")
        header_desc = dashboard.get_page_description()
        logger.info(f"Step 9: Header description retrieved (length: {len(header_desc)})")
        logger.info(f"Step 10: Description preview: {header_desc[:50]}...")
        reporter.print_info(f"Header Description: {header_desc[:50]}...")
        
        logger.info("Step 11: Checking if description is not empty")
        not_empty = len(header_desc) > 0
        logger.info(f"Step 12: Description not empty: {not_empty} (length: {len(header_desc)})")
        reporter.print_assertion("Description not empty", "length > 0", str(len(header_desc)), not_empty)
        assert not_empty, "Header description should not be empty"
        logger.info("✓ Description is not empty")
        
        logger.info("Step 13: Checking if description mentions virtual machines")
        vm_mentioned = "virtual machine" in header_desc.lower()
        logger.info(f"Step 14: Virtual machine mentioned: {vm_mentioned}")
        reporter.print_assertion("Description mentions VMs", "virtual machine in text", "found" if vm_mentioned else "not found", vm_mentioned)
        assert vm_mentioned, "Description should mention virtual machines"
        logger.info("✓ Virtual machine mention verified")
        reporter.print_test_step(3, "Verify Header Description", "pass")
        
        logger.info("Step 15: Header branding validation summary:")
        logger.info("  ✓ Building emoji present")
        logger.info("  ✓ Application name present")
        logger.info("  ✓ Description not empty")
        logger.info("  ✓ Virtual machines mentioned")
        
        logger.info("=" * 80)
        logger.info("✓✓✓ TEST PASSED: Dashboard header branding verified!")
        logger.info("=" * 80)
        reporter.print_success("Dashboard header branding verified!")
    
    @pytest.mark.slow
    def test_dashboard_metrics_are_numeric(self, page: Page):
        """Test that dashboard metrics contain valid numeric values"""
        logger.info("=" * 80)
        logger.info("TEST: Dashboard metrics are numeric - START")
        logger.info("=" * 80)
        
        # Step 1: Load dashboard
        logger.info("Step 1: Loading dashboard for numeric metrics validation")
        reporter.print_test_step(1, "Load Dashboard for Metrics Validation", "running")
        dashboard = DashboardPage(page)
        dashboard.load_dashboard()
        logger.info("✓ Dashboard loaded for metrics validation")
        reporter.print_test_step(1, "Load Dashboard for Metrics Validation", "pass")
        
        # Step 2: Validate Total VMs count
        logger.info("Step 2: Retrieving Total VMs count for validation")
        reporter.print_test_step(2, "Validate Total VMs is Non-Negative", "running")
        total_vms = dashboard.get_total_vms_count()
        logger.info(f"Step 3: Total VMs value: {total_vms}")
        
        logger.info("Step 4: Checking if Total VMs is non-negative")
        total_check = total_vms >= 0
        logger.info(f"Step 5: Total VMs >= 0: {total_check}")
        reporter.print_assertion("Total VMs >= 0", "non-negative", str(total_vms), total_check)
        assert total_check, "Total VMs should be non-negative"
        logger.info("✓ Total VMs is non-negative")
        reporter.print_test_step(2, "Validate Total VMs is Non-Negative", "pass")
        
        # Step 3: Validate Running VMs count
        logger.info("Step 6: Retrieving Running VMs count for validation")
        reporter.print_test_step(3, "Validate Running VMs is Non-Negative", "running")
        running_vms = dashboard.get_running_vms_count()
        logger.info(f"Step 7: Running VMs value: {running_vms}")
        
        logger.info("Step 8: Checking if Running VMs is non-negative")
        running_check = running_vms >= 0
        logger.info(f"Step 9: Running VMs >= 0: {running_check}")
        reporter.print_assertion("Running VMs >= 0", "non-negative", str(running_vms), running_check)
        assert running_check, "Running VMs should be non-negative"
        logger.info("✓ Running VMs is non-negative")
        reporter.print_test_step(3, "Validate Running VMs is Non-Negative", "pass")
        
        # Step 4: Validate CPU usage percentage
        logger.info("Step 10: Retrieving CPU usage for range validation")
        reporter.print_test_step(4, "Validate CPU Usage Percentage (0-100%)", "running")
        cpu_text = dashboard.get_system_cpu_usage()
        logger.info(f"Step 11: CPU usage text: {cpu_text}")
        
        logger.info("Step 12: Parsing CPU percentage value")
        cpu_value = int(cpu_text.replace("%", ""))
        logger.info(f"Step 13: Parsed CPU value: {cpu_value}%")
        reporter.print_info(f"CPU Usage Value: {cpu_value}%")
        
        logger.info("Step 14: Validating CPU is in range 0-100%")
        cpu_range = 0 <= cpu_value <= 100
        logger.info(f"Step 15: CPU in valid range (0-100%): {cpu_range}")
        reporter.print_assertion("CPU in range 0-100%", "0 <= value <= 100", str(cpu_value), cpu_range)
        assert cpu_range, f"CPU usage should be between 0-100%, got {cpu_value}%"
        logger.info(f"✓ CPU usage {cpu_value}% is within valid range")
        reporter.print_test_step(4, "Validate CPU Usage Percentage (0-100%)", "pass")
        
        # Step 5: Validate Memory usage percentage
        logger.info("Step 16: Retrieving Memory usage for range validation")
        reporter.print_test_step(5, "Validate Memory Usage Percentage (0-100%)", "running")
        memory_text = dashboard.get_system_memory_usage()
        logger.info(f"Step 17: Memory usage text: {memory_text}")
        
        logger.info("Step 18: Parsing Memory percentage value")
        memory_value = int(memory_text.replace("%", ""))
        logger.info(f"Step 19: Parsed Memory value: {memory_value}%")
        reporter.print_info(f"Memory Usage Value: {memory_value}%")
        
        logger.info("Step 20: Validating Memory is in range 0-100%")
        memory_range = 0 <= memory_value <= 100
        logger.info(f"Step 21: Memory in valid range (0-100%): {memory_range}")
        reporter.print_assertion("Memory in range 0-100%", "0 <= value <= 100", str(memory_value), memory_range)
        assert memory_range, f"Memory usage should be between 0-100%, got {memory_value}%"
        logger.info(f"✓ Memory usage {memory_value}% is within valid range")
        reporter.print_test_step(5, "Validate Memory Usage Percentage (0-100%)", "pass")
        
        logger.info("Step 22: Numeric validation summary:")
        logger.info(f"  - Total VMs: {total_vms} (non-negative ✓)")
        logger.info(f"  - Running VMs: {running_vms} (non-negative ✓)")
        logger.info(f"  - CPU Usage: {cpu_value}% (0-100% range ✓)")
        logger.info(f"  - Memory Usage: {memory_value}% (0-100% range ✓)")
        
        logger.info("=" * 80)
        logger.info(f"✓✓✓ TEST PASSED: All metrics validated successfully!")
        logger.info("=" * 80)
        reporter.print_success(f"All metrics validated! Total VMs={total_vms}, Running={running_vms}, CPU={cpu_value}%, Memory={memory_value}%")

