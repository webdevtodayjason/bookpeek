'use client'

import React, { useState, useCallback, useEffect } from 'react'
import { Search, Loader2, Book, Calendar, User, Hash } from 'lucide-react'

interface BookResult {
  id: string
  title: string
  authors: string[]
  description?: string
  isbn?: string
  isbn13?: string
  cover_image?: string
  thumbnail?: string
  published_date?: string
  publisher?: string
  page_count?: number
  categories: string[]
  average_rating?: number
  ratings_count?: number
  language?: string
  preview_link?: string
  info_link?: string
}

interface SearchResponse {
  success: boolean
  total_items: number
  books: BookResult[]
  query: string
  error?: string
}

export default function SearchInterface() {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<BookResult[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [totalResults, setTotalResults] = useState(0)
  const [currentPage, setCurrentPage] = useState(0)
  const [searchType, setSearchType] = useState<'general' | 'isbn'>('general')

  const detectSearchType = (query: string) => {
    // Check if query looks like an ISBN (10 or 13 digits, possibly with hyphens)
    const cleanQuery = query.replace(/[-\s]/g, '')
    if (/^\d{10}$|^\d{13}$/.test(cleanQuery)) {
      setSearchType('isbn')
    } else {
      setSearchType('general')
    }
  }

  const handleSearch = useCallback(async (e?: React.FormEvent) => {
    if (e) {
      e.preventDefault()
    }

    if (!searchQuery.trim() || searchQuery.length < 2) {
      setError('Please enter at least 2 characters to search')
      return
    }

    setLoading(true)
    setError(null)

    try {
      // Detect search type
      detectSearchType(searchQuery)

      // Use appropriate endpoint based on search type
      let response: Response
      
      if (searchType === 'isbn') {
        const isbn = searchQuery.replace(/[-\s]/g, '')
        response = await fetch(`/api/search/books/isbn/${isbn}`)
      } else {
        const params = new URLSearchParams({
          q: searchQuery,
          max_results: '20',
          start_index: (currentPage * 20).toString(),
          order_by: 'relevance'
        })
        response = await fetch(`/api/search/books?${params}`)
      }

      if (!response.ok) {
        throw new Error(`Search failed: ${response.statusText}`)
      }

      const data: SearchResponse = await response.json()

      if (data.success) {
        if (searchType === 'isbn' && 'book' in data) {
          // Single book result from ISBN search
          setSearchResults([data.book as BookResult])
          setTotalResults(1)
        } else {
          setSearchResults(data.books || [])
          setTotalResults(data.total_items || 0)
        }
      } else {
        setError(data.error || 'Search failed')
        setSearchResults([])
      }
    } catch (err) {
      console.error('Search error:', err)
      setError(err instanceof Error ? err.message : 'An error occurred during search')
      setSearchResults([])
    } finally {
      setLoading(false)
    }
  }, [searchQuery, currentPage, searchType])

  // Auto-search when page changes
  useEffect(() => {
    if (searchQuery && currentPage > 0) {
      handleSearch()
    }
  }, [currentPage])

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  const renderStars = (rating?: number) => {
    if (!rating) return null
    const stars = '★'.repeat(Math.round(rating)) + '☆'.repeat(5 - Math.round(rating))
    return <span className="text-yellow-500">{stars}</span>
  }

  const handleNextPage = () => {
    if ((currentPage + 1) * 20 < totalResults) {
      setCurrentPage(currentPage + 1)
    }
  }

  const handlePrevPage = () => {
    if (currentPage > 0) {
      setCurrentPage(currentPage - 1)
    }
  }

  return (
    <div className="w-full max-w-7xl mx-auto p-4">
      {/* Search Bar */}
      <div className="mb-8">
        <form onSubmit={handleSearch} className="relative">
          <input
            type="text"
            placeholder="Search by title, author, or ISBN..."
            value={searchQuery}
            onChange={(e) => {
              setSearchQuery(e.target.value)
              detectSearchType(e.target.value)
            }}
            onKeyDown={handleKeyDown}
            className="w-full px-4 py-3 pr-12 rounded-lg border border-input bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary transition-colors"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !searchQuery.trim()}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-muted-foreground hover:text-foreground disabled:opacity-50 transition-colors"
            aria-label="Search"
          >
            {loading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Search className="w-5 h-5" />
            )}
          </button>
        </form>
        
        {searchType === 'isbn' && searchQuery && (
          <p className="text-sm text-muted-foreground mt-2">
            Searching by ISBN: {searchQuery}
          </p>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 bg-destructive/10 border border-destructive/20 rounded-lg">
          <p className="text-destructive">{error}</p>
        </div>
      )}

      {/* Results Count */}
      {searchResults.length > 0 && (
        <div className="mb-4 text-muted-foreground">
          <p>Found {totalResults} results for "{searchQuery}"</p>
        </div>
      )}

      {/* Search Results */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {searchResults.map((book) => (
          <div
            key={book.id}
            className="bg-card p-4 rounded-lg border border-border shadow-sm hover:shadow-md transition-shadow"
          >
            <div className="flex gap-4">
              {/* Book Cover */}
              {book.thumbnail ? (
                <img
                  src={book.thumbnail}
                  alt={`Cover of ${book.title}`}
                  className="w-24 h-32 object-cover rounded"
                  loading="lazy"
                />
              ) : (
                <div className="w-24 h-32 bg-muted rounded flex items-center justify-center">
                  <Book className="w-8 h-8 text-muted-foreground" />
                </div>
              )}

              {/* Book Info */}
              <div className="flex-1 min-w-0">
                <h3 className="font-semibold text-lg mb-1 line-clamp-2">
                  {book.title}
                </h3>
                
                {book.authors && book.authors.length > 0 && (
                  <p className="text-sm text-muted-foreground mb-2 flex items-center gap-1">
                    <User className="w-3 h-3" />
                    {book.authors.join(', ')}
                  </p>
                )}

                {book.published_date && (
                  <p className="text-sm text-muted-foreground mb-1 flex items-center gap-1">
                    <Calendar className="w-3 h-3" />
                    {book.published_date}
                  </p>
                )}

                {(book.isbn || book.isbn13) && (
                  <p className="text-sm text-muted-foreground mb-2 flex items-center gap-1">
                    <Hash className="w-3 h-3" />
                    {book.isbn13 || book.isbn}
                  </p>
                )}

                {book.average_rating && (
                  <div className="text-sm mb-2">
                    {renderStars(book.average_rating)}
                    <span className="ml-1 text-muted-foreground">
                      ({book.ratings_count || 0})
                    </span>
                  </div>
                )}
              </div>
            </div>

            {/* Description */}
            {book.description && (
              <p className="text-sm mt-3 line-clamp-3 text-muted-foreground">
                {book.description}
              </p>
            )}

            {/* Categories */}
            {book.categories && book.categories.length > 0 && (
              <div className="mt-3 flex flex-wrap gap-1">
                {book.categories.slice(0, 3).map((category, idx) => (
                  <span
                    key={idx}
                    className="text-xs px-2 py-1 bg-secondary text-secondary-foreground rounded"
                  >
                    {category}
                  </span>
                ))}
              </div>
            )}

            {/* Actions */}
            {book.preview_link && (
              <div className="mt-4">
                <a
                  href={book.preview_link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-primary hover:underline"
                >
                  Preview on Google Books →
                </a>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Pagination */}
      {totalResults > 20 && searchResults.length > 0 && (
        <div className="mt-8 flex justify-center gap-4">
          <button
            onClick={handlePrevPage}
            disabled={currentPage === 0}
            className="px-4 py-2 bg-secondary text-secondary-foreground rounded disabled:opacity-50"
          >
            Previous
          </button>
          <span className="px-4 py-2">
            Page {currentPage + 1} of {Math.ceil(totalResults / 20)}
          </span>
          <button
            onClick={handleNextPage}
            disabled={(currentPage + 1) * 20 >= totalResults}
            className="px-4 py-2 bg-secondary text-secondary-foreground rounded disabled:opacity-50"
          >
            Next
          </button>
        </div>
      )}

      {/* Empty State */}
      {!loading && searchResults.length === 0 && searchQuery && !error && (
        <div className="text-center py-12">
          <Book className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
          <p className="text-muted-foreground">
            No books found for "{searchQuery}"
          </p>
          <p className="text-sm text-muted-foreground mt-2">
            Try adjusting your search terms
          </p>
        </div>
      )}
    </div>
  )
}