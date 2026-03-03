import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts'

const COLORS = {
  positive: '#34d399',
  negative: '#f87171',
  neutral: '#fbbf24',
}

export default function SentimentChart({ distribution }) {
  if (!distribution) return null

  const data = [
    { name: 'Positive', value: distribution.positive || 0, color: COLORS.positive },
    { name: 'Negative', value: distribution.negative || 0, color: COLORS.negative },
    { name: 'Neutral', value: distribution.neutral || 0, color: COLORS.neutral },
  ].filter(d => d.value > 0)

  const total = data.reduce((sum, d) => sum + d.value, 0)
  if (total === 0) return <EmptyState />

  return (
    <div className="glass-card p-5">
      <h4 className="text-sm font-semibold text-dark-200 mb-4 flex items-center gap-2">
        <span className="w-1.5 h-1.5 rounded-full bg-civic-400" />
        Sentiment Distribution
      </h4>
      <div className="flex items-center gap-6">
        <div className="w-32 h-32 flex-shrink-0">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={32}
                outerRadius={56}
                paddingAngle={3}
                dataKey="value"
                strokeWidth={0}
              >
                {data.map((entry, index) => (
                  <Cell key={index} fill={entry.color} />
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
        <div className="flex flex-col gap-2.5 flex-1">
          {data.map((item) => (
            <div key={item.name} className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                <span className="text-sm text-dark-300">{item.name}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm font-semibold text-dark-100">{item.value}</span>
                <span className="text-xs text-dark-500">
                  ({((item.value / total) * 100).toFixed(0)}%)
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function EmptyState() {
  return (
    <div className="glass-card p-5 text-center text-sm text-dark-500">
      No sentiment data available yet.
    </div>
  )
}
