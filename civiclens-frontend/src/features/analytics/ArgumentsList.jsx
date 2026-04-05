export default function ArgumentsList({ supporting = [], opposing = [] }) {
  const hasData = supporting.length > 0 || opposing.length > 0

  if (!hasData) {
    return (
      <div className="glass-card p-4 sm:p-5 text-center text-xs sm:text-sm text-dark-500">
        No classified arguments available yet.
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 gap-3 sm:gap-4">
      {/* Supporting Arguments */}
      {supporting.length > 0 && (
        <div className="glass-card p-4 sm:p-5">
          <h4 className="text-xs sm:text-sm font-semibold text-dark-200 mb-2 sm:mb-3 flex items-center gap-2">
            <span className="w-4 h-4 sm:w-5 sm:h-5 rounded-full bg-emerald-500/20 flex items-center justify-center">
              <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#34d399" strokeWidth="3" className="sm:w-[12px] sm:h-[12px]">
                <path d="M12 19V5M5 12l7-7 7 7" />
              </svg>
            </span>
            Top Supporting Arguments
          </h4>
          <div className="space-y-1.5 sm:space-y-2">
            {supporting.map((arg, idx) => (
              <div
                key={idx}
                className="flex gap-2 sm:gap-3 p-2.5 sm:p-3 bg-emerald-500/5 rounded-xl border border-emerald-500/10
                           hover:border-emerald-500/20 transition-all duration-200"
              >
                <span className="flex-shrink-0 w-4 h-4 sm:w-5 sm:h-5 rounded-full bg-emerald-500/20 
                               flex items-center justify-center text-[10px] sm:text-xs font-bold text-emerald-400 mt-0.5">
                  {idx + 1}
                </span>
                <p className="text-xs sm:text-sm text-dark-300 leading-relaxed">{arg}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Opposing Arguments */}
      {opposing.length > 0 && (
        <div className="glass-card p-4 sm:p-5">
          <h4 className="text-xs sm:text-sm font-semibold text-dark-200 mb-2 sm:mb-3 flex items-center gap-2">
            <span className="w-4 h-4 sm:w-5 sm:h-5 rounded-full bg-rose-500/20 flex items-center justify-center">
              <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#f87171" strokeWidth="3" className="sm:w-[12px] sm:h-[12px]">
                <path d="M12 5v14M19 12l-7 7-7-7" />
              </svg>
            </span>
            Top Opposing Arguments
          </h4>
          <div className="space-y-1.5 sm:space-y-2">
            {opposing.map((arg, idx) => (
              <div
                key={idx}
                className="flex gap-2 sm:gap-3 p-2.5 sm:p-3 bg-rose-500/5 rounded-xl border border-rose-500/10
                           hover:border-rose-500/20 transition-all duration-200"
              >
                <span className="flex-shrink-0 w-4 h-4 sm:w-5 sm:h-5 rounded-full bg-rose-500/20 
                               flex items-center justify-center text-[10px] sm:text-xs font-bold text-rose-400 mt-0.5">
                  {idx + 1}
                </span>
                <p className="text-xs sm:text-sm text-dark-300 leading-relaxed">{arg}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
