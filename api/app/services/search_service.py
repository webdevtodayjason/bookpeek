"""
Google Books API Search Service
Handles book searches using Google Books API
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import aiohttp
from urllib.parse import quote

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BookSearchResult:
    """Data class for book search results"""
    id: str
    title: str
    authors: List[str]
    description: Optional[str]
    isbn: Optional[str]
    isbn13: Optional[str]
    cover_image: Optional[str]
    thumbnail: Optional[str]
    published_date: Optional[str]
    publisher: Optional[str]
    page_count: Optional[int]
    categories: List[str]
    average_rating: Optional[float]
    ratings_count: Optional[int]
    language: Optional[str]
    preview_link: Optional[str]
    info_link: Optional[str]

class GoogleBooksSearchService:
    """
    Service for searching books using Google Books API
    """
    
    def __init__(self):
        """Initialize the search service"""
        self.api_key = os.getenv('GOOGLE_BOOKS_API_KEY', '')
        self.base_url = 'https://www.googleapis.com/books/v1/volumes'
        self.session = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def search_books(
        self, 
        query: str, 
        max_results: int = 10,
        start_index: int = 0,
        order_by: str = 'relevance',
        lang_restrict: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for books using Google Books API
        
        Args:
            query: Search query (title, author, ISBN, etc.)
            max_results: Maximum number of results (1-40)
            start_index: Starting index for pagination
            order_by: Sort order ('relevance' or 'newest')
            lang_restrict: Restrict to specific language (e.g., 'en')
            
        Returns:
            Dictionary containing search results and metadata
        """
        try:
            # Validate inputs
            if not query or not query.strip():
                raise ValueError("Search query cannot be empty")
            
            max_results = min(max(1, max_results), 40)  # API limit is 40
            
            # Build API parameters
            params = {
                'q': query,
                'maxResults': max_results,
                'startIndex': start_index,
                'orderBy': order_by
            }
            
            if self.api_key:
                params['key'] = self.api_key
                
            if lang_restrict:
                params['langRestrict'] = lang_restrict
            
            # Make API request
            if not self.session:
                self.session = aiohttp.ClientSession()
                
            async with self.session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Parse results
                    books = []
                    for item in data.get('items', []):
                        book = self._parse_book_item(item)
                        if book:
                            books.append(asdict(book))
                    
                    return {
                        'success': True,
                        'total_items': data.get('totalItems', 0),
                        'books': books,
                        'query': query,
                        'start_index': start_index,
                        'max_results': max_results
                    }
                    
                elif response.status == 429:
                    logger.error("Google Books API rate limit exceeded")
                    return {
                        'success': False,
                        'error': 'Rate limit exceeded. Please try again later.',
                        'books': []
                    }
                    
                else:
                    error_text = await response.text()
                    logger.error(f"Google Books API error: {response.status} - {error_text}")
                    return {
                        'success': False,
                        'error': f'API error: {response.status}',
                        'books': []
                    }
                    
        except aiohttp.ClientError as e:
            logger.error(f"Network error searching books: {str(e)}")
            return {
                'success': False,
                'error': 'Network error occurred',
                'books': []
            }
            
        except Exception as e:
            logger.error(f"Error searching books: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'books': []
            }
    
    async def search_by_isbn(self, isbn: str) -> Optional[BookSearchResult]:
        """
        Search for a specific book by ISBN
        
        Args:
            isbn: ISBN-10 or ISBN-13
            
        Returns:
            BookSearchResult or None if not found
        """
        # Clean ISBN (remove hyphens and spaces)
        isbn = isbn.replace('-', '').replace(' ', '')
        
        # Search using ISBN query
        query = f'isbn:{isbn}'
        result = await self.search_books(query, max_results=1)
        
        if result.get('success') and result.get('books'):
            book_data = result['books'][0]
            return BookSearchResult(**book_data)
        
        return None
    
    async def get_book_by_id(self, volume_id: str) -> Optional[BookSearchResult]:
        """
        Get detailed information for a specific book by volume ID
        
        Args:
            volume_id: Google Books volume ID
            
        Returns:
            BookSearchResult or None if not found
        """
        try:
            url = f"{self.base_url}/{volume_id}"
            params = {}
            
            if self.api_key:
                params['key'] = self.api_key
            
            if not self.session:
                self.session = aiohttp.ClientSession()
                
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_book_item(data)
                else:
                    logger.error(f"Failed to fetch book {volume_id}: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching book {volume_id}: {str(e)}")
            return None
    
    def _parse_book_item(self, item: Dict[str, Any]) -> Optional[BookSearchResult]:
        """
        Parse a book item from Google Books API response
        
        Args:
            item: Book item from API response
            
        Returns:
            BookSearchResult or None if parsing fails
        """
        try:
            volume_info = item.get('volumeInfo', {})
            sale_info = item.get('saleInfo', {})
            
            # Extract ISBNs
            isbn = None
            isbn13 = None
            identifiers = volume_info.get('industryIdentifiers', [])
            for identifier in identifiers:
                if identifier.get('type') == 'ISBN_10':
                    isbn = identifier.get('identifier')
                elif identifier.get('type') == 'ISBN_13':
                    isbn13 = identifier.get('identifier')
            
            # Extract image links
            image_links = volume_info.get('imageLinks', {})
            cover_image = image_links.get('large') or image_links.get('medium') or image_links.get('small')
            thumbnail = image_links.get('thumbnail') or image_links.get('smallThumbnail')
            
            # Ensure HTTPS for image URLs
            if cover_image and cover_image.startswith('http:'):
                cover_image = cover_image.replace('http:', 'https:', 1)
            if thumbnail and thumbnail.startswith('http:'):
                thumbnail = thumbnail.replace('http:', 'https:', 1)
            
            return BookSearchResult(
                id=item.get('id', ''),
                title=volume_info.get('title', 'Unknown Title'),
                authors=volume_info.get('authors', []),
                description=volume_info.get('description'),
                isbn=isbn,
                isbn13=isbn13,
                cover_image=cover_image,
                thumbnail=thumbnail,
                published_date=volume_info.get('publishedDate'),
                publisher=volume_info.get('publisher'),
                page_count=volume_info.get('pageCount'),
                categories=volume_info.get('categories', []),
                average_rating=volume_info.get('averageRating'),
                ratings_count=volume_info.get('ratingsCount'),
                language=volume_info.get('language'),
                preview_link=volume_info.get('previewLink'),
                info_link=volume_info.get('infoLink')
            )
            
        except Exception as e:
            logger.error(f"Error parsing book item: {str(e)}")
            return None
    
    def validate_search_input(self, query: str) -> bool:
        """
        Validate search query input
        
        Args:
            query: Search query to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not query or len(query.strip()) < 2:
            return False
        
        # Check for potential injection attempts
        forbidden_chars = ['<', '>', '{', '}', '\\', '`', '\n', '\r', '\t']
        if any(char in query for char in forbidden_chars):
            logger.warning(f"Invalid characters detected in search query: {query}")
            return False
        
        # Limit query length
        if len(query) > 500:
            logger.warning(f"Search query too long: {len(query)} characters")
            return False
        
        return True

# Create singleton instance
_search_service: Optional[GoogleBooksSearchService] = None

def get_search_service() -> GoogleBooksSearchService:
    """Get or create the search service singleton"""
    global _search_service
    if _search_service is None:
        _search_service = GoogleBooksSearchService()
    return _search_service

# Export main functionality
__all__ = [
    'GoogleBooksSearchService',
    'BookSearchResult',
    'get_search_service'
]