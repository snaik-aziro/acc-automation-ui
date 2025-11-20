#!/bin/bash

# Aziro Cluster Center - UI Automation Test Runner
# This script runs the Playwright automation tests in HEADED mode

echo "=========================================="
echo "Aziro Cluster Center - UI Automation"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 found${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Install Playwright browsers
echo -e "${YELLOW}Installing Playwright browsers...${NC}"
playwright install chromium
echo -e "${GREEN}✓ Playwright browsers installed${NC}"

# Create reports directory
mkdir -p reports/screenshots reports/allure-results

echo ""
echo "=========================================="
echo "Starting Test Execution (HEADED MODE)"
echo "=========================================="
echo ""

# Run tests in headed mode with HTML report
pytest tests/ \
    --headed \
    --browser chromium \
    --slowmo 500 \
    -v \
    --tb=short \
    --html=reports/test-report.html \
    --self-contained-html

# Capture exit code
TEST_EXIT_CODE=$?

echo ""
echo "=========================================="
echo "Test Execution Complete"
echo "=========================================="
echo ""

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
else
    echo -e "${RED}✗ Some tests failed. Check the report for details.${NC}"
fi

echo ""
echo "Reports generated:"
echo "  - HTML Report: reports/test-report.html"
echo "  - Screenshots: reports/screenshots/"
echo ""

# Start the results dashboard server in the background
echo ""
echo "=========================================="
echo "Starting Results Dashboard Server"
echo "=========================================="
echo ""

# Check if dashboard server is already running
if lsof -ti:8003 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Dashboard server already running on port 8003${NC}"
    echo -e "${GREEN}✓ Dashboard available at: http://localhost:8003${NC}"
else
    # Start dashboard server in background
    echo -e "${YELLOW}Starting dashboard server on port 8003...${NC}"
    python3 dashboard_server.py > dashboard.log 2>&1 &
    DASHBOARD_PID=$!
    sleep 2
    
    if kill -0 $DASHBOARD_PID 2>/dev/null; then
        echo -e "${GREEN}✓ Dashboard server started (PID: $DASHBOARD_PID)${NC}"
        echo -e "${GREEN}✓ Dashboard available at: http://localhost:8003${NC}"
        echo ""
        echo "To stop the dashboard server, run: kill $DASHBOARD_PID"
    else
        echo -e "${RED}✗ Failed to start dashboard server${NC}"
        echo "Check dashboard.log for errors"
    fi
fi

echo ""

# Open dashboard in browser (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Opening results dashboard in browser..."
    sleep 1
    open http://localhost:8003
fi

exit $TEST_EXIT_CODE

