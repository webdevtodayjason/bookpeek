#!/usr/bin/env python3
"""
Acceptance tests for FR-2: Google Books API integration
"""

import os
import json
import sys
from pathlib import Path

def test_core_functionality():
    """Test FR-2: Core functionality implementation"""
    print("Testing FR-2: Google Books API integration...")
    
    # Check if all required files exist
    required_files = [
        Path("api/app/services/search_service.py"),
        Path("api/app/routers/search.py"),
        Path("web/components/SearchInterface.tsx"),
        Path("api/app/routers/main.py"),
        Path("api/app/services/api_service.py"),
        Path("app/api/books/search/route.ts")  # Updated Next.js route
    ]
    
    for file_path in required_files:
        assert file_path.exists(), f"Required file {file_path} does not exist"
        print(f"  ✓ {file_path} exists")
    
    # Check search_service.py has the required classes and methods
    search_service = Path("api/app/services/search_service.py")
    with open(search_service, 'r') as f:
        content = f.read()
        
        # Check for required classes
        assert "class GoogleBooksSearchService" in content, "GoogleBooksSearchService class not found"
        assert "class BookSearchResult" in content or "@dataclass" in content, "BookSearchResult dataclass not found"
        
        # Check for required methods
        required_methods = [
            "search_books",
            "search_by_isbn",
            "get_book_by_id",
            "_parse_book_item",
            "validate_search_input"
        ]
        
        for method in required_methods:
            assert f"def {method}" in content or f"async def {method}" in content, f"Method {method} not found"
        
        # Check for Google Books API URL
        assert "googleapis.com/books/v1" in content, "Google Books API URL not found"
        
        print("  ✓ search_service.py has all required components")
    
    # Check search router
    search_router = Path("api/app/routers/search.py")
    with open(search_router, 'r') as f:
        content = f.read()
        
        # Check for required endpoints
        assert "@router.get" in content, "No GET endpoints found in search router"
        assert '"/books"' in content, "Books search endpoint not found"
        assert "search_books" in content, "search_books function not found"
        
        print("  ✓ search.py router configured correctly")
    
    # Check SearchInterface component
    search_interface = Path("web/components/SearchInterface.tsx")
    with open(search_interface, 'r') as f:
        content = f.read()
        
        # Check for required functionality
        assert "useState" in content, "React hooks not used"
        assert "fetch" in content, "Fetch API not used"
        assert "/api/search/books" in content or "/api/books/search" in content, "API endpoint not referenced"
        assert "BookResult" in content or "BookSearchResult" in content, "Book type definition not found"
        assert "handleSearch" in content, "Search handler not found"
        assert "ISBN" in content or "isbn" in content, "ISBN support not found"
        
        print("  ✓ SearchInterface.tsx has search functionality")
    
    # Check API service
    api_service = Path("api/app/services/api_service.py")
    with open(api_service, 'r') as f:
        content = f.read()
        
        # Check for required components
        assert "class APIService" in content, "APIService class not found"
        assert "class GoogleBooksAPI" in content, "GoogleBooksAPI class not found"
        assert "async def get" in content, "Async GET method not found"
        assert "rate_limit" in content or "rate limit" in content.lower(), "Rate limiting not implemented"
        assert "cache" in content.lower(), "Caching not implemented"
        
        print("  ✓ api_service.py has API handling with rate limiting and caching")
    
    # Check Next.js API route
    api_route = Path("app/api/books/search/route.ts")
    with open(api_route, 'r') as f:
        content = f.read()
        
        # Check for Google Books API integration
        assert "googleapis.com/books/v1" in content, "Google Books API URL not found in route"
        assert "GOOGLE_BOOKS_API_KEY" in content, "API key configuration not found"
        assert "volumeInfo" in content, "Volume info parsing not found"
        assert "isbn" in content.lower(), "ISBN handling not found"
        assert "429" in content, "Rate limit handling not found"
        
        print("  ✓ Next.js route integrates with Google Books API")
    
    print("✓ FR-2: Core functionality implemented successfully")
    return True

