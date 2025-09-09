import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const query = searchParams.get('q')

  if (!query) {
    return NextResponse.json(
      { error: 'Query parameter is required' },
      { status: 400 }
    )
  }

  try {
    // TODO: Integrate with Python service or Google Books API
    // For now, return mock data to test the architecture
    const mockBooks = [
      {
        id: '1',
        title: `Search results for: ${query}`,
        author: 'Author Name',
        description: 'This is a placeholder book description. The full architecture is set up and ready for Google Books API integration.',
      }
    ]

    return NextResponse.json({
      success: true,
      query: query,
      books: mockBooks,
      totalItems: mockBooks.length
    })
  } catch (error) {
    console.error('Search error:', error)
    return NextResponse.json(
      { error: 'Failed to search books' },
      { status: 500 }
    )
  }
}