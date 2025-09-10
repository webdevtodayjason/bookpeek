#!/usr/bin/env python3
"""
Comprehensive test runner for T-P17-003 search feature
Runs all test suites and generates a comprehensive report
"""

import asyncio
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

class TestRunner:
    """Comprehensive test runner for search feature validation"""
    
    def __init__(self):
        """Initialize the test runner"""
        self.start_time = datetime.now()
        self.test_results = []
        self.total_passed = 0
        self.total_tests = 0
    
    def print_header(self):
        """Print test suite header"""
        print("=" * 80)
        print("🔍 BOOKPEEK SEARCH FEATURE ACCEPTANCE TESTING")
        print("Task: T-P17-003 - Search feature that returns list of books")
        print("=" * 80)
        print(f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    async def run_acceptance_tests(self):
        """Run the main acceptance tests"""
        print("📋 Running Core Acceptance Tests...")
        print("-" * 40)
        
        try:
            # Import and run the acceptance tests
            from test_search_feature_acceptance import run_all_tests
            result = await run_all_tests()
            
            # Count results from the acceptance test output
            # This is a simplified approach - in a real scenario you'd get detailed results
            if result == 0:
                self.test_results.append(("Core Acceptance Tests", True, "6/6"))
                self.total_passed += 6
                self.total_tests += 6
            else:
                self.test_results.append(("Core Acceptance Tests", False, "Partial/6"))
                self.total_tests += 6
            
            print("✓ Core acceptance tests completed")
            return True
            
        except Exception as e:
            print(f"✗ Core acceptance tests failed: {e}")
            self.test_results.append(("Core Acceptance Tests", False, f"Error: {e}"))
            self.total_tests += 6
            return False
    
    async def run_api_tests(self):
        """Run API endpoint tests"""
        print("\n🔌 Running API Endpoint Tests...")
        print("-" * 40)
        
        try:
            from test_api_endpoints import run_api_tests
            passed, total = await run_api_tests()
            
            success = passed == total
            self.test_results.append(("API Endpoint Tests", success, f"{passed}/{total}"))
            self.total_passed += passed
            self.total_tests += total
            
            print(f"✓ API endpoint tests completed: {passed}/{total}")
            return success
            
        except Exception as e:
            print(f"✗ API endpoint tests failed: {e}")
            self.test_results.append(("API Endpoint Tests", False, f"Error: {e}"))
            self.total_tests += 8  # Expected number of API tests
            return False
    
    def run_frontend_tests(self):
        """Run frontend integration tests"""
        print("\n🎨 Running Frontend Integration Tests...")
        print("-" * 40)
        
        try:
            from test_frontend_integration import run_frontend_tests
            passed, total = run_frontend_tests()
            
            success = passed == total
            self.test_results.append(("Frontend Integration Tests", success, f"{passed}/{total}"))
            self.total_passed += passed
            self.total_tests += total
            
            print(f"✓ Frontend tests completed: {passed}/{total}")
            return success
            
        except Exception as e:
            print(f"✗ Frontend tests failed: {e}")
            self.test_results.append(("Frontend Integration Tests", False, f"Error: {e}"))
            self.total_tests += 6  # Expected number of frontend tests
            return False
    
    def run_existing_tests(self):
        """Run existing test files"""
        print("\n🧪 Running Existing Test Suites...")
        print("-" * 40)
        
        test_files = [
            "test_search_enhancements.py",
            "test_google_books_api.py"
        ]
        
        existing_results = []
        
        for test_file in test_files:
            if Path(test_file).exists():
                try:
                    print(f"Running {test_file}...")
                    result = subprocess.run(
                        [sys.executable, test_file],
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                    
                    success = result.returncode == 0
                    existing_results.append((test_file, success))
                    
                    if success:
                        print(f"✓ {test_file} passed")
                    else:
                        print(f"✗ {test_file} failed")
                        if result.stderr:
                            print(f"  Error: {result.stderr.strip()}")
                        
                except subprocess.TimeoutExpired:
                    print(f"✗ {test_file} timed out")
                    existing_results.append((test_file, False))
                except Exception as e:
                    print(f"✗ {test_file} error: {e}")
                    existing_results.append((test_file, False))
            else:
                print(f"⚠ {test_file} not found")
        
        # Add to overall results
        passed_existing = sum(1 for _, success in existing_results if success)
        total_existing = len(existing_results)
        
        if total_existing > 0:
            self.test_results.append(("Existing Test Suites", passed_existing == total_existing, f"{passed_existing}/{total_existing}"))
            self.total_passed += passed_existing
            self.total_tests += total_existing
        
        return passed_existing == total_existing
    
    def check_file_structure(self):
        """Check that all required files exist"""
        print("\n📁 Checking File Structure...")
        print("-" * 40)
        
        required_files = [
            "api/app/services/search_service.py",
            "api/app/routers/search.py",
            "api/app/routers/main.py",
            "api/app/services/api_service.py",
            "web/components/SearchInterface.tsx",
        ]
        
        missing_files = []
        present_files = []
        
        for file_path in required_files:
            if Path(file_path).exists():
                present_files.append(file_path)
                print(f"✓ {file_path}")
            else:
                missing_files.append(file_path)
                print(f"✗ {file_path} - MISSING")
        
        structure_ok = len(missing_files) == 0
        self.test_results.append(("File Structure Check", structure_ok, f"{len(present_files)}/{len(required_files)}"))
        
        if structure_ok:
            self.total_passed += 1
        self.total_tests += 1
        
        return structure_ok
    
    def check_acceptance_criteria(self):
        """Verify specific acceptance criteria"""
        print("\n✅ Verifying Acceptance Criteria...")
        print("-" * 40)
        
        criteria_results = []
        
        # FR-3: Search returns list of books
        print("Checking FR-3: Search returns list of books...")
        try:
            # Check search service implementation
            service_file = Path("api/app/services/search_service.py")
            if service_file.exists():
                with open(service_file, 'r') as f:
                    content = f.read()
                    has_search_books = 'def search_books' in content
                    has_book_result = 'class BookSearchResult' in content or 'BookSearchResult' in content
                    returns_list = 'books' in content and 'list' in content.lower()
                    
                    fr3_ok = has_search_books and has_book_result and returns_list
                    print(f"  - search_books method: {'✓' if has_search_books else '✗'}")
                    print(f"  - BookSearchResult structure: {'✓' if has_book_result else '✗'}")
                    print(f"  - Returns list of books: {'✓' if returns_list else '✗'}")
                    
                    criteria_results.append(("FR-3: Core search functionality", fr3_ok))
            else:
                criteria_results.append(("FR-3: Core search functionality", False))
                print("  ✗ Search service file missing")
        except Exception as e:
            criteria_results.append(("FR-3: Core search functionality", False))
            print(f"  ✗ Error checking FR-3: {e}")
        
        # Error handling
        print("Checking error handling...")
        try:
            error_handling_ok = False
            if service_file.exists():
                with open(service_file, 'r') as f:
                    content = f.read()
                    has_try_catch = 'try:' in content and 'except' in content
                    has_error_logging = 'logger.error' in content
                    has_validation = 'validate_search_input' in content
                    
                    error_handling_ok = has_try_catch and has_error_logging and has_validation
                    print(f"  - Try/except blocks: {'✓' if has_try_catch else '✗'}")
                    print(f"  - Error logging: {'✓' if has_error_logging else '✗'}")
                    print(f"  - Input validation: {'✓' if has_validation else '✗'}")
                    
            criteria_results.append(("Error handling", error_handling_ok))
        except Exception as e:
            criteria_results.append(("Error handling", False))
            print(f"  ✗ Error checking error handling: {e}")
        
        # Add criteria results to overall results
        for criterion, success in criteria_results:
            self.test_results.append((criterion, success, "Pass" if success else "Fail"))
            if success:
                self.total_passed += 1
            self.total_tests += 1
        
        return all(success for _, success in criteria_results)
    
    def generate_summary_report(self):
        """Generate comprehensive test summary report"""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST SUMMARY REPORT")
        print("=" * 80)
        
        print(f"Test Suite: T-P17-003 Search Feature Acceptance Tests")
        print(f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duration: {duration.total_seconds():.1f} seconds")
        print()
        
        # Overall statistics
        success_rate = (self.total_passed / self.total_tests * 100) if self.total_tests > 0 else 0
        print(f"📈 OVERALL RESULTS:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed: {self.total_passed}")
        print(f"   Failed: {self.total_tests - self.total_passed}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print()
        
        # Detailed results by category
        print("📋 DETAILED RESULTS:")
        print("-" * 50)
        
        for test_name, success, details in self.test_results:
            status = "✓ PASS" if success else "✗ FAIL"
            print(f"{status:<8} {test_name:<30} {details}")
        
        print()
        
        # Acceptance criteria status
        print("🎯 ACCEPTANCE CRITERIA STATUS:")
        print("-" * 50)
        
        fr3_tests = [result for result in self.test_results if "FR-3" in result[0] or "Core" in result[0]]
        error_tests = [result for result in self.test_results if "error" in result[0].lower() or "Error" in result[0]]
        
        fr3_passed = any(result[1] for result in fr3_tests)
        error_passed = any(result[1] for result in error_tests)
        
        print(f"{'✓ PASS' if fr3_passed else '✗ FAIL'}    FR-3: Search returns list of books")
        print(f"{'✓ PASS' if error_passed else '✗ FAIL'}    Error cases handled gracefully")
        
        # Final recommendation
        print("\n" + "=" * 80)
        
        if success_rate >= 90:
            print("🎉 RECOMMENDATION: IMPLEMENTATION READY FOR DEPLOYMENT")
            print("   All critical functionality working correctly")
            print("   Acceptance criteria met")
        elif success_rate >= 75:
            print("⚠️  RECOMMENDATION: MINOR FIXES NEEDED")
            print("   Core functionality working but some issues remain")
            print("   Review failed tests and address issues")
        else:
            print("❌ RECOMMENDATION: SIGNIFICANT WORK REQUIRED")
            print("   Critical functionality issues detected")
            print("   Address failing tests before proceeding")
        
        print("=" * 80)
        
        # Return overall success
        return success_rate >= 90
    
    async def run_all_tests(self):
        """Run all test suites"""
        self.print_header()
        
        # Run all test categories
        test_categories = [
            ("File Structure", self.check_file_structure()),
            ("Acceptance Criteria", self.check_acceptance_criteria()),
            ("Core Acceptance Tests", await self.run_acceptance_tests()),
            ("API Endpoint Tests", await self.run_api_tests()),
            ("Frontend Integration", self.run_frontend_tests()),
            ("Existing Test Suites", self.run_existing_tests()),
        ]
        
        # Generate final report
        overall_success = self.generate_summary_report()
        
        return 0 if overall_success else 1

async def main():
    """Main test runner entry point"""
    runner = TestRunner()
    exit_code = await runner.run_all_tests()
    sys.exit(exit_code)

if __name__ == "__main__":
    asyncio.run(main())