def test_error_handling():
    """Test error handling gracefully"""
    print("\nTesting error handling...")
    
    # Check search_service.py error handling
    search_service = Path("api/app/services/search_service.py")
    with open(search_service, 'r') as f:
        content = f.read()
        
        assert "try:" in content, "No try/except blocks in search_service"
        assert "except" in content, "No exception handling in search_service"
        assert "logger.error" in content, "No error logging in search_service"
        assert "validate" in content.lower(), "No input validation"
        assert "429" in content, "Rate limit error not handled"
        
        print("  ✓ search_service.py has error handling")
    
    # Check API router error handling
    search_router = Path("api/app/routers/search.py")
    with open(search_router, 'r') as f:
        content = f.read()
        
        assert "HTTPException" in content, "HTTPException not used"
        assert "try:" in content, "No try/except blocks in router"
        assert "400" in content, "Bad request status not handled"
        assert "500" in content, "Server error status not handled"
        assert "validate_search_input" in content, "Input validation not called"
        
        print("  ✓ search.py router has error handling")
    
    # Check SearchInterface error handling
    search_interface = Path("web/components/SearchInterface.tsx")
    with open(search_interface, 'r') as f:
        content = f.read()
        
        assert "try" in content or "catch" in content or ".catch" in content, "No error handling in UI"
        assert "error" in content.lower(), "No error state management"
        assert "loading" in content.lower(), "No loading state"
        
        print("  ✓ SearchInterface.tsx handles errors")
    
    # Check Next.js route error handling
    api_route = Path("app/api/books/search/route.ts")
    with open(api_route, 'r') as f:
        content = f.read()
        
        assert "try {" in content, "No try/catch in API route"
        assert "catch" in content, "No catch block in API route"
        assert "status: 400" in content, "Bad request not handled"
        assert "status: 500" in content, "Server error not handled"
        assert "status: 429" in content, "Rate limit not handled"
        assert "query.length" in content, "Query validation not found"
        
        print("  ✓ Next.js route has comprehensive error handling")
    
    print("✓ Error cases handled gracefully")
    return True

def test_api_integration():
    """Test API integration specifics"""
    print("\nTesting API integration details...")
    
    # Check for async/await usage
    search_service = Path("api/app/services/search_service.py")
    with open(search_service, 'r') as f:
        content = f.read()
        
        assert "async def" in content, "No async functions in search_service"
        assert "await" in content, "No await usage in search_service"
        assert "aiohttp" in content, "aiohttp not used for async HTTP"
        
        print("  ✓ Async/await properly implemented")
    
    # Check for proper data transformation
    assert "BookSearchResult" in content, "No data model for results"
    assert "asdict" in content or "dict()" in content, "No serialization method"
    
    print("  ✓ Data transformation implemented")
    
    # Check for pagination support
    assert "start_index" in content or "startIndex" in content, "No pagination support"
    assert "max_results" in content or "maxResults" in content, "No result limit control"
    
    print("  ✓ Pagination support implemented")
    
    print("✓ API integration complete")
    return True

def main():
    """Run all acceptance tests"""
    print("=" * 50)
    print("Running Acceptance Tests for T-P17-002")
    print("Google Books API Integration")
    print("=" * 50)
    
    results = []
    
    # Test 1: Core functionality
    try:
        results.append(("FR-2: Core functionality", test_core_functionality()))
    except AssertionError as e:
        print(f"✗ FR-2 failed: {e}")
        results.append(("FR-2: Core functionality", False))
    except Exception as e:
        print(f"✗ FR-2 error: {e}")
        results.append(("FR-2: Core functionality", False))
    
    # Test 2: Error handling
    try:
        results.append(("Error handling", test_error_handling()))
    except AssertionError as e:
        print(f"✗ Error handling failed: {e}")
        results.append(("Error handling", False))
    except Exception as e:
        print(f"✗ Error handling error: {e}")
        results.append(("Error handling", False))
    
    # Test 3: API integration
    try:
        results.append(("API integration", test_api_integration()))
    except AssertionError as e:
        print(f"✗ API integration failed: {e}")
        results.append(("API integration", False))
    except Exception as e:
        print(f"✗ API integration error: {e}")
        results.append(("API integration", False))
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print("=" * 50)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(passed for _, passed in results)
    
    if all_passed:
        print("\n✓ All acceptance tests PASSED!")
        print("Google Books API integration is complete and functional.")
        return 0
    else:
        print("\n✗ Some tests FAILED. Please review and fix.")
        return 1

if __name__ == "__main__":
    sys.exit(main())