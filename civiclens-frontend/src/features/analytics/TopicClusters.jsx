export default function TopicClusters({ clusters }) {
  if (!clusters || clusters.length === 0) {
    return (
      <div className="glass-card p-5 text-center text-sm text-dark-500">
        Not enough data for topic modeling.
      </div>
    )
  }

  const maxSize = Math.max(...clusters.map(c => c.size))

  return (
    <div className="glass-card p-5">
      <h4 className="text-sm font-semibold text-dark-200 mb-4 flex items-center gap-2">
        <span className="w-1.5 h-1.5 rounded-full bg-civic-400" />
        Key Topic Clusters
      </h4>
      <div className="space-y-3">
        {clusters.map((cluster, idx) => (
          <div key={idx} className="group">
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-sm text-dark-200 font-medium truncate pr-4 max-w-[70%]">
                {cluster.topic}
              </span>
              <span className="text-xs text-dark-500 flex-shrink-0">
                {cluster.size} mention{cluster.size !== 1 ? 's' : ''}
              </span>
            </div>
            <div className="relative h-2 bg-dark-800 rounded-full overflow-hidden">
              <div
                className="absolute top-0 left-0 h-full rounded-full bg-gradient-to-r from-civic-400/80 to-civic-500
                           transition-all duration-700 ease-out"
                style={{ width: `${(cluster.size / maxSize) * 100}%` }}
              />
            </div>
            {cluster.keywords && cluster.keywords.length > 0 && (
              <div className="flex flex-wrap gap-1.5 mt-2">
                {cluster.keywords.slice(0, 4).map((kw, i) => (
                  <span
                    key={i}
                    className="px-2 py-0.5 text-[10px] bg-dark-800 text-dark-400 rounded-md border border-dark-700/50"
                  >
                    {kw}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
