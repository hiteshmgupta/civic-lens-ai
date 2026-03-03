export default function EngagementMetrics({ analytics }) {
  if (!analytics) return null

  const metrics = [
    {
      label: 'Total Comments',
      value: analytics.totalComments || 0,
      icon: '💬',
      color: 'text-blue-400',
    },
    {
      label: 'Total Votes',
      value: analytics.totalVotes || 0,
      icon: '🗳️',
      color: 'text-purple-400',
    },
    {
      label: 'Upvotes',
      value: analytics.upvotes || 0,
      icon: '👍',
      color: 'text-emerald-400',
    },
    {
      label: 'Downvotes',
      value: analytics.downvotes || 0,
      icon: '👎',
      color: 'text-rose-400',
    },
  ]

  return (
    <div className="glass-card p-5">
      <h4 className="text-sm font-semibold text-dark-200 mb-4 flex items-center gap-2">
        <span className="w-1.5 h-1.5 rounded-full bg-civic-400" />
        Engagement Metrics
      </h4>
      <div className="grid grid-cols-2 gap-3">
        {metrics.map((m) => (
          <div
            key={m.label}
            className="bg-dark-800/50 rounded-xl p-3 border border-dark-700/30
                       hover:border-dark-600/50 transition-all duration-200"
          >
            <div className="flex items-center gap-2 mb-1">
              <span className="text-base">{m.icon}</span>
              <span className="text-xs text-dark-500">{m.label}</span>
            </div>
            <span className={`text-xl font-bold ${m.color}`}>
              {m.value.toLocaleString()}
            </span>
          </div>
        ))}
      </div>

      {/* Vote Polarity Bar */}
      {analytics.totalVotes > 0 && (
        <div className="mt-4">
          <div className="flex justify-between text-xs text-dark-500 mb-1.5">
            <span>Vote Polarity</span>
            <span>{((analytics.votePolarity || 0) * 100).toFixed(0)}%</span>
          </div>
          <div className="h-2 bg-dark-800 rounded-full overflow-hidden flex">
            <div
              className="bg-emerald-400 transition-all duration-500"
              style={{
                width: `${analytics.totalVotes > 0
                  ? (analytics.upvotes / analytics.totalVotes) * 100
                  : 50}%`
              }}
            />
            <div
              className="bg-rose-400 transition-all duration-500"
              style={{
                width: `${analytics.totalVotes > 0
                  ? (analytics.downvotes / analytics.totalVotes) * 100
                  : 50}%`
              }}
            />
          </div>
        </div>
      )}
    </div>
  )
}
