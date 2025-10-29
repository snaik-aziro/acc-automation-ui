# 🚀 START HERE - Aziro Cluster Center UI Automation

## Welcome! 👋

This folder contains a **complete UI automation suite** for the Aziro Cluster Center application built with **Playwright Python**.

---

## ⚡ Quick Start (60 seconds)

### Prerequisites ✅

Make sure these are running:
1. **Backend**: `http://localhost:5000` ✅
2. **Frontend**: `http://localhost:8082` ✅
3. **Python 3.8+** installed ✅

### Run Tests (3 commands)

```bash
# 1. Go to automation folder (you're here!)
cd automation

# 2. Make script executable (first time only)
chmod +x run_tests.sh

# 3. Run all tests in HEADED mode (browser visible)
./run_tests.sh
```

**That's it!** 🎉

The script will:
- ✅ Setup virtual environment
- ✅ Install all dependencies
- ✅ Install Playwright browser
- ✅ Run 22 tests in visible browser window
- ✅ Generate beautiful HTML report
- ✅ Open report automatically

---

## 📖 Documentation

| File | Description | When to Read |
|------|-------------|--------------|
| **QUICK_START.md** | Fast setup & common commands | Start here if in a hurry |
| **README.md** | Complete documentation | For comprehensive understanding |
| **ARCHITECTURE.md** | Technical architecture | For developers & maintainers |
| **PROJECT_SUMMARY.md** | Full project overview | For project managers & leads |

---

## 🎯 What Gets Tested?

### ✅ Dashboard (5 tests)
- Page loads correctly
- Metrics display properly
- Tab navigation works
- Values are valid

### ✅ VM Management (9 tests)
- Create VMs with different specs
- Start/Stop VMs
- Create & view snapshots
- Delete VMs
- Network type options

### ✅ Logging System (8 tests)
- Load L1 (Critical) logs
- Load L2 (Warning) logs
- Load L3 (Info) logs
- Filter by log level
- Clear log display

**Total: 22 comprehensive tests**

---

## 🎬 Execution Modes

### Headed Mode (Recommended - Watch Tests)
```bash
./run_tests.sh
# or
pytest tests/ --headed --slowmo 500 -v
```
**Use for**: Debugging, demonstrations, learning

### Headless Mode (Faster - Background)
```bash
pytest tests/ -v
```
**Use for**: CI/CD, bulk runs, quick verification

### Specific Features
```bash
# Dashboard only
pytest tests/test_dashboard.py --headed -v

# VM management only
pytest tests/test_vm_management.py --headed -v

# Logs only
pytest tests/test_logs.py --headed -v

# Smoke tests (quick essentials)
pytest -m smoke --headed -v
```

---

## 📊 View Results

### HTML Report (Automatic)
```bash
open reports/test-report.html
```

**Contains:**
- ✅ Pass/Fail summary
- ⏱️ Execution times
- 📸 Screenshots (failures)
- 📝 Detailed logs

### Screenshots (Failures)
```bash
ls reports/screenshots/
```

---

## 📁 Project Structure

```
automation/
├── pages/              # Page Object Model (POM)
│   ├── base_page.py       # Common methods
│   ├── dashboard_page.py  # Dashboard interactions
│   ├── vm_page.py         # VM operations
│   └── logs_page.py       # Logging interactions
│
├── tests/              # Test Suite (22 tests)
│   ├── test_dashboard.py       # 5 tests
│   ├── test_vm_management.py   # 9 tests
│   └── test_logs.py            # 8 tests
│
├── utils/              # Helper functions
│   └── helpers.py
│
├── reports/            # Generated reports
│   ├── test-report.html
│   └── screenshots/
│
├── run_tests.sh        # Main execution script ⭐
├── conftest.py         # Pytest configuration
├── pytest.ini          # Pytest settings
├── requirements.txt    # Dependencies
│
└── Documentation (you are here)
    ├── START_HERE.md         ⭐ This file
    ├── QUICK_START.md        ⭐ Fast setup
    ├── README.md             📖 Complete guide
    ├── ARCHITECTURE.md       🏗️ Technical details
    └── PROJECT_SUMMARY.md    📋 Full overview
```

