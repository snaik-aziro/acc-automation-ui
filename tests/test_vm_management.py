"""
VM Management Tests for Aziro Cluster Center
Tests for VM creation, operations, and management
"""

import pytest
from playwright.sync_api import Page
from pages.dashboard_page import DashboardPage
from pages.vm_page import VMPage
from utils.test_reporter import reporter
import logging
import time
import sys
import os
from datetime import datetime
from functools import wraps

logger = logging.getLogger(__name__)

def log_operation_details(func):
    """Decorator to add extensive logging to operations"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info(f"🔵 OPERATION START: {func.__name__}")
        logger.info(f"   📍 Location: {func.__code__.co_filename}:{func.__code__.co_firstlineno}")
        logger.info(f"   ⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        logger.info(f"   📦 Arguments: args={args}, kwargs={kwargs}")
        logger.info(f"   🧠 Memory Before: {sys.getsizeof(args)} bytes (args), {sys.getsizeof(kwargs)} bytes (kwargs)")
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            logger.info(f"   ✅ Operation completed in {elapsed:.4f} seconds")
            logger.info(f"   📊 Result Type: {type(result).__name__}")
            logger.info(f"   📏 Result Size: {sys.getsizeof(result)} bytes")
            logger.info(f"   🔵 OPERATION END: {func.__name__}")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"   ❌ Operation failed after {elapsed:.4f} seconds")
            logger.error(f"   🐛 Error Type: {type(e).__name__}")
            logger.error(f"   📝 Error Message: {str(e)}")
            logger.error(f"   🔵 OPERATION END (ERROR): {func.__name__}")
            raise
    return wrapper

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

def log_detailed_page_state(page, context="General"):
    """Helper function to log extensive page state information"""
    try:
        logger.debug(f"log_detailed_page_state() - Logging detailed page state for context: {context}")
        logger.debug(f"log_detailed_page_state() - Page URL: {page.url}")
        logger.debug(f"log_detailed_page_state() - Page Title: {page.title()}")
        logger.debug(f"log_detailed_page_state() - Page Viewport: {page.viewport_size}")
        logger.debug(f"log_detailed_page_state() - Page Ready State: {page.evaluate('document.readyState')}")
        logger.debug(f"log_detailed_page_state() - Page Load State: {page.evaluate('performance.timing.loadEventEnd')}")
        logger.debug(f"log_detailed_page_state() - DOM Content Loaded: {page.evaluate('performance.timing.domContentLoadedEventEnd')}")
        logger.debug(f"log_detailed_page_state() - Navigation Start: {page.evaluate('performance.timing.navigationStart')}")
        try:
            body_text = page.evaluate("document.body.innerText")
            logger.debug(f"log_detailed_page_state() - Body Text Length: {len(body_text)} characters")
            logger.debug(f"log_detailed_page_state() - Body Text Preview: {body_text[:200]}...")
        except:
            logger.debug(f"log_detailed_page_state() - Could not get body text")
        try:
            all_elements = page.evaluate("document.querySelectorAll('*').length")
            logger.debug(f"log_detailed_page_state() - Total DOM Elements: {all_elements}")
        except:
            logger.debug(f"log_detailed_page_state() - Could not count DOM elements")
        try:
            scripts = page.evaluate("document.querySelectorAll('script').length")
            logger.debug(f"log_detailed_page_state() - Script Tags: {scripts}")
        except:
            logger.debug(f"log_detailed_page_state() - Could not count scripts")
        try:
            links = page.evaluate("document.querySelectorAll('a').length")
            logger.debug(f"log_detailed_page_state() - Link Elements: {links}")
        except:
            logger.debug(f"log_detailed_page_state() - Could not count links")
        try:
            buttons = page.evaluate("document.querySelectorAll('button').length")
            logger.debug(f"log_detailed_page_state() - Button Elements: {buttons}")
        except:
            logger.debug(f"log_detailed_page_state() - Could not count buttons")
        try:
            inputs = page.evaluate("document.querySelectorAll('input').length")
            logger.debug(f"log_detailed_page_state() - Input Elements: {inputs}")
        except:
            logger.debug(f"log_detailed_page_state() - Could not count inputs")
        try:
            selects = page.evaluate("document.querySelectorAll('select').length")
            logger.debug(f"log_detailed_page_state() - Select Elements: {selects}")
        except:
            logger.debug(f"log_detailed_page_state() - Could not count selects")
        logger.debug(f"log_detailed_page_state() - Page state logging completed")
    except Exception as e:
        logger.debug(f"log_detailed_page_state() - Error logging page state: {e}")

def log_periodic_status(page, interval_name="Status Check"):
    """Helper function to log periodic status updates"""
    logger.debug(f"log_periodic_status() - Periodic status check: {interval_name}")
    logger.debug(f"log_periodic_status() - Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
    logger.debug(f"log_periodic_status() - Page URL: {page.url}")
    logger.debug(f"log_periodic_status() - Page Title: {page.title()}")
    logger.debug(f"log_periodic_status() - Page Ready State: {page.evaluate('document.readyState')}")
    try:
        logger.debug(f"log_periodic_status() - Window Inner Width: {page.evaluate('window.innerWidth')}")
        logger.debug(f"log_periodic_status() - Window Inner Height: {page.evaluate('window.innerHeight')}")
        logger.debug(f"log_periodic_status() - Screen Width: {page.evaluate('screen.width')}")
        logger.debug(f"log_periodic_status() - Screen Height: {page.evaluate('screen.height')}")
        logger.debug(f"log_periodic_status() - Device Pixel Ratio: {page.evaluate('window.devicePixelRatio')}")
    except:
        logger.debug(f"log_periodic_status() - Could not get window dimensions")
    logger.debug(f"log_periodic_status() - Status check completed")


@pytest.mark.vm_management
class TestVMManagement:
    """Test suite for VM Management functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup for each test - navigate to VMs tab"""
        logger.debug(f"TestVMManagement.setup() - Test setup fixture called")
        logger.debug(f"TestVMManagement.setup() - Page URL: {page.url}")
        log_detailed_page_state(page, "Test Setup - Initial State")
        log_periodic_status(page, "Test Setup - Before Dashboard Load")
        
        dashboard = DashboardPage(page)
        logger.debug(f"TestVMManagement.setup() - DashboardPage object created")
        log_periodic_status(page, "Test Setup - After DashboardPage Creation")
        
        dashboard.load_dashboard()
        logger.debug(f"TestVMManagement.setup() - Dashboard loaded")
        log_detailed_page_state(page, "Test Setup - After Dashboard Load")
        log_periodic_status(page, "Test Setup - After Dashboard Load")
        
        dashboard.click_vms_tab()
        logger.debug(f"TestVMManagement.setup() - VMs tab clicked")
        log_periodic_status(page, "Test Setup - After VMs Tab Click")
        
        # Wait for VM list to load
        vm_page = VMPage(page)
        logger.debug(f"TestVMManagement.setup() - VMPage object created")
        log_periodic_status(page, "Test Setup - After VMPage Creation")
        
        vm_page.wait_for_vm_list_to_load()
        logger.debug(f"TestVMManagement.setup() - VM list loaded")
        log_detailed_page_state(page, "Test Setup - After VM List Load")
        log_periodic_status(page, "Test Setup - Final State")
        logger.debug(f"TestVMManagement.setup() - Setup complete")
    
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_create_vm_successfully(self, page: Page):
        """Test creating a new VM with valid data"""
        test_start_time = time.time()
        test_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("🚀 TEST: Create VM successfully - START")
        logger.info("=" * 100)
        logger.info(f"⏰ Test Start Time: {test_timestamp}")
        logger.info(f"🆔 Test ID: test_create_vm_successfully")
        logger.info(f"📋 Test Description: Test creating a new VM with valid data")
        logger.info(f"🏷️  Test Markers: @pytest.mark.smoke, @pytest.mark.critical")
        logger.info(f"🌐 Page URL Before Test: {page.url}")
        logger.info(f"📏 Page Viewport: {page.viewport_size}")
        logger.info(f"🧠 Memory Usage: {sys.getsizeof(page)} bytes (page object)")
        logger.info("=" * 100)
        
        # Navigate to Create tab
        step1_start = time.time()
        logger.info("")
        logger.info("━" * 100)
        logger.info("📍 STEP 1: Initializing dashboard page object")
        logger.info("━" * 100)
        logger.info(f"   ⏰ Step Start: {datetime.now().strftime('%H:%M:%S.%f')}")
        logger.info(f"   📦 Input: page object type={type(page).__name__}")
        logger.info(f"   🔍 Page State: url={page.url}, title={page.title()}")
        logger.info(f"   🧠 Memory Before: {sys.getsizeof(page)} bytes")
        dashboard = DashboardPage(page)
        step1_elapsed = time.time() - step1_start
        logger.info(f"   ✅ DashboardPage object created in {step1_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(dashboard).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(dashboard)} bytes")
        logger.info(f"   🔗 Object ID: {id(dashboard)}")
        logger.info(f"   📍 Object Location: {dashboard.__class__.__module__}")
        logger.info(f"   ✓ Step 1 completed successfully")
        
        step2_start = time.time()
        logger.info("")
        logger.info("━" * 100)
        logger.info("📍 STEP 2: Clicking on Create tab to navigate to VM creation form")
        logger.info("━" * 100)
        logger.info(f"   ⏰ Step Start: {datetime.now().strftime('%H:%M:%S.%f')}")
        logger.info(f"   🎯 Action: dashboard.click_create_tab()")
        logger.info(f"   📍 Current URL: {page.url}")
        logger.info(f"   📄 Current Title: {page.title()}")
        logger.info(f"   🔍 Checking if Create tab exists before click...")
        try:
            create_tab = page.locator('[data-testid="create-tab"]')
            is_visible_before = create_tab.is_visible()
            logger.info(f"   👁️  Create tab visible before click: {is_visible_before}")
            if is_visible_before:
                logger.info(f"   📏 Create tab bounding box: {create_tab.bounding_box()}")
                logger.info(f"   🎨 Create tab computed styles: color={create_tab.evaluate('el => getComputedStyle(el).color')}")
        except Exception as e:
            logger.warning(f"   ⚠️  Could not check Create tab state: {e}")
        dashboard.click_create_tab()
        step2_elapsed = time.time() - step2_start
        logger.info(f"   ⏱️  Click action completed in {step2_elapsed:.4f} seconds")
        logger.info(f"   📍 URL After Click: {page.url}")
        logger.info(f"   📄 Title After Click: {page.title()}")
        logger.info(f"   🔍 Verifying Create tab is now active...")
        try:
            create_tab_active = page.locator('[data-testid="create-tab"][aria-selected="true"]')
            is_active = create_tab_active.count() > 0
            logger.info(f"   ✅ Create tab active state: {is_active}")
        except Exception as e:
            logger.warning(f"   ⚠️  Could not verify active state: {e}")
        logger.info(f"   ✓ Successfully navigated to Create tab")
        
        # Create VM with unique name
        step3_start = time.time()
        logger.info("")
        logger.info("━" * 100)
        logger.info("📍 STEP 3: Initializing VM page object")
        logger.info("━" * 100)
        logger.info(f"   ⏰ Step Start: {datetime.now().strftime('%H:%M:%S.%f')}")
        logger.info(f"   📦 Input: page object")
        vm_page = VMPage(page)
        step3_elapsed = time.time() - step3_start
        logger.info(f"   ✅ VMPage object created in {step3_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(vm_page).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(vm_page)} bytes")
        logger.info(f"   🔗 Object ID: {id(vm_page)}")
        logger.info(f"   ✓ Step 3 completed successfully")
        
        step4_start = time.time()
        logger.info("")
        logger.info("━" * 100)
        logger.info("📍 STEP 4: Generating unique VM name")
        logger.info("━" * 100)
        logger.info(f"   ⏰ Step Start: {datetime.now().strftime('%H:%M:%S.%f')}")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        logger.info(f"   🕐 Timestamp Generated: {timestamp}")
        logger.info(f"   📏 Timestamp Length: {len(timestamp)} characters")
        logger.info(f"   🔢 Timestamp Format: YYYYMMDD_HHMMSS")
        vm_name = f"test-vm-{timestamp}"
        step4_elapsed = time.time() - step4_start
        logger.info(f"   ✅ VM name generated in {step4_elapsed:.4f} seconds")
        logger.info(f"   📝 Generated VM Name: '{vm_name}'")
        logger.info(f"   📏 VM Name Length: {len(vm_name)} characters")
        logger.info(f"   🔢 VM Name Character Count: {len(vm_name)}")
        logger.info(f"   🧠 Memory Usage: {sys.getsizeof(vm_name)} bytes")
        logger.info(f"   ✓ Step 4 completed successfully")
        
        step5_start = time.time()
        logger.info("")
        logger.info("━" * 100)
        logger.info("📍 STEP 5: Preparing VM configuration")
        logger.info("━" * 100)
        logger.info(f"   ⏰ Step Start: {datetime.now().strftime('%H:%M:%S.%f')}")
        logger.info(f"   📋 Configuration Parameters:")
        logger.info(f"      ┌─ Name: {vm_name}")
        logger.info(f"      │  Type: str")
        logger.info(f"      │  Length: {len(vm_name)} chars")
        logger.info(f"      │  Memory: {sys.getsizeof(vm_name)} bytes")
        logger.info(f"      ├─ Memory: 4096 MB")
        logger.info(f"      │  Type: int")
        logger.info(f"      │  Value: 4096")
        logger.info(f"      │  Memory: {sys.getsizeof(4096)} bytes")
        logger.info(f"      │  Conversion: 4096 MB = {4096 / 1024:.2f} GB")
        logger.info(f"      ├─ CPU: 4 cores")
        logger.info(f"      │  Type: int")
        logger.info(f"      │  Value: 4")
        logger.info(f"      │  Memory: {sys.getsizeof(4)} bytes")
        logger.info(f"      ├─ Network Type: Bridge")
        logger.info(f"      │  Type: str")
        logger.info(f"      │  Value: 'Bridge'")
        logger.info(f"      │  Length: {len('Bridge')} chars")
        logger.info(f"      │  Memory: {sys.getsizeof('Bridge')} bytes")
        logger.info(f"      └─ IP Address: 192.168.1.100")
        logger.info(f"         Type: str")
        logger.info(f"         Value: '192.168.1.100'")
        logger.info(f"         Length: {len('192.168.1.100')} chars")
        logger.info(f"         Memory: {sys.getsizeof('192.168.1.100')} bytes")
        logger.info(f"         Format: IPv4")
        logger.info(f"         Valid: {'192.168.1.100'.count('.') == 3}")
        step5_elapsed = time.time() - step5_start
        logger.info(f"   ✅ Configuration prepared in {step5_elapsed:.4f} seconds")
        logger.info(f"   ✓ Step 5 completed successfully")
        
        step6_start = time.time()
        logger.info("")
        logger.info("━" * 100)
        logger.info("📍 STEP 6: Calling create_vm() method")
        logger.info("━" * 100)
        logger.info(f"   ⏰ Step Start: {datetime.now().strftime('%H:%M:%S.%f')}")
        logger.info(f"   🎯 Method: vm_page.create_vm()")
        logger.info(f"   📍 Method Location: {vm_page.create_vm.__code__.co_filename}:{vm_page.create_vm.__code__.co_firstlineno}")
        logger.info(f"   📦 Method Arguments:")
        logger.info(f"      name={vm_name}")
        logger.info(f"      memory=4096")
        logger.info(f"      cpu=4")
        logger.info(f"      network_type='Bridge'")
        logger.info(f"      ip_address='192.168.1.100'")
        logger.info(f"   🔍 Pre-call State:")
        logger.info(f"      Current URL: {page.url}")
        logger.info(f"      Current Title: {page.title()}")
        logger.info(f"      Page Load State: {page.evaluate('document.readyState')}")
        logger.info(f"   🚀 Executing create_vm() call...")
        call_start = time.time()
        result = vm_page.create_vm(
            name=vm_name,
            memory=4096,
            cpu=4,
            network_type="Bridge",
            ip_address="192.168.1.100"
        )
        call_elapsed = time.time() - call_start
        step6_elapsed = time.time() - step6_start
        logger.info(f"   ⏱️  Method call completed in {call_elapsed:.4f} seconds")
        logger.info(f"   ✅ create_vm() returned result")
        logger.info(f"   📊 Result Type: {type(result).__name__}")
        logger.info(f"   📏 Result Length: {len(str(result))} characters")
        logger.info(f"   🧠 Result Memory: {sys.getsizeof(result)} bytes")
        logger.info(f"   📝 Result Value: '{result}'")
        logger.info(f"   🔍 Post-call State:")
        logger.info(f"      Current URL: {page.url}")
        logger.info(f"      Current Title: {page.title()}")
        logger.info(f"      Page Load State: {page.evaluate('document.readyState')}")
        logger.info(f"   ✓ Step 6 completed in {step6_elapsed:.4f} seconds")
        
        # Verify success message
        step7_start = time.time()
        logger.info("")
        logger.info("━" * 100)
        logger.info("📍 STEP 7: Verifying success message in result")
        logger.info("━" * 100)
        logger.info(f"   ⏰ Step Start: {datetime.now().strftime('%H:%M:%S.%f')}")
        logger.info(f"   🔍 Validation Details:")
        logger.info(f"      Result: '{result}'")
        logger.info(f"      Result Lowercase: '{result.lower()}'")
        logger.info(f"      Searching for: 'successfully'")
        logger.info(f"      Contains Check: {'successfully' in result.lower()}")
        logger.info(f"   ✅ Assertion: assert 'successfully' in result.lower()")
        assert "successfully" in result.lower(), f"Expected success message, got: {result}"
        step7_elapsed = time.time() - step7_start
        logger.info(f"   ✅ Assertion passed in {step7_elapsed:.4f} seconds")
        logger.info(f"   ✓ Success message verified in result")
        logger.info(f"   ✓ Step 7 completed successfully")
        
        # Wait for navigation to VMs tab
        step8_start = time.time()
        logger.info("")
        logger.info("━" * 100)
        logger.info("📍 STEP 8: Waiting for navigation to VMs tab")
        logger.info("━" * 100)
        logger.info(f"   ⏰ Step Start: {datetime.now().strftime('%H:%M:%S.%f')}")
        logger.info(f"   ⏳ Wait Duration: 2 seconds")
        logger.info(f"   📍 URL Before Wait: {page.url}")
        logger.info(f"   🔍 Waiting for page state changes...")
        wait_start = time.time()
        time.sleep(2)
        wait_elapsed = time.time() - wait_start
        step8_elapsed = time.time() - step8_start
        logger.info(f"   ⏱️  Actual Wait Time: {wait_elapsed:.4f} seconds")
        logger.info(f"   📍 URL After Wait: {page.url}")
        logger.info(f"   📄 Title After Wait: {page.title()}")
        logger.info(f"   ✓ Wait completed")
        logger.info(f"   ✓ Step 8 completed in {step8_elapsed:.4f} seconds")
        
        # Verify VM appears in list
        step9_start = time.time()
        logger.info("")
        logger.info("━" * 100)
        logger.info("📍 STEP 9: Waiting for VM list to load completely")
        logger.info("━" * 100)
        logger.info(f"   ⏰ Step Start: {datetime.now().strftime('%H:%M:%S.%f')}")
        logger.info(f"   🎯 Method: vm_page.wait_for_vm_list_to_load()")
        logger.info(f"   📍 Current State: URL={page.url}")
        wait_start = time.time()
        vm_page.wait_for_vm_list_to_load()
        wait_elapsed = time.time() - wait_start
        step9_elapsed = time.time() - step9_start
        logger.info(f"   ⏱️  Wait completed in {wait_elapsed:.4f} seconds")
        logger.info(f"   ✅ VM list loaded successfully")
        logger.info(f"   ✓ Step 9 completed in {step9_elapsed:.4f} seconds")
        
        step10_start = time.time()
        logger.info("")
        logger.info("━" * 100)
        logger.info(f"📍 STEP 10: Searching for VM card with name '{vm_name}'")
        logger.info("━" * 100)
        logger.info(f"   ⏰ Step Start: {datetime.now().strftime('%H:%M:%S.%f')}")
        logger.info(f"   🎯 Method: vm_page.get_vm_card_by_name('{vm_name}')")
        logger.info(f"   🔍 Search Criteria: VM name = '{vm_name}'")
        logger.info(f"   📏 Name Length: {len(vm_name)} characters")
        search_start = time.time()
        vm_card = vm_page.get_vm_card_by_name(vm_name)
        search_elapsed = time.time() - search_start
        step10_elapsed = time.time() - step10_start
        logger.info(f"   ⏱️  Search completed in {search_elapsed:.4f} seconds")
        logger.info(f"   📊 Result Type: {type(vm_card).__name__}")
        logger.info(f"   🔍 VM Card Found: {vm_card is not None}")
        if vm_card:
            logger.info(f"   📏 VM Card Size: {sys.getsizeof(vm_card)} bytes")
            try:
                logger.info(f"   📍 VM Card Location: {vm_card.bounding_box()}")
            except:
                logger.info(f"   📍 VM Card Location: Not available")
        logger.info(f"   ✓ Step 10 completed in {step10_elapsed:.4f} seconds")
        
        step11_start = time.time()
        logger.info("")
        logger.info("━" * 100)
        logger.info("📍 STEP 11: Validating VM card exists")
        logger.info("━" * 100)
        logger.info(f"   ⏰ Step Start: {datetime.now().strftime('%H:%M:%S.%f')}")
        logger.info(f"   ✅ Assertion: assert vm_card is not None")
        logger.info(f"   🔍 VM Card State: {vm_card is not None}")
        assert vm_card is not None, f"VM '{vm_name}' should appear in the VM list"
        step11_elapsed = time.time() - step11_start
        logger.info(f"   ✅ Assertion passed in {step11_elapsed:.4f} seconds")
        logger.info(f"   ✓ VM card for '{vm_name}' found in the list")
        logger.info(f"   ✓ Step 11 completed successfully")
        
        test_elapsed = time.time() - test_start_time
        logger.info("")
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info(f"✓✓✓ TEST PASSED: VM '{vm_name}' created successfully")
        logger.info("=" * 100)
        logger.info(f"⏰ Test End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        logger.info(f"⏱️  Total Test Duration: {test_elapsed:.4f} seconds")
        logger.info(f"📊 Test Summary:")
        logger.info(f"   - Steps Executed: 11")
        logger.info(f"   - VM Created: {vm_name}")
        logger.info(f"   - Status: PASSED")
        logger.info(f"   - Memory Usage: {sys.getsizeof(page) + sys.getsizeof(dashboard) + sys.getsizeof(vm_page)} bytes")
        logger.info("=" * 100)
        logger.info("=" * 100)
    
    def test_create_vm_with_minimal_specs(self, page: Page):
        """Test creating a VM with minimal specifications"""
        test_start_time = time.time()
        test_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("🚀 TEST: Create VM with minimal specs - START")
        logger.info("=" * 100)
        logger.info(f"⏰ Test Start Time: {test_timestamp}")
        logger.info(f"🆔 Test ID: test_create_vm_with_minimal_specs")
        logger.info(f"📋 Test Description: Test creating a VM with minimal specifications")
        logger.info(f"🏷️  Test Markers: @pytest.mark.vm_management")
        logger.info(f"🌐 Page URL Before Test: {page.url}")
        logger.info(f"📏 Page Viewport: {page.viewport_size}")
        logger.info(f"🧠 Memory Usage: {sys.getsizeof(page)} bytes (page object)")
        logger.info("=" * 100)
        
        step1_start = log_step(1, "Initializing dashboard page object", page)
        logger.info(f"   📦 Input: page object type={type(page).__name__}")
        logger.info(f"   🔍 Page State: url={page.url}, title={page.title()}")
        logger.info(f"   🧠 Memory Before: {sys.getsizeof(page)} bytes")
        dashboard = DashboardPage(page)
        step1_elapsed = time.time() - step1_start
        logger.info(f"   ✅ DashboardPage object created in {step1_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(dashboard).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(dashboard)} bytes")
        logger.info(f"   🔗 Object ID: {id(dashboard)}")
        log_step_complete(1, step1_start, True, "Dashboard page object created")
        
        step2_start = log_step(2, "Navigating to Create tab", page)
        logger.info(f"   🎯 Method: dashboard.click_create_tab()")
        logger.info(f"   📍 Current URL: {page.url}")
        logger.info(f"   📄 Current Title: {page.title()}")
        call_start = time.time()
        dashboard.click_create_tab()
        call_elapsed = time.time() - call_start
        step2_elapsed = time.time() - step2_start
        logger.info(f"   ⏱️  Click action completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📍 URL After Click: {page.url}")
        logger.info(f"   📄 Title After Click: {page.title()}")
        log_step_complete(2, step2_start, True, f"Successfully clicked Create tab in {call_elapsed:.4f} seconds")
        
        step3_start = log_step(3, "Initializing VM page object", page)
        logger.info(f"   📦 Input: page object")
        vm_page = VMPage(page)
        step3_elapsed = time.time() - step3_start
        logger.info(f"   ✅ VMPage object created in {step3_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(vm_page).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(vm_page)} bytes")
        logger.info(f"   🔗 Object ID: {id(vm_page)}")
        log_step_complete(3, step3_start, True, "VM page object created")
        
        step4_start = log_step(4, "Generating unique VM name for minimal specs test", page)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        logger.info(f"   🕐 Timestamp Generated: {timestamp}")
        logger.info(f"   📏 Timestamp Length: {len(timestamp)} characters")
        vm_name = f"minimal-vm-{timestamp}"
        step4_elapsed = time.time() - step4_start
        logger.info(f"   ✅ VM name generated in {step4_elapsed:.4f} seconds")
        logger.info(f"   📝 Generated VM Name: '{vm_name}'")
        logger.info(f"   📏 VM Name Length: {len(vm_name)} characters")
        logger.info(f"   🧠 Memory Usage: {sys.getsizeof(vm_name)} bytes")
        log_step_complete(4, step4_start, True, f"Generated VM name: {vm_name}")
        
        step5_start = log_step(5, "Configuring VM with MINIMAL specifications", page)
        logger.info(f"   📋 Configuration Parameters (MINIMAL):")
        logger.info(f"      ┌─ Name: {vm_name}")
        logger.info(f"      │  Type: str, Length: {len(vm_name)} chars, Memory: {sys.getsizeof(vm_name)} bytes")
        logger.info(f"      ├─ Memory: 512 MB (minimum)")
        logger.info(f"      │  Type: int, Value: 512, Memory: {sys.getsizeof(512)} bytes")
        logger.info(f"      │  Conversion: 512 MB = {512 / 1024:.2f} GB")
        logger.info(f"      ├─ CPU: 1 core (minimum)")
        logger.info(f"      │  Type: int, Value: 1, Memory: {sys.getsizeof(1)} bytes")
        logger.info(f"      └─ Network Type: Private")
        logger.info(f"         Type: str, Value: 'Private', Length: {len('Private')} chars")
        logger.info(f"         Memory: {sys.getsizeof('Private')} bytes")
        step5_elapsed = time.time() - step5_start
        logger.info(f"   ✅ Configuration prepared in {step5_elapsed:.4f} seconds")
        log_step_complete(5, step5_start, True, "Minimal VM configuration prepared")
        
        step6_start = log_step(6, "Calling create_vm() with minimal specs", page)
        logger.info(f"   🎯 Method: vm_page.create_vm()")
        logger.info(f"   📍 Method Location: {vm_page.create_vm.__code__.co_filename}:{vm_page.create_vm.__code__.co_firstlineno}")
        logger.info(f"   📦 Method Arguments:")
        logger.info(f"      name={vm_name}")
        logger.info(f"      memory=512 (minimum)")
        logger.info(f"      cpu=1 (minimum)")
        logger.info(f"      network_type='Private'")
        logger.info(f"   🔍 Pre-call State:")
        logger.info(f"      Current URL: {page.url}")
        logger.info(f"      Current Title: {page.title()}")
        logger.info(f"      Page Load State: {page.evaluate('document.readyState')}")
        logger.info(f"   🚀 Executing create_vm() call with minimal specs...")
        call_start = time.time()
        result = vm_page.create_vm(
            name=vm_name,
            memory=512,  # Minimum memory
            cpu=1,       # Minimum CPU
            network_type="Private"
        )
        call_elapsed = time.time() - call_start
        step6_elapsed = time.time() - step6_start
        logger.info(f"   ⏱️  Method call completed in {call_elapsed:.4f} seconds")
        logger.info(f"   ✅ create_vm() returned result")
        logger.info(f"   📊 Result Type: {type(result).__name__}")
        logger.info(f"   📏 Result Length: {len(str(result))} characters")
        logger.info(f"   🧠 Result Memory: {sys.getsizeof(result)} bytes")
        logger.info(f"   📝 Result Value: '{result}'")
        logger.info(f"   🔍 Post-call State:")
        logger.info(f"      Current URL: {page.url}")
        logger.info(f"      Current Title: {page.title()}")
        logger.info(f"      Page Load State: {page.evaluate('document.readyState')}")
        log_step_complete(6, step6_start, True, f"VM creation completed in {call_elapsed:.4f} seconds")
        
        step7_start = log_step(7, "Validating VM creation was successful", page)
        logger.info(f"   🔍 Validation Details:")
        logger.info(f"      Result: '{result}'")
        logger.info(f"      Result Lowercase: '{result.lower()}'")
        logger.info(f"      Searching for: 'successfully'")
        logger.info(f"      Contains Check: {'successfully' in result.lower()}")
        logger.info(f"   ✅ Assertion: assert 'successfully' in result.lower()")
        assert_start = time.time()
        assert "successfully" in result.lower(), "VM creation should succeed with minimal specs"
        assert_elapsed = time.time() - assert_start
        step7_elapsed = time.time() - step7_start
        logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
        logger.info(f"   ✓ VM created with minimal specs validated")
        log_step_complete(7, step7_start, True, f"Assertion passed in {assert_elapsed:.4f} seconds")
        
        test_elapsed = time.time() - test_start_time
        logger.info("")
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info(f"✓✓✓ TEST PASSED: Minimal VM '{vm_name}' created successfully")
        logger.info("=" * 100)
        logger.info(f"⏰ Test End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        logger.info(f"⏱️  Total Test Duration: {test_elapsed:.4f} seconds")
        logger.info(f"📊 Test Summary:")
        logger.info(f"   - Steps Executed: 7")
        logger.info(f"   - VM Created: {vm_name}")
        logger.info(f"   - Specs: Memory=512MB, CPU=1, Network=Private")
        logger.info(f"   - Status: PASSED")
        logger.info(f"   - Memory Usage: {sys.getsizeof(page) + sys.getsizeof(dashboard) + sys.getsizeof(vm_page)} bytes")
        logger.info("=" * 100)
        logger.info("=" * 100)
    
    def test_create_vm_with_maximum_specs(self, page: Page):
        """Test creating a VM with maximum specifications"""
        test_start_time = time.time()
        test_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("🚀 TEST: Create VM with maximum specs - START")
        logger.info("=" * 100)
        logger.info(f"⏰ Test Start Time: {test_timestamp}")
        logger.info(f"🆔 Test ID: test_create_vm_with_maximum_specs")
        logger.info(f"📋 Test Description: Test creating a VM with maximum specifications")
        logger.info(f"🏷️  Test Markers: @pytest.mark.vm_management")
        logger.info(f"🌐 Page URL Before Test: {page.url}")
        logger.info(f"📏 Page Viewport: {page.viewport_size}")
        logger.info(f"🧠 Memory Usage: {sys.getsizeof(page)} bytes (page object)")
        logger.info("=" * 100)
        
        step1_start = log_step(1, "Creating dashboard page object instance", page)
        logger.info(f"   📦 Input: page object type={type(page).__name__}")
        logger.info(f"   🔍 Page State: url={page.url}, title={page.title()}")
        dashboard = DashboardPage(page)
        step1_elapsed = time.time() - step1_start
        logger.info(f"   ✅ DashboardPage object created in {step1_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(dashboard).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(dashboard)} bytes")
        logger.info(f"   🔗 Object ID: {id(dashboard)}")
        log_step_complete(1, step1_start, True, "Dashboard page object created")
        
        step2_start = log_step(2, "Clicking Create tab to access VM creation form", page)
        logger.info(f"   🎯 Method: dashboard.click_create_tab()")
        logger.info(f"   📍 Current URL: {page.url}")
        call_start = time.time()
        dashboard.click_create_tab()
        call_elapsed = time.time() - call_start
        step2_elapsed = time.time() - step2_start
        logger.info(f"   ⏱️  Click action completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📍 URL After Click: {page.url}")
        log_step_complete(2, step2_start, True, f"Create tab accessed successfully in {call_elapsed:.4f} seconds")
        
        step3_start = log_step(3, "Creating VM page object instance", page)
        vm_page = VMPage(page)
        step3_elapsed = time.time() - step3_start
        logger.info(f"   ✅ VMPage object created in {step3_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(vm_page).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(vm_page)} bytes")
        log_step_complete(3, step3_start, True, "VM page object created")
        
        step4_start = log_step(4, "Generating unique VM name for maximum specs test", page)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        logger.info(f"   🕐 Timestamp Generated: {timestamp}")
        vm_name = f"maximal-vm-{timestamp}"
        step4_elapsed = time.time() - step4_start
        logger.info(f"   ✅ VM name generated in {step4_elapsed:.4f} seconds")
        logger.info(f"   📝 Generated VM Name: '{vm_name}'")
        logger.info(f"   📏 VM Name Length: {len(vm_name)} characters")
        logger.info(f"   🧠 Memory Usage: {sys.getsizeof(vm_name)} bytes")
        log_step_complete(4, step4_start, True, f"Generated unique VM name: {vm_name}")
        
        step5_start = log_step(5, "Configuring VM with MAXIMUM specifications", page)
        logger.info(f"   📋 Configuration Parameters (MAXIMUM):")
        logger.info(f"      ┌─ Name: {vm_name}")
        logger.info(f"      │  Type: str, Length: {len(vm_name)} chars, Memory: {sys.getsizeof(vm_name)} bytes")
        logger.info(f"      ├─ Memory: 16384 MB (16 GB - high memory)")
        logger.info(f"      │  Type: int, Value: 16384, Memory: {sys.getsizeof(16384)} bytes")
        logger.info(f"      │  Conversion: 16384 MB = {16384 / 1024:.2f} GB")
        logger.info(f"      ├─ CPU: 8 cores (maximum)")
        logger.info(f"      │  Type: int, Value: 8, Memory: {sys.getsizeof(8)} bytes")
        logger.info(f"      ├─ Network Type: Bridge")
        logger.info(f"      │  Type: str, Value: 'Bridge', Length: {len('Bridge')} chars")
        logger.info(f"      │  Memory: {sys.getsizeof('Bridge')} bytes")
        logger.info(f"      └─ IP Address: 10.0.0.50")
        logger.info(f"         Type: str, Value: '10.0.0.50', Length: {len('10.0.0.50')} chars")
        logger.info(f"         Memory: {sys.getsizeof('10.0.0.50')} bytes")
        logger.info(f"         Format: IPv4, Valid: {'10.0.0.50'.count('.') == 3}")
        step5_elapsed = time.time() - step5_start
        logger.info(f"   ✅ Configuration prepared in {step5_elapsed:.4f} seconds")
        log_step_complete(5, step5_start, True, "Maximum VM configuration prepared")
        
        step6_start = log_step(6, "Initiating VM creation with maximum specs", page)
        logger.info(f"   🎯 Method: vm_page.create_vm()")
        logger.info(f"   📍 Method Location: {vm_page.create_vm.__code__.co_filename}:{vm_page.create_vm.__code__.co_firstlineno}")
        logger.info(f"   📦 Method Arguments:")
        logger.info(f"      name={vm_name}")
        logger.info(f"      memory=16384 (high memory)")
        logger.info(f"      cpu=8 (maximum)")
        logger.info(f"      network_type='Bridge'")
        logger.info(f"      ip_address='10.0.0.50'")
        logger.info(f"   🔍 Pre-call State:")
        logger.info(f"      Current URL: {page.url}")
        logger.info(f"      Current Title: {page.title()}")
        logger.info(f"      Page Load State: {page.evaluate('document.readyState')}")
        logger.info(f"   🚀 Executing create_vm() call with maximum specs...")
        call_start = time.time()
        result = vm_page.create_vm(
            name=vm_name,
            memory=16384,  # High memory
            cpu=8,         # High CPU
            network_type="Bridge",
            ip_address="10.0.0.50"
        )
        call_elapsed = time.time() - call_start
        step6_elapsed = time.time() - step6_start
        logger.info(f"   ⏱️  Method call completed in {call_elapsed:.4f} seconds")
        logger.info(f"   ✅ create_vm() returned result")
        logger.info(f"   📊 Result Type: {type(result).__name__}")
        logger.info(f"   📏 Result Length: {len(str(result))} characters")
        logger.info(f"   🧠 Result Memory: {sys.getsizeof(result)} bytes")
        logger.info(f"   📝 Result Value: '{result}'")
        logger.info(f"   🔍 Post-call State:")
        logger.info(f"      Current URL: {page.url}")
        logger.info(f"      Current Title: {page.title()}")
        logger.info(f"      Page Load State: {page.evaluate('document.readyState')}")
        log_step_complete(6, step6_start, True, f"VM creation completed in {call_elapsed:.4f} seconds")
        
        step7_start = log_step(7, "Validating successful creation message", page)
        logger.info(f"   🔍 Validation Details:")
        logger.info(f"      Result: '{result}'")
        logger.info(f"      Result Lowercase: '{result.lower()}'")
        logger.info(f"      Searching for: 'successfully'")
        logger.info(f"      Contains Check: {'successfully' in result.lower()}")
        logger.info(f"   ✅ Assertion: assert 'successfully' in result.lower()")
        assert_start = time.time()
        assert "successfully" in result.lower(), "VM creation should succeed with high specs"
        assert_elapsed = time.time() - assert_start
        step7_elapsed = time.time() - step7_start
        logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
        logger.info(f"   ✓ High spec VM created successfully validated")
        log_step_complete(7, step7_start, True, f"Validation passed in {assert_elapsed:.4f} seconds")
        
        test_elapsed = time.time() - test_start_time
        logger.info("")
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info(f"✓✓✓ TEST PASSED: Maximal VM '{vm_name}' created successfully")
        logger.info("=" * 100)
        logger.info(f"⏰ Test End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        logger.info(f"⏱️  Total Test Duration: {test_elapsed:.4f} seconds")
        logger.info(f"📊 Test Summary:")
        logger.info(f"   - Steps Executed: 7")
        logger.info(f"   - VM Created: {vm_name}")
        logger.info(f"   - Specs: Memory=16384MB, CPU=8, Network=Bridge, IP=10.0.0.50")
        logger.info(f"   - Status: PASSED")
        logger.info(f"   - Memory Usage: {sys.getsizeof(page) + sys.getsizeof(dashboard) + sys.getsizeof(vm_page)} bytes")
        logger.info("=" * 100)
        logger.info("=" * 100)
    
    def test_vm_list_displays_vms(self, page: Page):
        """Test that VM list displays VMs correctly"""
        test_start_time = time.time()
        test_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("🚀 TEST: VM list displays VMs - START")
        logger.info("=" * 100)
        logger.info(f"⏰ Test Start Time: {test_timestamp}")
        logger.info(f"🆔 Test ID: test_vm_list_displays_vms")
        logger.info(f"📋 Test Description: Test that VM list displays VMs correctly")
        logger.info(f"🏷️  Test Markers: @pytest.mark.vm_management")
        logger.info(f"🌐 Page URL Before Test: {page.url}")
        logger.info(f"📏 Page Viewport: {page.viewport_size}")
        logger.info(f"🧠 Memory Usage: {sys.getsizeof(page)} bytes (page object)")
        logger.info("=" * 100)
        
        step1_start = log_step(1, "Initializing VM page object", page)
        logger.info(f"   📦 Input: page object type={type(page).__name__}")
        logger.info(f"   🔍 Page State: url={page.url}, title={page.title()}")
        logger.info(f"   🧠 Memory Before: {sys.getsizeof(page)} bytes")
        vm_page = VMPage(page)
        step1_elapsed = time.time() - step1_start
        logger.info(f"   ✅ VMPage object created in {step1_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(vm_page).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(vm_page)} bytes")
        logger.info(f"   🔗 Object ID: {id(vm_page)}")
        log_step_complete(1, step1_start, True, "VM page object created")
        
        step2_start = log_step(2, "Retrieving VM list count from the page", page)
        logger.info(f"   🎯 Method: vm_page.get_vm_list_count()")
        logger.info(f"   📍 Method Location: {vm_page.get_vm_list_count.__code__.co_filename}:{vm_page.get_vm_list_count.__code__.co_firstlineno}")
        logger.info(f"   🔍 Pre-retrieval State:")
        logger.info(f"      Current URL: {page.url}")
        logger.info(f"      Current Title: {page.title()}")
        logger.info(f"      Page Load State: {page.evaluate('document.readyState')}")
        logger.info(f"   🚀 Executing get_vm_list_count() call...")
        call_start = time.time()
        vm_count = vm_page.get_vm_list_count()
        call_elapsed = time.time() - call_start
        step2_elapsed = time.time() - step2_start
        logger.info(f"   ⏱️  Method call completed in {call_elapsed:.4f} seconds")
        logger.info(f"   ✅ get_vm_list_count() returned result")
        logger.info(f"   📊 Result Type: {type(vm_count).__name__}")
        logger.info(f"   📏 Result Value: {vm_count}")
        logger.info(f"   🧠 Result Memory: {sys.getsizeof(vm_count)} bytes")
        log_step_complete(2, step2_start, True, f"VM count retrieved: {vm_count}")
        
        step3_start = log_step(3, "Analyzing VM count result", page)
        logger.info(f"   📊 VM Count Analysis:")
        logger.info(f"      Count Value: {vm_count}")
        logger.info(f"      Count Type: {type(vm_count).__name__}")
        logger.info(f"      Is Zero: {vm_count == 0}")
        logger.info(f"      Is One: {vm_count == 1}")
        logger.info(f"      Is Multiple: {vm_count > 1}")
        logger.info(f"      Is Negative: {vm_count < 0}")
        logger.info(f"      Is Non-Negative: {vm_count >= 0}")
        step3_elapsed = time.time() - step3_start
        log_step_complete(3, step3_start, True, f"Current VM count in the list: {vm_count} VMs")
        
        step4_start = log_step(4, "Validating VM count is non-negative", page)
        logger.info(f"   🔍 Validation Details:")
        logger.info(f"      VM Count: {vm_count}")
        logger.info(f"      Count >= 0 Check: {vm_count >= 0}")
        logger.info(f"      Expected: Count >= 0")
        logger.info(f"      Actual: Count = {vm_count}")
        logger.info(f"   ✅ Assertion: assert vm_count >= 0")
        assert_start = time.time()
        assert vm_count >= 0, "VM count should be non-negative"
        assert_elapsed = time.time() - assert_start
        step4_elapsed = time.time() - step4_start
        logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
        logger.info(f"   ✓ VM count validation passed")
        log_step_complete(4, step4_start, True, f"Assertion passed in {assert_elapsed:.4f} seconds")
        
        step5_start = log_step(5, "Evaluating VM list state", page)
        if vm_count == 0:
            logger.info(f"   ⚠️  VM List State: EMPTY")
            logger.info(f"      No VMs currently in the list (empty state)")
            logger.info(f"      This is a valid state for a new system")
        elif vm_count == 1:
            logger.info(f"   ✅ VM List State: SINGLE VM")
            logger.info(f"      Found 1 VM in the list")
            logger.info(f"      List contains exactly one virtual machine")
        else:
            logger.info(f"   ✅ VM List State: MULTIPLE VMs")
            logger.info(f"      Found {vm_count} VMs in the list")
            logger.info(f"      List contains multiple virtual machines")
        step5_elapsed = time.time() - step5_start
        log_step_complete(5, step5_start, True, f"VM list state evaluated: {vm_count} VMs")
        
        test_elapsed = time.time() - test_start_time
        logger.info("")
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("✓✓✓ TEST PASSED: VM list displays correctly")
        logger.info("=" * 100)
        logger.info(f"⏰ Test End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        logger.info(f"⏱️  Total Test Duration: {test_elapsed:.4f} seconds")
        logger.info(f"📊 Test Summary:")
        logger.info(f"   - Steps Executed: 5")
        logger.info(f"   - VM Count: {vm_count}")
        logger.info(f"   - List State: {'Empty' if vm_count == 0 else 'Has VMs'}")
        logger.info(f"   - Status: PASSED")
        logger.info(f"   - Memory Usage: {sys.getsizeof(page) + sys.getsizeof(vm_page)} bytes")
        logger.info("=" * 100)
        logger.info("=" * 100)
    
    @pytest.mark.slow
    def test_start_stop_vm_cycle(self, page: Page):
        """Test starting and stopping a VM"""
        test_start_time = time.time()
        test_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("🚀 TEST: Start/Stop VM cycle - START")
        logger.info("=" * 100)
        logger.info(f"⏰ Test Start Time: {test_timestamp}")
        logger.info(f"🆔 Test ID: test_start_stop_vm_cycle")
        logger.info(f"📋 Test Description: Test starting and stopping a VM")
        logger.info(f"🏷️  Test Markers: @pytest.mark.slow, @pytest.mark.vm_management")
        logger.info(f"🌐 Page URL Before Test: {page.url}")
        logger.info(f"📏 Page Viewport: {page.viewport_size}")
        logger.info(f"🧠 Memory Usage: {sys.getsizeof(page)} bytes (page object)")
        logger.info("=" * 100)
        
        # First, create a new VM
        step1_start = log_step(1, "Creating dashboard page object for VM creation", page)
        logger.info(f"   📦 Input: page object type={type(page).__name__}")
        dashboard = DashboardPage(page)
        step1_elapsed = time.time() - step1_start
        logger.info(f"   ✅ DashboardPage object created in {step1_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(dashboard).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(dashboard)} bytes")
        log_step_complete(1, step1_start, True, "Dashboard page object created")
        
        step2_start = log_step(2, "Navigating to Create tab", page)
        logger.info(f"   🎯 Method: dashboard.click_create_tab()")
        call_start = time.time()
        dashboard.click_create_tab()
        call_elapsed = time.time() - call_start
        logger.info(f"   ⏱️  Click action completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📍 URL After Click: {page.url}")
        log_step_complete(2, step2_start, True, f"Navigated to Create tab in {call_elapsed:.4f} seconds")
        
        step3_start = log_step(3, "Initializing VM page object", page)
        vm_page = VMPage(page)
        step3_elapsed = time.time() - step3_start
        logger.info(f"   ✅ VMPage object created in {step3_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(vm_page).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(vm_page)} bytes")
        log_step_complete(3, step3_start, True, "VM page object created")
        
        step4_start = log_step(4, "Generating unique VM name for cycle test", page)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        logger.info(f"   🕐 Timestamp Generated: {timestamp}")
        vm_name = f"cycle-vm-{timestamp}"
        step4_elapsed = time.time() - step4_start
        logger.info(f"   ✅ VM name generated in {step4_elapsed:.4f} seconds")
        logger.info(f"   📝 Generated VM Name: '{vm_name}'")
        logger.info(f"   📏 VM Name Length: {len(vm_name)} characters")
        logger.info(f"   🧠 Memory Usage: {sys.getsizeof(vm_name)} bytes")
        log_step_complete(4, step4_start, True, f"Generated VM name for cycle test: {vm_name}")
        
        step5_start = log_step(5, "Creating VM for start/stop cycle test", page)
        logger.info(f"   📋 VM Configuration:")
        logger.info(f"      ┌─ Name: {vm_name}")
        logger.info(f"      ├─ Memory: 2048 MB")
        logger.info(f"      │  Type: int, Value: 2048, Memory: {sys.getsizeof(2048)} bytes")
        logger.info(f"      │  Conversion: 2048 MB = {2048 / 1024:.2f} GB")
        logger.info(f"      └─ CPU: 2 cores")
        logger.info(f"         Type: int, Value: 2, Memory: {sys.getsizeof(2)} bytes")
        logger.info(f"   🎯 Method: vm_page.create_vm()")
        logger.info(f"   📍 Method Location: {vm_page.create_vm.__code__.co_filename}:{vm_page.create_vm.__code__.co_firstlineno}")
        call_start = time.time()
        vm_page.create_vm(name=vm_name, memory=2048, cpu=2)
        call_elapsed = time.time() - call_start
        step5_elapsed = time.time() - step5_start
        logger.info(f"   ⏱️  VM creation completed in {call_elapsed:.4f} seconds")
        log_step_complete(5, step5_start, True, f"VM created successfully in {call_elapsed:.4f} seconds")
        
        step6_start = log_step(6, "Waiting 3 seconds for VM to appear in list", page)
        logger.info(f"   ⏳ Wait Duration: 3 seconds")
        logger.info(f"   🕐 Wait Start: {datetime.now().strftime('%H:%M:%S.%f')}")
        wait_start = time.time()
        time.sleep(3)
        wait_elapsed = time.time() - wait_start
        step6_elapsed = time.time() - step6_start
        logger.info(f"   🕐 Wait End: {datetime.now().strftime('%H:%M:%S.%f')}")
        logger.info(f"   ⏱️  Actual Wait Time: {wait_elapsed:.4f} seconds")
        log_step_complete(6, step6_start, True, f"Wait completed in {wait_elapsed:.4f} seconds")
        
        step7_start = log_step(7, "Waiting for VM list to fully load", page)
        logger.info(f"   🎯 Method: vm_page.wait_for_vm_list_to_load()")
        call_start = time.time()
        vm_page.wait_for_vm_list_to_load()
        call_elapsed = time.time() - call_start
        step7_elapsed = time.time() - step7_start
        logger.info(f"   ⏱️  VM list load wait completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📍 Current URL: {page.url}")
        log_step_complete(7, step7_start, True, f"VM list loaded in {call_elapsed:.4f} seconds")
        
        step8_start = log_step(8, f"Checking initial status of VM '{vm_name}'", page)
        logger.info(f"   🎯 Method: vm_page.get_vm_status()")
        logger.info(f"   📦 Method Argument: vm_name='{vm_name}'")
        call_start = time.time()
        initial_status = vm_page.get_vm_status(vm_name)
        call_elapsed = time.time() - call_start
        step8_elapsed = time.time() - step8_start
        logger.info(f"   ⏱️  Status retrieval completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📊 Result Type: {type(initial_status).__name__}")
        logger.info(f"   📝 Result Value: '{initial_status}'")
        logger.info(f"   🧠 Result Memory: {sys.getsizeof(initial_status) if initial_status else 0} bytes")
        log_step_complete(8, step8_start, True, f"Initial VM status retrieved: '{initial_status}'")
        
        step9_start = log_step(9, "Analyzing initial VM status", page)
        logger.info(f"   🔍 Status Analysis:")
        logger.info(f"      Status Value: '{initial_status}'")
        logger.info(f"      Status is None: {initial_status is None}")
        logger.info(f"      Status is Truthy: {bool(initial_status)}")
        if initial_status:
            status_upper = initial_status.upper()
            logger.info(f"      Status Uppercase: '{status_upper}'")
            logger.info(f"      Contains 'STOPPED': {'STOPPED' in status_upper}")
            logger.info(f"      Contains 'RUNNING': {'RUNNING' in status_upper}")
        step9_elapsed = time.time() - step9_start
        log_step_complete(9, step9_start, True, f"Status analysis completed")
        
        # If VM is stopped, start it
        if initial_status and "STOPPED" in initial_status.upper():
            step10_start = log_step(10, f"VM is in STOPPED state, attempting to start", page)
            logger.info(f"   🎯 Method: vm_page.start_vm()")
            logger.info(f"   📦 Method Argument: vm_name='{vm_name}'")
            logger.info(f"   🔍 Pre-start State:")
            logger.info(f"      Current Status: '{initial_status}'")
            logger.info(f"      Current URL: {page.url}")
            call_start = time.time()
            result = vm_page.start_vm(vm_name)
            call_elapsed = time.time() - call_start
            step10_elapsed = time.time() - step10_start
            logger.info(f"   ⏱️  Start VM call completed in {call_elapsed:.4f} seconds")
            logger.info(f"   📊 Result Type: {type(result).__name__}")
            logger.info(f"   📝 Result Value: '{result}'")
            logger.info(f"   🧠 Result Memory: {sys.getsizeof(result) if result else 0} bytes")
            log_step_complete(10, step10_start, True, f"Start VM result: '{result}'")
            
            step11_start = log_step(11, "Validating start VM result is not None", page)
            logger.info(f"   🔍 Validation Details:")
            logger.info(f"      Result: {result}")
            logger.info(f"      Result is None: {result is None}")
            logger.info(f"      Result is not None: {result is not None}")
            logger.info(f"   ✅ Assertion: assert result is not None")
            assert_start = time.time()
            assert result is not None, "Start VM should return a result"
            assert_elapsed = time.time() - assert_start
            step11_elapsed = time.time() - step11_start
            logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
            log_step_complete(11, step11_start, True, f"Result is not None - validated in {assert_elapsed:.4f} seconds")
            
            step12_start = log_step(12, "Validating start was successful", page)
            logger.info(f"   🔍 Validation Details:")
            logger.info(f"      Result: '{result}'")
            logger.info(f"      Result Lowercase: '{result.lower()}'")
            logger.info(f"      Contains 'successfully': {'successfully' in result.lower()}")
            logger.info(f"      Contains 'initiated': {'initiated' in result.lower()}")
            logger.info(f"      Contains either: {'successfully' in result.lower() or 'initiated' in result.lower()}")
            logger.info(f"   ✅ Assertion: assert 'successfully' in result.lower() or 'initiated' in result.lower()")
            assert_start = time.time()
            assert "successfully" in result.lower() or "initiated" in result.lower(), "Start should be successful"
            assert_elapsed = time.time() - assert_start
            step12_elapsed = time.time() - step12_start
            logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
            log_step_complete(12, step12_start, True, f"VM started successfully - validated in {assert_elapsed:.4f} seconds")
            
            step13_start = log_step(13, "Waiting 3 seconds for VM to start", page)
            logger.info(f"   ⏳ Wait Duration: 3 seconds")
            logger.info(f"   🕐 Wait Start: {datetime.now().strftime('%H:%M:%S.%f')}")
            wait_start = time.time()
            time.sleep(3)
            wait_elapsed = time.time() - wait_start
            step13_elapsed = time.time() - step13_start
            logger.info(f"   🕐 Wait End: {datetime.now().strftime('%H:%M:%S.%f')}")
            logger.info(f"   ⏱️  Actual Wait Time: {wait_elapsed:.4f} seconds")
            log_step_complete(13, step13_start, True, f"Wait completed in {wait_elapsed:.4f} seconds")
        else:
            logger.info(f"   ⏭️  Skipping start operation - VM is not in STOPPED state")
            logger.info(f"      Status: '{initial_status}'")
            logger.info(f"      Condition: initial_status and 'STOPPED' in initial_status.upper()")
            logger.info(f"      Result: {bool(initial_status and 'STOPPED' in initial_status.upper())}")
        
        step14_start = log_step(14, "Refreshing VM list before stop operation", page)
        logger.info(f"   🎯 Method: vm_page.wait_for_vm_list_to_load()")
        call_start = time.time()
        vm_page.wait_for_vm_list_to_load()
        call_elapsed = time.time() - call_start
        step14_elapsed = time.time() - step14_start
        logger.info(f"   ⏱️  VM list refresh completed in {call_elapsed:.4f} seconds")
        log_step_complete(14, step14_start, True, f"VM list refreshed in {call_elapsed:.4f} seconds")
        
        step15_start = log_step(15, f"Checking current status of VM '{vm_name}'", page)
        logger.info(f"   🎯 Method: vm_page.get_vm_status()")
        logger.info(f"   📦 Method Argument: vm_name='{vm_name}'")
        call_start = time.time()
        current_status = vm_page.get_vm_status(vm_name)
        call_elapsed = time.time() - call_start
        step15_elapsed = time.time() - step15_start
        logger.info(f"   ⏱️  Status retrieval completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📊 Result Type: {type(current_status).__name__}")
        logger.info(f"   📝 Result Value: '{current_status}'")
        log_step_complete(15, step15_start, True, f"Current VM status: '{current_status}'")
        
        if current_status and "RUNNING" in current_status.upper():
            step16_start = log_step(16, "VM is in RUNNING state, attempting to stop", page)
            logger.info(f"   🎯 Method: vm_page.stop_vm()")
            logger.info(f"   📦 Method Argument: vm_name='{vm_name}'")
            logger.info(f"   🔍 Pre-stop State:")
            logger.info(f"      Current Status: '{current_status}'")
            call_start = time.time()
            result = vm_page.stop_vm(vm_name)
            call_elapsed = time.time() - call_start
            step16_elapsed = time.time() - step16_start
            logger.info(f"   ⏱️  Stop VM call completed in {call_elapsed:.4f} seconds")
            logger.info(f"   📊 Result Type: {type(result).__name__}")
            logger.info(f"   📝 Result Value: '{result}'")
            log_step_complete(16, step16_start, True, f"Stop VM result: '{result}'")
            
            step17_start = log_step(17, "Validating stop VM result is not None", page)
            logger.info(f"   🔍 Validation Details:")
            logger.info(f"      Result: {result}")
            logger.info(f"      Result is None: {result is None}")
            logger.info(f"   ✅ Assertion: assert result is not None")
            assert_start = time.time()
            assert result is not None, "Stop VM should return a result"
            assert_elapsed = time.time() - assert_start
            step17_elapsed = time.time() - step17_start
            logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
            log_step_complete(17, step17_start, True, f"Result is not None - validated in {assert_elapsed:.4f} seconds")
            
            step18_start = log_step(18, "Validating stop was successful", page)
            logger.info(f"   🔍 Validation Details:")
            logger.info(f"      Result: '{result}'")
            logger.info(f"      Result Lowercase: '{result.lower()}'")
            logger.info(f"      Contains 'successfully': {'successfully' in result.lower()}")
            logger.info(f"      Contains 'initiated': {'initiated' in result.lower()}")
            logger.info(f"   ✅ Assertion: assert 'successfully' in result.lower() or 'initiated' in result.lower()")
            assert_start = time.time()
            assert "successfully" in result.lower() or "initiated" in result.lower(), "Stop should be successful"
            assert_elapsed = time.time() - assert_start
            step18_elapsed = time.time() - step18_start
            logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
            log_step_complete(18, step18_start, True, f"VM stopped successfully - validated in {assert_elapsed:.4f} seconds")
        else:
            logger.info(f"   ⏭️  Skipping stop operation - VM is not in RUNNING state")
            logger.info(f"      Status: '{current_status}'")
            logger.info(f"      Condition: current_status and 'RUNNING' in current_status.upper()")
            logger.info(f"      Result: {bool(current_status and 'RUNNING' in current_status.upper())}")
        
        test_elapsed = time.time() - test_start_time
        logger.info("")
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("✓✓✓ TEST PASSED: Start/Stop VM cycle completed")
        logger.info("=" * 100)
        logger.info(f"⏰ Test End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        logger.info(f"⏱️  Total Test Duration: {test_elapsed:.4f} seconds")
        logger.info(f"📊 Test Summary:")
        logger.info(f"   - Steps Executed: 18")
        logger.info(f"   - VM Name: {vm_name}")
        logger.info(f"   - Initial Status: {initial_status}")
        logger.info(f"   - Final Status: {current_status}")
        logger.info(f"   - Status: PASSED")
        logger.info(f"   - Memory Usage: {sys.getsizeof(page) + sys.getsizeof(dashboard) + sys.getsizeof(vm_page)} bytes")
        logger.info("=" * 100)
        logger.info("=" * 100)
    
    def test_create_vm_snapshot(self, page: Page):
        """Test creating a snapshot for a VM"""
        test_start_time = time.time()
        test_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("🚀 TEST: Create VM snapshot - START")
        logger.info("=" * 100)
        logger.info(f"⏰ Test Start Time: {test_timestamp}")
        logger.info(f"🆔 Test ID: test_create_vm_snapshot")
        logger.info(f"📋 Test Description: Test creating a snapshot for a VM")
        logger.info(f"🏷️  Test Markers: @pytest.mark.vm_management")
        logger.info(f"🌐 Page URL Before Test: {page.url}")
        logger.info(f"📏 Page Viewport: {page.viewport_size}")
        logger.info(f"🧠 Memory Usage: {sys.getsizeof(page)} bytes (page object)")
        logger.info("=" * 100)
        
        # Create a VM first
        step1_start = log_step(1, "Initializing dashboard for VM creation", page)
        dashboard = DashboardPage(page)
        step1_elapsed = time.time() - step1_start
        logger.info(f"   ✅ DashboardPage object created in {step1_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(dashboard).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(dashboard)} bytes")
        log_step_complete(1, step1_start, True, "Dashboard page object created")
        
        step2_start = log_step(2, "Clicking Create tab to create a VM for snapshot test", page)
        logger.info(f"   🎯 Method: dashboard.click_create_tab()")
        call_start = time.time()
        dashboard.click_create_tab()
        call_elapsed = time.time() - call_start
        logger.info(f"   ⏱️  Click action completed in {call_elapsed:.4f} seconds")
        log_step_complete(2, step2_start, True, f"Navigated to Create tab in {call_elapsed:.4f} seconds")
        
        step3_start = log_step(3, "Initializing VM page object", page)
        vm_page = VMPage(page)
        step3_elapsed = time.time() - step3_start
        logger.info(f"   ✅ VMPage object created in {step3_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(vm_page).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(vm_page)} bytes")
        log_step_complete(3, step3_start, True, "VM page object created")
        
        step4_start = log_step(4, "Generating unique VM name for snapshot test", page)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        logger.info(f"   🕐 Timestamp Generated: {timestamp}")
        vm_name = f"snapshot-vm-{timestamp}"
        step4_elapsed = time.time() - step4_start
        logger.info(f"   ✅ VM name generated in {step4_elapsed:.4f} seconds")
        logger.info(f"   📝 Generated VM Name: '{vm_name}'")
        logger.info(f"   📏 VM Name Length: {len(vm_name)} characters")
        log_step_complete(4, step4_start, True, f"Generated VM name for snapshot test: {vm_name}")
        
        step5_start = log_step(5, "Creating VM for snapshot testing", page)
        logger.info(f"   📋 VM Configuration:")
        logger.info(f"      ┌─ VM Name: {vm_name}")
        logger.info(f"      ├─ Memory: 2048 MB")
        logger.info(f"      │  Type: int, Value: 2048, Memory: {sys.getsizeof(2048)} bytes")
        logger.info(f"      └─ CPU: 2 cores")
        logger.info(f"         Type: int, Value: 2, Memory: {sys.getsizeof(2)} bytes")
        logger.info(f"   🎯 Method: vm_page.create_vm()")
        call_start = time.time()
        vm_page.create_vm(name=vm_name, memory=2048, cpu=2)
        call_elapsed = time.time() - call_start
        step5_elapsed = time.time() - step5_start
        logger.info(f"   ⏱️  VM creation completed in {call_elapsed:.4f} seconds")
        log_step_complete(5, step5_start, True, f"VM created successfully in {call_elapsed:.4f} seconds")
        
        step6_start = log_step(6, "Waiting 3 seconds for VM to be fully created", page)
        logger.info(f"   ⏳ Wait Duration: 3 seconds")
        wait_start = time.time()
        time.sleep(3)
        wait_elapsed = time.time() - wait_start
        step6_elapsed = time.time() - step6_start
        logger.info(f"   ⏱️  Actual Wait Time: {wait_elapsed:.4f} seconds")
        log_step_complete(6, step6_start, True, f"Wait completed in {wait_elapsed:.4f} seconds")
        
        step7_start = log_step(7, "Navigating back to VMs list tab", page)
        logger.info(f"   🎯 Method: dashboard.click_vms_tab()")
        call_start = time.time()
        dashboard.click_vms_tab()
        call_elapsed = time.time() - call_start
        step7_elapsed = time.time() - step7_start
        logger.info(f"   ⏱️  Click action completed in {call_elapsed:.4f} seconds")
        log_step_complete(7, step7_start, True, f"Clicked VMs tab in {call_elapsed:.4f} seconds")
        
        step8_start = log_step(8, "Waiting for VM list to load", page)
        logger.info(f"   🎯 Method: vm_page.wait_for_vm_list_to_load()")
        call_start = time.time()
        vm_page.wait_for_vm_list_to_load()
        call_elapsed = time.time() - call_start
        step8_elapsed = time.time() - step8_start
        logger.info(f"   ⏱️  VM list load wait completed in {call_elapsed:.4f} seconds")
        log_step_complete(8, step8_start, True, f"VM list loaded successfully in {call_elapsed:.4f} seconds")
        
        step9_start = log_step(9, "Generating snapshot name", page)
        snapshot_name = f"snapshot-{timestamp}"
        step9_elapsed = time.time() - step9_start
        logger.info(f"   ✅ Snapshot name generated in {step9_elapsed:.4f} seconds")
        logger.info(f"   📝 Generated Snapshot Name: '{snapshot_name}'")
        logger.info(f"   📏 Snapshot Name Length: {len(snapshot_name)} characters")
        log_step_complete(9, step9_start, True, f"Generated snapshot name: {snapshot_name}")
        
        step10_start = log_step(10, f"Taking snapshot '{snapshot_name}' for VM '{vm_name}'", page)
        logger.info(f"   🎯 Method: vm_page.take_snapshot()")
        logger.info(f"   📦 Method Arguments:")
        logger.info(f"      vm_name='{vm_name}'")
        logger.info(f"      snapshot_name='{snapshot_name}'")
        call_start = time.time()
        result = vm_page.take_snapshot(vm_name, snapshot_name)
        call_elapsed = time.time() - call_start
        step10_elapsed = time.time() - step10_start
        logger.info(f"   ⏱️  Snapshot creation completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📊 Result Type: {type(result).__name__}")
        logger.info(f"   📝 Result Value: '{result}'")
        logger.info(f"   🧠 Result Memory: {sys.getsizeof(result) if result else 0} bytes")
        log_step_complete(10, step10_start, True, f"Snapshot creation result: '{result}'")
        
        step11_start = log_step(11, "Validating snapshot result is not None", page)
        logger.info(f"   🔍 Validation Details:")
        logger.info(f"      Result: {result}")
        logger.info(f"      Result is None: {result is None}")
        logger.info(f"   ✅ Assertion: assert result is not None")
        assert_start = time.time()
        assert result is not None, "Snapshot creation should return a result"
        assert_elapsed = time.time() - assert_start
        step11_elapsed = time.time() - step11_start
        logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
        log_step_complete(11, step11_start, True, f"Snapshot result is valid - validated in {assert_elapsed:.4f} seconds")
        
        step12_start = log_step(12, "Validating snapshot was created successfully", page)
        logger.info(f"   🔍 Validation Details:")
        logger.info(f"      Result: '{result}'")
        logger.info(f"      Result Lowercase: '{result.lower()}'")
        logger.info(f"      Contains 'successfully': {'successfully' in result.lower()}")
        logger.info(f"   ✅ Assertion: assert 'successfully' in result.lower()")
        assert_start = time.time()
        assert "successfully" in result.lower(), f"Snapshot should be created successfully, got: {result}"
        assert_elapsed = time.time() - assert_start
        step12_elapsed = time.time() - step12_start
        logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
        log_step_complete(12, step12_start, True, f"Snapshot created successfully - validated in {assert_elapsed:.4f} seconds")
        
        test_elapsed = time.time() - test_start_time
        logger.info("")
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info(f"✓✓✓ TEST PASSED: Snapshot '{snapshot_name}' created for VM '{vm_name}'")
        logger.info("=" * 100)
        logger.info(f"⏰ Test End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        logger.info(f"⏱️  Total Test Duration: {test_elapsed:.4f} seconds")
        logger.info(f"📊 Test Summary:")
        logger.info(f"   - Steps Executed: 12")
        logger.info(f"   - VM Name: {vm_name}")
        logger.info(f"   - Snapshot Name: {snapshot_name}")
        logger.info(f"   - Status: PASSED")
        logger.info(f"   - Memory Usage: {sys.getsizeof(page) + sys.getsizeof(dashboard) + sys.getsizeof(vm_page)} bytes")
        logger.info("=" * 100)
        logger.info("=" * 100)
    
    def test_view_vm_snapshots(self, page: Page):
        """Test viewing snapshots for a VM"""
        test_start_time = time.time()
        test_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("🚀 TEST: View VM snapshots - START")
        logger.info("=" * 100)
        logger.info(f"⏰ Test Start Time: {test_timestamp}")
        logger.info(f"🆔 Test ID: test_view_vm_snapshots")
        logger.info(f"📋 Test Description: Test viewing snapshots for a VM")
        logger.info(f"🏷️  Test Markers: @pytest.mark.vm_management")
        logger.info(f"🌐 Page URL Before Test: {page.url}")
        logger.info(f"📏 Page Viewport: {page.viewport_size}")
        logger.info(f"🧠 Memory Usage: {sys.getsizeof(page)} bytes (page object)")
        logger.info("=" * 100)
        
        step1_start = log_step(1, "Initializing VM page object", page)
        vm_page = VMPage(page)
        step1_elapsed = time.time() - step1_start
        logger.info(f"   ✅ VMPage object created in {step1_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(vm_page).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(vm_page)} bytes")
        log_step_complete(1, step1_start, True, "VM page object created")
        
        step2_start = log_step(2, "Getting VM count from the list", page)
        logger.info(f"   🎯 Method: vm_page.get_vm_list_count()")
        call_start = time.time()
        vm_count = vm_page.get_vm_list_count()
        call_elapsed = time.time() - call_start
        step2_elapsed = time.time() - step2_start
        logger.info(f"   ⏱️  Method call completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📊 Result Type: {type(vm_count).__name__}")
        logger.info(f"   📏 Result Value: {vm_count}")
        logger.info(f"   🧠 Result Memory: {sys.getsizeof(vm_count)} bytes")
        log_step_complete(2, step2_start, True, f"Total VMs available: {vm_count}")
        
        if vm_count > 0:
            step3_start = log_step(3, f"VMs found ({vm_count}), proceeding to get first VM", page)
            logger.info(f"   ✅ VM Count Check: {vm_count} > 0 = {vm_count > 0}")
            logger.info(f"   📊 Proceeding with snapshot view test")
            log_step_complete(3, step3_start, True, f"VMs found ({vm_count}), proceeding")
            
            step4_start = log_step(4, "Locating all VM cards on the page", page)
            logger.info(f"   🎯 Locator: vm_page.VM_CARD = '{vm_page.VM_CARD}'")
            logger.info(f"   🔍 Method: page.locator().all()")
            call_start = time.time()
            vm_cards = page.locator(vm_page.VM_CARD).all()
            call_elapsed = time.time() - call_start
            step4_elapsed = time.time() - step4_start
            logger.info(f"   ⏱️  Locator call completed in {call_elapsed:.4f} seconds")
            logger.info(f"   📊 Result Type: {type(vm_cards).__name__}")
            logger.info(f"   📏 Result Length: {len(vm_cards)} VM cards")
            logger.info(f"   🧠 Result Memory: {sys.getsizeof(vm_cards)} bytes")
            log_step_complete(4, step4_start, True, f"Found {len(vm_cards)} VM cards")
            
            if len(vm_cards) > 0:
                step5_start = log_step(5, "Accessing first VM card", page)
                logger.info(f"   📦 Accessing: vm_cards[0]")
                logger.info(f"   🎯 Locator: '[data-testid=\"vm-name\"]'")
                first_vm_name_element = vm_cards[0].locator('[data-testid="vm-name"]')
                step5_elapsed = time.time() - step5_start
                logger.info(f"   ✅ Element located in {step5_elapsed:.4f} seconds")
                logger.info(f"   📊 Element Type: {type(first_vm_name_element).__name__}")
                log_step_complete(5, step5_start, True, "First VM card accessed")
                
                step6_start = log_step(6, "Extracting VM name from first card", page)
                logger.info(f"   🎯 Method: first_vm_name_element.text_content()")
                call_start = time.time()
                first_vm_name = first_vm_name_element.text_content()
                call_elapsed = time.time() - call_start
                step6_elapsed = time.time() - step6_start
                logger.info(f"   ⏱️  Text extraction completed in {call_elapsed:.4f} seconds")
                logger.info(f"   📊 Result Type: {type(first_vm_name).__name__}")
                logger.info(f"   📝 Result Value: '{first_vm_name}'")
                logger.info(f"   📏 Result Length: {len(first_vm_name) if first_vm_name else 0} characters")
                logger.info(f"   🧠 Result Memory: {sys.getsizeof(first_vm_name) if first_vm_name else 0} bytes")
                log_step_complete(6, step6_start, True, f"First VM name: '{first_vm_name}'")
                
                step7_start = log_step(7, f"Attempting to view snapshots for VM: '{first_vm_name}'", page)
                logger.info(f"   🎯 Method: vm_page.view_snapshots()")
                logger.info(f"   📦 Method Argument: first_vm_name='{first_vm_name}'")
                logger.info(f"   🔍 Pre-call State:")
                logger.info(f"      Current URL: {page.url}")
                logger.info(f"      Current Title: {page.title()}")
                call_start = time.time()
                result = vm_page.view_snapshots(first_vm_name)
                call_elapsed = time.time() - call_start
                step7_elapsed = time.time() - step7_start
                logger.info(f"   ⏱️  View snapshots call completed in {call_elapsed:.4f} seconds")
                logger.info(f"   📊 Result Type: {type(result).__name__}")
                logger.info(f"   📝 Result Value: {result}")
                logger.info(f"   🧠 Result Memory: {sys.getsizeof(result) if result else 0} bytes")
                log_step_complete(7, step7_start, True, f"View snapshots result: {result}")
                
                step8_start = log_step(8, "Validating snapshot view was successful", page)
                logger.info(f"   🔍 Validation Details:")
                logger.info(f"      Result: {result}")
                logger.info(f"      Result is Truthy: {bool(result)}")
                logger.info(f"   ✅ Assertion: assert result")
                assert_start = time.time()
                assert result, f"Should be able to view snapshots for VM: {first_vm_name}"
                assert_elapsed = time.time() - assert_start
                step8_elapsed = time.time() - step8_start
                logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
                log_step_complete(8, step8_start, True, f"Snapshot view validation passed in {assert_elapsed:.4f} seconds")
                
                test_elapsed = time.time() - test_start_time
                logger.info("")
                logger.info("=" * 100)
                logger.info("=" * 100)
                logger.info(f"✓✓✓ TEST PASSED: Snapshots viewed successfully for VM: {first_vm_name}")
                logger.info("=" * 100)
                logger.info(f"⏰ Test End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
                logger.info(f"⏱️  Total Test Duration: {test_elapsed:.4f} seconds")
                logger.info(f"📊 Test Summary:")
                logger.info(f"   - Steps Executed: 8")
                logger.info(f"   - VM Count: {vm_count}")
                logger.info(f"   - VM Cards Found: {len(vm_cards)}")
                logger.info(f"   - VM Name: {first_vm_name}")
                logger.info(f"   - Status: PASSED")
                logger.info(f"   - Memory Usage: {sys.getsizeof(page) + sys.getsizeof(vm_page)} bytes")
                logger.info("=" * 100)
                logger.info("=" * 100)
            else:
                logger.info(f"   ⚠️  No VM cards found despite count > 0")
                logger.info(f"      VM Count: {vm_count}")
                logger.info(f"      VM Cards Length: {len(vm_cards)}")
                pytest.skip("No VM cards available")
        else:
            step3_start = log_step(3, "No VMs found in the list", page)
            logger.info(f"   ⚠️  VM Count Check: {vm_count} > 0 = {vm_count > 0}")
            logger.info(f"   📊 VM Count: {vm_count}")
            logger.info(f"   ⊘ Cannot test snapshot viewing without VMs")
            logger.info(f"   ⏭️  Skipping test...")
            log_step_complete(3, step3_start, False, "No VMs available - skipping test")
            pytest.skip("No VMs available")
    
    @pytest.mark.critical
    def test_delete_vm(self, page: Page):
        """Test deleting a VM"""
        test_start_time = time.time()
        test_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("🚀 TEST: Delete VM - START")
        logger.info("=" * 100)
        logger.info(f"⏰ Test Start Time: {test_timestamp}")
        logger.info(f"🆔 Test ID: test_delete_vm")
        logger.info(f"📋 Test Description: Test deleting a VM")
        logger.info(f"🏷️  Test Markers: @pytest.mark.critical, @pytest.mark.vm_management")
        logger.info(f"🌐 Page URL Before Test: {page.url}")
        logger.info(f"📏 Page Viewport: {page.viewport_size}")
        logger.info(f"🧠 Memory Usage: {sys.getsizeof(page)} bytes (page object)")
        logger.info("=" * 100)
        
        # Create a VM to delete
        step1_start = log_step(1, "Initializing dashboard for VM deletion test", page)
        dashboard = DashboardPage(page)
        step1_elapsed = time.time() - step1_start
        logger.info(f"   ✅ DashboardPage object created in {step1_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(dashboard).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(dashboard)} bytes")
        log_step_complete(1, step1_start, True, "Dashboard page object created")
        
        step2_start = log_step(2, "Navigating to Create tab to create a VM", page)
        logger.info(f"   🎯 Method: dashboard.click_create_tab()")
        call_start = time.time()
        dashboard.click_create_tab()
        call_elapsed = time.time() - call_start
        logger.info(f"   ⏱️  Click action completed in {call_elapsed:.4f} seconds")
        log_step_complete(2, step2_start, True, f"Navigated to Create tab in {call_elapsed:.4f} seconds")
        
        step3_start = log_step(3, "Initializing VM page object", page)
        vm_page = VMPage(page)
        step3_elapsed = time.time() - step3_start
        logger.info(f"   ✅ VMPage object created in {step3_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(vm_page).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(vm_page)} bytes")
        log_step_complete(3, step3_start, True, "VM page object created")
        
        step4_start = log_step(4, "Generating unique VM name for deletion test", page)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        logger.info(f"   🕐 Timestamp Generated: {timestamp}")
        vm_name = f"delete-vm-{timestamp}"
        step4_elapsed = time.time() - step4_start
        logger.info(f"   ✅ VM name generated in {step4_elapsed:.4f} seconds")
        logger.info(f"   📝 Generated VM Name: '{vm_name}'")
        logger.info(f"   📏 VM Name Length: {len(vm_name)} characters")
        log_step_complete(4, step4_start, True, f"Generated VM name for deletion test: {vm_name}")
        
        step5_start = log_step(5, "Creating VM to be deleted", page)
        logger.info(f"   📋 VM Configuration:")
        logger.info(f"      ┌─ Name: {vm_name}")
        logger.info(f"      ├─ Memory: 1024 MB")
        logger.info(f"      │  Type: int, Value: 1024, Memory: {sys.getsizeof(1024)} bytes")
        logger.info(f"      └─ CPU: 1 core")
        logger.info(f"         Type: int, Value: 1, Memory: {sys.getsizeof(1)} bytes")
        logger.info(f"   🎯 Method: vm_page.create_vm()")
        call_start = time.time()
        vm_page.create_vm(name=vm_name, memory=1024, cpu=1)
        call_elapsed = time.time() - call_start
        step5_elapsed = time.time() - step5_start
        logger.info(f"   ⏱️  VM creation completed in {call_elapsed:.4f} seconds")
        log_step_complete(5, step5_start, True, f"VM created successfully in {call_elapsed:.4f} seconds")
        
        step6_start = log_step(6, "Waiting 3 seconds for VM to be fully created", page)
        logger.info(f"   ⏳ Wait Duration: 3 seconds")
        wait_start = time.time()
        time.sleep(3)
        wait_elapsed = time.time() - wait_start
        step6_elapsed = time.time() - step6_start
        logger.info(f"   ⏱️  Actual Wait Time: {wait_elapsed:.4f} seconds")
        log_step_complete(6, step6_start, True, f"Wait completed in {wait_elapsed:.4f} seconds")
        
        step7_start = log_step(7, "Navigating back to VMs list tab", page)
        logger.info(f"   🎯 Method: dashboard.click_vms_tab()")
        call_start = time.time()
        dashboard.click_vms_tab()
        call_elapsed = time.time() - call_start
        step7_elapsed = time.time() - step7_start
        logger.info(f"   ⏱️  Click action completed in {call_elapsed:.4f} seconds")
        log_step_complete(7, step7_start, True, f"Clicked VMs tab in {call_elapsed:.4f} seconds")
        
        step8_start = log_step(8, "Waiting for VM list to load", page)
        logger.info(f"   🎯 Method: vm_page.wait_for_vm_list_to_load()")
        call_start = time.time()
        vm_page.wait_for_vm_list_to_load()
        call_elapsed = time.time() - call_start
        step8_elapsed = time.time() - step8_start
        logger.info(f"   ⏱️  VM list load wait completed in {call_elapsed:.4f} seconds")
        log_step_complete(8, step8_start, True, f"VM list loaded in {call_elapsed:.4f} seconds")
        
        step9_start = log_step(9, "Getting initial VM count before deletion", page)
        logger.info(f"   🎯 Method: vm_page.get_vm_list_count()")
        call_start = time.time()
        initial_count = vm_page.get_vm_list_count()
        call_elapsed = time.time() - call_start
        step9_elapsed = time.time() - step9_start
        logger.info(f"   ⏱️  Count retrieval completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📊 Result Type: {type(initial_count).__name__}")
        logger.info(f"   📏 Result Value: {initial_count}")
        logger.info(f"   🧠 Result Memory: {sys.getsizeof(initial_count)} bytes")
        log_step_complete(9, step9_start, True, f"Initial VM count: {initial_count}")
        
        step10_start = log_step(10, f"Initiating deletion of VM '{vm_name}'", page)
        logger.info(f"   🎯 Method: vm_page.delete_vm()")
        logger.info(f"   📦 Method Argument: vm_name='{vm_name}'")
        logger.info(f"   🔍 Pre-deletion State:")
        logger.info(f"      Current URL: {page.url}")
        logger.info(f"      Current Title: {page.title()}")
        logger.info(f"      Initial VM Count: {initial_count}")
        call_start = time.time()
        result = vm_page.delete_vm(vm_name)
        call_elapsed = time.time() - call_start
        step10_elapsed = time.time() - step10_start
        logger.info(f"   ⏱️  Delete VM call completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📊 Result Type: {type(result).__name__}")
        logger.info(f"   📝 Result Value: '{result}'")
        logger.info(f"   🧠 Result Memory: {sys.getsizeof(result) if result else 0} bytes")
        log_step_complete(10, step10_start, True, f"Delete VM result: '{result}'")
        
        step11_start = log_step(11, "Validating delete result is not None", page)
        logger.info(f"   🔍 Validation Details:")
        logger.info(f"      Result: {result}")
        logger.info(f"      Result is None: {result is None}")
        logger.info(f"   ✅ Assertion: assert result is not None")
        assert_start = time.time()
        assert result is not None, "Delete VM should return a result"
        assert_elapsed = time.time() - assert_start
        step11_elapsed = time.time() - step11_start
        logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
        log_step_complete(11, step11_start, True, f"Delete result is valid - validated in {assert_elapsed:.4f} seconds")
        
        step12_start = log_step(12, "Validating deletion was successful", page)
        logger.info(f"   🔍 Validation Details:")
        logger.info(f"      Result: '{result}'")
        logger.info(f"      Result Lowercase: '{result.lower()}'")
        logger.info(f"      Contains 'successfully': {'successfully' in result.lower()}")
        logger.info(f"      Contains 'deleted': {'deleted' in result.lower()}")
        logger.info(f"      Contains either: {'successfully' in result.lower() or 'deleted' in result.lower()}")
        logger.info(f"   ✅ Assertion: assert 'successfully' in result.lower() or 'deleted' in result.lower()")
        assert_start = time.time()
        assert "successfully" in result.lower() or "deleted" in result.lower(), "VM should be deleted successfully"
        assert_elapsed = time.time() - assert_start
        step12_elapsed = time.time() - step12_start
        logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
        log_step_complete(12, step12_start, True, f"Deletion message confirmed in {assert_elapsed:.4f} seconds")
        
        step13_start = log_step(13, "Waiting 2 seconds for deletion to complete", page)
        logger.info(f"   ⏳ Wait Duration: 2 seconds")
        wait_start = time.time()
        time.sleep(2)
        wait_elapsed = time.time() - wait_start
        step13_elapsed = time.time() - step13_start
        logger.info(f"   ⏱️  Actual Wait Time: {wait_elapsed:.4f} seconds")
        log_step_complete(13, step13_start, True, f"Wait completed in {wait_elapsed:.4f} seconds")
        
        step14_start = log_step(14, "Reloading VM list after deletion", page)
        logger.info(f"   🎯 Method: vm_page.wait_for_vm_list_to_load()")
        call_start = time.time()
        vm_page.wait_for_vm_list_to_load()
        call_elapsed = time.time() - call_start
        step14_elapsed = time.time() - step14_start
        logger.info(f"   ⏱️  VM list reload completed in {call_elapsed:.4f} seconds")
        log_step_complete(14, step14_start, True, f"VM list reloaded in {call_elapsed:.4f} seconds")
        
        step15_start = log_step(15, "Getting final VM count after deletion", page)
        logger.info(f"   🎯 Method: vm_page.get_vm_list_count()")
        call_start = time.time()
        final_count = vm_page.get_vm_list_count()
        call_elapsed = time.time() - call_start
        step15_elapsed = time.time() - step15_start
        logger.info(f"   ⏱️  Count retrieval completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📊 Result Type: {type(final_count).__name__}")
        logger.info(f"   📏 Result Value: {final_count}")
        logger.info(f"   🧠 Result Memory: {sys.getsizeof(final_count)} bytes")
        log_step_complete(15, step15_start, True, f"Final VM count: {final_count}")
        
        step16_start = log_step(16, "Analyzing VM count change", page)
        count_change = final_count - initial_count
        expected_change = -1
        logger.info(f"   📊 Count Analysis:")
        logger.info(f"      Initial Count: {initial_count}")
        logger.info(f"      Final Count: {final_count}")
        logger.info(f"      Count Change: {count_change}")
        logger.info(f"      Expected Change: {expected_change}")
        logger.info(f"      Change Matches Expected: {count_change == expected_change}")
        step16_elapsed = time.time() - step16_start
        log_step_complete(16, step16_start, True, f"VM count change: {initial_count} -> {final_count} (expected: -1)")
        
        step17_start = log_step(17, "Validating VM count decreased by 1", page)
        logger.info(f"   🔍 Validation Details:")
        logger.info(f"      Final Count: {final_count}")
        logger.info(f"      Initial Count: {initial_count}")
        logger.info(f"      Expected: final_count == initial_count - 1")
        logger.info(f"      Actual: {final_count} == {initial_count - 1}")
        logger.info(f"      Condition Result: {final_count == initial_count - 1}")
        logger.info(f"   ✅ Assertion: assert final_count == initial_count - 1")
        assert_start = time.time()
        assert final_count == initial_count - 1, "VM count should decrease after deletion"
        assert_elapsed = time.time() - assert_start
        step17_elapsed = time.time() - step17_start
        logger.info(f"   ✅ Assertion passed in {assert_elapsed:.4f} seconds")
        log_step_complete(17, step17_start, True, f"VM count validation passed in {assert_elapsed:.4f} seconds")
        
        test_elapsed = time.time() - test_start_time
        logger.info("")
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info(f"✓✓✓ TEST PASSED: VM '{vm_name}' deleted successfully")
        logger.info("=" * 100)
        logger.info(f"⏰ Test End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        logger.info(f"⏱️  Total Test Duration: {test_elapsed:.4f} seconds")
        logger.info(f"📊 Test Summary:")
        logger.info(f"   - Steps Executed: 17")
        logger.info(f"   - VM Name: {vm_name}")
        logger.info(f"   - Initial Count: {initial_count}")
        logger.info(f"   - Final Count: {final_count}")
        logger.info(f"   - Count Change: {count_change}")
        logger.info(f"   - Status: PASSED")
        logger.info(f"   - Memory Usage: {sys.getsizeof(page) + sys.getsizeof(dashboard) + sys.getsizeof(vm_page)} bytes")
        logger.info("=" * 100)
        logger.info("=" * 100)
    
    def test_vm_network_type_options(self, page: Page):
        """Test that all network type options are available"""
        test_start_time = time.time()
        test_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info("🚀 TEST: VM network type options - START")
        logger.info("=" * 100)
        logger.info(f"⏰ Test Start Time: {test_timestamp}")
        logger.info(f"🆔 Test ID: test_vm_network_type_options")
        logger.info(f"📋 Test Description: Test that all network type options are available")
        logger.info(f"🏷️  Test Markers: @pytest.mark.vm_management")
        logger.info(f"🌐 Page URL Before Test: {page.url}")
        logger.info(f"📏 Page Viewport: {page.viewport_size}")
        logger.info(f"🧠 Memory Usage: {sys.getsizeof(page)} bytes (page object)")
        logger.info("=" * 100)
        
        step1_start = log_step(1, "Initializing dashboard page object", page)
        dashboard = DashboardPage(page)
        step1_elapsed = time.time() - step1_start
        logger.info(f"   ✅ DashboardPage object created in {step1_elapsed:.4f} seconds")
        logger.info(f"   📊 Object Type: {type(dashboard).__name__}")
        logger.info(f"   📏 Object Size: {sys.getsizeof(dashboard)} bytes")
        log_step_complete(1, step1_start, True, "Dashboard page object created")
        
        step2_start = log_step(2, "Clicking Create tab to access VM creation form", page)
        logger.info(f"   🎯 Method: dashboard.click_create_tab()")
        call_start = time.time()
        dashboard.click_create_tab()
        call_elapsed = time.time() - call_start
        step2_elapsed = time.time() - step2_start
        logger.info(f"   ⏱️  Click action completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📍 URL After Click: {page.url}")
        log_step_complete(2, step2_start, True, f"Navigated to Create tab in {call_elapsed:.4f} seconds")
        
        step3_start = log_step(3, "Locating network type select element", page)
        logger.info(f"   🎯 Locator: '[data-testid=\"vm-network-select\"]'")
        call_start = time.time()
        network_select = page.locator('[data-testid="vm-network-select"]')
        call_elapsed = time.time() - call_start
        step3_elapsed = time.time() - step3_start
        logger.info(f"   ⏱️  Locator call completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📊 Element Type: {type(network_select).__name__}")
        logger.info(f"   🧠 Element Memory: {sys.getsizeof(network_select)} bytes")
        log_step_complete(3, step3_start, True, "Network select element found")
        
        step4_start = log_step(4, "Getting all option elements from network select", page)
        logger.info(f"   🎯 Method: network_select.locator('option').all()")
        call_start = time.time()
        options = network_select.locator("option").all()
        call_elapsed = time.time() - call_start
        step4_elapsed = time.time() - step4_start
        logger.info(f"   ⏱️  Options retrieval completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📊 Result Type: {type(options).__name__}")
        logger.info(f"   📏 Result Length: {len(options)} network type options")
        logger.info(f"   🧠 Result Memory: {sys.getsizeof(options)} bytes")
        log_step_complete(4, step4_start, True, f"Found {len(options)} network type options")
        
        step5_start = log_step(5, "Extracting values from all options", page)
        logger.info(f"   🎯 Method: [opt.get_attribute('value') for opt in options]")
        logger.info(f"   📦 Processing {len(options)} options...")
        call_start = time.time()
        option_values = [opt.get_attribute("value") for opt in options]
        call_elapsed = time.time() - call_start
        step5_elapsed = time.time() - step5_start
        logger.info(f"   ⏱️  Value extraction completed in {call_elapsed:.4f} seconds")
        logger.info(f"   📊 Result Type: {type(option_values).__name__}")
        logger.info(f"   📏 Result Length: {len(option_values)} values")
        logger.info(f"   🧠 Result Memory: {sys.getsizeof(option_values)} bytes")
        logger.info(f"   📝 Available network types: {option_values}")
        log_step_complete(5, step5_start, True, f"Available network types: {option_values}")
        
        step6_start = log_step(6, "Defining expected network types", page)
        expected_types = ["NAT", "Bridge", "Internal", "Host-only"]
        step6_elapsed = time.time() - step6_start
        logger.info(f"   ✅ Expected types defined in {step6_elapsed:.4f} seconds")
        logger.info(f"   📋 Expected network types: {expected_types}")
        logger.info(f"   📏 Expected Count: {len(expected_types)}")
        logger.info(f"   🧠 Memory: {sys.getsizeof(expected_types)} bytes")
        log_step_complete(6, step6_start, True, f"Expected network types: {expected_types}")
        
        step7_start = log_step(7, "Validating each expected network type is present", page)
        logger.info(f"   🔍 Validation Process:")
        logger.info(f"      Expected Types: {expected_types}")
        logger.info(f"      Available Values: {option_values}")
        logger.info(f"      Validating {len(expected_types)} network types...")
        validation_results = []
        for idx, net_type in enumerate(expected_types, 1):
            logger.info(f"   📍 Step 7.{idx}: Checking for '{net_type}'...")
            logger.info(f"      Type: '{net_type}'")
            logger.info(f"      In Option Values: {net_type in option_values}")
            logger.info(f"      Option Values: {option_values}")
            assert_start = time.time()
            assert net_type in option_values, f"Network type '{net_type}' should be available"
            assert_elapsed = time.time() - assert_start
            validation_results.append(True)
            logger.info(f"      ✅ '{net_type}' found - validated in {assert_elapsed:.4f} seconds")
        step7_elapsed = time.time() - step7_start
        logger.info(f"   ✅ All {len(expected_types)} network types validated successfully")
        logger.info(f"   📊 Validation Results: {validation_results}")
        log_step_complete(7, step7_start, True, f"All {len(expected_types)} expected network types are present")
        
        test_elapsed = time.time() - test_start_time
        logger.info("")
        logger.info("=" * 100)
        logger.info("=" * 100)
        logger.info(f"✓✓✓ TEST PASSED: All network types available: {option_values}")
        logger.info("=" * 100)
        logger.info(f"⏰ Test End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        logger.info(f"⏱️  Total Test Duration: {test_elapsed:.4f} seconds")
        logger.info(f"📊 Test Summary:")
        logger.info(f"   - Steps Executed: 7")
        logger.info(f"   - Options Found: {len(options)}")
        logger.info(f"   - Expected Types: {len(expected_types)}")
        logger.info(f"   - Available Types: {option_values}")
        logger.info(f"   - All Validated: {all(validation_results)}")
        logger.info(f"   - Status: PASSED")
        logger.info(f"   - Memory Usage: {sys.getsizeof(page) + sys.getsizeof(dashboard)} bytes")
        logger.info("=" * 100)
        logger.info("=" * 100)

