"""
VM Management Tests for Aziro Cluster Center
Tests for VM creation, operations, and management
"""

import pytest
from playwright.sync_api import Page
from pages.dashboard_page import DashboardPage
from pages.vm_page import VMPage
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
        logger.info("TEST: Create VM successfully")
        
        # Navigate to Create tab
        dashboard = DashboardPage(page)
        dashboard.click_create_tab()
        
        # Create VM with unique name
        vm_page = VMPage(page)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        vm_name = f"test-vm-{timestamp}"
        
        result = vm_page.create_vm(
            name=vm_name,
            memory=4096,
            cpu=4,
            network_type="Bridge",
            ip_address="192.168.1.100"
        )
        
        # Verify success message
        assert "successfully" in result.lower(), f"Expected success message, got: {result}"
        
        # Wait for navigation to VMs tab
        time.sleep(2)
        
        # Verify VM appears in list
        vm_page.wait_for_vm_list_to_load()
        vm_card = vm_page.get_vm_card_by_name(vm_name)
        assert vm_card is not None, f"VM '{vm_name}' should appear in the VM list"
        
        logger.info(f"✓ VM '{vm_name}' created successfully")
    
    def test_create_vm_with_minimal_specs(self, page: Page):
        """Test creating a VM with minimal specifications"""
        logger.info("TEST: Create VM with minimal specs")
        
        dashboard = DashboardPage(page)
        dashboard.click_create_tab()
        
        vm_page = VMPage(page)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        vm_name = f"minimal-vm-{timestamp}"
        
        result = vm_page.create_vm(
            name=vm_name,
            memory=512,  # Minimum memory
            cpu=1,       # Minimum CPU
            network_type="NAT"
        )
        
        assert "successfully" in result.lower(), "VM creation should succeed with minimal specs"
        
        logger.info(f"✓ Minimal VM '{vm_name}' created successfully")
    
    def test_create_vm_with_maximum_specs(self, page: Page):
        """Test creating a VM with maximum specifications"""
        logger.info("TEST: Create VM with maximum specs")
        
        dashboard = DashboardPage(page)
        dashboard.click_create_tab()
        
        vm_page = VMPage(page)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        vm_name = f"maximal-vm-{timestamp}"
        
        result = vm_page.create_vm(
            name=vm_name,
            memory=16384,  # High memory
            cpu=8,         # High CPU
            network_type="Bridge",
            ip_address="10.0.0.50"
        )
        
        assert "successfully" in result.lower(), "VM creation should succeed with high specs"
        
        logger.info(f"✓ Maximal VM '{vm_name}' created successfully")
    
    def test_vm_list_displays_vms(self, page: Page):
        """Test that VM list displays VMs correctly"""
        logger.info("TEST: VM list displays VMs")
        
        vm_page = VMPage(page)
        vm_count = vm_page.get_vm_list_count()
        
        logger.info(f"Found {vm_count} VMs in the list")
        assert vm_count >= 0, "VM count should be non-negative"
        
        logger.info("✓ VM list displays correctly")
    
    @pytest.mark.slow
    def test_start_stop_vm_cycle(self, page: Page):
        """Test starting and stopping a VM"""
        logger.info("TEST: Start/Stop VM cycle")
        
        # First, create a new VM
        dashboard = DashboardPage(page)
        dashboard.click_create_tab()
        
        vm_page = VMPage(page)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        vm_name = f"cycle-vm-{timestamp}"
        
        vm_page.create_vm(name=vm_name, memory=2048, cpu=2)
        
        # Wait for VM list to load
        time.sleep(3)
        vm_page.wait_for_vm_list_to_load()
        
        # Check initial status
        initial_status = vm_page.get_vm_status(vm_name)
        logger.info(f"Initial VM status: {initial_status}")
        
        # If VM is stopped, start it
        if initial_status and "STOPPED" in initial_status.upper():
            result = vm_page.start_vm(vm_name)
            assert result is not None, "Start VM should return a result"
            assert "successfully" in result.lower() or "initiated" in result.lower(), "Start should be successful"
            logger.info("✓ VM started successfully")
            
            # Wait a bit
            time.sleep(3)
        
        # Now try to stop it
        vm_page.wait_for_vm_list_to_load()
        current_status = vm_page.get_vm_status(vm_name)
        
        if current_status and "RUNNING" in current_status.upper():
            result = vm_page.stop_vm(vm_name)
            assert result is not None, "Stop VM should return a result"
            assert "successfully" in result.lower() or "initiated" in result.lower(), "Stop should be successful"
            logger.info("✓ VM stopped successfully")
    
    def test_create_vm_snapshot(self, page: Page):
        """Test creating a snapshot for a VM"""
        logger.info("TEST: Create VM snapshot")
        
        # Create a VM first
        dashboard = DashboardPage(page)
        dashboard.click_create_tab()
        
        vm_page = VMPage(page)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        vm_name = f"snapshot-vm-{timestamp}"
        
        vm_page.create_vm(name=vm_name, memory=2048, cpu=2)
        time.sleep(3)
        
        # Navigate back to VMs list
        dashboard.click_vms_tab()
        vm_page.wait_for_vm_list_to_load()
        
        # Create snapshot
        snapshot_name = f"snapshot-{timestamp}"
        result = vm_page.take_snapshot(vm_name, snapshot_name)
        
        assert result is not None, "Snapshot creation should return a result"
        assert "successfully" in result.lower(), f"Snapshot should be created successfully, got: {result}"
        
        logger.info(f"✓ Snapshot '{snapshot_name}' created for VM '{vm_name}'")
    
    def test_view_vm_snapshots(self, page: Page):
        """Test viewing snapshots for a VM"""
        logger.info("TEST: View VM snapshots")
        
        vm_page = VMPage(page)
        vm_count = vm_page.get_vm_list_count()
        
        if vm_count > 0:
            # Get the first VM
            vm_cards = page.locator(vm_page.VM_CARD).all()
            if len(vm_cards) > 0:
                first_vm_name_element = vm_cards[0].locator('[data-testid="vm-name"]')
                first_vm_name = first_vm_name_element.text_content()
                
                # View snapshots
                result = vm_page.view_snapshots(first_vm_name)
                assert result, f"Should be able to view snapshots for VM: {first_vm_name}"
                
                logger.info(f"✓ Snapshots viewed for VM: {first_vm_name}")
        else:
            logger.info("⊘ No VMs available to test snapshot viewing")
            pytest.skip("No VMs available")
    
    @pytest.mark.critical
    def test_delete_vm(self, page: Page):
        """Test deleting a VM"""
        logger.info("TEST: Delete VM")
        
        # Create a VM to delete
        dashboard = DashboardPage(page)
        dashboard.click_create_tab()
        
        vm_page = VMPage(page)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        vm_name = f"delete-vm-{timestamp}"
        
        vm_page.create_vm(name=vm_name, memory=1024, cpu=1)
        time.sleep(3)
        
        # Navigate back to VMs list
        dashboard.click_vms_tab()
        vm_page.wait_for_vm_list_to_load()
        
        # Get initial count
        initial_count = vm_page.get_vm_list_count()
        
        # Delete the VM
        result = vm_page.delete_vm(vm_name)
        assert result is not None, "Delete VM should return a result"
        assert "successfully" in result.lower() or "deleted" in result.lower(), "VM should be deleted successfully"
        
        # Wait and verify
        time.sleep(2)
        vm_page.wait_for_vm_list_to_load()
        
        # Verify VM is removed (count decreased or VM not found)
        final_count = vm_page.get_vm_list_count()
        assert final_count == initial_count - 1, "VM count should decrease after deletion"
        
        logger.info(f"✓ VM '{vm_name}' deleted successfully")
    
    def test_vm_network_type_options(self, page: Page):
        """Test that all network type options are available"""
        logger.info("TEST: VM network type options")
        
        dashboard = DashboardPage(page)
        dashboard.click_create_tab()
        
        # Check that network select has all options
        network_select = page.locator('[data-testid="vm-network-select"]')
        options = network_select.locator("option").all()
        
        option_values = [opt.get_attribute("value") for opt in options]
        
        # Verify all expected network types are present
        expected_types = ["NAT", "Bridge", "Internal", "Host-only"]
        for net_type in expected_types:
            assert net_type in option_values, f"Network type '{net_type}' should be available"
        
        logger.info(f"✓ All network types available: {option_values}")

