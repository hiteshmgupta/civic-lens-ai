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
    <div className="glass-card p-4 sm:p-5 flex flex-col h-full">
      <h4 className="text-xs sm:text-sm font-semibold text-dark-200 mb-3 sm:mb-4 flex items-center gap-2">
        <span className="w-1.5 h-1.5 rounded-full bg-civic-400" />
        Sentiment Distribution
      </h4>
      {/* Donut chart — grows to fill available space */}
      <div className="flex-1 min-h-0 flex items-center justify-center">
        <ResponsiveContainer width="100%" height={200}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={55}
              outerRadius={88}
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
      {/* Legend rows — pinned to bottom */}
      <div className="flex flex-col gap-2.5 mt-3">
        {data.map((item) => (
          <div key={item.name} className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <span className="w-3 h-3 rounded-full flex-shrink-0" style={{ backgroundColor: item.color }} />
              <span className="text-sm text-dark-300">{item.name}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-bold text-dark-100">{item.value}</span>
              <span className="text-xs text-dark-500">({((item.value / total) * 100).toFixed(0)}%)</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function EmptyState() {
  return (
    <div className="glass-card p-4 sm:p-5 text-center text-xs sm:text-sm text-dark-500">
      No sentiment data available yet.
    </div>
  )
}
