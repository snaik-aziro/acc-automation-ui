#!/usr/bin/env python3
"""
Aziro Automation Results Dashboard Server
Serves a beautiful dashboard showing test results with passed/failed counts
and detailed summaries for failed test cases.
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from html import escape
from bs4 import BeautifulSoup
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

# Configuration
PORT = 8003
REPORTS_DIR = Path(__file__).parent / "reports"
HTML_REPORT = REPORTS_DIR / "test-report.html"
ALLURE_RESULTS_DIR = REPORTS_DIR / "allure-results"
LOGS_DIR = Path(__file__).parent / "logs"
HISTORY_FILE = REPORTS_DIR / "test_history.json"
PRODUCT_NAME = "Aziro Cluster Center"


class TestResult:
    """Represents a single test result"""
    def __init__(self, name: str, status: str, duration: float = 0.0, error: str = ""):
        self.name = name
        self.status = status  # 'passed', 'failed', 'skipped'
        self.duration = duration
        self.error = error
        self.summary = ""
        self.feature = self._extract_feature(name)
        self.log_file = None
        self.log_start_line = None
        self.log_end_line = None
    
    def _extract_feature(self, name: str) -> str:
        """Extract feature from test name"""
        if 'dashboard' in name.lower():
            return 'Dashboard'
        elif 'vm' in name.lower() or 'management' in name.lower():
            return 'VM Management'
        elif 'log' in name.lower():
            return 'Logging'
        return 'General'


def save_test_run_history(results: Dict) -> None:
    """Save current test run to history file"""
    try:
        # Ensure reports directory exists
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Load existing history
        history = []
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except Exception:
                history = []
        
        # Create history entry
        history_entry = {
            "build_number": results.get('build_number', ''),
            "timestamp": results.get('timestamp').isoformat() if results.get('timestamp') else '',
            "total": results.get('total', 0),
            "passed": results.get('passed', 0),
            "failed": results.get('failed', 0),
            "skipped": results.get('skipped', 0),
            "pass_rate": round((results.get('passed', 0) / results.get('total', 1)) * 100, 2),
            "duration": sum(t.duration for t in results.get('tests', [])),
            "product_name": PRODUCT_NAME
        }
        
        # Add to beginning of history
        history.insert(0, history_entry)
        
        # Keep only last 5 runs
        history = history[:5]
        
        # Save back to file
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)
    
    except Exception as e:
        print(f"Error saving test run history: {e}")


def load_test_run_history() -> List[Dict]:
    """Load test run history from file"""
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading test run history: {e}")
    
    return []


def parse_html_report() -> Dict:
    """Parse the pytest HTML report"""
    if not HTML_REPORT.exists():
        return {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "tests": [],
            "timestamp": None
        }
    
    try:
        with open(HTML_REPORT, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Initialize counters - will be calculated from parsed tests
        passed = 0
        failed = 0
        skipped = 0
        tests = []
        
        # Parse test results using BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all test rows in the results table
        results_table = soup.find('table', id='results-table')
        if results_table:
            # Find all tbody elements with test data
            tbody_elements = results_table.find_all('tbody', class_='results-table-row')
            for tbody in tbody_elements:
                rows = tbody.find_all('tr')
                for row in rows:
                    # Skip header rows
                    if row.find('th'):
                        continue
                    
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        # Extract test name
                        name_col = cols[0]
                        test_name = name_col.get_text(strip=True)
                        if not test_name:
                            continue
                        
                        # Extract status
                        status_col = cols[1]
                        status_text = status_col.get_text(strip=True).lower()
                        if 'passed' in status_text:
                            status = 'passed'
                        elif 'failed' in status_text or 'error' in status_text:
                            status = 'failed'
                        elif 'skipped' in status_text:
                            status = 'skipped'
                        else:
                            status = 'unknown'
                        
                        # Extract duration
                        duration = 0.0
                        if len(cols) >= 3:
                            duration_col = cols[2]
                            duration_text = duration_col.get_text(strip=True)
                            duration_match = re.search(r'([\d.]+)', duration_text)
                            if duration_match:
                                duration = float(duration_match.group(1))
                        
                        # Extract error message for failed tests
                        error = ""
                        if status == 'failed':
                            # Look for log wrapper or error details
                            log_wrapper = row.find_next('div', class_='logwrapper')
                            if log_wrapper:
                                log_elem = log_wrapper.find('div', class_='log')
                                if log_elem:
                                    error = log_elem.get_text(strip=True)[:1000]  # Limit error length
                            
                            # Also check for error in the row itself
                            if not error:
                                error_elem = row.find('div', class_='log')
                                if error_elem:
                                    error = error_elem.get_text(strip=True)[:1000]
                        
                        test_result = TestResult(test_name, status, duration, error)
                        tests.append(test_result)
        
        # If no tests found in table, try extracting from JSON data blob
        if not tests:
            # Try to extract from data-jsonblob attribute (pytest-html format)
            data_match = re.search(r'data-jsonblob="([^"]+)"', content)
        if data_match:
            try:
                from html import unescape
                json_str = unescape(data_match.group(1))
                data = json.loads(json_str)
                
                # Extract tests from the data
                tests_data = data.get('tests', {})
                
                # Handle both dict and list formats
                if isinstance(tests_data, dict):
                    for test_id, test_info in tests_data.items():
                        test_name = test_id  # Default to test_id
                        outcome = ''
                        duration = 0.0
                        error = ""
                        
                        # Handle list format (pytest-html format where test_info is a list)
                        if isinstance(test_info, list) and test_info:
                            first_item = test_info[0]
                            if isinstance(first_item, dict):
                                test_name = first_item.get('testId', test_id)
                                result = first_item.get('result', '').lower()
                                
                                # Map result to outcome
                                if 'passed' in result:
                                    outcome = 'passed'
                                elif 'failed' in result or 'error' in result:
                                    outcome = 'failed'
                                elif 'skipped' in result:
                                    outcome = 'skipped'
                                
                                # Extract duration - can be float or "HH:MM:SS" format
                                duration_str = first_item.get('duration', 0)
                                try:
                                    if isinstance(duration_str, str) and ':' in duration_str:
                                        # Parse "HH:MM:SS" format
                                        parts = duration_str.split(':')
                                        if len(parts) == 3:
                                            duration = int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
                                        else:
                                            duration = 0.0
                                    else:
                                        duration = float(duration_str)
                                except (ValueError, TypeError):
                                    duration = 0.0
                                
                                # Extract error message from log or extras
                                if outcome in ['failed', 'error']:
                                    # Try log field first
                                    log_content = first_item.get('log', '')
                                    if log_content:
                                        error = str(log_content)[:2000]
                                    else:
                                        # Try extras
                                        extras = first_item.get('extras', [])
                                        for extra in extras:
                                            if isinstance(extra, dict):
                                                content = extra.get('content', '')
                                                if content:
                                                    error = str(content)[:2000]
                                                    break
                        
                        # Handle dict format (alternative format)
                        elif isinstance(test_info, dict):
                            test_name = test_info.get('name', test_id)
                            outcome = test_info.get('outcome', '').lower()
                            duration = float(test_info.get('duration', 0))
                            longrepr = test_info.get('longrepr', '')
                            
                            # Extract error message
                            if outcome in ['failed', 'error']:
                                if longrepr:
                                    error = str(longrepr)[:2000]
                                elif isinstance(test_info.get('call'), dict) and test_info.get('call', {}).get('longrepr'):
                                    error = str(test_info.get('call', {}).get('longrepr'))[:2000]
                                elif isinstance(test_info.get('setup'), dict) and test_info.get('setup', {}).get('longrepr'):
                                    error = str(test_info.get('setup', {}).get('longrepr'))[:2000]
                        
                        # Determine status
                        status = 'unknown'
                        if outcome == 'passed':
                            status = 'passed'
                        elif outcome in ['failed', 'error']:
                            status = 'failed'
                        elif outcome == 'skipped':
                            status = 'skipped'
                        
                        test_result = TestResult(test_name, status, duration, error)
                        tests.append(test_result)
                
                elif isinstance(tests_data, list):
                    # Handle list format
                    for test_info in tests_data:
                        if isinstance(test_info, dict):
                            test_name = test_info.get('name', test_info.get('nodeid', 'unknown'))
                            outcome = test_info.get('outcome', '').lower()
                            duration = float(test_info.get('duration', 0))
                            longrepr = test_info.get('longrepr', '')
                            
                            # Extract error message - try multiple sources
                            error = ""
                            if outcome in ['failed', 'error']:
                                if longrepr:
                                    error = str(longrepr)[:2000]
                                elif test_info.get('call', {}).get('longrepr'):
                                    error = str(test_info.get('call', {}).get('longrepr'))[:2000]
                                elif test_info.get('setup', {}).get('longrepr'):
                                    error = str(test_info.get('setup', {}).get('longrepr'))[:2000]
                            
                            # Determine status
                            status = 'unknown'
                            if outcome == 'passed':
                                status = 'passed'
                            elif outcome in ['failed', 'error']:
                                status = 'failed'
                            elif outcome == 'skipped':
                                status = 'skipped'
                            
                            test_result = TestResult(test_name, status, duration, error)
                            tests.append(test_result)
                    
            except Exception as e:
                print(f"Error parsing JSON data: {e}")
                import traceback
                traceback.print_exc()
        
        # Calculate counts from the actual parsed test objects (most accurate)
        passed = len([t for t in tests if t.status == 'passed'])
        failed = len([t for t in tests if t.status == 'failed'])
        skipped = len([t for t in tests if t.status == 'skipped'])
        total = len(tests)
        
        # Get timestamp from file modification time
        timestamp = datetime.fromtimestamp(HTML_REPORT.stat().st_mtime)
        
        # Generate build number from timestamp (format: YYYYMMDD-HHMMSS)
        build_number = timestamp.strftime('%Y%m%d-%H%M%S')
        
        # Find latest log file and extract test log sections for failed tests
        latest_log_file = find_latest_log_file()
        if latest_log_file:
            for test in tests:
                if test.status == 'failed':
                    # Try multiple name variations
                    test_name_variations = [
                        test.name,  # Original name
                        test.name.split('[')[0] if '[' in test.name else test.name,  # Without browser suffix
                        test.name.split('::')[-1] if '::' in test.name else test.name,  # Just function name
                    ]
                    
                    for name_variant in test_name_variations:
                        start_line, end_line = extract_test_log_section(latest_log_file, name_variant)
                        if start_line:
                            test.log_file = latest_log_file.name
                            test.log_start_line = start_line
                            test.log_end_line = end_line
                            break
        
        # Save to history
        result_dict = {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "tests": tests,
            "timestamp": timestamp,
            "build_number": build_number,
            "log_file": latest_log_file.name if latest_log_file else None
        }
        
        save_test_run_history(result_dict)
        
        return result_dict
    
    except Exception as e:
        import traceback
        print(f"Error parsing HTML report: {e}")
        print(traceback.format_exc())
        return {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "tests": [],
            "timestamp": None,
            "error": str(e)
        }


def find_latest_log_file() -> Optional[Path]:
    """Find the most recent test execution log file"""
    if not LOGS_DIR.exists():
        return None
    
    log_files = list(LOGS_DIR.glob("test_execution_*.log"))
    if not log_files:
        return None
    
    # Sort by modification time, most recent first
    log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return log_files[0]


def extract_test_log_section(log_file: Path, test_name: str) -> tuple:
    """Extract start and end line numbers for a specific test in the log file"""
    if not log_file or not log_file.exists():
        return None, None
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Normalize test name for matching
        normalized_test_name = test_name.lower().strip()
        # Remove browser suffix like [chromium]
        if '[' in normalized_test_name:
            normalized_test_name = normalized_test_name.split('[')[0].strip()
        
        # Extract just the function name if it's a full path
        if '::' in normalized_test_name:
            parts = normalized_test_name.split('::')
            descriptive_name = parts[-1] if parts else normalized_test_name
        else:
            descriptive_name = normalized_test_name
        
        start_line = None
        end_line = None
        
        # Look for test start markers
        for i, line in enumerate(lines, 1):
            line_lower = line.lower()
            
            # Check for test start patterns
            if start_line is None:
                # Pattern 1: "🚀 TEST: [Descriptive Name] - START"
                if "🚀 test:" in line_lower and "start" in line_lower:
                    if descriptive_name in line_lower or normalized_test_name in line_lower:
                        start_line = i
                        continue
                
                # Pattern 2: "Test ID: [test_func_name]"
                if "test id:" in line_lower:
                    if descriptive_name in line_lower or normalized_test_name in line_lower:
                        # Look back a few lines for the test start
                        for j in range(max(0, i - 5), i):
                            if "🚀" in lines[j] or "test:" in lines[j].lower():
                                start_line = j + 1
                                break
                        if start_line:
                            continue
                        else:
                            start_line = i
            
            # Look for test end
            if start_line is not None and end_line is None:
                if i > start_line + 10:
                    line_lower = line.lower()
                    # Check if this is a different test starting
                    if ("🚀 test:" in line_lower or "test:" in line_lower) and "start" in line_lower:
                        # Make sure it's not the same test
                        if normalized_test_name.lower() not in line_lower:
                            end_line = i
                            break
                    
                    # Or look for session end markers
                    if "FINAL TEST SUMMARY" in line or "Test session" in line or "pytest" in line_lower:
                        if i > start_line + 10:
                            end_line = i
                            break
                    
                    # Or look for test completion markers
                    if ("PASSED" in line or "FAILED" in line or "SKIPPED" in line) and i > start_line + 10:
                        # Check if this is the end of our test (look for test name nearby)
                        lookback = min(50, i - start_line)
                        for j in range(max(0, i - lookback), i):
                            if normalized_test_name.lower() in lines[j].lower():
                                end_line = i + 20  # Include some lines after completion
                                break
                        if end_line:
                            break
            
            # Check for test end (next test start or session end)
            if start_line is not None and end_line is None:
                # Look for next test start (but not the same test)
                if i > start_line + 10:
                    line_lower = line.lower()
                    # Check if this is a different test starting
                    if ("🚀 test:" in line_lower or "test:" in line_lower) and "start" in line_lower:
                        # Make sure it's not the same test
                        if normalized_test_name.lower() not in line_lower:
                            end_line = i
                            break
                    
                    # Or look for session end markers
                    if "FINAL TEST SUMMARY" in line or "Test session" in line or "pytest" in line_lower:
                        if i > start_line + 10:
                            end_line = i
                            break
                    
                    # Or look for test completion markers
                    if ("PASSED" in line or "FAILED" in line or "SKIPPED" in line) and i > start_line + 10:
                        # Check if this is the end of our test (look for test name nearby)
                        lookback = min(50, i - start_line)
                        for j in range(max(0, i - lookback), i):
                            if normalized_test_name.lower() in lines[j].lower():
                                end_line = i + 20  # Include some lines after completion
                                break
                        if end_line:
                            break
        
        # If no end found, use end of file
        if start_line is not None and end_line is None:
            end_line = len(lines)
        
        return start_line, end_line
    
    except Exception as e:
        print(f"Error extracting test log section: {e}")
        import traceback
        traceback.print_exc()
        return None, None


def get_test_log_content(log_file: Path, start_line: int, end_line: int) -> str:
    """Get log content for a specific test"""
    if not log_file or not log_file.exists() or start_line is None:
        return ""
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if end_line is None:
            end_line = len(lines)
        
        # Extract the relevant section
        content_lines = lines[start_line-1:end_line]
        return ''.join(content_lines)
    
    except Exception as e:
        print(f"Error reading test log content: {e}")
        return ""


def parse_allure_results() -> Dict:
    """Parse Allure JSON results for additional details"""
    if not ALLURE_RESULTS_DIR.exists():
        return {}
    
    allure_data = {}
    try:
        for json_file in ALLURE_RESULTS_DIR.glob("*-result.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'name' in data:
                        test_name = data['name']
                        allure_data[test_name] = {
                            "status": data.get('status', 'unknown'),
                            "statusDetails": data.get('statusDetails', {}),
                            "steps": data.get('steps', []),
                            "attachments": data.get('attachments', [])
                        }
            except Exception as e:
                continue
    except Exception as e:
        print(f"Error parsing Allure results: {e}")
    
    return allure_data


def generate_2line_summary(error_message: str) -> str:
    """Generate a 2-line summary from error message"""
    if not error_message or error_message == "No error details available":
        return "No error details available<br>Please check the full log for more information"
    
    # Clean up the error message
    error_lines = error_message.split('\n')
    error_lines = [line.strip() for line in error_lines if line.strip()]
    
    # Extract key information
    summary_line1 = ""
    summary_line2 = ""
    
    # Try to find the main error/exception
    for line in error_lines:
        if any(keyword in line.lower() for keyword in ['error:', 'exception:', 'failed:', 'timeout', 'assertion']):
            if not summary_line1:
                summary_line1 = line[:150]  # First 150 chars
                if len(line) > 150:
                    summary_line1 += "..."
            elif not summary_line2:
                summary_line2 = line[:150]
                if len(line) > 150:
                    summary_line2 += "..."
                break
    
    # If we didn't find specific error keywords, use first two meaningful lines
    if not summary_line1:
        for line in error_lines:
            if len(line) > 20 and not line.startswith('File') and not line.startswith('Traceback'):
                if not summary_line1:
                    summary_line1 = line[:150]
                    if len(line) > 150:
                        summary_line1 += "..."
                elif not summary_line2:
                    summary_line2 = line[:150]
                    if len(line) > 150:
                        summary_line2 += "..."
                    break
    
    # Fallback
    if not summary_line1:
        summary_line1 = error_lines[0][:150] if error_lines else "Error occurred during test execution"
        if len(error_lines) > 1:
            summary_line2 = error_lines[1][:150] if len(error_lines[1]) > 150 else error_lines[1]
        else:
            summary_line2 = "Check full error details below"
    
    # Escape HTML and format
    summary_line1 = escape(summary_line1)
    summary_line2 = escape(summary_line2)
    
    return f"<div style='color: #dc2626;'>{summary_line1}</div><div style='color: #991b1b; margin-top: 4px;'>{summary_line2}</div>"


def generate_dashboard_html(results: Dict, allure_data: Dict = None) -> str:
    """Generate the dashboard HTML"""
    if allure_data is None:
        allure_data = {}
    
    total = results.get('total', 0)
    passed = results.get('passed', 0)
    failed = results.get('failed', 0)
    skipped = results.get('skipped', 0)
    tests = results.get('tests', [])
    timestamp = results.get('timestamp')
    build_number = results.get('build_number', 'N/A')
    
    # Calculate pass rate
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    # Group tests by feature
    tests_by_feature = {}
    for test in tests:
        feature = test.feature
        if feature not in tests_by_feature:
            tests_by_feature[feature] = []
        tests_by_feature[feature].append(test)
    
    # Get failed tests
    failed_tests = [t for t in tests if t.status == 'failed']
    
    # Format timestamp
    timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S') if timestamp else 'N/A'
    
    # Load test run history
    history = load_test_run_history()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aziro Automation Results Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-attachment: fixed;
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(20px);
            padding: 30px 40px;
            border-radius: 20px;
            margin-bottom: 30px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            color: #718096;
            font-size: 1.1em;
            margin-bottom: 15px;
        }}
        
        .header .build-info {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            color: #4a5568;
            font-size: 0.95em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(20px);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 50px rgba(0, 0, 0, 0.15);
        }}
        
        .stat-card .label {{
            font-size: 0.9em;
            color: #718096;
            margin-bottom: 8px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .stat-card .value {{
            font-size: 2.5em;
            font-weight: 800;
            margin-bottom: 5px;
        }}
        
        .stat-card.passed .value {{
            color: #10b981;
        }}
        
        .stat-card.failed .value {{
            color: #ef4444;
        }}
        
        .stat-card.skipped .value {{
            color: #f59e0b;
        }}
        
        .stat-card.total .value {{
            color: #667eea;
        }}
        
        .stat-card .percentage {{
            font-size: 0.9em;
            color: #a0aec0;
            font-weight: 500;
        }}
        
        .section {{
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(20px);
            padding: 30px;
            border-radius: 20px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        
        .section h2 {{
            font-size: 1.8em;
            font-weight: 700;
            margin-bottom: 20px;
            color: #2d3748;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .history-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        .history-table th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .history-table td {{
            padding: 15px;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .history-table tr:hover {{
            background: #f7fafc;
        }}
        
        .history-table tr:last-child td {{
            border-bottom: none;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .status-badge.passed {{
            background: #d1fae5;
            color: #065f46;
        }}
        
        .status-badge.failed {{
            background: #fee2e2;
            color: #991b1b;
        }}
        
        .status-badge.partial {{
            background: #fef3c7;
            color: #92400e;
        }}
        
        .build-number {{
            font-family: 'Courier New', monospace;
            font-weight: 600;
            color: #667eea;
        }}
        
        .test-results-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        .test-results-table th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .test-results-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .test-results-table tr:hover {{
            background: #f7fafc;
        }}
        
        .test-results-table .status {{
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
        }}
        
        .test-results-table .status.passed {{
            color: #10b981;
        }}
        
        .test-results-table .status.failed {{
            color: #ef4444;
        }}
        
        .test-results-table .status.skipped {{
            color: #f59e0b;
        }}
        
        .failed-test-card {{
            background: #fef2f2;
            border-left: 4px solid #ef4444;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
        }}
        
        .failed-test-card h3 {{
            color: #991b1b;
            margin-bottom: 10px;
            font-size: 1.2em;
        }}
        
        .failed-test-card .summary {{
            color: #7f1d1d;
            margin: 10px 0;
            line-height: 1.6;
        }}
        
        .failed-test-card .details {{
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #fecaca;
        }}
        
        .failed-test-card .toggle-details {{
            background: #ef4444;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9em;
            margin-top: 10px;
        }}
        
        .failed-test-card .toggle-details:hover {{
            background: #dc2626;
        }}
        
        .error-details {{
            display: none;
            background: #1f2937;
            color: #f3f4f6;
            padding: 15px;
            border-radius: 5px;
            margin-top: 10px;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            white-space: pre-wrap;
            overflow-x: auto;
        }}
        
        .error-details.show {{
            display: block;
        }}
        
        .log-link {{
            display: inline-block;
            margin-top: 10px;
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            padding: 8px 16px;
            background: white;
            border-radius: 5px;
            border: 2px solid #667eea;
            transition: all 0.3s ease;
        }}
        
        .log-link:hover {{
            background: #667eea;
            color: white;
        }}
        
        .auto-refresh {{
            text-align: center;
            color: #718096;
            font-size: 0.9em;
            margin-top: 30px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Aziro Automation Results Dashboard</h1>
            <div class="subtitle">Comprehensive test execution results and analytics</div>
            <div class="build-info">
                <span><strong>Build:</strong> <span class="build-number">{build_number}</span></span>
                <span><strong>Product:</strong> {PRODUCT_NAME}</span>
                <span><strong>Last Updated:</strong> {timestamp_str}</span>
            </div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card total">
                <div class="label">Total Tests</div>
                <div class="value">{total}</div>
                <div class="percentage">100%</div>
            </div>
            <div class="stat-card passed">
                <div class="label">Passed</div>
                <div class="value">{passed}</div>
                <div class="percentage">{pass_rate:.1f}% pass rate</div>
            </div>
            <div class="stat-card failed">
                <div class="label">Failed</div>
                <div class="value">{failed}</div>
                <div class="percentage">{(failed/total*100) if total > 0 else 0:.1f}% failure rate</div>
            </div>
            <div class="stat-card skipped">
                <div class="label">Skipped</div>
                <div class="value">{skipped}</div>
                <div class="percentage">{(skipped/total*100) if total > 0 else 0:.1f}% skip rate</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Test Run History</h2>
            <p style="color: #718096; margin-bottom: 20px;">Previous 5 test runs for {PRODUCT_NAME}</p>
            <table class="history-table">
                <thead>
                    <tr>
                        <th>Build Number</th>
                        <th>Timestamp</th>
                        <th>Total</th>
                        <th>Passed</th>
                        <th>Failed</th>
                        <th>Skipped</th>
                        <th>Pass Rate</th>
                        <th>Duration</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    # Add history rows
    if history:
        for entry in history:
            entry_timestamp = entry.get('timestamp', '')
            try:
                if entry_timestamp:
                    dt = datetime.fromisoformat(entry_timestamp.replace('Z', '+00:00'))
                    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    formatted_time = 'N/A'
            except:
                formatted_time = entry_timestamp
            
            total_hist = entry.get('total', 0)
            passed_hist = entry.get('passed', 0)
            failed_hist = entry.get('failed', 0)
            skipped_hist = entry.get('skipped', 0)
            pass_rate_hist = entry.get('pass_rate', 0)
            duration_hist = entry.get('duration', 0)
            build_num = entry.get('build_number', 'N/A')
            
            # Determine status badge
            if failed_hist == 0:
                status_class = 'passed'
                status_text = 'All Passed'
            elif passed_hist == 0:
                status_class = 'failed'
                status_text = 'All Failed'
            else:
                status_class = 'partial'
                status_text = 'Partial'
            
            # Format duration
            if duration_hist >= 3600:
                duration_str = f"{int(duration_hist // 3600)}h {int((duration_hist % 3600) // 60)}m"
            elif duration_hist >= 60:
                duration_str = f"{int(duration_hist // 60)}m {int(duration_hist % 60)}s"
            else:
                duration_str = f"{duration_hist:.1f}s"
            
            html += f"""
                    <tr>
                        <td><span class="build-number">{build_num}</span></td>
                        <td>{formatted_time}</td>
                        <td><strong>{total_hist}</strong></td>
                        <td style="color: #10b981;"><strong>{passed_hist}</strong></td>
                        <td style="color: #ef4444;"><strong>{failed_hist}</strong></td>
                        <td style="color: #f59e0b;"><strong>{skipped_hist}</strong></td>
                        <td><strong>{pass_rate_hist}%</strong></td>
                        <td>{duration_str}</td>
                        <td><span class="status-badge {status_class}">{status_text}</span></td>
                    </tr>
