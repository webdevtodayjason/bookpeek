#!/usr/bin/env python3
"""
Frontend integration tests for search functionality
Tests that the frontend components properly integrate with the API
"""

import json
import sys
from pathlib import Path

def test_search_interface_component():
    """Test SearchInterface component implementation"""
    print("Testing SearchInterface component...")
    
    try:
        # Read the SearchInterface component
        component_path = Path("web/components/SearchInterface.tsx")
        if not component_path.exists():
            print(f"✗ SearchInterface component not found at {component_path}")
            return False
        
        with open(component_path, 'r') as f:
            content = f.read()
        
        # Check for required functionality
        required_features = [
            'useState',  # State management
            'useCallback',  # Performance optimization
            'useEffect',  # Side effects
            'handleSearch',  # Search handler
            'SearchResponse',  # Type definition
            'BookResult',  # Type definition
            'fetch(',  # API calls
            'api/search/books',  # API endpoint
            'loading',  # Loading state
            'error',  # Error state
            'searchResults',  # Results state
            'searchQuery',  # Query state
            'ISBN',  # ISBN support
            'Advanced Search',  # Advanced search UI
            'pagination',  # Pagination support
        ]
        
        missing_features = []
        for feature in required_features:
            if feature not in content:
                missing_features.append(feature)
        
        if missing_features:
            print(f"✗ Missing features in SearchInterface: {missing_features}")
            return False
        
        # Check for advanced search features
        advanced_features = [
            'advancedFilters',
            'showAdvanced',
            'author:',
            'title:',
            'publisher:',
            'category:',
        ]
        
        missing_advanced = []
        for feature in advanced_features:
            if feature not in content:
                missing_advanced.append(feature)
        
        if missing_advanced:
            print(f"✗ Missing advanced features: {missing_advanced}")
            return False
        
        # Check error handling
        error_handling_patterns = [
            'catch (',
            'setError',
            'error &&',
            'err instanceof Error',
        ]
        
        for pattern in error_handling_patterns:
            if pattern not in content:
                print(f"✗ Missing error handling pattern: {pattern}")
                return False
        
        # Check for proper TypeScript types
        typescript_patterns = [
            'interface BookResult',
            'interface SearchResponse',
            'React.FormEvent',
            'React.KeyboardEvent',
        ]
        
        for pattern in typescript_patterns:
            if pattern not in content:
                print(f"✗ Missing TypeScript pattern: {pattern}")
                return False
        
        print("✓ SearchInterface component has all required features")
        return True
        
    except Exception as e:
        print(f"✗ SearchInterface test failed: {e}")
        return False

def test_search_api_integration():
    """Test that frontend properly calls search API endpoints"""
    print("Testing search API integration...")
    
    try:
        component_path = Path("web/components/SearchInterface.tsx")
        with open(component_path, 'r') as f:
            content = f.read()
        
        # Check for all expected API calls
        expected_endpoints = [
            '/api/search/books/isbn/',  # ISBN search
            '/api/search/books/advanced',  # Advanced search
            '/api/search/books?',  # General search
        ]
        
        for endpoint in expected_endpoints:
            if endpoint not in content:
                print(f"✗ Missing API endpoint: {endpoint}")
                return False
        
        # Check for proper query parameter handling
        query_params = [
            'URLSearchParams',
            'max_results',
            'start_index',
            'order_by',
        ]
        
        for param in query_params:
            if param not in content:
                print(f"✗ Missing query parameter handling: {param}")
                return False
        
        # Check for proper response handling
        response_handling = [
            'response.ok',
            'response.json()',
            'data.success',
            'data.books',
            'data.error',
        ]
        
        for handler in response_handling:
            if handler not in content:
                print(f"✗ Missing response handling: {handler}")
                return False
        
        print("✓ Search API integration implemented correctly")
        return True
        
    except Exception as e:
        print(f"✗ API integration test failed: {e}")
        return False

def test_search_state_management():
    """Test proper state management in search component"""
    print("Testing search state management...")
    
    try:
        component_path = Path("web/components/SearchInterface.tsx")
        with open(component_path, 'r') as f:
            content = f.read()
        
        # Check for all required state variables
        state_variables = [
            'searchQuery',
            'searchResults',
            'loading',
            'error',
            'totalResults',
            'currentPage',
            'searchType',
            'showAdvanced',
            'advancedFilters',
            'sortOrder',
            'language',
        ]
        
        for var in state_variables:
            if f'[{var},' not in content and f'const {var} =' not in content:
                print(f"✗ Missing state variable: {var}")
                return False
        
        # Check for proper state updates
        state_setters = [
            'setSearchQuery',
            'setSearchResults',
            'setLoading',
            'setError',
            'setTotalResults',
            'setCurrentPage',
        ]
        
        for setter in state_setters:
            if setter not in content:
                print(f"✗ Missing state setter: {setter}")
                return False
        
        print("✓ Search state management implemented correctly")
        return True
        
    except Exception as e:
        print(f"✗ State management test failed: {e}")
        return False

