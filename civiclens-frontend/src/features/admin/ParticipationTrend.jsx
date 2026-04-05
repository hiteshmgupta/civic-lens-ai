import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

export default function ParticipationTrend({ dashboard }) {
  if (!dashboard) return null

  const { participationTrend } = dashboard

  if (!participationTrend || participationTrend.length === 0) {
    return (
      <div className="glass-card p-4 sm:p-6">
        <h3 className="section-title text-sm sm:text-lg">Participation Growth Trend</h3>
        <div className="text-center text-xs sm:text-sm text-dark-500 py-6 sm:py-8">
          No participation data available yet.
        </div>
      </div>
    )
  }

  return (
    <div className="glass-card p-4 sm:p-6">
      <h3 className="section-title flex items-center gap-2 text-sm sm:text-lg">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#c8ee44" strokeWidth="2" className="sm:w-[18px] sm:h-[18px]">
          <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
          <circle cx="9" cy="7" r="4" />
          <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
          <path d="M16 3.13a4 4 0 0 1 0 7.75" />
        </svg>
        Participation Growth Trend
      </h3>
      <div className="h-44 sm:h-56">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={participationTrend} margin={{ top: 5, right: 5, bottom: 5, left: -20 }}>
            <XAxis
              dataKey="period"
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#64748b', fontSize: 10 }}
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#64748b', fontSize: 10 }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid #334155',
                borderRadius: '12px',
                fontSize: '11px',
                color: '#e2e8f0',
              }}
            />
            <Bar
              dataKey="comments"
              fill="#c8ee44"
              radius={[6, 6, 0, 0]}
              maxBarSize={32}
              name="Comments"
            />
            <Bar
              dataKey="votes"
              fill="#64748b"
              radius={[6, 6, 0, 0]}
              maxBarSize={32}
              name="Votes"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