"""
    else:
        html += """
                    <tr>
                        <td colspan="9" style="text-align: center; padding: 40px; color: #718096;">
                            No test run history available yet. Run tests to see history.
                        </td>
                    </tr>
"""
    
    html += """
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>📋 Test Results Table</h2>
            <table class="test-results-table">
                <thead>
                    <tr>
                        <th>Test Name</th>
                        <th>Feature</th>
                        <th>Status</th>
                        <th>Duration</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    # Add test results rows
    for test in tests:
        status_class = test.status
        duration_str = f"{test.duration:.2f}s" if test.duration else "N/A"
        html += f"""
                    <tr>
                        <td>{escape(test.name)}</td>
                        <td>{test.feature}</td>
                        <td class="status {status_class}">{status_class.upper()}</td>
                        <td>{duration_str}</td>
                    </tr>
"""
    
    html += """
                </tbody>
            </table>
        </div>
"""
    
    # Add failed tests section
    if failed_tests:
        failed_count = len(failed_tests)
        html += f"""
        <div class="section">
            <h2>❌ Failed Test Cases - Summary</h2>
            <p style="color: #718096; margin-bottom: 20px;">Total Failed: {failed_count}</p>
"""
        
        for i, test in enumerate(failed_tests, 1):
            summary = generate_2line_summary(test.error)
            log_link = ""
            if test.log_file and test.log_start_line:
                log_link = f'<a href="/log/{escape(test.name)}" class="log-link" target="_blank">📋 View Full Log</a>'
            
            html += f"""
            <div class="failed-test-card">
                <h3>{i}. {escape(test.name)}</h3>
                <div style="color: #718096; margin-bottom: 10px;">
                    <strong>Feature:</strong> {test.feature} | 
                    <strong>Duration:</strong> {test.duration:.2f}s
                </div>
                <div class="summary">
                    {summary}
                </div>
                {log_link}
                <button class="toggle-details" onclick="toggleDetails('error-{i}')">View Full Error Details</button>
                <div id="error-{i}" class="error-details">
{escape(test.error if test.error else "No error details available")}
                </div>
            </div>
"""
        
        html += """
        </div>
"""
    
    html += """
        <div class="auto-refresh">
            <p>🔄 Dashboard auto-refreshes every 30 seconds</p>
        </div>
    </div>
    
    <script>
        function toggleDetails(id) {
            const element = document.getElementById(id);
            element.classList.toggle('show');
            const button = element.previousElementSibling;
            if (element.classList.contains('show')) {
                button.textContent = 'Hide Error Details';
            } else {
                button.textContent = 'View Full Error Details';
            }
        }
        
        // Auto-refresh every 30 seconds
        setTimeout(function() {
            location.reload();
        }, 30000);
    </script>
</body>
</html>
"""
    
    return html


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for the dashboard server"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        # Handle log viewing endpoint
        if parsed_path.path.startswith('/log/'):
            test_name = parsed_path.path.replace('/log/', '').replace('%3A%3A', '::')
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            results = parse_html_report()
            tests = results.get('tests', [])
            latest_log_file = find_latest_log_file()
            
            # Find the test
            test = None
            for t in tests:
                if t.name == test_name or test_name in t.name:
                    test = t
                    break
            
            if test and test.log_file and test.log_start_line:
                log_content = get_test_log_content(
                    LOGS_DIR / test.log_file,
                    test.log_start_line,
                    test.log_end_line
                )
            else:
                log_content = "Log content not available for this test."
            
            log_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Test Log: {escape(test_name)}</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: #1a1a1a;
            color: #e0e0e0;
            padding: 20px;
            margin: 0;
        }}
        pre {{
            background: #0d1117;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            border: 1px solid #30363d;
        }}
        .header {{
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #30363d;
        }}
        .back-link {{
            color: #58a6ff;
            text-decoration: none;
            margin-bottom: 10px;
            display: inline-block;
        }}
    </style>
