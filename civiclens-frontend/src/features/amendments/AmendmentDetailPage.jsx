import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getAmendment } from '../../api/amendmentApi'
import CategoryBadge from './CategoryBadge'
import CountdownTimer from './CountdownTimer'
import CommentSection from './CommentSection'
import SentimentIndicator from './SentimentIndicator'
import AnalyticsPanel from '../analytics/AnalyticsPanel'
import { PageLoader } from '../../components/LoadingSpinner'
import { formatDateTime } from '../../utils/constants'

export default function AmendmentDetailPage() {
  const { id } = useParams()
  const [amendment, setAmendment] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showAnalytics, setShowAnalytics] = useState(true)

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
      <div className="glass-card p-8 text-center animate-fade-in">
        <p className="text-rose-400 mb-4">{error || 'Amendment not found'}</p>
        <Link to="/" className="btn-primary text-sm">Back to Amendments</Link>
      </div>
    )
  }

  return (
    <div className="animate-fade-in h-[calc(100vh-112px)] flex flex-col">
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-sm text-dark-500 mb-6 flex-shrink-0">
        <Link to="/" className="hover:text-civic-400 transition-colors">Amendments</Link>
        <span>/</span>
        <span className="text-dark-300 truncate max-w-[300px]">{amendment.title}</span>
      </div>

      <div className="flex flex-col lg:flex-row gap-6 flex-1 min-h-0 overflow-hidden">
        {/* Main Content */}
        <div className="flex-1 min-w-0 space-y-6 overflow-y-auto pr-1 pb-6 relative">
          {/* Amendment Header */}
          <div className="glass-card p-6">
            {/* Meta row */}
            <div className="flex flex-wrap items-center gap-2 mb-3">
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

            {/* Title */}
            <h1 className="text-2xl font-bold text-dark-50 mb-3 leading-tight">
              {amendment.title}
            </h1>

            {/* Author + Date */}
            <div className="flex items-center gap-3 text-sm text-dark-400 mb-4">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 bg-dark-700 rounded-full flex items-center justify-center">
                  <span className="text-[10px] font-semibold text-civic-400">
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
              <div className="bg-dark-800/40 rounded-xl p-5 border border-dark-700/30">
                <p className="text-dark-200 leading-relaxed whitespace-pre-wrap text-sm">
                  {amendment.body}
                </p>
              </div>
            </div>
          </div>

          {/* Timer */}
          {amendment.closesAt && amendment.status === 'ACTIVE' && (
            <CountdownTimer closesAt={amendment.closesAt} />
          )}

          {/* Mobile Analytics toggle */}
          <div className="lg:hidden">
            <button
              onClick={() => setShowAnalytics(!showAnalytics)}
              className="btn-ghost w-full flex items-center justify-center gap-2 text-sm"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 21H4.6c-.56 0-.84 0-1.05-.11a1 1 0 0 1-.44-.44C3 20.24 3 19.96 3 19.4V3" />
                <path d="M7 14l4-4 4 4 6-6" />
              </svg>
              {showAnalytics ? 'Hide' : 'Show'} Analytics Panel
            </button>
          </div>

          {/* Mobile Analytics Panel */}
          <div className={`lg:hidden ${showAnalytics ? '' : 'hidden'}`}>
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
