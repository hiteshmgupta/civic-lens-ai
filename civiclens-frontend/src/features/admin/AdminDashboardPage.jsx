import { useState, useEffect } from 'react'
import { getAdminDashboard } from '../../api/analyticsApi'
import CreateAmendmentForm from './CreateAmendmentForm'
import GlobalSentimentOverview from './GlobalSentimentOverview'
import ParticipationTrend from './ParticipationTrend'
import TopControversial from './TopControversial'
import { PageLoader } from '../../components/LoadingSpinner'

export default function AdminDashboardPage() {
  const [dashboard, setDashboard] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')

  const fetchDashboard = async () => {
    try {
      const res = await getAdminDashboard()
      setDashboard(res.data)
    } catch (err) {
      console.error('Failed to load dashboard:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchDashboard()
  }, [])

  const tabs = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'create', label: 'Create Amendment', icon: '➕' },
  ]

  return (
    <div className="space-y-4 sm:space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-xl sm:text-2xl font-bold text-dark-100 flex items-center gap-2 sm:gap-3">
          <div className="w-8 h-8 sm:w-10 sm:h-10 bg-civic-400/20 rounded-xl flex items-center justify-center">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#c8ee44" strokeWidth="2" className="sm:w-5 sm:h-5">
              <rect x="3" y="3" width="18" height="18" rx="2" />
              <path d="M3 9h18" />
              <path d="M9 21V9" />
            </svg>
          </div>
          Admin Dashboard
        </h1>
        <p className="text-xs sm:text-sm text-dark-400 mt-1">
          Manage amendments and monitor platform intelligence metrics
        </p>
      </div>

      {/* Tabs */}
      <div className="flex items-center bg-dark-900/60 rounded-xl p-1 border border-dark-700/50 w-full sm:w-fit overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex-1 sm:flex-none px-3 sm:px-5 py-2 sm:py-2.5 text-xs sm:text-sm font-medium rounded-lg transition-all duration-200 flex items-center justify-center gap-1.5 sm:gap-2 whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-dark-700 text-civic-400 shadow-sm'
                : 'text-dark-400 hover:text-dark-200'
            }`}
          >
            <span>{tab.icon}</span>
            {tab.label}
          </button>
        ))}
      </div>

      {loading ? (
        <PageLoader />
      ) : activeTab === 'overview' ? (
        <div className="space-y-4 sm:space-y-6">
          {/* Stat Cards */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-2 sm:gap-4">
            <StatCard
              label="Total Amendments"
              value={dashboard?.totalAmendments || 0}
              icon="📜"
              color="text-civic-400"
            />
            <StatCard
              label="Active"
              value={dashboard?.activeAmendments || 0}
              icon="🟢"
              color="text-emerald-400"
            />
            <StatCard
              label="Total Comments"
              value={dashboard?.totalComments || 0}
              icon="💬"
              color="text-blue-400"
            />
            <StatCard
              label="Total Votes"
              value={dashboard?.totalVotes || 0}
              icon="🗳️"
              color="text-purple-400"
            />
          </div>

          {/* Charts Row */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
            <GlobalSentimentOverview dashboard={dashboard} />
            <ParticipationTrend dashboard={dashboard} />
          </div>

          {/* Most Controversial */}
          <TopControversial amendments={dashboard?.mostControversial} />
        </div>
      ) : (
        <CreateAmendmentForm onCreated={() => {
          fetchDashboard()
          setActiveTab('overview')
        }} />
      )}
    </div>
  )
}

function StatCard({ label, value, icon, color }) {
  return (
    <div className="stat-card hover:border-civic-400/20 transition-all duration-200 p-3 sm:p-5">
      <div className="flex items-center gap-1.5 sm:gap-2">
        <span className="text-sm sm:text-lg">{icon}</span>
        <span className="text-[10px] sm:text-xs text-dark-500 uppercase tracking-wider truncate">{label}</span>
      </div>
      <span className={`text-xl sm:text-2xl font-bold ${color} mt-0.5 sm:mt-1`}>
        {typeof value === 'number' ? value.toLocaleString() : value}
      </span>
    </div>
  )
}
