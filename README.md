# Automation Test Suite

Playwright-based UI automation test suite for Aziro Cluster Center with comprehensive test reporting and dashboard.

## Project Structure

```
automation/
├── tests/
│   ├── test_dashboard.py       # Dashboard functionality tests
│   ├── test_vm_management.py   # VM management tests
│   └── test_logs.py            # Logging system tests
├── pages/
│   ├── base_page.py            # Base page object
│   ├── dashboard_page.py       # Dashboard page object
│   ├── vm_page.py             # VM management page object
│   └── logs_page.py           # Logs page object
├── utils/
│   ├── helpers.py             # Helper functions
│   └── test_reporter.py      # Test reporting utilities
├── reports/
│   ├── test-report.html       # HTML test report
│   ├── test_history.json      # Test run history
│   └── screenshots/           # Failure screenshots
├── logs/
│   └── test_execution_*.log   # Test execution logs
├── dashboard_server.py        # Results dashboard server
├── run_tests.sh              # Test execution script
├── conftest.py               # Pytest configuration
├── pytest.ini                # Pytest settings
└── requirements.txt          # Python dependencies
```

## How to Run

### Prerequisites
- **Python 3.8+** (Python 3.14 now supported - greenlet dependency removed)
- Node.js (for backend/frontend servers)

### Installation

```bash
cd automation

# Verify Python version
python3 --version

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Upgrade pip
python3 -m pip install --upgrade pip

# Install greenlet 3.2.4 first (Python 3.14 compatibility)
# Playwright requires greenlet, and 3.2.4+ supports Python 3.14
python3 -m pip install "greenlet>=3.2.4"

# Install dependencies
python3 -m pip install -r requirements.txt

# Install Playwright browsers
python3 -m playwright install chromium
```

**Note**: The `allure-pytest` dependency has been removed to avoid `greenlet` compatibility issues with Python 3.14. The dashboard will still work perfectly - it gracefully handles missing Allure results.

### Run Tests

```bash
# Run all tests (headed mode)
./run_tests.sh

# Or run directly with pytest
pytest tests/ --headed -v

# Headless mode (faster)
pytest tests/ -v

# Run specific test file
pytest tests/test_dashboard.py --headed -v
```

### View Results Dashboard

After running tests, the dashboard server automatically starts:

```bash
# Dashboard is available at:
http://localhost:8003
```

Or start manually:

```bash
python3 dashboard_server.py
```

## Access Points

- **Test Results Dashboard**: `http://localhost:8003`
- **Test Log Viewer**: `http://localhost:8003/log/<test_name>`
- **HTML Report**: `reports/test-report.html`

## Ports

- **Dashboard Server**: Port 8003
- **Frontend (test target)**: Port 8082
- **Backend API (test target)**: Port 5000

## Test Coverage

- **Dashboard Tests**: 5 tests
- **VM Management Tests**: 9 tests
- **Logging Tests**: 8 tests
- **Total**: 22+ tests

## Features

- Comprehensive test reporting
- Test run history (last 5 runs)
- Detailed failure analysis
- Screenshot capture on failures
- Log integration
- Build number tracking
