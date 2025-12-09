#!/usr/bin/env python3
"""
Live Proctoring Backend - Comprehensive Test Script
Run this after starting the server with:
  cd backend && python -m uvicorn app.main:app --reload
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def colored(text, color):
    colors = {
        "green": "\033[92m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "end": "\033[0m"
    }
    return f"{colors.get(color, '')}{text}{colors['end']}"

def test_api():
    print(colored(f"\n{'='*60}", "blue"))
    print(colored("Live Proctoring Backend - Test Suite", "blue"))
    print(colored("="*60, "blue"))
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Health Check
    print(colored("\n1. Health Check", "yellow"))
    try:
        resp = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if resp.status_code == 200:
            print(colored("✅ PASS", "green"))
            print(json.dumps(resp.json(), indent=2))
            tests_passed += 1
        else:
            print(colored(f"❌ FAIL: {resp.status_code}", "red"))
            tests_failed += 1
    except Exception as e:
        print(colored(f"❌ FAIL: {e}", "red"))
        tests_failed += 1
    
    # Test 2: Start Session
    print(colored("\n2. Start Session", "yellow"))
    try:
        resp = requests.post(f"{BASE_URL}/api/session/start?client_id=test_user_1", timeout=5)
        if resp.status_code == 200:
            print(colored("✅ PASS", "green"))
            print(json.dumps(resp.json(), indent=2))
            tests_passed += 1
        else:
            print(colored(f"❌ FAIL: {resp.status_code}", "red"))
            tests_failed += 1
    except Exception as e:
        print(colored(f"❌ FAIL: {e}", "red"))
        tests_failed += 1
    
    # Test 3: Get Violations
    print(colored("\n3. Get Violations", "yellow"))
    try:
        resp = requests.get(f"{BASE_URL}/api/violations/test_user_1", timeout=5)
        if resp.status_code == 200:
            print(colored("✅ PASS", "green"))
            print(json.dumps(resp.json(), indent=2))
            tests_passed += 1
        else:
            print(colored(f"❌ FAIL: {resp.status_code}", "red"))
            tests_failed += 1
    except Exception as e:
        print(colored(f"❌ FAIL: {e}", "red"))
        tests_failed += 1
    
    # Test 4: End Session
    print(colored("\n4. End Session", "yellow"))
    try:
        resp = requests.post(f"{BASE_URL}/api/session/end?client_id=test_user_1", timeout=5)
        if resp.status_code == 200:
            print(colored("✅ PASS", "green"))
            print(json.dumps(resp.json(), indent=2))
            tests_passed += 1
        else:
            print(colored(f"❌ FAIL: {resp.status_code}", "red"))
            tests_failed += 1
    except Exception as e:
        print(colored(f"❌ FAIL: {e}", "red"))
        tests_failed += 1
    
    # Test 5: Get Report
    print(colored("\n5. Get Report", "yellow"))
    try:
        resp = requests.get(f"{BASE_URL}/api/report/test_user_1", timeout=5)
        if resp.status_code == 200:
            print(colored("✅ PASS", "green"))
            print(json.dumps(resp.json(), indent=2))
            tests_passed += 1
        else:
            print(colored(f"❌ FAIL: {resp.status_code}", "red"))
            tests_failed += 1
    except Exception as e:
        print(colored(f"❌ FAIL: {e}", "red"))
        tests_failed += 1
    
    # Summary
    print(colored(f"\n{'='*60}", "blue"))
    print(colored("Test Summary", "blue"))
    print(colored("="*60, "blue"))
    print(colored(f"✅ Passed: {tests_passed}", "green"))
    print(colored(f"❌ Failed: {tests_failed}", "red"))
    print(colored(f"Total: {tests_passed + tests_failed}\n", "yellow"))
    
    return 0 if tests_failed == 0 else 1

if __name__ == "__main__":
    exit_code = test_api()
    sys.exit(exit_code)
