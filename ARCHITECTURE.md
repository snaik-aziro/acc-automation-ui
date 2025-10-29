# 🏗️ Automation Architecture - Aziro Cluster Center

## Overview

This automation suite is built using **Playwright Python** with a **Page Object Model (POM)** design pattern for maintainable and scalable test automation.

## Design Patterns

### 1. Page Object Model (POM)

The Page Object Model separates test logic from page interactions, making tests more maintainable and reducing code duplication.

```
pages/
├── base_page.py       # Common methods for all pages
├── dashboard_page.py  # Dashboard-specific interactions
├── vm_page.py         # VM management interactions
└── logs_page.py       # Logging system interactions
```

**Benefits:**
- ✅ Reusable page methods
- ✅ Easy maintenance when UI changes
- ✅ Clear separation of concerns
- ✅ Reduced code duplication

### 2. Test Organization

Tests are organized by feature with clear naming conventions:

```
tests/
├── test_dashboard.py       # Dashboard feature tests
├── test_vm_management.py   # VM management tests
└── test_logs.py            # Logging system tests
```

**Naming Convention:**
- Test files: `test_<feature>.py`
- Test classes: `Test<Feature>`
- Test methods: `test_<scenario_description>`

### 3. Fixtures and Configuration

Centralized configuration and reusable fixtures in `conftest.py`:

```python
@pytest.fixture
def dashboard_page(page: Page):
    """Navigate to dashboard and return page"""
    # Setup code
    yield page
    # Teardown code
```

## Architecture Layers

```
┌─────────────────────────────────────────────────┐
│                 Test Layer                      │
│  (test_dashboard.py, test_vm_management.py)     │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│              Page Object Layer                  │
│   (DashboardPage, VMPage, LogsPage)             │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│               Base Page Layer                   │
│        (Common methods and utilities)           │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│              Playwright API                     │
│         (Browser automation core)               │
└─────────────────────────────────────────────────┘
```

## Component Details

### Base Page (`base_page.py`)

**Purpose**: Provides common functionality for all page objects

**Key Methods:**
- `navigate_to()` - Navigate to URLs
- `click_element()` - Click with logging
- `fill_input()` - Fill form fields
- `wait_for_selector()` - Wait for elements
- `wait_for_alert()` - Wait for success/error alerts
- `take_screenshot()` - Capture screenshots

**Example:**
```python
class BasePage:
    def click_element(self, selector: str, timeout: int = 10000):
        logger.info(f"Clicking element: {selector}")
        self.page.click(selector, timeout=timeout)
```

### Dashboard Page (`dashboard_page.py`)

**Purpose**: Handle dashboard-specific interactions

**Key Methods:**
- `load_dashboard()` - Navigate and verify load
- `get_total_vms_count()` - Get VM count
- `click_vms_tab()` - Navigate to VMs tab
- `verify_dashboard_loaded()` - Verify page elements

**Element Locators:**
```python
TAB_DASHBOARD = '[data-testid="dashboard-tab"]'
TOTAL_VMS_VALUE = '[data-testid="total-vms-value"]'
```

### VM Page (`vm_page.py`)

**Purpose**: Handle VM management operations

**Key Methods:**
- `create_vm()` - Create new VM
- `start_vm()` - Start a VM
- `stop_vm()` - Stop a VM
- `take_snapshot()` - Create snapshot
- `delete_vm()` - Delete a VM

**Example:**
```python
def create_vm(self, name: str, memory: int = 2048, cpu: int = 2):
    self.fill_input(self.VM_NAME_INPUT, name)
    self.fill_input(self.VM_MEMORY_INPUT, str(memory))
    self.click_element(self.CREATE_VM_BUTTON)
    return self.wait_for_alert("success")
```

### Logs Page (`logs_page.py`)

**Purpose**: Handle logging system interactions

**Key Methods:**
- `load_l1_logs()` - Load critical logs
- `load_l2_logs()` - Load warning logs
- `load_l3_logs()` - Load info logs
- `get_log_count()` - Count log entries
- `clear_logs()` - Clear log display

## Test Structure

### Standard Test Pattern

```python
@pytest.mark.feature_name
class TestFeatureName:
    """Test suite for Feature Name"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup for each test"""
        # Setup code
        yield
        # Teardown code
    
    def test_scenario_description(self, page: Page):
        """Test description"""
        # Arrange
        page_object = PageObject(page)
        
        # Act
        result = page_object.perform_action()
        
        # Assert
        assert expected in result
```

### Test Markers

