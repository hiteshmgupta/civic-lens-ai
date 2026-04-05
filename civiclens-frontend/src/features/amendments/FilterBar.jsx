import { CATEGORIES, STATUS_FILTERS } from '../../utils/constants'

export default function FilterBar({ statusFilter, category, onStatusChange, onCategoryChange }) {
  return (
    <div className="flex flex-col sm:flex-row sm:flex-wrap items-stretch sm:items-center gap-2 sm:gap-3">
      {/* Status Tabs */}
      <div className="flex items-center bg-dark-900/60 rounded-xl p-1 border border-dark-700/50">
        {STATUS_FILTERS.map(({ value, label }) => (
          <button
            key={label}
            onClick={() => onStatusChange(value)}
            className={`flex-1 sm:flex-none px-3 sm:px-4 py-2 text-xs sm:text-sm font-medium rounded-lg transition-all duration-200 ${
              statusFilter === value
                ? 'bg-dark-700 text-civic-400 shadow-sm'
                : 'text-dark-400 hover:text-dark-200'
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Category Dropdown */}
      <div className="relative">
        <select
          value={category || ''}
          onChange={(e) => onCategoryChange(e.target.value || null)}
          className="appearance-none w-full sm:w-auto bg-dark-900/60 border border-dark-700/50 text-dark-200 text-xs sm:text-sm
                     rounded-xl px-3 sm:px-4 py-2.5 pr-8 outline-none cursor-pointer
                     transition-all duration-200 focus:border-civic-400/50 focus:ring-2 focus:ring-civic-400/20
                     hover:border-dark-600"
        >
          <option value="">All Categories</option>
          {CATEGORIES.map((cat) => (
            <option key={cat} value={cat}>
              {cat.replace('_', ' ')}
            </option>
          ))}
        </select>
        <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" className="text-dark-400">
            <path d="M6 9l6 6 6-6" />
          </svg>
        </div>
      </div>
    </div>
  )
}
