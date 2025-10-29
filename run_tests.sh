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

# Open HTML report (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Opening test report in browser..."
    open reports/test-report.html
fi

exit $TEST_EXIT_CODE

