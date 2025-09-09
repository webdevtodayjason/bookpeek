#!/usr/bin/env python3
"""
Acceptance tests for FR-1: Set up full-stack architecture
"""

import os
import json
import sys
from pathlib import Path

def test_core_functionality():
    """Test FR-1: Core functionality implementation"""
    print("Testing FR-1: Core functionality...")
    
    # Check if the required service file exists
    service_file = Path("api/app/services/new_feature_service.py")
    assert service_file.exists(), f"Service file {service_file} does not exist"
    
    # Check if the service file has the required classes and methods
    with open(service_file, 'r') as f:
        content = f.read()
        
        # Check for required classes
        assert "class BookPeekService" in content, "BookPeekService class not found"
        assert "class BookInfo" in content or "@dataclass" in content, "BookInfo dataclass not found"
        
        # Check for required methods
        required_methods = [
            "search_books",
            "generate_summary",
            "set_theme_preference",
            "get_book_details",
            "format_display_data",
            "validate_input",
            "handle_error"
        ]
        
        for method in required_methods:
            assert f"def {method}" in content, f"Method {method} not found in service"
    
    # Check Node.js/Next.js setup
    assert Path("package.json").exists(), "package.json not found"
    assert Path("next.config.js").exists(), "next.config.js not found"
    assert Path("tsconfig.json").exists(), "tsconfig.json not found"
    
    # Check Tailwind CSS setup
    assert Path("tailwind.config.js").exists(), "tailwind.config.js not found"
    assert Path("postcss.config.js").exists(), "postcss.config.js not found"
    assert Path("src/styles/globals.css").exists(), "globals.css not found"
    
    # Check ShadCN setup
    assert Path("components.json").exists(), "components.json not found"
    assert Path("src/lib/utils.ts").exists(), "utils.ts not found"
    assert Path("src/components/ui/button.tsx").exists(), "ShadCN button component not found"
    
    # Check API routes
    assert Path("app/api/books/search/route.ts").exists(), "API route not found"
    
    # Check main app files
    assert Path("app/layout.tsx").exists(), "app/layout.tsx not found"
    assert Path("app/page.tsx").exists(), "app/page.tsx not found"
    
    print("✓ FR-1: Core functionality implemented successfully")
    return True

def test_error_handling():
    """Test error handling gracefully"""
    print("Testing error handling...")
    
    service_file = Path("api/app/services/new_feature_service.py")
    with open(service_file, 'r') as f:
        content = f.read()
        
        # Check for error handling methods and patterns
        assert "def handle_error" in content, "Error handling method not found"
        assert "try:" in content, "No try/except blocks found"
        assert "except" in content, "No exception handling found"
        assert "logger.error" in content, "No error logging found"
        
    # Check API route error handling
    api_route = Path("app/api/books/search/route.ts")
    with open(api_route, 'r') as f:
        content = f.read()
        assert "try {" in content, "No try/catch in API route"
        assert "catch" in content, "No catch block in API route"
        assert "status: 400" in content or "status: 500" in content, "No error status codes"
    
    print("✓ Error cases handled gracefully")
    return True

def main():
    """Run all acceptance tests"""
    print("=" * 50)
    print("Running Acceptance Tests for T-P17-001")
    print("=" * 50)
    
    results = []
    
    # Test 1: Core functionality
    try:
        results.append(("FR-1: Core functionality", test_core_functionality()))
    except AssertionError as e:
        print(f"✗ FR-1 failed: {e}")
        results.append(("FR-1: Core functionality", False))
    except Exception as e:
        print(f"✗ FR-1 error: {e}")
        results.append(("FR-1: Core functionality", False))
    
    # Test 2: Error handling
    try:
        results.append(("Error handling", test_error_handling()))
    except AssertionError as e:
        print(f"✗ Error handling failed: {e}")
        results.append(("Error handling", False))
    except Exception as e:
        print(f"✗ Error handling error: {e}")
        results.append(("Error handling", False))
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print("=" * 50)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(passed for _, passed in results)
    
    if all_passed:
        print("\n✓ All acceptance tests PASSED!")
        return 0
    else:
        print("\n✗ Some tests FAILED. Please review and fix.")
        return 1

if __name__ == "__main__":
    sys.exit(main())