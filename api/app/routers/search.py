"""
Search router for book searches
"""

from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional, Dict, Any
import logging

from ..services.search_service import get_search_service, GoogleBooksSearchService

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/search",
    tags=["search"],
    responses={404: {"description": "Not found"}}
)

@router.get("/books")
async def search_books(
    q: str = Query(..., min_length=2, max_length=500, description="Search query"),
    max_results: int = Query(10, ge=1, le=40, description="Maximum results to return"),
    start_index: int = Query(0, ge=0, description="Starting index for pagination"),
    order_by: str = Query("relevance", regex="^(relevance|newest)$", description="Sort order"),
    lang: Optional[str] = Query(None, min_length=2, max_length=5, description="Language restriction")
) -> Dict[str, Any]:
    """
    Search for books using Google Books API
    
    Args:
        q: Search query (title, author, ISBN, etc.)
        max_results: Maximum number of results (1-40)
        start_index: Starting index for pagination
        order_by: Sort order ('relevance' or 'newest')
        lang: Language restriction (e.g., 'en' for English)
    
    Returns:
        Search results with books and metadata
    """
    try:
        # Get search service
        search_service = get_search_service()
        
        # Validate input
        if not search_service.validate_search_input(q):
            raise HTTPException(
                status_code=400,
                detail="Invalid search query"
            )
        
        # Perform search
        async with search_service as service:
            results = await service.search_books(
                query=q,
                max_results=max_results,
                start_index=start_index,
                order_by=order_by,
                lang_restrict=lang
            )
        
        if not results.get('success', False):
            # Log error but return empty results
            logger.error(f"Search failed: {results.get('error', 'Unknown error')}")
            return {
                'success': False,
                'error': results.get('error', 'Search failed'),
                'books': [],
                'total_items': 0
            }
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in search: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during search"
        )

@router.get("/books/isbn/{isbn}")
async def search_by_isbn(
    isbn: str = Path(..., min_length=10, max_length=13, description="ISBN-10 or ISBN-13")
) -> Dict[str, Any]:
    """
    Search for a book by ISBN
    
    Args:
        isbn: ISBN-10 or ISBN-13
    
    Returns:
        Book information if found
    """
    try:
        # Clean ISBN
        isbn_clean = isbn.replace('-', '').replace(' ', '')
        
        # Validate ISBN format
        if len(isbn_clean) not in [10, 13]:
            raise HTTPException(
                status_code=400,
                detail="Invalid ISBN format. Must be ISBN-10 or ISBN-13"
            )
        
        # Get search service
        search_service = get_search_service()
        
        # Search by ISBN
        async with search_service as service:
            book = await service.search_by_isbn(isbn_clean)
        
        if book:
            return {
                'success': True,
                'book': book
            }
        else:
            raise HTTPException(
                status_code=404,
                detail="Book not found with given ISBN"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching by ISBN: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during ISBN search"
        )

@router.get("/books/{volume_id}")
async def get_book_details(
    volume_id: str = Path(..., description="Google Books volume ID")
) -> Dict[str, Any]:
    """
    Get detailed information for a specific book
    
    Args:
        volume_id: Google Books volume ID
    
    Returns:
        Detailed book information
    """
    try:
        # Get search service
        search_service = get_search_service()
        
        # Get book details
        async with search_service as service:
            book = await service.get_book_by_id(volume_id)
        
        if book:
            return {
                'success': True,
                'book': book
            }
        else:
            raise HTTPException(
                status_code=404,
                detail="Book not found with given ID"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching book details: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error fetching book details"
        )

# Export router
__all__ = ['router']