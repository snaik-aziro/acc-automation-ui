"""
Test Reporter with Color Coding and Decorations
Professional test execution reporting with visual enhancements
"""

import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


class Colors:
    """ANSI color codes for terminal output"""
    # Text colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # Background colors
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'
    BG_BLUE = '\033[104m'
    
    # Reset
    RESET = '\033[0m'


class TestReporter:
    """Enhanced test reporter with decorations and color coding"""
    
    def __init__(self):
        self.test_counter = 0
        self.feature_counter = {}
        self.start_time = None
    
    def print_header(self, title: str, subtitle: str = ""):
        """Print a decorative header"""
        width = 80
        print(f"\n{Colors.CYAN}{'═' * width}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}║{' ' * ((width - len(title) - 2) // 2)}{title}{' ' * ((width - len(title) - 1) // 2)}║{Colors.RESET}")
        if subtitle:
            print(f"{Colors.CYAN}║{' ' * ((width - len(subtitle) - 2) // 2)}{subtitle}{' ' * ((width - len(subtitle) - 1) // 2)}║{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * width}{Colors.RESET}\n")
    
    def print_separator(self, char: str = "─", color: str = Colors.BLUE):
        """Print a separator line"""
        print(f"{color}{char * 80}{Colors.RESET}")
    
    def print_test_start(self, test_name: str, feature: str = "General", test_number: Optional[int] = None):
        """Print test start with decorations"""
        self.test_counter += 1
        self.start_time = datetime.now()
        
        # Track feature-specific counter
        if feature not in self.feature_counter:
            self.feature_counter[feature] = 0
        self.feature_counter[feature] += 1
        
        test_num = test_number if test_number else self.test_counter
        feature_num = self.feature_counter[feature]
        
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'┌' + '─' * 78 + '┐'}{Colors.RESET}")
        print(f"{Colors.BLUE}│{Colors.RESET} {Colors.BOLD}{Colors.YELLOW}🧪 TEST #{test_num:03d}{Colors.RESET} {Colors.CYAN}[{feature} #{feature_num}]{Colors.RESET}")
        print(f"{Colors.BLUE}│{Colors.RESET} {Colors.WHITE}{test_name}{Colors.RESET}")
        print(f"{Colors.BLUE}│{Colors.RESET} {Colors.MAGENTA}Started at: {self.start_time.strftime('%H:%M:%S')}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'└' + '─' * 78 + '┘'}{Colors.RESET}")
    
    def print_test_step(self, step_number: int, description: str, status: str = "running"):
        """Print a test step with status"""
        status_icon = {
            "running": f"{Colors.YELLOW}⟳{Colors.RESET}",
            "pass": f"{Colors.GREEN}✓{Colors.RESET}",
            "fail": f"{Colors.RED}✗{Colors.RESET}",
            "skip": f"{Colors.YELLOW}⊘{Colors.RESET}"
        }.get(status, "•")
        
        print(f"  {Colors.CYAN}[Step {step_number}]{Colors.RESET} {status_icon} {description}")
    
    def print_test_end(self, status: str = "pass", message: str = ""):
        """Print test end with status"""
        if self.start_time:
            duration = (datetime.now() - self.start_time).total_seconds()
        else:
            duration = 0
        
        if status == "pass":
            status_text = f"{Colors.BG_GREEN}{Colors.BOLD} PASSED {Colors.RESET}"
            icon = f"{Colors.GREEN}✓{Colors.RESET}"
        elif status == "fail":
            status_text = f"{Colors.BG_RED}{Colors.BOLD} FAILED {Colors.RESET}"
            icon = f"{Colors.RED}✗{Colors.RESET}"
        elif status == "skip":
            status_text = f"{Colors.BG_YELLOW}{Colors.BOLD} SKIPPED {Colors.RESET}"
            icon = f"{Colors.YELLOW}⊘{Colors.RESET}"
        else:
            status_text = f"{Colors.BG_BLUE}{Colors.BOLD} UNKNOWN {Colors.RESET}"
            icon = "•"
        
        print(f"\n  {icon} {status_text} {Colors.MAGENTA}Duration: {duration:.2f}s{Colors.RESET}")
        if message:
            print(f"  {Colors.YELLOW}→ {message}{Colors.RESET}")
        print()
    
    def print_assertion(self, description: str, expected: str, actual: str, passed: bool):
        """Print an assertion result"""
        if passed:
            print(f"  {Colors.GREEN}✓{Colors.RESET} {description}")
            print(f"    {Colors.CYAN}Expected:{Colors.RESET} {expected} {Colors.GREEN}=={Colors.RESET} {Colors.CYAN}Actual:{Colors.RESET} {actual}")
        else:
            print(f"  {Colors.RED}✗{Colors.RESET} {description}")
            print(f"    {Colors.CYAN}Expected:{Colors.RESET} {expected} {Colors.RED}!={Colors.RESET} {Colors.CYAN}Actual:{Colors.RESET} {actual}")
    
    def print_feature_summary(self, feature: str, passed: int, failed: int, skipped: int):
        """Print feature test summary"""
        total = passed + failed + skipped
        print(f"\n{Colors.BOLD}{Colors.CYAN}┌{'─' * 78}┐{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET} {Colors.BOLD}{feature} Summary{Colors.RESET}")
        print(f"{Colors.CYAN}├{'─' * 78}┤{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET} Total Tests: {total}")
        print(f"{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}✓ Passed:{Colors.RESET} {passed}")
        print(f"{Colors.CYAN}│{Colors.RESET} {Colors.RED}✗ Failed:{Colors.RESET} {failed}")
        print(f"{Colors.CYAN}│{Colors.RESET} {Colors.YELLOW}⊘ Skipped:{Colors.RESET} {skipped}")
        
        if total > 0:
            pass_rate = (passed / total) * 100
            print(f"{Colors.CYAN}│{Colors.RESET} Pass Rate: {Colors.GREEN if pass_rate >= 90 else Colors.YELLOW if pass_rate >= 70 else Colors.RED}{pass_rate:.1f}%{Colors.RESET}")
        
        print(f"{Colors.BOLD}{Colors.CYAN}└{'─' * 78}┘{Colors.RESET}\n")
    
    def print_final_summary(self, total_passed: int, total_failed: int, total_skipped: int, duration: float):
        """Print final test execution summary"""
        total = total_passed + total_failed + total_skipped
        
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'═' * 80}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}║{' ' * 25}FINAL TEST SUMMARY{' ' * 36}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}{'═' * 80}{Colors.RESET}")
        
        print(f"\n{Colors.BOLD}Total Tests Executed:{Colors.RESET} {total}")
        print(f"{Colors.GREEN}✓ Passed:{Colors.RESET}  {total_passed} ({(total_passed/total*100) if total > 0 else 0:.1f}%)")
        print(f"{Colors.RED}✗ Failed:{Colors.RESET}  {total_failed} ({(total_failed/total*100) if total > 0 else 0:.1f}%)")
        print(f"{Colors.YELLOW}⊘ Skipped:{Colors.RESET} {total_skipped} ({(total_skipped/total*100) if total > 0 else 0:.1f}%)")
        print(f"\n{Colors.MAGENTA}Total Duration:{Colors.RESET} {duration:.2f}s")
        
        if total_failed == 0:
            print(f"\n{Colors.BG_GREEN}{Colors.BOLD} ALL TESTS PASSED! 🎉 {Colors.RESET}")
        else:
            print(f"\n{Colors.BG_RED}{Colors.BOLD} SOME TESTS FAILED ❌ {Colors.RESET}")
        
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'═' * 80}{Colors.RESET}\n")
    
    def print_info(self, message: str):
        """Print an info message"""
        print(f"{Colors.BLUE}ℹ{Colors.RESET} {message}")
    
    def print_success(self, message: str):
        """Print a success message"""
        print(f"{Colors.GREEN}✓{Colors.RESET} {message}")
    
    def print_warning(self, message: str):
        """Print a warning message"""
        print(f"{Colors.YELLOW}⚠{Colors.RESET} {message}")
    
    def print_error(self, message: str):
        """Print an error message"""
        print(f"{Colors.RED}✗{Colors.RESET} {message}")


# Global reporter instance
reporter = TestReporter()

