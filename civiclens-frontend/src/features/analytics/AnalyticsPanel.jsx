import { useState, useEffect } from 'react'
import { getAnalytics, triggerAnalysis, downloadReport } from '../../api/analyticsApi'
import { useAuth } from '../../context/AuthContext'
import SentimentChart from './SentimentChart'
import SentimentTimeline from './SentimentTimeline'
import TopicClusters from './TopicClusters'
import ArgumentsList from './ArgumentsList'
import EngagementMetrics from './EngagementMetrics'
import ControversyScore from './ControversyScore'
import PolicyBrief from './PolicyBrief'
import LoadingSpinner from '../../components/LoadingSpinner'

export default function AnalyticsPanel({ amendmentId }) {
  const { isAdmin } = useAuth()
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [analyzing, setAnalyzing] = useState(false)
  const [exporting, setExporting] = useState(false)
  const [error, setError] = useState(null)

  const fetchAnalytics = async () => {
    try {
      const res = await getAnalytics(amendmentId)
      setAnalytics(res.data)
    } catch (err) {
      console.error('Failed to load analytics:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchAnalytics()
  }, [amendmentId])

  const handleReanalyze = async () => {
    setAnalyzing(true)
    setError(null)
    try {
      await triggerAnalysis(amendmentId)
      await fetchAnalytics()
    } catch (err) {
      console.error('Analysis trigger failed:', err)
      const msg = err.response?.data?.message || err.response?.data?.detail || err.message || 'Analysis failed'
      setError(`Analysis failed: ${msg} (HTTP ${err.response?.status || 'unknown'})`)
    } finally {
      setAnalyzing(false)
    }
  }

  const handleExportPdf = async () => {
    setExporting(true)
    try {
      const res = await downloadReport(amendmentId)
      const url = window.URL.createObjectURL(new Blob([res.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `amendment-${amendmentId}-report.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      console.error('PDF export failed:', err)
    } finally {
      setExporting(false)
    }
  }

  if (loading) {
    return (
      <div className="space-y-4">
        <div className="glass-card p-5 sm:p-6 flex items-center justify-center">
          <LoadingSpinner size="md" />
        </div>
      </div>
    )
  }

  const hasData = analytics && analytics.totalComments > 0

  return (
    <div className="space-y-3 sm:space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-base sm:text-lg font-bold text-dark-100 flex items-center gap-2">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#c8ee44" strokeWidth="2" className="sm:w-5 sm:h-5">
            <path d="M21 21H4.6c-.56 0-.84 0-1.05-.11a1 1 0 0 1-.44-.44C3 20.24 3 19.96 3 19.4V3" />
            <path d="M7 14l4-4 4 4 6-6" />
          </svg>
          AI Impact Analysis
        </h3>
        <div className="flex items-center gap-2">
          {isAdmin && (
            <button
              onClick={handleReanalyze}
              disabled={analyzing}
              className="btn-ghost text-[10px] sm:text-xs disabled:opacity-50 flex items-center gap-1 sm:gap-1.5"
            >
              {analyzing ? (
                <LoadingSpinner size="sm" />
              ) : (
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="sm:w-[14px] sm:h-[14px]">
                  <path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8" />
                  <path d="M21 3v5h-5" />
                </svg>
              )}
              {analyzing ? 'Analyzing...' : 'Re-analyze'}
            </button>
          )}
        </div>
      </div>

      {!hasData ? (
        <div className="glass-card p-6 sm:p-8 text-center">
          <div className="text-3xl sm:text-4xl mb-3">🔬</div>
          <h4 className="text-dark-200 font-semibold mb-2 text-sm sm:text-base">No Analysis Available</h4>
          <p className="text-xs sm:text-sm text-dark-400 mb-4">
            Click below to run AI analysis on the existing comments.
          </p>
          {isAdmin && (
            <button onClick={handleReanalyze} disabled={analyzing} className="btn-primary text-xs sm:text-sm">
              {analyzing ? 'Analyzing...' : 'Generate Analysis'}
            </button>
          )}
          {error && (
            <div className="mt-4 p-2.5 sm:p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-[10px] sm:text-xs text-left">
              ⚠️ {error}
            </div>
          )}
        </div>
      ) : (
        <>
          {/* Controversy Score */}
          <ControversyScore
            score={analytics.controversyScore}
            label={analytics.controversyLabel}
            analytics={analytics}
          />

          {/* Sentiment */}
          <SentimentChart distribution={analytics.sentimentDistribution} />
          <SentimentTimeline timeline={analytics.sentimentTimeline} />

          {/* Topics */}
          <TopicClusters clusters={analytics.topicClusters} />

          {/* Arguments */}
          <ArgumentsList
            supporting={analytics.topSupporting}
            opposing={analytics.topOpposing}
          />

          {/* Engagement */}
          <EngagementMetrics analytics={analytics} />

          {/* Policy Brief */}
          <PolicyBrief brief={analytics.policyBrief} />

          {/* Export Button */}
          <button
            onClick={handleExportPdf}
            disabled={exporting}
            className="btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-50 text-xs sm:text-sm"
          >
            {exporting ? (
              <>
                <LoadingSpinner size="sm" />
                Generating Report...
              </>
            ) : (
              <>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="sm:w-4 sm:h-4">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <path d="M14 2v6h6" />
                  <path d="M12 18v-6M9 15l3 3 3-3" />
                </svg>
                Generate Full Report →
              </>
            )}
          </button>
        </>
      )}
    </div>
  )
}
