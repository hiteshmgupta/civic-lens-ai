export default function ControversyScore({ score, label, analytics }) {
  if (score === null || score === undefined) return null

  const percentage = Math.round(score * 100)

  const colorMap = {
    Low: { ring: 'stroke-emerald-400', text: 'text-emerald-400', bg: 'bg-emerald-500/10', border: 'border-emerald-500/20' },
    Moderate: { ring: 'stroke-amber-400', text: 'text-amber-400', bg: 'bg-amber-500/10', border: 'border-amber-500/20' },
    High: { ring: 'stroke-orange-400', text: 'text-orange-400', bg: 'bg-orange-500/10', border: 'border-orange-500/20' },
    Extreme: { ring: 'stroke-rose-400', text: 'text-rose-400', bg: 'bg-rose-500/10', border: 'border-rose-500/20' },
  }

  const colors = colorMap[label] || colorMap.Low

  // SVG circular gauge
  const radius = 54
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (score * circumference)

  return (
    <div className="glass-card p-4 sm:p-5">
      <h4 className="text-xs sm:text-sm font-semibold text-dark-200 mb-3 sm:mb-4 flex items-center gap-2">
        <span className="w-1.5 h-1.5 rounded-full bg-civic-400" />
        Controversy Index
      </h4>

      <div className="flex flex-col items-center">
        {/* Circular Gauge */}
        <div className="relative w-28 h-28 sm:w-36 sm:h-36 mb-3 sm:mb-4">
          <svg className="w-full h-full transform -rotate-90" viewBox="0 0 120 120">
            {/* Background ring */}
            <circle
              cx="60"
              cy="60"
              r={radius}
              fill="none"
              stroke="#1e293b"
              strokeWidth="8"
            />
            {/* Score ring */}
            <circle
              cx="60"
              cy="60"
              r={radius}
              fill="none"
              className={colors.ring}
              strokeWidth="8"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              style={{ transition: 'stroke-dashoffset 1s ease-in-out' }}
            />
          </svg>
          {/* Center text */}
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className={`text-2xl sm:text-3xl font-bold font-mono ${colors.text}`}>
              {percentage}
            </span>
            <span className="text-[9px] sm:text-[10px] text-dark-500 uppercase tracking-wider">Score</span>
          </div>
        </div>

        {/* Label Badge */}
        <div className={`px-3 sm:px-4 py-1 sm:py-1.5 rounded-full text-xs sm:text-sm font-semibold border ${colors.bg} ${colors.text} ${colors.border}`}>
          {label || 'Low'} Controversy
        </div>
      </div>

      {/* Breakdown */}
      {analytics && (
        <div className="mt-4 sm:mt-5 pt-3 sm:pt-4 border-t border-dark-700/50 space-y-2 sm:space-y-2.5">
          <BreakdownRow
            label="Sentiment Variance (S)"
            value={analytics.sentimentVariance}
            textLabel={getSentimentLabel(analytics.sentimentVariance)}
          />
          <BreakdownRow
            label="Vote Polarity (P)"
            value={analytics.votePolarity}
            textLabel={getPolarityLabel(analytics.votePolarity)}
          />
          <BreakdownRow
            label="Stance Entropy (D)"
            value={analytics.stanceEntropy}
            textLabel={getEntropyLabel(analytics.stanceEntropy)}
          />
          <BreakdownRow
            label="Engagement (E)"
            value={analytics.engagementScore}
            textLabel={getEngagementLabel(analytics.engagementScore)}
          />
        </div>
      )}
    </div>
  )
}

// Admin-Friendly Helper Functions
function getSentimentLabel(val) {
  if (val < 0.25) return "Highly Uniform"
  if (val < 0.50) return "Mostly Consistent"
  if (val < 0.75) return "Moderately Divided"
  return "Highly Divided"
}

function getPolarityLabel(val) {
  if (val < 0.25) return "Unanimous"
  if (val < 0.50) return "Strongly Skewed"
  if (val < 0.75) return "Moderately Split"
  return "Evenly Split"
}

function getEntropyLabel(val) {
  if (val < 0.25) return "Single Narrative"
  if (val < 0.50) return "Few Perspectives"
  if (val < 0.75) return "Multiple Views"
  return "Highly Diverse"
}

function getEngagementLabel(val) {
  if (val < 0.25) return "Low Activity"
  if (val < 0.50) return "Moderate Activity"
  if (val < 0.75) return "High Traffic"
  return "Viral Activity"
}

function BreakdownRow({ label, value, textLabel }) {
  if (value === null || value === undefined) return null
  const pct = Math.round(value * 100)
  return (
    <div>
      <div className="flex justify-between text-[10px] sm:text-xs mb-1">
        <span className="text-dark-400">
          {label} {textLabel && <span className="text-dark-500 ml-1 hidden sm:inline">· {textLabel}</span>}
        </span>
        <span className="text-dark-300 font-mono">{value.toFixed(3)}</span>
      </div>
      <div className="h-1 sm:h-1.5 bg-dark-800 rounded-full overflow-hidden">
        <div
          className="h-full bg-civic-400/60 rounded-full transition-all duration-700"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}
