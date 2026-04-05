export default function PolicyBrief({ brief }) {
  if (!brief) {
    return (
      <div className="glass-card p-4 sm:p-5 text-center text-xs sm:text-sm text-dark-500">
        Policy brief not generated yet.
      </div>
    )
  }

  return (
    <div className="glass-card p-4 sm:p-5">
      <h4 className="text-xs sm:text-sm font-semibold text-dark-200 mb-2 sm:mb-3 flex items-center gap-2">
        <span className="w-4 h-4 sm:w-5 sm:h-5 rounded-full bg-civic-400/20 flex items-center justify-center">
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#c8ee44" strokeWidth="2.5" className="sm:w-[12px] sm:h-[12px]">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <path d="M14 2v6h6" />
            <path d="M16 13H8M16 17H8M10 9H8" />
          </svg>
        </span>
        Policy Brief
      </h4>
      <div className="bg-dark-800/40 rounded-xl p-3 sm:p-4 border border-dark-700/30">
        <p className="text-xs sm:text-sm text-dark-300 leading-relaxed whitespace-pre-wrap">
          {brief}
        </p>
      </div>
    </div>
  )
}
