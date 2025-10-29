"""
Helper utilities for Aziro Cluster Center UI Automation
Common helper functions used across tests
"""

import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def generate_unique_name(prefix: str = "test") -> str:
    """
    Generate a unique name with timestamp
    
    Args:
        prefix: Prefix for the name
    
    Returns:
        Unique name string
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"{prefix}-{timestamp}"


def wait_for_seconds(seconds: int, reason: str = ""):
    """
    Wait for specified seconds with logging
    
    Args:
        seconds: Number of seconds to wait
        reason: Optional reason for waiting
    """
    if reason:
        logger.info(f"Waiting {seconds}s: {reason}")
    else:
        logger.info(f"Waiting {seconds}s")
    
    time.sleep(seconds)


def parse_percentage(text: str) -> int:
    """
    Parse percentage value from text
    
    Args:
        text: Text containing percentage (e.g., "75%")
    
    Returns:
        Integer percentage value
    """
    try:
        return int(text.replace("%", "").strip())
    except ValueError:
        logger.error(f"Failed to parse percentage from: {text}")
        return 0


def validate_vm_name(name: str) -> bool:
    """
    Validate VM name format
    
    Args:
        name: VM name to validate
    
    Returns:
        True if valid, False otherwise
    """
    if not name or len(name) < 1 or len(name) > 100:
        return False
    
    # VM name should not contain special characters
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")
    return all(c in allowed_chars for c in name)


def format_memory_mb(memory_mb: int) -> str:
    """
    Format memory value in MB to human-readable string
    
    Args:
        memory_mb: Memory in MB
    
    Returns:
        Formatted string (e.g., "2 GB" or "512 MB")
    """
    if memory_mb >= 1024:
        gb = memory_mb / 1024
        return f"{gb:.1f} GB"
    return f"{memory_mb} MB"


def is_valid_ip_address(ip: str) -> bool:
    """
    Validate IPv4 address format
    
    Args:
        ip: IP address string
    
    Returns:
        True if valid IPv4, False otherwise
    """
    if not ip:
        return False
    
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False


def log_test_step(step_number: int, description: str):
    """
    Log a test step with formatting
    
    Args:
        step_number: Step number
        description: Step description
    """
    logger.info(f"\n{'='*60}")
    logger.info(f"STEP {step_number}: {description}")
    logger.info(f"{'='*60}")


def extract_vm_id_from_card(card_element) -> str:
    """
    Extract VM ID from VM card element
    
    Args:
        card_element: Playwright locator for VM card
    
    Returns:
        VM ID string or None
    """
    try:
        return card_element.get_attribute("data-vm-id")
    except Exception as e:
        logger.error(f"Failed to extract VM ID: {e}")
        return None


class TestDataGenerator:
    """Generate test data for various scenarios"""
    
    @staticmethod
    def get_vm_config_minimal():
        """Get minimal VM configuration"""
        return {
            "name": generate_unique_name("minimal-vm"),
            "memory": 512,
            "cpu": 1,
            "network_type": "NAT",
            "ip_address": ""
        }
    
    @staticmethod
    def get_vm_config_standard():
        """Get standard VM configuration"""
        return {
            "name": generate_unique_name("standard-vm"),
            "memory": 2048,
            "cpu": 2,
            "network_type": "Bridge",
            "ip_address": "192.168.1.100"
        }
    
    @staticmethod
    def get_vm_config_high_performance():
        """Get high-performance VM configuration"""
        return {
            "name": generate_unique_name("highperf-vm"),
            "memory": 16384,
            "cpu": 8,
            "network_type": "Bridge",
            "ip_address": "10.0.0.50"
        }

