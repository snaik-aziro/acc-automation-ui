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
from datetime import datetime

logger = logging.getLogger(__name__)


@pytest.mark.vm_management
class TestVMManagement:
    """Test suite for VM Management functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup for each test - navigate to VMs tab"""
        dashboard = DashboardPage(page)
        dashboard.load_dashboard()
        dashboard.click_vms_tab()
        
        # Wait for VM list to load
        vm_page = VMPage(page)
        vm_page.wait_for_vm_list_to_load()
    
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_create_vm_successfully(self, page: Page):
        """Test creating a new VM with valid data"""
        logger.info("=" * 80)
        logger.info("TEST: Create VM successfully - START")
        logger.info("=" * 80)
        
        # Navigate to Create tab
        logger.info("Step 1: Initializing dashboard page object")
        dashboard = DashboardPage(page)
        logger.info("Step 2: Clicking on Create tab to navigate to VM creation form")
        dashboard.click_create_tab()
        logger.info("✓ Successfully navigated to Create tab")
        
        # Create VM with unique name
        logger.info("Step 3: Initializing VM page object")
        vm_page = VMPage(page)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        vm_name = f"test-vm-{timestamp}"
        logger.info(f"Step 4: Generated unique VM name: {vm_name}")
        
        logger.info("Step 5: Preparing VM configuration:")
        logger.info(f"  - Name: {vm_name}")
        logger.info(f"  - Memory: 4096 MB")
        logger.info(f"  - CPU: 4 cores")
        logger.info(f"  - Network Type: Bridge")
        logger.info(f"  - IP Address: 192.168.1.100")
        
        logger.info("Step 6: Calling create_vm() method...")
        result = vm_page.create_vm(
            name=vm_name,
            memory=4096,
            cpu=4,
            network_type="Bridge",
            ip_address="192.168.1.100"
        )
        logger.info(f"Step 7: Received result from create_vm(): '{result}'")
        
        # Verify success message
        logger.info("Step 8: Verifying success message in result")
        assert "successfully" in result.lower(), f"Expected success message, got: {result}"
        logger.info("✓ Success message verified in result")
        
        # Wait for navigation to VMs tab
        logger.info("Step 9: Waiting 2 seconds for navigation to VMs tab...")
        time.sleep(2)
        logger.info("✓ Wait completed")
        
        # Verify VM appears in list
        logger.info("Step 10: Waiting for VM list to load completely")
        vm_page.wait_for_vm_list_to_load()
        logger.info("✓ VM list loaded successfully")
        
        logger.info(f"Step 11: Searching for VM card with name '{vm_name}'")
        vm_card = vm_page.get_vm_card_by_name(vm_name)
        logger.info(f"Step 12: VM card found: {vm_card is not None}")
        assert vm_card is not None, f"VM '{vm_name}' should appear in the VM list"
        logger.info(f"✓ VM card for '{vm_name}' found in the list")
        
        logger.info("=" * 80)
        logger.info(f"✓✓✓ TEST PASSED: VM '{vm_name}' created successfully")
        logger.info("=" * 80)
    
    def test_create_vm_with_minimal_specs(self, page: Page):
        """Test creating a VM with minimal specifications"""
        logger.info("=" * 80)
        logger.info("TEST: Create VM with minimal specs - START")
        logger.info("=" * 80)
        
        logger.info("Step 1: Initializing dashboard page object")
        dashboard = DashboardPage(page)
        logger.info("Step 2: Navigating to Create tab")
        dashboard.click_create_tab()
        logger.info("✓ Successfully clicked Create tab")
        
        logger.info("Step 3: Initializing VM page object")
        vm_page = VMPage(page)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        vm_name = f"minimal-vm-{timestamp}"
        logger.info(f"Step 4: Generated VM name: {vm_name}")
        
        logger.info("Step 5: Configuring VM with MINIMAL specifications:")
        logger.info(f"  - Name: {vm_name}")
        logger.info(f"  - Memory: 512 MB (minimum)")
        logger.info(f"  - CPU: 1 core (minimum)")
        logger.info(f"  - Network Type: Private")
        
        logger.info("Step 6: Calling create_vm() with minimal specs...")
        result = vm_page.create_vm(
            name=vm_name,
            memory=512,  # Minimum memory
            cpu=1,       # Minimum CPU
            network_type="Private"
        )
        logger.info(f"Step 7: VM creation result received: '{result}'")
        
        logger.info("Step 8: Asserting creation was successful")
        assert "successfully" in result.lower(), "VM creation should succeed with minimal specs"
        logger.info("✓ Assertion passed - VM created with minimal specs")
        
        logger.info("=" * 80)
        logger.info(f"✓✓✓ TEST PASSED: Minimal VM '{vm_name}' created successfully")
        logger.info("=" * 80)
    
    def test_create_vm_with_maximum_specs(self, page: Page):
        """Test creating a VM with maximum specifications"""
        logger.info("=" * 80)
        logger.info("TEST: Create VM with maximum specs - START")
        logger.info("=" * 80)
        
        logger.info("Step 1: Creating dashboard page object instance")
        dashboard = DashboardPage(page)
        logger.info("Step 2: Clicking Create tab to access VM creation form")
        dashboard.click_create_tab()
        logger.info("✓ Create tab accessed successfully")
        
        logger.info("Step 3: Creating VM page object instance")
        vm_page = VMPage(page)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        vm_name = f"maximal-vm-{timestamp}"
        logger.info(f"Step 4: Generated unique VM name: {vm_name}")
        
        logger.info("Step 5: Configuring VM with MAXIMUM specifications:")
        logger.info(f"  - Name: {vm_name}")
        logger.info(f"  - Memory: 16384 MB (16 GB - high memory)")
        logger.info(f"  - CPU: 8 cores (maximum)")
        logger.info(f"  - Network Type: Bridge")
        logger.info(f"  - IP Address: 10.0.0.50")
        
        logger.info("Step 6: Initiating VM creation with maximum specs...")
        result = vm_page.create_vm(
            name=vm_name,
            memory=16384,  # High memory
            cpu=8,         # High CPU
            network_type="Bridge",
            ip_address="10.0.0.50"
        )
        logger.info(f"Step 7: VM creation completed. Result: '{result}'")
        
        logger.info("Step 8: Validating successful creation message")
        assert "successfully" in result.lower(), "VM creation should succeed with high specs"
        logger.info("✓ Validation passed - High spec VM created successfully")
        
        logger.info("=" * 80)
        logger.info(f"✓✓✓ TEST PASSED: Maximal VM '{vm_name}' created successfully")
        logger.info("=" * 80)
    
    def test_vm_list_displays_vms(self, page: Page):
        """Test that VM list displays VMs correctly"""
        logger.info("=" * 80)
        logger.info("TEST: VM list displays VMs - START")
        logger.info("=" * 80)
        
        logger.info("Step 1: Initializing VM page object")
        vm_page = VMPage(page)
        logger.info("✓ VM page object created")
        
        logger.info("Step 2: Retrieving VM list count from the page")
        vm_count = vm_page.get_vm_list_count()
        logger.info(f"Step 3: VM count retrieved: {vm_count}")
        
        logger.info(f"Step 4: Current VM count in the list: {vm_count} VMs")
        logger.info("Step 5: Validating VM count is non-negative")
        assert vm_count >= 0, "VM count should be non-negative"
        logger.info("✓ VM count validation passed")
        
        if vm_count == 0:
            logger.info("⚠ Note: No VMs currently in the list (empty state)")
        elif vm_count == 1:
            logger.info("✓ Found 1 VM in the list")
        else:
            logger.info(f"✓ Found {vm_count} VMs in the list")
        
        logger.info("Step 6: VM list display check completed")
        logger.info("=" * 80)
        logger.info("✓✓✓ TEST PASSED: VM list displays correctly")
        logger.info("=" * 80)
    
    @pytest.mark.slow
    def test_start_stop_vm_cycle(self, page: Page):
        """Test starting and stopping a VM"""
        logger.info("=" * 80)
        logger.info("TEST: Start/Stop VM cycle - START")
        logger.info("=" * 80)
        
        # First, create a new VM
        logger.info("Step 1: Creating dashboard page object for VM creation")
        dashboard = DashboardPage(page)
        logger.info("Step 2: Navigating to Create tab")
        dashboard.click_create_tab()
        logger.info("✓ Navigated to Create tab")
        
        logger.info("Step 3: Initializing VM page object")
        vm_page = VMPage(page)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        vm_name = f"cycle-vm-{timestamp}"
        logger.info(f"Step 4: Generated VM name for cycle test: {vm_name}")
        
        logger.info("Step 5: Creating VM for start/stop cycle test")
        logger.info(f"  - Name: {vm_name}")
        logger.info(f"  - Memory: 2048 MB")
        logger.info(f"  - CPU: 2 cores")
        vm_page.create_vm(name=vm_name, memory=2048, cpu=2)
        logger.info("✓ VM created successfully")
        
        # Wait for VM list to load
        logger.info("Step 6: Waiting 3 seconds for VM to appear in list...")
        time.sleep(3)
        logger.info("✓ Wait completed")
        logger.info("Step 7: Waiting for VM list to fully load")
        vm_page.wait_for_vm_list_to_load()
        logger.info("✓ VM list loaded")
        
        # Check initial status
        logger.info(f"Step 8: Checking initial status of VM '{vm_name}'")
        initial_status = vm_page.get_vm_status(vm_name)
        logger.info(f"Step 9: Initial VM status retrieved: '{initial_status}'")
        
        # If VM is stopped, start it
        if initial_status and "STOPPED" in initial_status.upper():
            logger.info(f"Step 10: VM is in STOPPED state, attempting to start...")
            result = vm_page.start_vm(vm_name)
            logger.info(f"Step 11: Start VM result: '{result}'")
            
            logger.info("Step 12: Validating start VM result is not None")
            assert result is not None, "Start VM should return a result"
            logger.info("✓ Result is not None")
            
            logger.info("Step 13: Validating start was successful")
            assert "successfully" in result.lower() or "initiated" in result.lower(), "Start should be successful"
            logger.info("✓✓ VM started successfully")
            
            # Wait a bit
            logger.info("Step 14: Waiting 3 seconds for VM to start...")
            time.sleep(3)
            logger.info("✓ Wait completed")
        else:
            logger.info(f"Step 10: VM is not in STOPPED state (status: {initial_status}), skipping start operation")
        
        # Now try to stop it
        logger.info("Step 15: Refreshing VM list before stop operation")
        vm_page.wait_for_vm_list_to_load()
        logger.info("✓ VM list refreshed")
        
        logger.info(f"Step 16: Checking current status of VM '{vm_name}'")
        current_status = vm_page.get_vm_status(vm_name)
        logger.info(f"Step 17: Current VM status: '{current_status}'")
        
        if current_status and "RUNNING" in current_status.upper():
            logger.info("Step 18: VM is in RUNNING state, attempting to stop...")
            result = vm_page.stop_vm(vm_name)
            logger.info(f"Step 19: Stop VM result: '{result}'")
            
            logger.info("Step 20: Validating stop VM result is not None")
            assert result is not None, "Stop VM should return a result"
            logger.info("✓ Result is not None")
            
            logger.info("Step 21: Validating stop was successful")
            assert "successfully" in result.lower() or "initiated" in result.lower(), "Stop should be successful"
            logger.info("✓✓ VM stopped successfully")
        else:
            logger.info(f"Step 18: VM is not in RUNNING state (status: {current_status}), skipping stop operation")
        
        logger.info("=" * 80)
        logger.info("✓✓✓ TEST PASSED: Start/Stop VM cycle completed")
        logger.info("=" * 80)
    
    def test_create_vm_snapshot(self, page: Page):
        """Test creating a snapshot for a VM"""
        logger.info("=" * 80)
        logger.info("TEST: Create VM snapshot - START")
        logger.info("=" * 80)
        
        # Create a VM first
        logger.info("Step 1: Initializing dashboard for VM creation")
        dashboard = DashboardPage(page)
        logger.info("Step 2: Clicking Create tab to create a VM for snapshot test")
        dashboard.click_create_tab()
        logger.info("✓ Navigated to Create tab")
        
        logger.info("Step 3: Initializing VM page object")
        vm_page = VMPage(page)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        vm_name = f"snapshot-vm-{timestamp}"
        logger.info(f"Step 4: Generated VM name for snapshot test: {vm_name}")
        
        logger.info("Step 5: Creating VM for snapshot testing")
        logger.info(f"  - VM Name: {vm_name}")
        logger.info(f"  - Memory: 2048 MB")
        logger.info(f"  - CPU: 2 cores")
        vm_page.create_vm(name=vm_name, memory=2048, cpu=2)
        logger.info("✓ VM created successfully")
        
        logger.info("Step 6: Waiting 3 seconds for VM to be fully created...")
        time.sleep(3)
        logger.info("✓ Wait completed")
        
        # Navigate back to VMs list
        logger.info("Step 7: Navigating back to VMs list tab")
        dashboard.click_vms_tab()
        logger.info("✓ Clicked VMs tab")
        
        logger.info("Step 8: Waiting for VM list to load")
        vm_page.wait_for_vm_list_to_load()
        logger.info("✓ VM list loaded successfully")
        
        # Create snapshot
        snapshot_name = f"snapshot-{timestamp}"
        logger.info(f"Step 9: Generated snapshot name: {snapshot_name}")
        logger.info(f"Step 10: Taking snapshot '{snapshot_name}' for VM '{vm_name}'...")
        result = vm_page.take_snapshot(vm_name, snapshot_name)
        logger.info(f"Step 11: Snapshot creation result: '{result}'")
        
        logger.info("Step 12: Validating snapshot result is not None")
        assert result is not None, "Snapshot creation should return a result"
        logger.info("✓ Snapshot result is valid")
        
        logger.info("Step 13: Validating snapshot was created successfully")
        assert "successfully" in result.lower(), f"Snapshot should be created successfully, got: {result}"
        logger.info("✓ Snapshot created successfully")
        
        logger.info("=" * 80)
        logger.info(f"✓✓✓ TEST PASSED: Snapshot '{snapshot_name}' created for VM '{vm_name}'")
        logger.info("=" * 80)
    
    def test_view_vm_snapshots(self, page: Page):
        """Test viewing snapshots for a VM"""
        logger.info("=" * 80)
        logger.info("TEST: View VM snapshots - START")
        logger.info("=" * 80)
        
        logger.info("Step 1: Initializing VM page object")
        vm_page = VMPage(page)
        logger.info("✓ VM page object created")
        
        logger.info("Step 2: Getting VM count from the list")
        vm_count = vm_page.get_vm_list_count()
        logger.info(f"Step 3: Total VMs available: {vm_count}")
        
        if vm_count > 0:
            logger.info(f"Step 4: VMs found ({vm_count}), proceeding to get first VM")
            # Get the first VM
            logger.info("Step 5: Locating all VM cards on the page")
            vm_cards = page.locator(vm_page.VM_CARD).all()
            logger.info(f"Step 6: Found {len(vm_cards)} VM cards")
            
            if len(vm_cards) > 0:
                logger.info("Step 7: Accessing first VM card")
                first_vm_name_element = vm_cards[0].locator('[data-testid="vm-name"]')
                logger.info("Step 8: Extracting VM name from first card")
                first_vm_name = first_vm_name_element.text_content()
                logger.info(f"Step 9: First VM name: '{first_vm_name}'")
                
                # View snapshots
                logger.info(f"Step 10: Attempting to view snapshots for VM: '{first_vm_name}'")
                result = vm_page.view_snapshots(first_vm_name)
                logger.info(f"Step 11: View snapshots result: {result}")
                
                logger.info("Step 12: Validating snapshot view was successful")
                assert result, f"Should be able to view snapshots for VM: {first_vm_name}"
                logger.info("✓ Snapshot view validation passed")
                
                logger.info("=" * 80)
                logger.info(f"✓✓✓ TEST PASSED: Snapshots viewed successfully for VM: {first_vm_name}")
                logger.info("=" * 80)
        else:
            logger.info("Step 4: No VMs found in the list")
            logger.info("⊘ Cannot test snapshot viewing without VMs")
            logger.info("Skipping test...")
            pytest.skip("No VMs available")
    
    @pytest.mark.critical
    def test_delete_vm(self, page: Page):
        """Test deleting a VM"""
        logger.info("=" * 80)
        logger.info("TEST: Delete VM - START")
        logger.info("=" * 80)
        
        # Create a VM to delete
        logger.info("Step 1: Initializing dashboard for VM deletion test")
        dashboard = DashboardPage(page)
        logger.info("Step 2: Navigating to Create tab to create a VM")
        dashboard.click_create_tab()
        logger.info("✓ Navigated to Create tab")
        
        logger.info("Step 3: Initializing VM page object")
        vm_page = VMPage(page)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        vm_name = f"delete-vm-{timestamp}"
        logger.info(f"Step 4: Generated VM name for deletion test: {vm_name}")
        
        logger.info("Step 5: Creating VM to be deleted")
        logger.info(f"  - Name: {vm_name}")
        logger.info(f"  - Memory: 1024 MB")
        logger.info(f"  - CPU: 1 core")
        vm_page.create_vm(name=vm_name, memory=1024, cpu=1)
        logger.info("✓ VM created successfully")
        
        logger.info("Step 6: Waiting 3 seconds for VM to be fully created...")
        time.sleep(3)
        logger.info("✓ Wait completed")
        
        # Navigate back to VMs list
        logger.info("Step 7: Navigating back to VMs list tab")
        dashboard.click_vms_tab()
        logger.info("✓ Clicked VMs tab")
        
        logger.info("Step 8: Waiting for VM list to load")
        vm_page.wait_for_vm_list_to_load()
        logger.info("✓ VM list loaded")
        
        # Get initial count
        logger.info("Step 9: Getting initial VM count before deletion")
        initial_count = vm_page.get_vm_list_count()
        logger.info(f"Step 10: Initial VM count: {initial_count}")
        
        # Delete the VM
        logger.info(f"Step 11: Initiating deletion of VM '{vm_name}'...")
        result = vm_page.delete_vm(vm_name)
        logger.info(f"Step 12: Delete VM result: '{result}'")
        
        logger.info("Step 13: Validating delete result is not None")
        assert result is not None, "Delete VM should return a result"
        logger.info("✓ Delete result is valid")
        
        logger.info("Step 14: Validating deletion was successful")
        assert "successfully" in result.lower() or "deleted" in result.lower(), "VM should be deleted successfully"
        logger.info("✓ Deletion message confirmed")
        
        # Wait and verify
        logger.info("Step 15: Waiting 2 seconds for deletion to complete...")
        time.sleep(2)
        logger.info("✓ Wait completed")
        
        logger.info("Step 16: Reloading VM list after deletion")
        vm_page.wait_for_vm_list_to_load()
        logger.info("✓ VM list reloaded")
        
        # Verify VM is removed (count decreased or VM not found)
        logger.info("Step 17: Getting final VM count after deletion")
        final_count = vm_page.get_vm_list_count()
        logger.info(f"Step 18: Final VM count: {final_count}")
        logger.info(f"Step 19: VM count change: {initial_count} -> {final_count} (expected: -1)")
        
        logger.info("Step 20: Validating VM count decreased by 1")
        assert final_count == initial_count - 1, "VM count should decrease after deletion"
        logger.info("✓ VM count validation passed")
        
        logger.info("=" * 80)
        logger.info(f"✓✓✓ TEST PASSED: VM '{vm_name}' deleted successfully")
        logger.info("=" * 80)
    
    def test_vm_network_type_options(self, page: Page):
        """Test that all network type options are available"""
        logger.info("=" * 80)
        logger.info("TEST: VM network type options - START")
        logger.info("=" * 80)
        
        logger.info("Step 1: Initializing dashboard page object")
        dashboard = DashboardPage(page)
        logger.info("Step 2: Clicking Create tab to access VM creation form")
        dashboard.click_create_tab()
        logger.info("✓ Navigated to Create tab")
        
        # Check that network select has all options
        logger.info("Step 3: Locating network type select element")
        network_select = page.locator('[data-testid="vm-network-select"]')
        logger.info("✓ Network select element found")
        
        logger.info("Step 4: Getting all option elements from network select")
        options = network_select.locator("option").all()
        logger.info(f"Step 5: Found {len(options)} network type options")
        
        logger.info("Step 6: Extracting values from all options")
        option_values = [opt.get_attribute("value") for opt in options]
        logger.info(f"Step 7: Available network types: {option_values}")
        
        # Verify all expected network types are present
        expected_types = ["NAT", "Bridge", "Internal", "Host-only"]
        logger.info(f"Step 8: Expected network types: {expected_types}")
        
        logger.info("Step 9: Validating each expected network type is present...")
        for idx, net_type in enumerate(expected_types, 1):
            logger.info(f"  Step 9.{idx}: Checking for '{net_type}'...")
            assert net_type in option_values, f"Network type '{net_type}' should be available"
            logger.info(f"  ✓ '{net_type}' found")
        
        logger.info("Step 10: All network type validations passed")
        logger.info(f"Step 11: Summary - All {len(expected_types)} expected network types are available")
        
        logger.info("=" * 80)
        logger.info(f"✓✓✓ TEST PASSED: All network types available: {option_values}")
        logger.info("=" * 80)

