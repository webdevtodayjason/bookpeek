"""
API Service for handling HTTP requests and responses
"""

import os
import logging
from typing import Dict, Any, Optional, List
import aiohttp
from urllib.parse import urlencode, quote
import asyncio
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIService:
    """
    Service for handling external API calls with rate limiting and caching
    """
    
    def __init__(self):
        """Initialize the API service"""
        self.session = None
        self.cache = {}
        self.cache_ttl = timedelta(minutes=15)  # Cache for 15 minutes
        self.rate_limit_delay = 0.1  # 100ms between requests
        self.last_request_time = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=10),
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def _apply_rate_limit(self):
        """Apply rate limiting between requests"""
        if self.last_request_time:
            elapsed = datetime.now() - self.last_request_time
            if elapsed.total_seconds() < self.rate_limit_delay:
                await asyncio.sleep(self.rate_limit_delay - elapsed.total_seconds())
        self.last_request_time = datetime.now()
    
    def _get_cache_key(self, url: str, params: Optional[Dict] = None) -> str:
        """Generate cache key from URL and parameters"""
        if params:
            return f"{url}?{urlencode(params)}"
        return url
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get data from cache if not expired"""
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < self.cache_ttl:
                logger.debug(f"Cache hit for: {cache_key}")
                return cached_data
            else:
                # Remove expired cache entry
                del self.cache[cache_key]
        return None
    
    def _set_cache(self, cache_key: str, data: Dict[str, Any]):
        """Store data in cache"""
        self.cache[cache_key] = (data, datetime.now())
        logger.debug(f"Cached data for: {cache_key}")
        
        # Clean old cache entries
        self._clean_cache()
    
    def _clean_cache(self):
        """Remove expired cache entries"""
        now = datetime.now()
        expired_keys = [
            key for key, (_, timestamp) in self.cache.items()
            if now - timestamp >= self.cache_ttl
        ]
        for key in expired_keys:
            del self.cache[key]
    
    async def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Make GET request with caching and rate limiting
        
        Args:
            url: URL to request
            params: Query parameters
            headers: Request headers
            use_cache: Whether to use caching
            
        Returns:
            Response data as dictionary
        """
        try:
            # Check cache first
            if use_cache:
                cache_key = self._get_cache_key(url, params)
                cached_data = self._get_from_cache(cache_key)
                if cached_data:
                    return cached_data
            
            # Apply rate limiting
            await self._apply_rate_limit()
            
            # Make request
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            async with self.session.get(url, params=params, headers=headers) as response:
                # Handle different response codes
                if response.status == 200:
                    data = await response.json()
                    
                    # Cache successful response
                    if use_cache:
                        self._set_cache(cache_key, data)
                    
                    return {
                        'success': True,
                        'data': data,
                        'status': response.status
                    }
                    
                elif response.status == 429:
                    # Rate limit exceeded
                    logger.warning(f"Rate limit exceeded for: {url}")
                    return {
                        'success': False,
                        'error': 'Rate limit exceeded',
                        'status': response.status,
                        'retry_after': response.headers.get('Retry-After', 60)
                    }
                    
                elif response.status == 404:
                    return {
                        'success': False,
                        'error': 'Resource not found',
                        'status': response.status
                    }
                    
                else:
                    error_text = await response.text()
                    logger.error(f"API error {response.status}: {error_text}")
                    return {
                        'success': False,
                        'error': f'API error: {response.status}',
                        'status': response.status,
                        'details': error_text
                    }
                    
        except asyncio.TimeoutError:
            logger.error(f"Request timeout for: {url}")
            return {
                'success': False,
                'error': 'Request timeout',
                'status': 0
            }
            
        except aiohttp.ClientError as e:
            logger.error(f"Client error for {url}: {str(e)}")
            return {
                'success': False,
                'error': f'Network error: {str(e)}',
                'status': 0
            }
            
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {str(e)}")
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'status': 0
            }
    
    async def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make POST request
        
        Args:
            url: URL to request
            data: Form data
            json_data: JSON data
            headers: Request headers
            
        Returns:
            Response data as dictionary
        """
        try:
            # Apply rate limiting
            await self._apply_rate_limit()
            
            # Make request
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            async with self.session.post(
                url,
                data=data,
                json=json_data,
                headers=headers
            ) as response:
                if response.status in [200, 201]:
                    response_data = await response.json()
                    return {
                        'success': True,
                        'data': response_data,
                        'status': response.status
                    }
                else:
                    error_text = await response.text()
                    logger.error(f"POST error {response.status}: {error_text}")
                    return {
                        'success': False,
                        'error': f'API error: {response.status}',
                        'status': response.status,
                        'details': error_text
                    }
                    
        except Exception as e:
            logger.error(f"POST error for {url}: {str(e)}")
            return {
                'success': False,
                'error': f'Error: {str(e)}',
                'status': 0
            }
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        self._clean_cache()
        return {
            'entries': len(self.cache),
            'ttl_minutes': self.cache_ttl.total_seconds() / 60,
            'oldest_entry': min(
                (timestamp for _, timestamp in self.cache.values()),
                default=None
            )
        }

class GoogleBooksAPI:
    """
    Specialized service for Google Books API
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Google Books API service"""
        self.api_key = api_key or os.getenv('GOOGLE_BOOKS_API_KEY', '')
        self.base_url = 'https://www.googleapis.com/books/v1'
        self.api_service = APIService()
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.api_service.__aenter__()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.api_service.__aexit__(exc_type, exc_val, exc_tb)
    
    async def search_volumes(
        self,
        query: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Search for book volumes
        
        Args:
            query: Search query
            **kwargs: Additional parameters (maxResults, startIndex, etc.)
            
        Returns:
            Search results
        """
        url = f"{self.base_url}/volumes"
        params = {'q': query}
        
        if self.api_key:
            params['key'] = self.api_key
            
        params.update(kwargs)
        
        result = await self.api_service.get(url, params=params)
        
        if result['success']:
            return result['data']
        else:
            raise Exception(f"Google Books API error: {result.get('error', 'Unknown error')}")
    
    async def get_volume(self, volume_id: str) -> Dict[str, Any]:
        """
        Get specific volume details
        
        Args:
            volume_id: Google Books volume ID
            
        Returns:
            Volume details
        """
        url = f"{self.base_url}/volumes/{volume_id}"
        params = {}
        
        if self.api_key:
            params['key'] = self.api_key
        
        result = await self.api_service.get(url, params=params)
        
        if result['success']:
            return result['data']
        else:
            raise Exception(f"Google Books API error: {result.get('error', 'Unknown error')}")

# Create singleton instances
_api_service: Optional[APIService] = None
_google_books_api: Optional[GoogleBooksAPI] = None

def get_api_service() -> APIService:
    """Get or create the API service singleton"""
    global _api_service
    if _api_service is None:
        _api_service = APIService()
    return _api_service

def get_google_books_api() -> GoogleBooksAPI:
    """Get or create the Google Books API singleton"""
    global _google_books_api
    if _google_books_api is None:
        _google_books_api = GoogleBooksAPI()
    return _google_books_api

# Export main functionality
__all__ = [
    'APIService',
    'GoogleBooksAPI',
    'get_api_service',
    'get_google_books_api'
]