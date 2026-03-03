export default function PolicyBrief({ brief }) {
  if (!brief) {
    return (
      <div className="glass-card p-5 text-center text-sm text-dark-500">
        AI policy brief not generated yet.
      </div>
    )
  }

  return (
    <div className="glass-card p-5">
      <h4 className="text-sm font-semibold text-dark-200 mb-3 flex items-center gap-2">
        <span className="w-5 h-5 rounded-full bg-civic-400/20 flex items-center justify-center">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#c8ee44" strokeWidth="2.5">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <path d="M14 2v6h6" />
            <path d="M16 13H8M16 17H8M10 9H8" />
          </svg>
        </span>
        AI-Generated Policy Brief
      </h4>
      <div className="bg-dark-800/40 rounded-xl p-4 border border-dark-700/30">
        <p className="text-sm text-dark-300 leading-relaxed whitespace-pre-wrap">
          {brief}
        </p>
      </div>
      <div className="flex items-center gap-2 mt-3">
        <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-civic-400/10 text-civic-400 text-[10px] font-semibold rounded-full">
          ✦ AI Generated
        </span>
        <span className="text-[10px] text-dark-600">
          Summarized using BART-large-CNN
        </span>
      </div>
    </div>
  )
}
