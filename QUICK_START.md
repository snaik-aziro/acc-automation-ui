# 🚀 Quick Start Guide - Aziro Cluster Center Automation

## Prerequisites Check ✅

Before starting, make sure:

1. **Backend is running** on port 5000
   ```bash
   # In backend directory
   cd ../backend
   npm run dev
   ```

2. **Frontend is running** on port 8080
   ```bash
   # In frontend directory
   cd ../frontend
   node simple-server.js
   ```

3. **Python 3.8+** is installed
   ```bash
   python3 --version
   ```

## Run Tests (3 Simple Steps) 🎯

### Step 1: Navigate to automation folder
```bash
cd automation
```

### Step 2: Make run script executable (first time only)
```bash
chmod +x run_tests.sh
```

### Step 3: Run the tests!
```bash
./run_tests.sh
```

That's it! The script will:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Install Playwright browsers
- ✅ Run all tests in HEADED mode (you can see the browser)
- ✅ Generate HTML report
- ✅ Open report automatically (on macOS)

## Alternative: Manual Commands 📝

If you prefer manual control:

```bash
# Setup (first time only)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# Run tests (HEADED mode - browser visible)
pytest tests/ --headed --browser chromium --slowmo 500 -v

# View report
open reports/test-report.html
```

## Run Specific Tests 🎯

```bash
# Activate virtual environment first
source venv/bin/activate

# Dashboard tests only
pytest tests/test_dashboard.py --headed -v

# VM management tests only
pytest tests/test_vm_management.py --headed -v

# Logging tests only
pytest tests/test_logs.py --headed -v

# Smoke tests only (quick essential tests)
pytest -m smoke --headed -v

# Critical tests only
pytest -m critical --headed -v
```

## Viewing Results 📊

### HTML Report
```bash
open reports/test-report.html
```

The report shows:
- ✅ Pass/Fail status for each test
- ⏱️ Execution time
- 📸 Screenshots (for failures)
- 📝 Detailed logs

### Screenshots (for failed tests)
```bash
ls -la reports/screenshots/
```

## Test Execution Speed 🏃

| Mode | Command | Speed | Use Case |
|------|---------|-------|----------|
| **Headed (Slow)** | `--headed --slowmo 1000` | Slow | Debugging, watching tests |
| **Headed (Normal)** | `--headed --slowmo 500` | Medium | Default, demo |
| **Headed (Fast)** | `--headed --slowmo 100` | Fast | Quick verification |
| **Headless** | No flags | Fastest | CI/CD, bulk runs |

## Troubleshooting 🔧

### Issue: "Application not running"
**Solution**: Start both servers first
```bash
# Terminal 1: Backend
cd backend && npm run dev

# Terminal 2: Frontend  
cd frontend && node simple-server.js

# Terminal 3: Tests
cd automation && ./run_tests.sh
```

### Issue: "Playwright not found"
**Solution**: Install Playwright browsers
```bash
source venv/bin/activate
playwright install chromium
```

### Issue: "Tests running too fast"
**Solution**: Increase slow motion
```bash
pytest tests/ --headed --slowmo 1000 -v
```

### Issue: "Virtual environment not activating"
**Solution**: Recreate it
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## What Gets Tested? ✅

### Dashboard
- ✅ Page loads correctly
- ✅ All metrics display
- ✅ Tab navigation works
- ✅ Values are numeric

### VM Management
- ✅ Create VM with different specs
- ✅ List VMs
- ✅ Start/Stop VMs
- ✅ Create snapshots
- ✅ View snapshots
- ✅ Delete VMs

### Logging System
- ✅ Load L1 (Critical) logs
- ✅ Load L2 (Warning) logs
- ✅ Load L3 (Info) logs
- ✅ Filter by log level
- ✅ Clear logs

## Pro Tips 💡

1. **First time?** Use `--headed --slowmo 1000` to see everything clearly
2. **Debugging?** Use `-vv --tb=long` for maximum details
3. **In a hurry?** Use `-m smoke` to run only essential tests
4. **CI/CD?** Remove `--headed` for headless mode

## Quick Reference Commands 📋

```bash
# All tests (default speed)
./run_tests.sh

# All tests (slow motion)
pytest tests/ --headed --slowmo 1000 -v

# Smoke tests only
pytest -m smoke --headed -v

# Single test file
pytest tests/test_dashboard.py --headed -v

# Single test function
pytest tests/test_dashboard.py::TestDashboard::test_dashboard_loads_successfully --headed -v

# Parallel execution (faster, headless)
pytest tests/ -n 3 -v

# With debug logging
pytest tests/ --headed -vv --log-cli-level=DEBUG
```

## Success! 🎉

If everything works, you should see:
- ✅ Browser window opens (Chromium)
- ✅ Tests execute one by one
- ✅ Green checkmarks for passed tests
- ✅ HTML report opens automatically
- ✅ "All tests passed!" message

## Need Help? 🆘

1. Check the HTML report: `reports/test-report.html`
2. Review screenshots: `reports/screenshots/`
3. Look at console output for error messages
4. Make sure application is running correctly

---

**Happy Testing! 🚀**