</head>
<body>
    <div class="header">
        <a href="/" class="back-link">← Back to Dashboard</a>
        <h2 style="color: #58a6ff;">Test Log: {escape(test_name)}</h2>
    </div>
    <pre>{escape(log_content)}</pre>
</body>
</html>
"""
            self.wfile.write(log_html.encode('utf-8'))
            return
        
        # Handle main dashboard
        if parsed_path.path == '/' or parsed_path.path == '':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            results = parse_html_report()
            allure_data = parse_allure_results()
            html = generate_dashboard_html(results, allure_data)
            
            self.wfile.write(html.encode('utf-8'))
        else:
            super().do_GET()


def main():
    """Main function to start the dashboard server"""
    # Ensure reports directory exists
    # Change to script directory to ensure correct paths
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    # Log the working directory for debugging
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"📁 Script location: {script_dir}")
    print(f"📁 Reports directory: {REPORTS_DIR.absolute()}")
    print(f"📁 Logs directory: {LOGS_DIR.absolute()}")
    
    # Ensure reports directory exists
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Verify report file exists
    if not HTML_REPORT.exists():
        print(f"⚠️  WARNING: HTML report not found at {HTML_REPORT.absolute()}")
        print(f"   Reports directory contents: {list(REPORTS_DIR.glob('*')) if REPORTS_DIR.exists() else 'Directory does not exist'}")
    else:
        print(f"✅ HTML report found: {HTML_REPORT.absolute()}")
    
    handler = DashboardHandler
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"🌐 Dashboard URL: http://localhost:{PORT}")
        print(f"\n💡 The dashboard will auto-refresh every 30 seconds")
        print(f"💡 Run tests with './run_tests.sh' to generate new results")
        print(f"\n{'='*80}\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Server stopped by user")


if __name__ == "__main__":
    main()
