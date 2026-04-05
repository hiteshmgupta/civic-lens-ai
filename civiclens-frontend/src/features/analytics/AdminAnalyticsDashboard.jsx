import { useState, useEffect } from 'react'
import { getAnalytics, triggerAnalysis, downloadReport } from '../../api/analyticsApi'
import SentimentChart from './SentimentChart'
import SentimentTimeline from './SentimentTimeline'
import TopicClusters from './TopicClusters'
import ArgumentsList from './ArgumentsList'
import EngagementMetrics from './EngagementMetrics'
import ControversyScore from './ControversyScore'
import PolicyBrief from './PolicyBrief'
import LoadingSpinner from '../../components/LoadingSpinner'

export default function AdminAnalyticsDashboard({ amendmentId }) {
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
      <div className="glass-card p-6 sm:p-8 flex items-center justify-center">
        <LoadingSpinner size="md" />
      </div>
    )
  }

  const hasData = analytics && analytics.totalComments > 0

  return (
    <div className="space-y-3 sm:space-y-4">
      {/* Dashboard Header */}
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h3 className="text-base sm:text-lg font-bold text-dark-100 flex items-center gap-2">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#c8ee44" strokeWidth="2" className="sm:w-5 sm:h-5">
            <path d="M21 21H4.6c-.56 0-.84 0-1.05-.11a1 1 0 0 1-.44-.44C3 20.24 3 19.96 3 19.4V3" />
            <path d="M7 14l4-4 4 4 6-6" />
          </svg>
          Impact Analysis
        </h3>
        <div className="flex items-center gap-2">
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
          {hasData && (
            <button
              onClick={handleExportPdf}
              disabled={exporting}
              className="btn-ghost text-[10px] sm:text-xs disabled:opacity-50 flex items-center gap-1 sm:gap-1.5"
            >
              {exporting ? (
                <LoadingSpinner size="sm" />
              ) : (
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="sm:w-[14px] sm:h-[14px]">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <path d="M14 2v6h6" />
                  <path d="M12 18v-6M9 15l3 3 3-3" />
                </svg>
              )}
              {exporting ? 'Exporting...' : 'Export PDF'}
            </button>
          )}
        </div>
      </div>

      {error && (
        <div className="p-2.5 sm:p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-[10px] sm:text-xs">
          ⚠️ {error}
        </div>
      )}

      {!hasData ? (
        <div className="glass-card p-6 sm:p-8 text-center">
          <div className="text-3xl sm:text-4xl mb-3">🔬</div>
          <h4 className="text-dark-200 font-semibold mb-2 text-sm sm:text-base">No Analysis Available</h4>
          <p className="text-xs sm:text-sm text-dark-400 mb-4">
            Click Re-analyze above to run analysis on existing comments.
          </p>
        </div>
      ) : (
        <>
          {/* === KPI Row: 3 cols on desktop, 2 on tablet, 1 on mobile === */}
          <div className="analytics-dashboard-grid items-stretch">
            <div className="flex flex-col">
              <ControversyScore
                score={analytics.controversyScore}
                label={analytics.controversyLabel}
                analytics={analytics}
              />
            </div>
            <div className="flex flex-col flex-1">
              <SentimentChart distribution={analytics.sentimentDistribution} />
            </div>
            <div className="flex flex-col flex-1 sm:col-span-2 lg:col-span-1">
              <EngagementMetrics analytics={analytics} />
            </div>
          </div>

          {/* === Sentiment Timeline: always full width === */}
          <SentimentTimeline timeline={analytics.sentimentTimeline} />

          {/* === Bottom section: Topics+Brief stacked left, Arguments right (wide) === */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-3 lg:gap-4 items-stretch">
            {/* Left column — stacked small widgets */}
            <div className="flex flex-col gap-3 lg:gap-4 lg:col-span-1">
              <TopicClusters clusters={analytics.topicClusters} />
              <div className="flex-1 flex flex-col">
                <PolicyBrief brief={analytics.policyBrief} />
              </div>
            </div>

            {/* Right column — arguments, takes 2/3 width on desktop */}
            <div className="lg:col-span-2 flex flex-col">
              <div className="flex-1">
                <ArgumentsList
                  supporting={analytics.topSupporting}
                  opposing={analytics.topOpposing}
                />
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
