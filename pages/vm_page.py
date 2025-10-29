"""
VM Management Page Object for Aziro Cluster Center
Handles all VM management interactions
"""

from playwright.sync_api import Page
from pages.base_page import BasePage
import logging
import time

logger = logging.getLogger(__name__)


class VMPage(BasePage):
    """VM management page object"""
    
    # VM Creation Form
    VM_NAME_INPUT = '[data-testid="vm-name-input"]'
    VM_MEMORY_INPUT = '[data-testid="vm-memory-input"]'
    VM_CPU_INPUT = '[data-testid="vm-cpu-input"]'
    VM_NETWORK_SELECT = '[data-testid="vm-network-select"]'
    VM_IP_INPUT = '[data-testid="vm-ip-input"]'
    CREATE_VM_BUTTON = '[data-testid="create-vm-button"]'
    
    # VM List
    VM_LIST = '[data-testid="vm-list"]'
    VM_CARD = '[data-testid^="vm-card-"]'
    
    # Success/Error alerts
    SUCCESS_ALERT = '.alert.success'
    ERROR_ALERT = '.alert.error'
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def create_vm(self, name: str, memory: int = 2048, cpu: int = 2, 
                  network_type: str = "NAT", ip_address: str = ""):
        """
        Create a new VM with specified parameters
        
        Args:
            name: VM name
            memory: Memory in MB
            cpu: Number of CPU cores
            network_type: Network type (NAT, Bridge, Internal, Host-only)
            ip_address: Optional IP address
        """
        logger.info(f"Creating VM: {name}")
        
        # Fill form fields
        self.fill_input(self.VM_NAME_INPUT, name)
        
        # Clear and fill memory
        self.page.fill(self.VM_MEMORY_INPUT, "")
        self.fill_input(self.VM_MEMORY_INPUT, str(memory))
        
        # Clear and fill CPU
        self.page.fill(self.VM_CPU_INPUT, "")
        self.fill_input(self.VM_CPU_INPUT, str(cpu))
        
        # Select network type
        self.select_option(self.VM_NETWORK_SELECT, network_type)
        
        # Fill IP if provided
        if ip_address:
            self.fill_input(self.VM_IP_INPUT, ip_address)
        
        # Click create button
        self.click_element(self.CREATE_VM_BUTTON)
        
        # Wait for success alert
        logger.info("Waiting for VM creation success message")
        alert_message = self.wait_for_alert("success", timeout=15000)
        logger.info(f"VM creation result: {alert_message}")
        
        return alert_message
    
    def get_vm_list_count(self) -> int:
        """Get the count of VMs in the list"""
        self.wait_for_selector(self.VM_LIST)
        time.sleep(1)  # Wait for VMs to load
        
        vm_cards = self.page.locator(self.VM_CARD).all()
        count = len(vm_cards)
        logger.info(f"VM count in list: {count}")
        return count
    
    def get_vm_card_by_name(self, vm_name: str):
        """Find VM card by VM name"""
        logger.info(f"Looking for VM: {vm_name}")
        vm_cards = self.page.locator(self.VM_CARD).all()
        
        for card in vm_cards:
            name_element = card.locator('[data-testid="vm-name"]')
            if name_element.is_visible():
                name = name_element.text_content()
                if vm_name in name:
                    logger.info(f"Found VM card for: {vm_name}")
                    return card
        
        logger.warning(f"VM card not found for: {vm_name}")
        return None
    
    def get_vm_status(self, vm_name: str) -> str:
        """Get the status of a VM by name"""
        vm_card = self.get_vm_card_by_name(vm_name)
        if vm_card:
            status = vm_card.locator('[data-testid="vm-status"]').text_content()
            logger.info(f"VM {vm_name} status: {status}")
            return status.strip()
        return None
    
    def start_vm(self, vm_name: str):
        """Start a VM by name"""
        logger.info(f"Starting VM: {vm_name}")
        vm_card = self.get_vm_card_by_name(vm_name)
        
        if vm_card:
            # Get VM ID from card
            vm_id = vm_card.get_attribute("data-vm-id")
            start_button = f'[data-testid="start-vm-{vm_id}"]'
            
            if self.is_visible(start_button):
                self.click_element(start_button)
                alert_message = self.wait_for_alert("success", timeout=15000)
                logger.info(f"Start VM result: {alert_message}")
                return alert_message
            else:
                logger.warning(f"Start button not visible for VM: {vm_name}")
                return None
    
    def stop_vm(self, vm_name: str):
        """Stop a VM by name"""
        logger.info(f"Stopping VM: {vm_name}")
        vm_card = self.get_vm_card_by_name(vm_name)
        
        if vm_card:
            # Get VM ID from card
            vm_id = vm_card.get_attribute("data-vm-id")
            stop_button = f'[data-testid="stop-vm-{vm_id}"]'
            
            if self.is_visible(stop_button):
                self.click_element(stop_button)
                alert_message = self.wait_for_alert("success", timeout=15000)
                logger.info(f"Stop VM result: {alert_message}")
                return alert_message
            else:
                logger.warning(f"Stop button not visible for VM: {vm_name}")
                return None
    
    def take_snapshot(self, vm_name: str, snapshot_name: str):
        """Take a snapshot of a VM"""
        logger.info(f"Taking snapshot '{snapshot_name}' for VM: {vm_name}")
        vm_card = self.get_vm_card_by_name(vm_name)
        
        if vm_card:
            vm_id = vm_card.get_attribute("data-vm-id")
            snapshot_button = f'[data-testid="snapshot-vm-{vm_id}"]'
            
            # Handle the prompt dialog
            self.page.once("dialog", lambda dialog: dialog.accept(snapshot_name))
            
            # Click snapshot button
            self.click_element(snapshot_button)
            
            # Wait for success
            alert_message = self.wait_for_alert("success", timeout=15000)
            logger.info(f"Snapshot result: {alert_message}")
            return alert_message
    
    def view_snapshots(self, vm_name: str):
        """View snapshots for a VM"""
        logger.info(f"Viewing snapshots for VM: {vm_name}")
        vm_card = self.get_vm_card_by_name(vm_name)
        
        if vm_card:
            vm_id = vm_card.get_attribute("data-vm-id")
            view_snapshots_button = f'[data-testid="view-snapshots-{vm_id}"]'
            
            # Click view snapshots button
            self.click_element(view_snapshots_button)
            
            # Wait for snapshots section to be visible
            snapshots_section = f'[data-testid="snapshots-section-{vm_id}"]'
            self.wait_for_selector(snapshots_section)
            
            # Wait a bit for snapshots to load
            time.sleep(2)
            
            logger.info(f"Snapshots section opened for VM: {vm_name}")
            return True
        
        return False
    
    def delete_vm(self, vm_name: str):
        """Delete a VM by name"""
        logger.info(f"Deleting VM: {vm_name}")
        vm_card = self.get_vm_card_by_name(vm_name)
        
        if vm_card:
            vm_id = vm_card.get_attribute("data-vm-id")
            delete_button = f'[data-testid="delete-vm-{vm_id}"]'
            
            # Handle the confirmation dialog
            self.page.once("dialog", lambda dialog: dialog.accept())
            
            # Click delete button
            self.click_element(delete_button)
            
            # Wait for success
            alert_message = self.wait_for_alert("success", timeout=15000)
            logger.info(f"Delete VM result: {alert_message}")
            return alert_message
    
    def wait_for_vm_list_to_load(self):
        """Wait for VM list to fully load"""
        logger.info("Waiting for VM list to load")
        self.wait_for_selector(self.VM_LIST)
        time.sleep(2)  # Additional wait for data to populate

