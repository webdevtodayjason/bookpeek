'use client'

import { useState } from 'react'
import { Search } from 'lucide-react'

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [loading, setLoading] = useState(false)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!searchQuery.trim()) return

    setLoading(true)
    try {
      const response = await fetch(`/api/books/search?q=${encodeURIComponent(searchQuery)}`)
      const data = await response.json()
      setSearchResults(data.books || [])
    } catch (error) {
      console.error('Search failed:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center mb-8">BookPeek</h1>
        <p className="text-center text-muted-foreground mb-8">
          Discover books with AI-powered summaries and reviews
        </p>
        
        <form onSubmit={handleSearch} className="max-w-2xl mx-auto mb-12">
          <div className="relative">
            <input
              type="text"
              placeholder="Search by title or ISBN..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-4 py-3 pr-12 rounded-lg border border-input bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            />
            <button
              type="submit"
              disabled={loading}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-muted-foreground hover:text-foreground disabled:opacity-50"
            >
              <Search className="w-5 h-5" />
            </button>
          </div>
        </form>

        {loading && (
          <div className="text-center">
            <p className="text-muted-foreground">Searching...</p>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {searchResults.map((book: any) => (
            <div key={book.id} className="bg-card p-4 rounded-lg border border-border shadow-sm">
              <h3 className="font-semibold text-lg mb-2">{book.title}</h3>
              <p className="text-sm text-muted-foreground mb-2">{book.author}</p>
              <p className="text-sm">{book.description}</p>
            </div>
          ))}
        </div>
      </div>
    </main>
  )
}