---

## 🎓 Learning Path

### For Beginners
1. ✅ Read this file (you're here!)
2. ✅ Read `QUICK_START.md`
3. ✅ Run `./run_tests.sh` and watch
4. ✅ Open `test_dashboard.py` and read
5. ✅ Try modifying a simple test

### For Experienced Users
1. ✅ Read `ARCHITECTURE.md`
2. ✅ Review page object pattern
3. ✅ Understand test structure
4. ✅ Extend with new tests
5. ✅ Customize for your needs

---

## ⚙️ Common Commands Reference

```bash
# Setup (first time)
chmod +x run_tests.sh
./run_tests.sh

# Run all tests
pytest tests/ --headed -v

# Run specific test file
pytest tests/test_dashboard.py --headed -v

# Run specific test
pytest tests/test_dashboard.py::TestDashboard::test_dashboard_loads_successfully --headed -v

# Run by marker
pytest -m smoke --headed -v          # Smoke tests
pytest -m critical --headed -v       # Critical tests
pytest -m vm_management --headed -v  # VM tests

# Different speeds
pytest tests/ --headed --slowmo 100 -v    # Fast
pytest tests/ --headed --slowmo 500 -v    # Normal
pytest tests/ --headed --slowmo 1000 -v   # Slow (debug)

# Headless (faster)
pytest tests/ -v

# Parallel (3 workers)
pytest tests/ -n 3 -v

# With maximum details
pytest tests/ --headed -vv --tb=long
```

---

## 🐛 Troubleshooting

### Issue: Backend/Frontend not running
```bash
# Terminal 1: Start backend
cd ../backend && npm run dev

# Terminal 2: Start frontend
cd ../frontend && node simple-server.js

# Terminal 3: Run tests
cd automation && ./run_tests.sh
```

### Issue: Python not found
```bash
python3 --version  # Check if installed
```

### Issue: Virtual environment issues
```bash
rm -rf venv                    # Remove old venv
python3 -m venv venv           # Create new
source venv/bin/activate       # Activate
pip install -r requirements.txt # Install deps
```

### Issue: Playwright not installed
```bash
source venv/bin/activate
playwright install chromium
```

---

## ✨ Features

- ✅ **22 comprehensive tests** covering all features
- ✅ **Headed mode execution** - watch tests run
- ✅ **Clean, readable code** with Page Object Model
- ✅ **Beautiful HTML reports** with screenshots
- ✅ **Comprehensive logging** at all levels
- ✅ **Easy to run** - one script does everything
- ✅ **Easy to extend** - add new tests easily
- ✅ **Production-ready** - error handling, retries

---

## 🎉 Success Indicators

When everything works, you'll see:

1. ✅ Browser window opens (Chromium)
2. ✅ Tests execute one by one (you can watch!)
3. ✅ Green checkmarks for passed tests
4. ✅ Console shows "All tests passed!"
5. ✅ HTML report opens automatically
6. ✅ Report shows test results

---

## 📞 Need Help?

1. **Quick questions?** → Check `QUICK_START.md`
2. **Technical details?** → Check `README.md` or `ARCHITECTURE.md`
3. **Test failed?** → Check `reports/test-report.html`
4. **Screenshot?** → Check `reports/screenshots/`

---

## 🚀 Ready to Go!

Everything is set up and ready to run. Just execute:

```bash
./run_tests.sh
```

And watch the magic happen! ✨

---

**Status**: ✅ Complete & Production-Ready  
**Framework**: Playwright Python  
**Tests**: 22 comprehensive test cases  
**Execution**: Headed mode (browser visible)  
**Reports**: Clean HTML with screenshots  

**Happy Testing! 🧪**

