import { useState, useEffect } from 'react'
import { getAmendments } from '../../api/amendmentApi'
import AmendmentCard from './AmendmentCard'
import FilterBar from './FilterBar'
import { PageLoader } from '../../components/LoadingSpinner'

export default function AmendmentListPage() {
  const [amendments, setAmendments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [sort, setSort] = useState('LATEST')
  const [category, setCategory] = useState(null)
  const [page, setPage] = useState(0)
  const [totalPages, setTotalPages] = useState(0)

  const fetchAmendments = async () => {
    setLoading(true)
    setError(null)
    try {
      const params = { sort, page, size: 10 }
      if (category) params.category = category
      const res = await getAmendments(params)
      setAmendments(res.data.content || [])
      setTotalPages(res.data.totalPages || 0)
    } catch (err) {
      setError('Failed to load amendments')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchAmendments()
  }, [sort, category, page])

  const handleSortChange = (newSort) => {
    setSort(newSort)
    setPage(0)
  }

  const handleCategoryChange = (newCat) => {
    setCategory(newCat)
    setPage(0)
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-dark-100">Amendments</h1>
          <p className="text-sm text-dark-400 mt-1">
            Browse active legislative amendments and share your voice
          </p>
        </div>
      </div>

      {/* Filters */}
      <FilterBar
        sort={sort}
        category={category}
        onSortChange={handleSortChange}
        onCategoryChange={handleCategoryChange}
      />

      {/* Content */}
      {loading ? (
        <PageLoader />
      ) : error ? (
        <div className="glass-card p-8 text-center">
          <p className="text-rose-400 mb-4">{error}</p>
          <button onClick={fetchAmendments} className="btn-primary text-sm">
            Retry
          </button>
        </div>
      ) : amendments.length === 0 ? (
        <div className="glass-card p-12 text-center">
          <div className="text-4xl mb-4">📋</div>
          <h3 className="text-lg font-semibold text-dark-200 mb-2">No amendments found</h3>
          <p className="text-sm text-dark-400">
            {category ? 'Try selecting a different category.' : 'No amendments have been created yet.'}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {amendments.map((amendment) => (
            <AmendmentCard key={amendment.id} amendment={amendment} />
          ))}
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-2 pt-4">
          <button
            onClick={() => setPage(prev => Math.max(0, prev - 1))}
            disabled={page === 0}
            className="btn-ghost text-sm disabled:opacity-30"
          >
            ← Previous
          </button>
          <div className="flex items-center gap-1">
            {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => {
              const pageNum = totalPages <= 5 ? i : Math.max(0, Math.min(page - 2, totalPages - 5)) + i
              return (
                <button
                  key={pageNum}
                  onClick={() => setPage(pageNum)}
                  className={`w-9 h-9 rounded-lg text-sm font-medium transition-all duration-200 ${
                    page === pageNum
                      ? 'bg-civic-400 text-dark-950'
                      : 'text-dark-400 hover:bg-dark-800'
                  }`}
                >
                  {pageNum + 1}
                </button>
              )
            })}
          </div>
          <button
            onClick={() => setPage(prev => Math.min(totalPages - 1, prev + 1))}
            disabled={page >= totalPages - 1}
            className="btn-ghost text-sm disabled:opacity-30"
          >
            Next →
          </button>
        </div>
      )}
    </div>
  )
}
