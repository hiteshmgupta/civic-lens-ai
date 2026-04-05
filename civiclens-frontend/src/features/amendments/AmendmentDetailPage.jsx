import { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { getAmendment, deleteAmendment } from '../../api/amendmentApi'
import { useAuth } from '../../context/AuthContext'
import CategoryBadge from './CategoryBadge'
import CountdownTimer from './CountdownTimer'
import CommentSection from './CommentSection'
import SentimentIndicator from './SentimentIndicator'
import AnalyticsPanel from '../analytics/AnalyticsPanel'
import { PageLoader } from '../../components/LoadingSpinner'
import { formatDateTime } from '../../utils/constants'

export default function AmendmentDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { isAdmin } = useAuth()
  
  const [amendment, setAmendment] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showAnalytics, setShowAnalytics] = useState(false)

  const [isDeleting, setIsDeleting] = useState(false)

  const handleDelete = async () => {
    const confirmDelete = window.confirm("Are you sure you want to delete this amendment? This action cannot be undone and will delete all associated analytics, comments, and votes.")
    if (!confirmDelete) return

    setIsDeleting(true)
    try {
      await deleteAmendment(id)
      navigate('/')
    } catch (err) {
      console.error('Failed to delete amendment:', err)
      alert('Failed to delete amendment. Please try again.')
      setIsDeleting(false)
    }
  }

  useEffect(() => {
    const fetchAmendment = async () => {
      setLoading(true)
      try {
        const res = await getAmendment(id)
        setAmendment(res.data)
      } catch (err) {
        setError('Failed to load amendment')
      } finally {
        setLoading(false)
      }
    }
    fetchAmendment()
  }, [id])

  if (loading) return <PageLoader />
  if (error || !amendment) {
    return (
      <div className="glass-card p-6 sm:p-8 text-center animate-fade-in">
        <p className="text-rose-400 mb-4">{error || 'Amendment not found'}</p>
        <Link to="/" className="btn-primary text-sm">Back to Amendments</Link>
      </div>
    )
  }

  return (
    <div className="animate-fade-in lg:h-[calc(100vh-112px)] flex flex-col">
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-xs sm:text-sm text-dark-500 mb-4 sm:mb-6 flex-shrink-0">
        <Link to="/" className="hover:text-civic-400 transition-colors">Amendments</Link>
        <span>/</span>
        <span className="text-dark-300 truncate max-w-[200px] sm:max-w-[300px]">{amendment.title}</span>
      </div>

      <div className="flex flex-col lg:flex-row gap-4 sm:gap-6 flex-1 min-h-0 lg:overflow-hidden">
        {/* Main Content */}
        <div className="flex-1 min-w-0 space-y-4 sm:space-y-6 lg:overflow-y-auto lg:pr-1 pb-6 relative">
          {/* Amendment Header */}
          <div className="glass-card p-4 sm:p-6">
            {/* Meta row */}
            <div className="flex flex-wrap items-center gap-1.5 sm:gap-2 mb-3">
              <CategoryBadge category={amendment.category} size="md" />
              <span className={`badge ${
                amendment.status === 'ACTIVE'
                  ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/20'
                  : 'bg-dark-700 text-dark-400 border border-dark-600'
              }`}>
                {amendment.status}
              </span>
              <SentimentIndicator score={amendment.sentimentMean} size="md" />
            </div>

            {/* Title & Delete Button */}
            <div className="flex items-start justify-between gap-3 sm:gap-4 mb-3">
              <h1 className="text-xl sm:text-2xl font-bold text-dark-50 leading-tight">
                {amendment.title}
              </h1>
              {isAdmin && (
                <button
                  onClick={handleDelete}
                  disabled={isDeleting}
                  className="flex-shrink-0 px-2.5 sm:px-3 py-1.5 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 text-xs font-semibold rounded-lg border border-rose-500/20 transition-colors disabled:opacity-50"
                  title="Delete Amendment (Admin Only)"
                >
                  {isDeleting ? 'Deleting...' : '🗑️ Delete'}
                </button>
              )}
            </div>

            {/* Author + Date */}
            <div className="flex flex-wrap items-center gap-2 sm:gap-3 text-xs sm:text-sm text-dark-400 mb-4">
              <div className="flex items-center gap-1.5 sm:gap-2">
                <div className="w-5 h-5 sm:w-6 sm:h-6 bg-dark-700 rounded-full flex items-center justify-center">
                  <span className="text-[9px] sm:text-[10px] font-semibold text-civic-400">
                    {amendment.createdByUsername?.charAt(0).toUpperCase()}
                  </span>
                </div>
                <span>By <span className="text-dark-200">{amendment.createdByUsername}</span></span>
              </div>
              <span>•</span>
              <span>{formatDateTime(amendment.createdAt)}</span>
            </div>

            {/* Body */}
            <div className="prose prose-invert max-w-none">
              <div className="bg-dark-800/40 rounded-xl p-3 sm:p-5 border border-dark-700/30">
                <p className="text-dark-200 leading-relaxed whitespace-pre-wrap text-xs sm:text-sm">
                  {amendment.body}
                </p>
              </div>
            </div>
          </div>

          {/* Timer */}
          {amendment.closesAt && amendment.status === 'ACTIVE' && (
            <CountdownTimer closesAt={amendment.closesAt} />
          )}

          {/* Mobile/Tablet Analytics toggle */}
          <div className="lg:hidden">
            <button
              onClick={() => setShowAnalytics(!showAnalytics)}
              className="btn-ghost w-full flex items-center justify-center gap-2 text-sm border border-dark-700/50 rounded-xl"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 21H4.6c-.56 0-.84 0-1.05-.11a1 1 0 0 1-.44-.44C3 20.24 3 19.96 3 19.4V3" />
                <path d="M7 14l4-4 4 4 6-6" />
              </svg>
              {showAnalytics ? 'Hide' : 'Show'} Analytics Panel
              <svg
                width="12" height="12" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" strokeWidth="2.5"
                className={`transition-transform duration-200 ${showAnalytics ? 'rotate-180' : ''}`}
              >
                <path d="M6 9l6 6 6-6" />
              </svg>
            </button>
          </div>

          {/* Mobile/Tablet Analytics Panel */}
          <div className={`lg:hidden transition-all duration-300 ${showAnalytics ? 'opacity-100' : 'hidden opacity-0'}`}>
            <AnalyticsPanel amendmentId={amendment.id} />
          </div>

          {/* Comments */}
          <CommentSection amendmentId={amendment.id} status={amendment.status} />
        </div>

        {/* Right Sidebar — Analytics (Desktop) */}
        <div className="hidden lg:block w-[380px] flex-shrink-0 overflow-y-auto pr-1 pb-6 relative">
          <AnalyticsPanel amendmentId={amendment.id} />
        </div>
      </div>
    </div>
  )
}
