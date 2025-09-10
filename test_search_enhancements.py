#!/usr/bin/env python3
"""
Test script to verify search functionality enhancements
"""

import asyncio
import sys
from pathlib import Path

# Add the project directory to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "api"))

async def test_search_service():
    """Test the enhanced search service functionality"""
    print("Testing enhanced search service...")
    
    try:
        from api.app.services.search_service import get_search_service
        
        service = get_search_service()
        
        # Test basic validation
        print("✓ Search service imported successfully")
        
        # Test input validation
        assert service.validate_search_input("python"), "Basic validation failed"
        assert not service.validate_search_input("a"), "Single character should fail"
        assert not service.validate_search_input(""), "Empty string should fail"
        print("✓ Input validation working correctly")
        
        # Test advanced search methods exist
        assert hasattr(service, 'search_by_author'), "search_by_author method missing"
        assert hasattr(service, 'search_by_title'), "search_by_title method missing"
        assert hasattr(service, 'search_by_category'), "search_by_category method missing"
        assert hasattr(service, 'search_by_publisher'), "search_by_publisher method missing"
        assert hasattr(service, 'advanced_search'), "advanced_search method missing"
        print("✓ All advanced search methods present")
        
        # Test that methods are callable
        async with service as svc:
            # Test with a simple query that should work
            result = await svc.search_books("python programming", max_results=5)
            
            # Check result structure
            assert isinstance(result, dict), "Result should be a dictionary"
            assert 'success' in result, "Result should have success key"
            assert 'books' in result, "Result should have books key"
            assert isinstance(result['books'], list), "Books should be a list"
            
            print(f"✓ Basic search returned {len(result.get('books', []))} results")
            
            if result.get('success') and result.get('books'):
                book = result['books'][0]
                required_fields = ['id', 'title', 'authors']
                for field in required_fields:
                    assert field in book, f"Book should have {field} field"
                print("✓ Book data structure is correct")
        
        print("✓ Enhanced search service tests passed!")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

def test_router_imports():
    """Test that router imports work correctly"""
    print("Testing router imports...")
    
    try:
        # Test router imports
        from api.app.routers.search import router
        from api.app.routers.main import router as main_router
        
        print("✓ Router imports successful")
        
        # Check that Path is properly imported
        import inspect
        from api.app.routers import search
        
        # Check if Path is in the module's globals
        assert 'Path' in dir(search), "Path should be imported in search router"
        
        print("✓ All required imports present in routers")
        return True
        
    except ImportError as e:
        print(f"✗ Router import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Router test failed: {e}")
        return False

def test_search_endpoints():
    """Test that search endpoints are properly defined"""
    print("Testing search endpoint definitions...")
    
    try:
        from api.app.routers.search import router
        
        # Get all routes from the router
        routes = [route.path for route in router.routes]
        
        expected_routes = [
            '/books',
            '/books/isbn/{isbn}', 
            '/books/{volume_id}',
            '/books/advanced',
            '/books/author/{author}'
        ]
        
        for expected_route in expected_routes:
            assert any(expected_route in route for route in routes), f"Route {expected_route} not found"
        
        print("✓ All expected search endpoints are defined")
        return True
        
    except Exception as e:
        print(f"✗ Endpoint test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing Search Functionality Enhancements")
    print("=" * 60)
    
    tests = [
        ("Search Service", test_search_service()),
        ("Router Imports", test_router_imports()),
        ("Search Endpoints", test_search_endpoints())
    ]
    
    results = []
    
    for test_name, test_coro in tests:
        try:
            if asyncio.iscoroutine(test_coro):
                result = await test_coro
            else:
                result = test_coro
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("Test Results Summary:")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(passed for _, passed in results)
    
    if all_passed:
        print("\n✓ All search enhancement tests PASSED!")
        return 0
    else:
        print("\n✗ Some tests FAILED. Please review and fix.")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))