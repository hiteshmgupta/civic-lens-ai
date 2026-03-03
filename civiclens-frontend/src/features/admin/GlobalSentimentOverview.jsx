import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts'

const COLORS = ['#34d399', '#f87171', '#fbbf24']

export default function GlobalSentimentOverview({ dashboard }) {
  if (!dashboard) return null

  const { totalComments, globalSentimentDistribution } = dashboard

  const data = globalSentimentDistribution ? [
    { name: 'Positive', value: globalSentimentDistribution.positive || 0 },
    { name: 'Negative', value: globalSentimentDistribution.negative || 0 },
    { name: 'Neutral', value: globalSentimentDistribution.neutral || 0 },
  ].filter(d => d.value > 0) : []

  const total = data.reduce((sum, d) => sum + d.value, 0)

  return (
    <div className="glass-card p-6">
      <h3 className="section-title flex items-center gap-2">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#c8ee44" strokeWidth="2">
          <circle cx="12" cy="12" r="10" />
          <path d="M8 14s1.5 2 4 2 4-2 4-2" />
          <line x1="9" y1="9" x2="9.01" y2="9" />
          <line x1="15" y1="9" x2="15.01" y2="9" />
        </svg>
        Global Sentiment Overview
      </h3>

      {total === 0 ? (
        <div className="text-center text-sm text-dark-500 py-8">
          No sentiment data available yet.
        </div>
      ) : (
        <div className="flex items-center gap-6">
          <div className="w-40 h-40 flex-shrink-0">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data}
                  cx="50%"
                  cy="50%"
                  innerRadius={40}
                  outerRadius={65}
                  paddingAngle={3}
                  dataKey="value"
                  strokeWidth={0}
                >
                  {data.map((entry, index) => (
                    <Cell key={index} fill={COLORS[index]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1e293b',
                    border: '1px solid #334155',
                    borderRadius: '12px',
                    fontSize: '12px',
                    color: '#e2e8f0',
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex-1 space-y-3">
            {data.map((item, idx) => {
              const pct = ((item.value / total) * 100).toFixed(1)
              return (
                <div key={item.name}>
                  <div className="flex items-center justify-between mb-1">
                    <div className="flex items-center gap-2">
                      <span className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS[idx] }} />
                      <span className="text-sm text-dark-300">{item.name}</span>
                    </div>
                    <span className="text-sm font-semibold text-dark-100">{pct}%</span>
                  </div>
                  <div className="h-1.5 bg-dark-800 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-700"
                      style={{ width: `${pct}%`, backgroundColor: COLORS[idx] }}
                    />
                  </div>
                </div>
              )
            })}
            <div className="pt-2 border-t border-dark-700/50">
              <span className="text-xs text-dark-500">
                Total Comments: <span className="text-dark-300 font-semibold">{totalComments?.toLocaleString()}</span>
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