```python
@pytest.mark.smoke          # Quick smoke tests
@pytest.mark.regression     # Full regression suite
@pytest.mark.critical       # Critical path tests
@pytest.mark.slow           # Longer running tests
@pytest.mark.dashboard      # Dashboard feature
@pytest.mark.vm_management  # VM management feature
@pytest.mark.logs           # Logging feature
```

## Configuration Management

### pytest.ini

```ini
[pytest]
testpaths = tests
markers =
    smoke: Quick smoke tests
    regression: Full regression suite
addopts = 
    -v
    --html=reports/test-report.html
```

### conftest.py

- **Browser Configuration**: Viewport, locale, permissions
- **Fixtures**: Reusable test components
- **Hooks**: Custom pytest behavior
- **Logging**: Test execution tracking
- **Screenshots**: Capture on failure

## Logging Strategy

### Three-Level Logging

1. **Pytest Logging**: Test execution flow
2. **Page Object Logging**: User actions
3. **Browser Console**: Application logs

**Example:**
```python
logger.info("TEST: Create VM successfully")
logger.info(f"Clicking element: {selector}")
logger.info(f"✓ VM '{vm_name}' created successfully")
```

## Error Handling

### Automatic Error Handling

1. **Screenshot on Failure**: Auto-capture when tests fail
2. **Wait Strategies**: Implicit waits with timeouts
3. **Retry Logic**: Configurable retry for flaky tests
4. **Clear Error Messages**: Descriptive assertions

**Example:**
```python
def screenshot_on_failure(request, page: Page):
    yield
    if request.node.rep_call.failed:
        page.screenshot(path=f"reports/screenshots/{test_name}.png")
```

## Execution Flow

```
1. pytest discovers tests
   ↓
2. Session setup (conftest.py)
   ↓
3. For each test:
   a. Test setup (fixtures)
   b. Page object initialization
   c. Test execution
   d. Assertions
   e. Screenshot on failure
   f. Test teardown
   ↓
4. Session teardown
   ↓
5. Generate reports
```

## Reporting

### HTML Report

Generated automatically with:
- Test execution summary
- Pass/Fail statistics
- Execution time
- Screenshots (for failures)
- Detailed logs

**Configuration:**
```python
addopts = --html=reports/test-report.html --self-contained-html
```

### Console Output

Real-time feedback with:
- Test names
- Step-by-step logging
- Timing information
- Pass/Fail indicators

## Best Practices

### 1. Page Objects

✅ **DO:**
- Keep page objects focused on single pages
- Use descriptive method names
- Add logging to methods
- Handle waits at the page object level

❌ **DON'T:**
- Mix business logic with page interactions
- Duplicate selectors across page objects
- Skip error handling

### 2. Tests

✅ **DO:**
- Keep tests independent
- Use descriptive test names
- Follow Arrange-Act-Assert pattern
- Use appropriate markers

❌ **DON'T:**
- Create test dependencies
- Hardcode wait times
- Skip assertions

### 3. Selectors

✅ **DO:**
- Use `data-testid` attributes
- Define selectors as constants
- Use specific selectors

❌ **DON'T:**
- Use XPath unless necessary
- Use CSS classes as primary selectors
- Use brittle selectors (nth-child)

### 4. Waits

✅ **DO:**
- Use explicit waits
- Wait for specific conditions
- Set appropriate timeouts

❌ **DON'T:**
- Use `time.sleep()` for synchronization
- Use too short timeouts
- Skip waits

## Scalability Considerations

### Parallel Execution

```bash
pytest tests/ -n 3  # Run with 3 workers
```

### Test Data Management

```python
class TestDataGenerator:
    @staticmethod
    def get_vm_config_minimal():
        return {"name": generate_unique_name(), ...}
```

### Environment Configuration

```python
BASE_URL = os.getenv("BASE_URL", "http://localhost:8082")
API_URL = os.getenv("API_URL", "http://localhost:5000/api")
```

## Maintenance

### When UI Changes

1. Update selectors in page objects
2. Update methods if behavior changed
3. Tests remain unchanged (benefit of POM)

### Adding New Tests

1. Identify the feature
2. Add methods to appropriate page object
3. Create test in relevant test file
4. Add appropriate markers

### Adding New Page Objects

1. Create new file in `pages/`
2. Inherit from `BasePage`
3. Define selectors as constants
4. Implement methods for interactions
5. Add logging to methods

## Performance Optimization

1. **Parallel Execution**: Use `-n` flag
2. **Headed vs Headless**: Headless is faster
3. **Selective Test Running**: Use markers
4. **Efficient Selectors**: Use `data-testid`

## Security Considerations

- No hardcoded credentials
- Use environment variables
- Sanitize logs (no sensitive data)
- Screenshots don't capture sensitive info

---

**Architecture Version**: 1.0.0  
**Last Updated**: October 29, 2025

