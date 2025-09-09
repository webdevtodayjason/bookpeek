import { NextRequest, NextResponse } from 'next/server'

const GOOGLE_BOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes'
const GOOGLE_BOOKS_API_KEY = process.env.GOOGLE_BOOKS_API_KEY || ''

interface BookItem {
  id: string
  volumeInfo: {
    title?: string
    authors?: string[]
    description?: string
    publishedDate?: string
    publisher?: string
    pageCount?: number
    categories?: string[]
    averageRating?: number
    ratingsCount?: number
    imageLinks?: {
      thumbnail?: string
      smallThumbnail?: string
    }
    industryIdentifiers?: Array<{
      type: string
      identifier: string
    }>
    language?: string
    previewLink?: string
    infoLink?: string
  }
}

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const query = searchParams.get('q')
  const maxResults = searchParams.get('max_results') || '10'
  const startIndex = searchParams.get('start_index') || '0'
  const orderBy = searchParams.get('order_by') || 'relevance'

  if (!query) {
    return NextResponse.json(
      { error: 'Query parameter is required' },
      { status: 400 }
    )
  }

  // Validate query
  if (query.length < 2 || query.length > 500) {
    return NextResponse.json(
      { error: 'Query must be between 2 and 500 characters' },
      { status: 400 }
    )
  }

  try {
    // Build Google Books API URL
    const params = new URLSearchParams({
      q: query,
      maxResults: maxResults,
      startIndex: startIndex,
      orderBy: orderBy
    })

    if (GOOGLE_BOOKS_API_KEY) {
      params.append('key', GOOGLE_BOOKS_API_KEY)
    }

    const apiUrl = `${GOOGLE_BOOKS_API_URL}?${params.toString()}`

    // Fetch from Google Books API
    const response = await fetch(apiUrl, {
      headers: {
        'Accept': 'application/json',
      },
      // Cache for 5 minutes
      next: { revalidate: 300 }
    })

    if (!response.ok) {
      if (response.status === 429) {
        return NextResponse.json(
          { error: 'Rate limit exceeded. Please try again later.' },
          { status: 429 }
        )
      }
      throw new Error(`Google Books API error: ${response.status}`)
    }

    const data = await response.json()

    // Transform the response
    const books = (data.items || []).map((item: BookItem) => {
      const volumeInfo = item.volumeInfo || {}
      const imageLinks = volumeInfo.imageLinks || {}
      
      // Extract ISBNs
      let isbn = null
      let isbn13 = null
      const identifiers = volumeInfo.industryIdentifiers || []
      for (const identifier of identifiers) {
        if (identifier.type === 'ISBN_10') {
          isbn = identifier.identifier
        } else if (identifier.type === 'ISBN_13') {
          isbn13 = identifier.identifier
        }
      }

      // Ensure HTTPS for image URLs
      const thumbnail = imageLinks.thumbnail || imageLinks.smallThumbnail
      const secureThumbnail = thumbnail?.replace('http:', 'https:')

      return {
        id: item.id,
        title: volumeInfo.title || 'Unknown Title',
        authors: volumeInfo.authors || [],
        description: volumeInfo.description,
        isbn: isbn,
        isbn13: isbn13,
        thumbnail: secureThumbnail,
        published_date: volumeInfo.publishedDate,
        publisher: volumeInfo.publisher,
        page_count: volumeInfo.pageCount,
        categories: volumeInfo.categories || [],
        average_rating: volumeInfo.averageRating,
        ratings_count: volumeInfo.ratingsCount,
        language: volumeInfo.language,
        preview_link: volumeInfo.previewLink,
        info_link: volumeInfo.infoLink
      }
    })

    return NextResponse.json({
      success: true,
      query: query,
      books: books,
      total_items: data.totalItems || 0,
      start_index: parseInt(startIndex),
      max_results: parseInt(maxResults)
    })
  } catch (error) {
    console.error('Search error:', error)
    return NextResponse.json(
      { 
        error: 'Failed to search books',
        success: false,
        books: []
      },
      { status: 500 }
    )
  }
}