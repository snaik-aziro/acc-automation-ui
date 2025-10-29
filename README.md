# 🧪 Aziro Cluster Center - UI Automation Suite

Comprehensive Playwright Python automation test suite for the Aziro Cluster Center application.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Test Reports](#test-reports)
- [Test Coverage](#test-coverage)
- [Writing Tests](#writing-tests)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This automation suite provides comprehensive end-to-end testing for the Aziro Cluster Center application, covering:

- ✅ Dashboard functionality and metrics
- ✅ VM creation, management, and operations
- ✅ Snapshot creation and management
- ✅ System logging and log filtering
- ✅ Navigation and UI interactions

## ✨ Features

- **Page Object Model (POM)**: Clean, maintainable test code organization
- **Comprehensive Logging**: Detailed test execution logs
- **HTML Reports**: Beautiful, self-contained test reports
- **Screenshot on Failure**: Automatic screenshots for failed tests
- **Headed Mode**: Watch tests execute in real browser
- **Parallel Execution**: Run tests in parallel for faster execution
- **Test Markers**: Organize tests by feature, priority, and speed

## 📁 Project Structure

```
automation/
├── pages/                      # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py           # Base page with common methods
│   ├── dashboard_page.py      # Dashboard page interactions
│   ├── vm_page.py             # VM management interactions
│   └── logs_page.py           # Logging system interactions
├── tests/                      # Test files
│   ├── __init__.py
│   ├── test_dashboard.py      # Dashboard tests
│   ├── test_vm_management.py  # VM management tests
│   └── test_logs.py           # Logging system tests
├── utils/                      # Helper utilities
│   ├── __init__.py
│   └── helpers.py             # Common helper functions
├── reports/                    # Test reports and screenshots
│   ├── screenshots/           # Failure screenshots
│   └── test-report.html       # HTML test report
├── conftest.py                # Pytest fixtures and configuration
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
├── run_tests.sh              # Test execution script (headed mode)
└── README.md                 # This file
```

## 🔧 Prerequisites

Before running the tests, ensure you have:

1. **Python 3.8+** installed
   ```bash
   python3 --version
   ```

2. **Application Running**:
   - Backend server running on `http://localhost:5000`
   - Frontend server running on `http://localhost:8082`
   - MongoDB database connected

3. **System Requirements**:
   - macOS, Linux, or Windows
   - At least 4GB RAM
   - Internet connection (for first-time Playwright installation)

## 📦 Installation

### Option 1: Quick Setup (Recommended)

```bash
# Navigate to automation directory
cd automation

# Make the run script executable
chmod +x run_tests.sh

# Run the script (it will handle installation and test execution)
./run_tests.sh
```

### Option 2: Manual Setup

```bash
# 1. Navigate to automation directory
cd automation

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install Playwright browsers
playwright install chromium
```

## 🚀 Running Tests

### **HEADED MODE (Recommended - Watch Tests Execute)**

```bash
# Run all tests in headed mode (browser visible)
pytest tests/ --headed --browser chromium --slowmo 500 -v

# Or use the convenient run script
./run_tests.sh
```

### **Run Specific Test Suites**

```bash
# Run only dashboard tests
pytest tests/test_dashboard.py --headed -v

# Run only VM management tests
pytest tests/test_vm_management.py --headed -v

# Run only logging tests
pytest tests/test_logs.py --headed -v
```

### **Run Tests by Markers**

```bash
# Run only smoke tests
pytest -m smoke --headed -v

# Run only critical tests
pytest -m critical --headed -v

# Run regression tests
pytest -m regression --headed -v

# Run dashboard feature tests
pytest -m dashboard --headed -v

# Run VM management tests
pytest -m vm_management --headed -v

# Run logging tests
pytest -m logs --headed -v
```

### **Headless Mode (Background Execution)**

```bash
# Run tests in headless mode (no browser window)
pytest tests/ -v

# Run with parallel execution (faster)
pytest tests/ -n 3 -v  # Run with 3 workers
```

### **Advanced Options**

```bash
# Run with specific timeout
pytest tests/ --headed --timeout=60 -v

# Run and generate Allure report
pytest tests/ --headed --alluredir=reports/allure-results
allure serve reports/allure-results

# Run with maximum verbosity and full traceback
pytest tests/ --headed -vv --tb=long

# Run specific test function
pytest tests/test_dashboard.py::TestDashboard::test_dashboard_loads_successfully --headed -v
```

## 📊 Test Reports

### HTML Report

After test execution, an HTML report is automatically generated:

```
reports/test-report.html
```

The report includes:
- ✅ Test execution summary
- ⏱️ Execution time for each test
- 📸 Screenshots for failed tests
- 📝 Detailed logs and error messages
- 📈 Pass/Fail statistics

**Opening the Report**:
```bash
# macOS
open reports/test-report.html

# Linux
xdg-open reports/test-report.html

# Windows
start reports/test-report.html
```

### Screenshots

Failed test screenshots are saved in:
```
reports/screenshots/
```

Each screenshot is named with the test name and timestamp.

### Console Output

Real-time test execution logs are displayed in the console with:
- Test names and descriptions
- Step-by-step execution details
- Timing information
- Pass/Fail status

## ✅ Test Coverage

### Dashboard Tests (`test_dashboard.py`)

| Test | Description |
|------|-------------|
| `test_dashboard_loads_successfully` | Verify dashboard loads with all elements |
| `test_dashboard_displays_metrics` | Verify all metric cards display correctly |
| `test_tab_navigation_works` | Test navigation between all tabs |
| `test_dashboard_header_content` | Verify header branding and content |
| `test_dashboard_metrics_are_numeric` | Validate metric values are numeric |

### VM Management Tests (`test_vm_management.py`)

| Test | Description |
|------|-------------|
| `test_create_vm_successfully` | Create VM with valid data |
| `test_create_vm_with_minimal_specs` | Create VM with minimum specifications |
| `test_create_vm_with_maximum_specs` | Create VM with high specifications |
| `test_vm_list_displays_vms` | Verify VM list displays correctly |
| `test_start_stop_vm_cycle` | Test starting and stopping VMs |
| `test_create_vm_snapshot` | Create snapshot for a VM |
| `test_view_vm_snapshots` | View VM snapshots |
| `test_delete_vm` | Delete a VM |
| `test_vm_network_type_options` | Verify network type options |

### Logging System Tests (`test_logs.py`)

| Test | Description |
|------|-------------|
| `test_load_l1_critical_logs` | Load and verify L1 critical logs |
| `test_load_l2_warning_logs` | Load and verify L2 warning logs |
| `test_load_l3_info_logs` | Load and verify L3 info logs |
| `test_log_level_filtering` | Test log level filtering |
| `test_clear_logs_display` | Test clearing log display |
| `test_log_entries_have_correct_format` | Verify log entry format |
| `test_all_log_levels_accessible` | Verify all log buttons work |
| `test_multiple_log_level_switches` | Test switching between levels |

## 📝 Writing Tests

### Basic Test Structure

```python
import pytest
from playwright.sync_api import Page
from pages.dashboard_page import DashboardPage

@pytest.mark.your_feature
class TestYourFeature:
    """Test suite for your feature"""
    
    def test_your_scenario(self, page: Page):
        """Test description"""
        # Arrange
        dashboard = DashboardPage(page)
        dashboard.load_dashboard()
        
        # Act
        result = dashboard.get_page_title()
        
        # Assert
        assert "Expected" in result
```

### Using Page Objects

```python
# Import page objects
from pages.dashboard_page import DashboardPage
from pages.vm_page import VMPage

# Use in tests
def test_example(page: Page):
    # Dashboard operations
    dashboard = DashboardPage(page)
    dashboard.load_dashboard()
    dashboard.click_vms_tab()
    
    # VM operations
    vm_page = VMPage(page)
    vm_page.create_vm("test-vm", memory=2048, cpu=2)
```

### Test Markers

Add markers to organize tests:

```python
@pytest.mark.smoke          # Quick smoke tests
@pytest.mark.regression     # Full regression suite
@pytest.mark.critical       # Critical path tests
@pytest.mark.slow           # Longer running tests
@pytest.mark.dashboard      # Dashboard feature
@pytest.mark.vm_management  # VM management feature
@pytest.mark.logs           # Logging feature
```

## 🐛 Troubleshooting

### Common Issues

**1. Application Not Running**
```bash
Error: Failed to connect to backend

Solution: Ensure both frontend and backend servers are running:
- Frontend: http://localhost:8082
- Backend: http://localhost:5000
```

**2. Playwright Not Installed**
```bash
Error: Executable doesn't exist

Solution: Install Playwright browsers:
playwright install chromium
```

**3. Tests Running Too Fast**
```bash
Solution: Add slowmo parameter:
pytest --headed --browser chromium --slowmo 1000
```

**4. Virtual Environment Issues**
```bash
Solution: Recreate virtual environment:
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**5. Port Already in Use**
```bash
Error: Address already in use

Solution: Stop any existing servers:
lsof -ti:3000 | xargs kill -9  # Kill frontend
lsof -ti:5000 | xargs kill -9  # Kill backend
```

### Debug Mode

Run tests with maximum verbosity:

```bash
pytest tests/ --headed -vv --tb=long --log-cli-level=DEBUG
```

### Getting Help

If you encounter issues:

1. Check the test report: `reports/test-report.html`
2. Review screenshots: `reports/screenshots/`
3. Check console logs for detailed error messages
4. Verify application is running correctly

## 📈 Best Practices

1. **Always run in headed mode first** to see what's happening
2. **Use descriptive test names** that explain what's being tested
3. **Keep tests independent** - each test should run standalone
4. **Use page objects** for all UI interactions
5. **Add logging** to track test execution
6. **Take screenshots** on important steps or failures
7. **Use markers** to organize and filter tests
8. **Clean up test data** created during tests

## 🎉 Quick Start Summary

```bash
# 1. Navigate to automation folder
cd automation

# 2. Make run script executable
chmod +x run_tests.sh

# 3. Run tests in headed mode (browser visible)
./run_tests.sh

# 4. View the report (opens automatically on macOS)
open reports/test-report.html
```

That's it! Your tests will run in a visible browser window, and you'll see a detailed report at the end.

## 📞 Support

For questions or issues with the automation suite, please check:
- The test report for detailed error information
- Screenshots in `reports/screenshots/`
- Console logs during test execution

---

**Built with ❤️ using Playwright & Python**

*Happy Testing! 🚀*