def test_search_ui_components():
    """Test search UI components and user experience"""
    print("Testing search UI components...")
    
    try:
        component_path = Path("web/components/SearchInterface.tsx")
        with open(component_path, 'r') as f:
            content = f.read()
        
        # Check for essential UI elements
        ui_elements = [
            'Search',  # Search icon
            'Loader2',  # Loading icon
            'Book',  # Book icon
            'input',  # Search input
            'form',  # Search form
            'button',  # Search button
            'onSubmit',  # Form submission
            'placeholder=',  # Input placeholder
            'disabled={loading}',  # Disabled state
        ]
        
        for element in ui_elements:
            if element not in content:
                print(f"✗ Missing UI element: {element}")
                return False
        
        # Check for search result display
        result_display = [
            'searchResults.map',
            'book.title',
            'book.authors',
            'book.thumbnail',
            'book.description',
            'book.published_date',
            'book.categories',
        ]
        
        for display in result_display:
            if display not in content:
                print(f"✗ Missing result display: {display}")
                return False
        
        # Check for pagination
        pagination_elements = [
            'currentPage',
            'totalResults',
            'handleNextPage',
            'handlePrevPage',
            'Previous',
            'Next',
        ]
        
        for element in pagination_elements:
            if element not in content:
                print(f"✗ Missing pagination element: {element}")
                return False
        
        # Check for advanced search UI
        advanced_ui = [
            'Advanced Search',
            'advancedFilters.title',
            'advancedFilters.author',
            'advancedFilters.publisher',
            'advancedFilters.category',
            'Clear Filters',
        ]
        
        for ui in advanced_ui:
            if ui not in content:
                print(f"✗ Missing advanced search UI: {ui}")
                return False
        
        print("✓ Search UI components implemented correctly")
        return True
        
    except Exception as e:
        print(f"✗ UI components test failed: {e}")
        return False

def test_search_accessibility():
    """Test search component accessibility features"""
    print("Testing search accessibility...")
    
    try:
        component_path = Path("web/components/SearchInterface.tsx")
        with open(component_path, 'r') as f:
            content = f.read()
        
        # Check for accessibility features
        accessibility_features = [
            'aria-label',  # ARIA labels
            'alt=',  # Image alt text
            'disabled=',  # Proper disabled state
            'onKeyDown',  # Keyboard support
            'htmlFor',  # Label association (if present)
        ]
        
        found_features = []
        for feature in accessibility_features:
            if feature in content:
                found_features.append(feature)
        
        if len(found_features) < 3:  # At least 3 accessibility features
            print(f"✗ Insufficient accessibility features. Found: {found_features}")
            return False
        
        # Check for proper error messaging
        if 'error &&' not in content:
            print("✗ Missing error display")
            return False
        
        print("✓ Search accessibility features present")
        return True
        
    except Exception as e:
        print(f"✗ Accessibility test failed: {e}")
        return False

def test_search_performance():
    """Test search component performance optimizations"""
    print("Testing search performance optimizations...")
    
    try:
        component_path = Path("web/components/SearchInterface.tsx")
        with open(component_path, 'r') as f:
            content = f.read()
        
        # Check for performance optimizations
        performance_features = [
            'useCallback',  # Memoized callbacks
            'loading="lazy"',  # Lazy loading images
            'debounce' in content.lower() or 'throttle' in content.lower(),  # Debouncing/throttling
            'currentPage > 0' in content,  # Smart pagination
        ]
        
        found_optimizations = sum(1 for feature in performance_features if 
                                (isinstance(feature, bool) and feature) or 
                                (isinstance(feature, str) and feature in content))
        
        if found_optimizations < 2:  # At least 2 optimizations
            print(f"✗ Insufficient performance optimizations. Found: {found_optimizations}")
            return False
        
        print("✓ Search performance optimizations present")
        return True
        
    except Exception as e:
        print(f"✗ Performance test failed: {e}")
        return False

def run_frontend_tests():
    """Run all frontend integration tests"""
    print("=" * 70)
    print("Running Frontend Integration Tests")
    print("=" * 70)
    
    tests = [
        ("SearchInterface Component", test_search_interface_component()),
        ("Search API Integration", test_search_api_integration()),
        ("Search State Management", test_search_state_management()),
        ("Search UI Components", test_search_ui_components()),
        ("Search Accessibility", test_search_accessibility()),
        ("Search Performance", test_search_performance()),
    ]
    
    results = []
    
    for test_name, test_result in tests:
        try:
            results.append((test_name, test_result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 70)
    print("Frontend Integration Test Results:")
    print("=" * 70)
    
    passed_tests = 0
    total_tests = len(results)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
        if passed:
            passed_tests += 1
    
    print(f"\nTests Passed: {passed_tests}/{total_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    return passed_tests, total_tests

if __name__ == "__main__":
    passed, total = run_frontend_tests()
    exit_code = 0 if passed == total else 1
    sys.exit(exit_code)