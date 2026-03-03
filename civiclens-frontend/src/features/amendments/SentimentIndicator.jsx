export default function SentimentIndicator({ score, size = 'sm' }) {
  if (score === null || score === undefined) return null

  const normalized = Math.max(-1, Math.min(1, score))
  const percentage = ((normalized + 1) / 2) * 100

  let color, label, bgColor
  if (normalized > 0.2) {
    color = 'text-emerald-400'
    bgColor = 'bg-emerald-400/10'
    label = 'Positive'
  } else if (normalized < -0.2) {
    color = 'text-rose-400'
    bgColor = 'bg-rose-400/10'
    label = 'Negative'
  } else {
    color = 'text-amber-400'
    bgColor = 'bg-amber-400/10'
    label = 'Neutral'
  }

  const sizeClasses = {
    sm: 'text-xs gap-1.5',
    md: 'text-sm gap-2',
    lg: 'text-base gap-2.5',
  }

  return (
    <div className={`inline-flex items-center ${sizeClasses[size]}`}>
      <div className={`flex items-center gap-1.5 px-2 py-0.5 rounded-full ${bgColor}`}>
        <div className="relative w-8 h-1.5 bg-dark-700 rounded-full overflow-hidden">
          <div
            className={`absolute top-0 left-0 h-full rounded-full transition-all duration-500 ${
              normalized > 0.2 ? 'bg-emerald-400' : normalized < -0.2 ? 'bg-rose-400' : 'bg-amber-400'
            }`}
            style={{ width: `${percentage}%` }}
          />
        </div>
        <span className={`font-semibold ${color}`}>
          {normalized > 0 ? '+' : ''}{normalized.toFixed(1)}
        </span>
      </div>
    </div>
  )
}

export function SentimentDot({ score }) {
  if (score === null || score === undefined) return null
  let color = 'bg-amber-400'
  if (score > 0.2) color = 'bg-emerald-400'
  else if (score < -0.2) color = 'bg-rose-400'

  return (
    <span className={`inline-block w-2 h-2 rounded-full ${color} animate-pulse-slow`} />
  )
}
