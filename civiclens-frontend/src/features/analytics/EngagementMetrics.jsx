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
    <div className="glass-card p-4 sm:p-5 flex flex-col h-full">
      <h4 className="text-xs sm:text-sm font-semibold text-dark-200 mb-3 sm:mb-4 flex items-center gap-2">
        <span className="w-1.5 h-1.5 rounded-full bg-civic-400" />
        Engagement Metrics
      </h4>
      {/* Metric tiles — grow to fill space */}
      <div className="grid grid-cols-2 gap-2 sm:gap-3 flex-1">
        {metrics.map((m) => (
          <div
            key={m.label}
            className="bg-dark-800/50 rounded-xl p-3 sm:p-4 border border-dark-700/30
                       hover:border-dark-600/50 transition-all duration-200 flex flex-col justify-between"
          >
            <div className="flex items-center gap-1.5 mb-2">
              <span className="text-base sm:text-lg">{m.icon}</span>
              <span className="text-[10px] sm:text-xs text-dark-500 truncate">{m.label}</span>
            </div>
            <span className={`text-2xl sm:text-3xl font-bold ${m.color}`}>
              {m.value.toLocaleString()}
            </span>
          </div>
        ))}
      </div>

      {/* Vote Polarity Bar — pinned to bottom */}
      {analytics.totalVotes > 0 && (
        <div className="mt-3 sm:mt-4">
          <div className="flex justify-between text-[10px] sm:text-xs text-dark-500 mb-1.5">
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
