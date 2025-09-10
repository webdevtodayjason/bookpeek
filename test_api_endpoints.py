#!/usr/bin/env python3
"""
API endpoint tests for search functionality
Tests actual FastAPI endpoints and request/response handling
"""

import asyncio
import sys
import json
from pathlib import Path
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from fastapi import FastAPI

# Add the project directory to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "api"))

class TestAPIEndpoints:
    """Test API endpoints for search functionality"""

    def setup_test_app(self):
        """Set up a test FastAPI app with search routes"""
        try:
            from api.app.routers.search import router as search_router
            from api.app.routers.main import router as main_router
            
            app = FastAPI(title="BookPeek Test API")
            app.include_router(main_router)
            
            return TestClient(app)
        except Exception as e:
            print(f"Error setting up test app: {e}")
            return None

    async def test_basic_search_endpoint(self):
        """Test the basic search endpoint /api/search/books"""
        print("Testing basic search endpoint...")
        
        try:
            client = self.setup_test_app()
            if not client:
                print("✗ Could not set up test client")
                return False
            
            # Mock the search service
            with patch('api.app.routers.search.get_search_service') as mock_get_service:
                mock_service = AsyncMock()
                mock_service.__aenter__.return_value = mock_service
                mock_service.__aexit__.return_value = None
                mock_service.validate_search_input.return_value = True
                mock_service.search_books.return_value = {
                    'success': True,
                    'total_items': 1,
                    'books': [{
                        'id': 'test_id',
                        'title': 'Test Book',
                        'authors': ['Test Author'],
                        'description': 'Test description',
                        'isbn': '1234567890',
                        'categories': ['Test'],
                        'published_date': '2023',
                        'publisher': 'Test Publisher'
                    }],
                    'query': 'test query',
                    'start_index': 0,
                    'max_results': 10
                }
                
                mock_get_service.return_value = mock_service
                
                # Test valid search
                response = client.get("/api/search/books?q=test%20query")
                
                assert response.status_code == 200, f"Expected 200, got {response.status_code}"
                
                data = response.json()
                assert data['success'] is True, "Response should indicate success"
                assert 'books' in data, "Response should contain books"
                assert len(data['books']) > 0, "Should return books"
                
                # Test query validation
                response = client.get("/api/search/books?q=x")  # Too short
                # This should still return 200 but with an error based on validation
                
                print("✓ Basic search endpoint working correctly")
                return True
                
        except Exception as e:
            print(f"✗ Basic search endpoint test failed: {e}")
            return False

    async def test_isbn_search_endpoint(self):
        """Test the ISBN search endpoint /api/search/books/isbn/{isbn}"""
        print("Testing ISBN search endpoint...")
        
        try:
            client = self.setup_test_app()
            if not client:
                return False
            
            # Mock the search service
            with patch('api.app.routers.search.get_search_service') as mock_get_service:
                mock_service = AsyncMock()
                mock_service.__aenter__.return_value = mock_service
                mock_service.__aexit__.return_value = None
                
                # Mock successful ISBN search
                from api.app.services.search_service import BookSearchResult
                mock_book = {
                    'id': 'isbn_test',
                    'title': 'ISBN Test Book',
                    'authors': ['ISBN Author'],
                    'isbn': '1234567890',
                    'description': 'Found by ISBN'
                }
                mock_service.search_by_isbn.return_value = mock_book
                
                mock_get_service.return_value = mock_service
                
                # Test valid ISBN search
                response = client.get("/api/search/books/isbn/1234567890")
                
                assert response.status_code == 200, f"Expected 200, got {response.status_code}"
                
                data = response.json()
                assert data['success'] is True, "ISBN search should succeed"
                assert 'book' in data, "Response should contain book"
                assert data['book']['isbn'] == '1234567890', "Should return correct book"
                
                # Test invalid ISBN
                response = client.get("/api/search/books/isbn/123")  # Too short
                assert response.status_code == 400, "Short ISBN should return 400"
                
                # Test not found
                mock_service.search_by_isbn.return_value = None
                response = client.get("/api/search/books/isbn/9999999999")
                assert response.status_code == 404, "Not found should return 404"
                
                print("✓ ISBN search endpoint working correctly")
                return True
                
        except Exception as e:
            print(f"✗ ISBN search endpoint test failed: {e}")
            return False

    async def test_advanced_search_endpoint(self):
        """Test the advanced search endpoint /api/search/books/advanced"""
        print("Testing advanced search endpoint...")
        
        try:
            client = self.setup_test_app()
            if not client:
                return False
            
            # Mock the search service
            with patch('api.app.routers.search.get_search_service') as mock_get_service:
                mock_service = AsyncMock()
                mock_service.__aenter__.return_value = mock_service
                mock_service.__aexit__.return_value = None
                mock_service.advanced_search.return_value = {
                    'success': True,
                    'total_items': 1,
                    'books': [{
                        'id': 'advanced_test',
                        'title': 'Advanced Test Book',
                        'authors': ['Advanced Author'],
                        'categories': ['Advanced']
                    }],
                    'query': 'advanced search'
                }
                
                mock_get_service.return_value = mock_service
                
                # Test advanced search with multiple parameters
                response = client.get(
                    "/api/search/books/advanced?title=Python&author=John&category=Programming"
                )
                
                assert response.status_code == 200, f"Expected 200, got {response.status_code}"
                
                data = response.json()
                assert data['success'] is True, "Advanced search should succeed"
                assert 'books' in data, "Response should contain books"
                
                # Test advanced search with no parameters
                response = client.get("/api/search/books/advanced")
                assert response.status_code == 400, "No parameters should return 400"
                
                print("✓ Advanced search endpoint working correctly")
                return True
                
        except Exception as e:
            print(f"✗ Advanced search endpoint test failed: {e}")
            return False

    async def test_author_search_endpoint(self):
        """Test the author search endpoint /api/search/books/author/{author}"""
        print("Testing author search endpoint...")
        
        try:
            client = self.setup_test_app()
            if not client:
                return False
            
            # Mock the search service
            with patch('api.app.routers.search.get_search_service') as mock_get_service:
                mock_service = AsyncMock()
                mock_service.__aenter__.return_value = mock_service
                mock_service.__aexit__.return_value = None
                mock_service.search_by_author.return_value = {
                    'success': True,
                    'total_items': 1,
                    'books': [{
                        'id': 'author_test',
                        'title': 'Author Test Book',
                        'authors': ['John Doe'],
                        'categories': ['Fiction']
                    }],
                    'query': 'inauthor:"John Doe"'
                }
                
                mock_get_service.return_value = mock_service
                
                # Test author search
                response = client.get("/api/search/books/author/John%20Doe")
                
                assert response.status_code == 200, f"Expected 200, got {response.status_code}"
                
                data = response.json()
                assert data['success'] is True, "Author search should succeed"
                assert 'books' in data, "Response should contain books"
                
                print("✓ Author search endpoint working correctly")
                return True
                
        except Exception as e:
            print(f"✗ Author search endpoint test failed: {e}")
            return False

    async def test_book_details_endpoint(self):
        """Test the book details endpoint /api/search/books/{volume_id}"""
        print("Testing book details endpoint...")
        
        try:
            client = self.setup_test_app()
            if not client:
                return False
            
            # Mock the search service
            with patch('api.app.routers.search.get_search_service') as mock_get_service:
                mock_service = AsyncMock()
                mock_service.__aenter__.return_value = mock_service
                mock_service.__aexit__.return_value = None
                mock_book = {
                    'id': 'volume_123',
                    'title': 'Volume Test Book',
                    'authors': ['Volume Author'],
                    'description': 'Detailed book information'
                }
                mock_service.get_book_by_id.return_value = mock_book
                
                mock_get_service.return_value = mock_service
                
                # Test book details retrieval
                response = client.get("/api/search/books/volume_123")
                
                assert response.status_code == 200, f"Expected 200, got {response.status_code}"
                
                data = response.json()
                assert data['success'] is True, "Book details should succeed"
                assert 'book' in data, "Response should contain book"
                assert data['book']['id'] == 'volume_123', "Should return correct book"
                
                # Test not found
                mock_service.get_book_by_id.return_value = None
                response = client.get("/api/search/books/nonexistent")
                assert response.status_code == 404, "Not found should return 404"
                
                print("✓ Book details endpoint working correctly")
                return True
                
        except Exception as e:
            print(f"✗ Book details endpoint test failed: {e}")
            return False

    async def test_error_responses(self):
        """Test error response handling"""
        print("Testing error response handling...")
        
        try:
            client = self.setup_test_app()
            if not client:
                return False
            
            # Mock the search service to return errors
            with patch('api.app.routers.search.get_search_service') as mock_get_service:
                mock_service = AsyncMock()
                mock_service.__aenter__.return_value = mock_service
                mock_service.__aexit__.return_value = None
                mock_service.validate_search_input.return_value = False
                
                mock_get_service.return_value = mock_service
                
                # Test invalid query
                response = client.get("/api/search/books?q=<script>")
                # Should handle gracefully with proper error response
                
                # Test search service error
                mock_service.validate_search_input.return_value = True
                mock_service.search_books.return_value = {
                    'success': False,
                    'error': 'API rate limit exceeded',
                    'books': []
                }
                
                response = client.get("/api/search/books?q=test")
                assert response.status_code == 200, "Service errors should return 200 with error info"
                
                data = response.json()
                assert data['success'] is False, "Should indicate failure"
                assert 'error' in data, "Should contain error message"
                
                print("✓ Error response handling working correctly")
                return True
                
        except Exception as e:
            print(f"✗ Error response test failed: {e}")
            return False

    def test_health_endpoint(self):
        """Test health check endpoint"""
        print("Testing health check endpoint...")
        
        try:
            client = self.setup_test_app()
            if not client:
                return False
            
            response = client.get("/health")
            
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            assert 'status' in data, "Health check should have status"
            assert data['status'] == 'healthy', "Status should be healthy"
            
            print("✓ Health endpoint working correctly")
            return True
            
        except Exception as e:
            print(f"✗ Health endpoint test failed: {e}")
            return False

    def test_api_documentation(self):
        """Test API root endpoint provides documentation"""
        print("Testing API documentation endpoint...")
        
        try:
            client = self.setup_test_app()
            if not client:
                return False
            
            response = client.get("/")
            
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            assert 'message' in data, "Root should have message"
            assert 'endpoints' in data, "Root should list endpoints"
            
            # Check that all expected endpoints are documented
            endpoints = data['endpoints']
            expected_endpoints = [
                'search', 'isbn_search', 'book_details', 
                'advanced_search', 'author_search', 'health'
            ]
            
            for endpoint in expected_endpoints:
                assert endpoint in endpoints, f"Endpoint {endpoint} should be documented"
            
            print("✓ API documentation endpoint working correctly")
            return True
            
        except Exception as e:
            print(f"✗ API documentation test failed: {e}")
            return False

async def run_api_tests():
    """Run all API endpoint tests"""
    print("=" * 70)
    print("Running API Endpoint Tests")
    print("=" * 70)
    
    test_instance = TestAPIEndpoints()
    
    tests = [
        ("Basic Search Endpoint", test_instance.test_basic_search_endpoint()),
        ("ISBN Search Endpoint", test_instance.test_isbn_search_endpoint()),
        ("Advanced Search Endpoint", test_instance.test_advanced_search_endpoint()),
        ("Author Search Endpoint", test_instance.test_author_search_endpoint()),
        ("Book Details Endpoint", test_instance.test_book_details_endpoint()),
        ("Error Response Handling", test_instance.test_error_responses()),
        ("Health Check Endpoint", test_instance.test_health_endpoint()),
        ("API Documentation", test_instance.test_api_documentation()),
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
    
    # Print summary
    print("\n" + "=" * 70)
    print("API Endpoint Test Results:")
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
    passed, total = asyncio.run(run_api_tests())
    exit_code = 0 if passed == total else 1
    sys.exit(exit_code)