"""
Main router aggregating all API routes
"""

from fastapi import APIRouter
from .search import router as search_router

# Create main router
router = APIRouter()

# Include sub-routers
router.include_router(search_router)

# Health check endpoint
@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "bookpeek-api"}

# Root endpoint
@router.get("/")
async def root():
    """Root API endpoint"""
    return {
        "message": "BookPeek API",
        "version": "1.0.0",
        "endpoints": {
            "search": "/api/search/books",
            "isbn_search": "/api/search/books/isbn/{isbn}",
            "book_details": "/api/search/books/{volume_id}",
            "advanced_search": "/api/search/books/advanced",
            "author_search": "/api/search/books/author/{author}",
            "health": "/health"
        }
    }

# Export router
__all__ = ['router']