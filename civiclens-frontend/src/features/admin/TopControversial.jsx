import { Link } from 'react-router-dom'
import CategoryBadge from '../amendments/CategoryBadge'

export default function TopControversial({ amendments = [] }) {
  if (!amendments || amendments.length === 0) {
    return (
      <div className="glass-card p-4 sm:p-6">
        <h3 className="section-title text-sm sm:text-lg">Most Controversial Amendments</h3>
        <div className="text-center text-xs sm:text-sm text-dark-500 py-6 sm:py-8">
          No controversial amendments to show.
        </div>
      </div>
    )
  }

  return (
    <div className="glass-card p-4 sm:p-6">
      <h3 className="section-title flex items-center gap-2 text-sm sm:text-lg">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#c8ee44" strokeWidth="2" className="sm:w-[18px] sm:h-[18px]">
          <path d="M12 2L2 7l10 5 10-5-10-5z" />
          <path d="M2 17l10 5 10-5" />
          <path d="M2 12l10 5 10-5" />
        </svg>
        Most Controversial Amendments
      </h3>
      <div className="space-y-2 sm:space-y-3">
        {amendments.map((a, idx) => {
          const scoreColor =
            a.controversyLabel === 'Extreme' ? 'text-rose-400 bg-rose-500/10' :
            a.controversyLabel === 'High' ? 'text-orange-400 bg-orange-500/10' :
            a.controversyLabel === 'Moderate' ? 'text-amber-400 bg-amber-500/10' :
            'text-dark-400 bg-dark-700'

          return (
            <Link
              key={a.id}
              to={`/amendments/${a.id}`}
              className="flex items-center gap-2 sm:gap-4 p-2.5 sm:p-3 rounded-xl bg-dark-800/40 border border-dark-700/30
                         hover:border-civic-400/20 hover:bg-dark-800/70 transition-all duration-200 group"
            >
              {/* Rank */}
              <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-full bg-dark-700 flex items-center justify-center flex-shrink-0">
                <span className="text-xs sm:text-sm font-bold text-dark-300">#{idx + 1}</span>
              </div>

              {/* Info */}
              <div className="flex-1 min-w-0">
                <p className="text-xs sm:text-sm font-medium text-dark-200 truncate group-hover:text-civic-400 transition-colors">
                  {a.title}
                </p>
                <div className="flex items-center gap-1.5 sm:gap-2 mt-0.5 sm:mt-1">
                  <CategoryBadge category={a.category} size="sm" />
                  <span className="text-[10px] sm:text-xs text-dark-500 hidden sm:inline">{a.commentCount} comments</span>
                </div>
              </div>

              {/* Score */}
              <div className={`flex-shrink-0 px-2 sm:px-3 py-1 sm:py-1.5 rounded-xl text-xs sm:text-sm font-bold font-mono ${scoreColor}`}>
                {a.controversyScore != null ? (a.controversyScore * 100).toFixed(0) : '—'}
              </div>
            </Link>
          )
        })}
      </div>
    </div>
  )
}
