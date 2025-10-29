# 🔗 URL Configuration - Aziro Cluster Center Automation

## Application URLs

| Service | URL | Status |
|---------|-----|--------|
| **Frontend** | `http://localhost:8082` | ✅ Configured |
| **Backend API** | `http://localhost:5000/api` | ✅ Configured |
| **Health Check** | `http://localhost:5000/api/health` | ✅ Available |

---

## Configuration Files Updated

All core files have been updated to use the correct URLs:

### Python Files
- ✅ `conftest.py` - BASE_URL = `http://localhost:8082`
- ✅ `pages/base_page.py` - self.base_url = `http://localhost:8082`

### Documentation Files
- ✅ `README.md`
- ✅ `QUICK_START.md`
- ✅ `START_HERE.md`
- ✅ `ARCHITECTURE.md`

---

## Verification

To verify the URLs are configured correctly:

```bash
# Check configuration in conftest.py
grep "BASE_URL" conftest.py

# Check configuration in base_page.py
grep "base_url" pages/base_page.py
```

Expected output:
```python
BASE_URL = os.getenv("BASE_URL", "http://localhost:8082")
self.base_url = "http://localhost:8082"
```

---

## Environment Variable Override

You can override the URLs using environment variables if needed:

```bash
# Set environment variables
export BASE_URL="http://localhost:8082"
export API_URL="http://localhost:5000/api"

# Run tests
pytest tests/ --headed -v
```

---

## Before Running Tests

**Start the servers:**

```bash
# Terminal 1: Backend (port 5000)
cd ../backend
npm run dev

# Terminal 2: Frontend (port 8080)
cd ../frontend
node simple-server.js

# Terminal 3: Tests
cd automation
./run_tests.sh
```

**Verify servers are running:**

```bash
# Check frontend
curl http://localhost:8082

# Check backend health
curl http://localhost:5000/api/health
```

---

## Quick Start

```bash
cd automation
./run_tests.sh
```

The automation will automatically connect to:
- Frontend: `http://localhost:8082`
- Backend: `http://localhost:5000/api`

---

**Status**: ✅ All URLs configured correctly  
**Last Updated**: October 29, 2025

