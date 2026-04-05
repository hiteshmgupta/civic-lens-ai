import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts'

export default function SentimentTimeline({ timeline }) {
  if (!timeline || timeline.length === 0) {
    return (
      <div className="glass-card p-4 sm:p-5 text-center text-xs sm:text-sm text-dark-500">
        No timeline data available yet.
      </div>
    )
  }

  return (
    <div className="glass-card p-4 sm:p-5">
      <h4 className="text-xs sm:text-sm font-semibold text-dark-200 mb-3 sm:mb-4 flex items-center gap-2">
        <span className="w-1.5 h-1.5 rounded-full bg-civic-400" />
        Sentiment Timeline
      </h4>
      <div className="h-36 sm:h-48">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={timeline} margin={{ top: 5, right: 5, bottom: 5, left: -20 }}>
            <defs>
              <linearGradient id="sentimentGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#c8ee44" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#c8ee44" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis
              dataKey="bucket"
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#64748b', fontSize: 10 }}
            />
            <YAxis
              domain={[-1, 1]}
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#64748b', fontSize: 10 }}
              tickFormatter={(v) => v.toFixed(1)}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid #334155',
                borderRadius: '12px',
                fontSize: '11px',
                color: '#e2e8f0',
              }}
              formatter={(value) => [value.toFixed(3), 'Avg Sentiment']}
              labelFormatter={(label) => `Bucket ${label}`}
            />
            <ReferenceLine y={0} stroke="#334155" strokeDasharray="3 3" />
            <Area
              type="monotone"
              dataKey="avg_sentiment"
              stroke="#c8ee44"
              strokeWidth={2}
              fill="url(#sentimentGradient)"
              dot={{ r: 2, fill: '#c8ee44', strokeWidth: 0 }}
              activeDot={{ r: 4, fill: '#c8ee44', strokeWidth: 2, stroke: '#0a0f1a' }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
