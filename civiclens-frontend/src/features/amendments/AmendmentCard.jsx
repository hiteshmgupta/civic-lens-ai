import { Link } from 'react-router-dom'
import CategoryBadge from './CategoryBadge'
import SentimentIndicator from './SentimentIndicator'
import CountdownTimer from './CountdownTimer'

export default function AmendmentCard({ amendment }) {
  const {
    id, title, body, category, status, createdAt, closesAt,
    createdByUsername, commentCount,
    sentimentMean, controversyScore, controversyLabel
  } = amendment

  return (
    <div className="glass-card-hover p-0 overflow-hidden animate-fade-in group">
      {/* Content */}
      <div className="p-3 sm:p-4 min-w-0">
        {/* Header row */}
        <div className="flex flex-wrap items-center gap-1.5 sm:gap-2 mb-2">
          <CategoryBadge category={category} size="sm" />
          {status === 'CLOSED' && (
            <span className="badge bg-dark-700 text-dark-400 border border-dark-600">
              Closed
            </span>
          )}
          {closesAt && status === 'ACTIVE' && (
            <CountdownTimer closesAt={closesAt} compact />
          )}
          <SentimentIndicator score={sentimentMean} size="sm" />
        </div>

        {/* Title */}
        <Link
          to={`/amendments/${id}`}
          className="block group/title"
        >
          <h3 className="text-base sm:text-lg font-semibold text-dark-100 mb-1 sm:mb-1.5 
                         group-hover/title:text-civic-400 transition-colors duration-200 line-clamp-2">
            {title}
          </h3>
        </Link>

        {/* Body preview */}
        <p className="text-xs sm:text-sm text-dark-400 mb-2 sm:mb-3 line-clamp-2 leading-relaxed">
          {body}
        </p>

        {/* Footer */}
        <div className="flex flex-wrap items-center gap-2 sm:gap-4 text-[10px] sm:text-xs text-dark-500">
          <span className="flex items-center gap-1">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="sm:w-[14px] sm:h-[14px]">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
            {createdByUsername}
          </span>
          <span className="flex items-center gap-1">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="sm:w-[14px] sm:h-[14px]">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
            </svg>
            {commentCount} comments
          </span>
          <span className="hidden xs:inline">
            {new Date(createdAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
          </span>
          {controversyScore != null && controversyScore > 0 && (
            <span className={`flex items-center gap-1 px-1.5 sm:px-2 py-0.5 rounded-full text-[10px] sm:text-xs font-semibold ${
              controversyLabel === 'Extreme' ? 'bg-rose-500/15 text-rose-400' :
              controversyLabel === 'High' ? 'bg-orange-500/15 text-orange-400' :
              controversyLabel === 'Moderate' ? 'bg-amber-500/15 text-amber-400' :
              'bg-dark-700 text-dark-400'
            }`}>
              🔥 {(controversyScore * 100).toFixed(0)}
            </span>
          )}
        </div>
      </div>
    </div>
  )
}
