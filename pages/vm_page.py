"""
VM Management Page Object for Aziro Cluster Center
Handles all VM management interactions
"""

from playwright.sync_api import Page
from pages.base_page import BasePage
import logging
import time
import sys
from datetime import datetime

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
        method_start = time.time()
        logger.debug(f"VMPage.create_vm() - Method called")
        logger.debug(f"VMPage.create_vm() - Method parameters:")
        logger.debug(f"VMPage.create_vm() -   name: {name} (type: {type(name).__name__}, length: {len(name)})")
        logger.debug(f"VMPage.create_vm() -   memory: {memory} (type: {type(memory).__name__}, value: {memory} MB)")
        logger.debug(f"VMPage.create_vm() -   cpu: {cpu} (type: {type(cpu).__name__}, value: {cpu} cores)")
        logger.debug(f"VMPage.create_vm() -   network_type: {network_type} (type: {type(network_type).__name__})")
        logger.debug(f"VMPage.create_vm() -   ip_address: {ip_address} (type: {type(ip_address).__name__}, length: {len(ip_address)})")
        logger.debug(f"VMPage.create_vm() - Current page URL: {self.page.url}")
        logger.debug(f"VMPage.create_vm() - Current page title: {self.page.title()}")
        logger.debug(f"VMPage.create_vm() - Page ready state: {self.page.evaluate('document.readyState')}")
        logger.info(f"Creating VM: {name}")
        
        # Fill form fields
        logger.debug(f"VMPage.create_vm() - Step 1: Filling VM name input")
        logger.debug(f"VMPage.create_vm() -   Selector: {self.VM_NAME_INPUT}")
        logger.debug(f"VMPage.create_vm() -   Value: {name}")
        fill_name_start = time.time()
        self.fill_input(self.VM_NAME_INPUT, name)
        fill_name_elapsed = time.time() - fill_name_start
        logger.debug(f"VMPage.create_vm() -   VM name filled in {fill_name_elapsed:.4f} seconds")
        
        # Clear and fill memory
        logger.debug(f"VMPage.create_vm() - Step 2: Clearing and filling memory input")
        logger.debug(f"VMPage.create_vm() -   Selector: {self.VM_MEMORY_INPUT}")
        logger.debug(f"VMPage.create_vm() -   Memory value: {memory} MB")
        clear_mem_start = time.time()
        self.page.fill(self.VM_MEMORY_INPUT, "")
        clear_mem_elapsed = time.time() - clear_mem_start
        logger.debug(f"VMPage.create_vm() -   Memory input cleared in {clear_mem_elapsed:.4f} seconds")
        fill_mem_start = time.time()
        self.fill_input(self.VM_MEMORY_INPUT, str(memory))
        fill_mem_elapsed = time.time() - fill_mem_start
        logger.debug(f"VMPage.create_vm() -   Memory value filled in {fill_mem_elapsed:.4f} seconds")
        
        # Clear and fill CPU
        logger.debug(f"VMPage.create_vm() - Step 3: Clearing and filling CPU input")
        logger.debug(f"VMPage.create_vm() -   Selector: {self.VM_CPU_INPUT}")
        logger.debug(f"VMPage.create_vm() -   CPU value: {cpu} cores")
        clear_cpu_start = time.time()
        self.page.fill(self.VM_CPU_INPUT, "")
        clear_cpu_elapsed = time.time() - clear_cpu_start
        logger.debug(f"VMPage.create_vm() -   CPU input cleared in {clear_cpu_elapsed:.4f} seconds")
        fill_cpu_start = time.time()
        self.fill_input(self.VM_CPU_INPUT, str(cpu))
        fill_cpu_elapsed = time.time() - fill_cpu_start
        logger.debug(f"VMPage.create_vm() -   CPU value filled in {fill_cpu_elapsed:.4f} seconds")
        
        # Select network type
        logger.debug(f"VMPage.create_vm() - Step 4: Selecting network type")
        logger.debug(f"VMPage.create_vm() -   Selector: {self.VM_NETWORK_SELECT}")
        logger.debug(f"VMPage.create_vm() -   Network type: {network_type}")
        select_net_start = time.time()
        self.select_option(self.VM_NETWORK_SELECT, network_type)
        select_net_elapsed = time.time() - select_net_start
        logger.debug(f"VMPage.create_vm() -   Network type selected in {select_net_elapsed:.4f} seconds")
        
        # Fill IP if provided
        if ip_address:
            logger.debug(f"VMPage.create_vm() - Step 5: Filling IP address (optional)")
            logger.debug(f"VMPage.create_vm() -   Selector: {self.VM_IP_INPUT}")
            logger.debug(f"VMPage.create_vm() -   IP address: {ip_address}")
            fill_ip_start = time.time()
            self.fill_input(self.VM_IP_INPUT, ip_address)
            fill_ip_elapsed = time.time() - fill_ip_start
            logger.debug(f"VMPage.create_vm() -   IP address filled in {fill_ip_elapsed:.4f} seconds")
        else:
            logger.debug(f"VMPage.create_vm() - Step 5: Skipping IP address (not provided)")
        
        # Click create button
        logger.debug(f"VMPage.create_vm() - Step 6: Clicking create VM button")
        logger.debug(f"VMPage.create_vm() -   Selector: {self.CREATE_VM_BUTTON}")
        click_start = time.time()
        self.click_element(self.CREATE_VM_BUTTON)
        click_elapsed = time.time() - click_start
        logger.debug(f"VMPage.create_vm() -   Create button clicked in {click_elapsed:.4f} seconds")
        
        # Wait for success alert
        logger.debug(f"VMPage.create_vm() - Step 7: Waiting for VM creation success message")
        logger.debug(f"VMPage.create_vm() -   Alert selector: {self.SUCCESS_ALERT}")
        logger.debug(f"VMPage.create_vm() -   Timeout: 15000ms")
        logger.info("Waiting for VM creation success message")
        alert_start = time.time()
        alert_message = self.wait_for_alert("success", timeout=15000)
        alert_elapsed = time.time() - alert_start
        logger.debug(f"VMPage.create_vm() -   Alert appeared after {alert_elapsed:.4f} seconds")
        method_elapsed = time.time() - method_start
        logger.debug(f"VMPage.create_vm() - Total method execution time: {method_elapsed:.4f} seconds")
        logger.debug(f"VMPage.create_vm() - Alert message type: {type(alert_message).__name__}")
        logger.debug(f"VMPage.create_vm() - Alert message length: {len(alert_message) if alert_message else 0} characters")
        logger.debug(f"VMPage.create_vm() - Alert message memory: {sys.getsizeof(alert_message) if alert_message else 0} bytes")
        logger.info(f"VM creation result: {alert_message}")
        
        return alert_message
    
    def get_vm_list_count(self) -> int:
        """Get the count of VMs in the list"""
        method_start = time.time()
        logger.debug(f"VMPage.get_vm_list_count() - Method called")
        logger.debug(f"VMPage.get_vm_list_count() - Current page URL: {self.page.url}")
        logger.debug(f"VMPage.get_vm_list_count() - Current page title: {self.page.title()}")
        logger.debug(f"VMPage.get_vm_list_count() - VM list selector: {self.VM_LIST}")
        logger.debug(f"VMPage.get_vm_list_count() - VM card selector: {self.VM_CARD}")
        
        wait_start = time.time()
        self.wait_for_selector(self.VM_LIST)
        wait_elapsed = time.time() - wait_start
        logger.debug(f"VMPage.get_vm_list_count() - VM list selector found after {wait_elapsed:.4f} seconds")
        
        logger.debug(f"VMPage.get_vm_list_count() - Waiting 1 second for VMs to load")
        sleep_start = time.time()
        time.sleep(1)  # Wait for VMs to load
        sleep_elapsed = time.time() - sleep_start
        logger.debug(f"VMPage.get_vm_list_count() - Sleep completed in {sleep_elapsed:.4f} seconds")
        
        logger.debug(f"VMPage.get_vm_list_count() - Locating all VM cards")
        locate_start = time.time()
        vm_cards = self.page.locator(self.VM_CARD).all()
        locate_elapsed = time.time() - locate_start
        logger.debug(f"VMPage.get_vm_list_count() - VM cards located in {locate_elapsed:.4f} seconds")
        logger.debug(f"VMPage.get_vm_list_count() - VM cards list type: {type(vm_cards).__name__}")
        logger.debug(f"VMPage.get_vm_list_count() - VM cards list length: {len(vm_cards)}")
        logger.debug(f"VMPage.get_vm_list_count() - VM cards list memory: {sys.getsizeof(vm_cards)} bytes")
        
        count = len(vm_cards)
        method_elapsed = time.time() - method_start
        logger.debug(f"VMPage.get_vm_list_count() - Total method execution time: {method_elapsed:.4f} seconds")
        logger.debug(f"VMPage.get_vm_list_count() - Count result type: {type(count).__name__}")
        logger.debug(f"VMPage.get_vm_list_count() - Count result value: {count}")
        logger.debug(f"VMPage.get_vm_list_count() - Count result memory: {sys.getsizeof(count)} bytes")
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

