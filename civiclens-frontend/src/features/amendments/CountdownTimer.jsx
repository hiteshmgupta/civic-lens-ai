import useCountdown from '../../hooks/useCountdown'

export default function CountdownTimer({ closesAt, compact = false }) {
  const timeLeft = useCountdown(closesAt)

  if (!closesAt || !timeLeft) return null

  if (timeLeft.expired) {
    return (
      <div className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-dark-700/60 rounded-lg">
        <span className="w-2 h-2 rounded-full bg-dark-500" />
        <span className="text-xs font-medium text-dark-400">Closed</span>
      </div>
    )
  }

  const isUrgent = timeLeft.days === 0 && timeLeft.hours < 6
  const isWarning = timeLeft.days === 0

  if (compact) {
    return (
      <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg ${
        isUrgent ? 'bg-rose-500/10 border border-rose-500/20' :
        isWarning ? 'bg-amber-500/10 border border-amber-500/20' :
        'bg-dark-700/60'
      }`}>
        <span className={`w-2 h-2 rounded-full animate-pulse ${
          isUrgent ? 'bg-rose-400' : isWarning ? 'bg-amber-400' : 'bg-emerald-400'
        }`} />
        <span className={`text-xs font-mono font-medium ${
          isUrgent ? 'text-rose-400' : isWarning ? 'text-amber-400' : 'text-dark-300'
        }`}>
          {timeLeft.days > 0 && `${timeLeft.days}d `}
          {String(timeLeft.hours).padStart(2, '0')}:
          {String(timeLeft.minutes).padStart(2, '0')}:
          {String(timeLeft.seconds).padStart(2, '0')}
        </span>
      </div>
    )
  }

  return (
    <div className={`glass-card p-4 ${isUrgent ? 'border-rose-500/30' : isWarning ? 'border-amber-500/30' : ''}`}>
      <div className="flex items-center gap-2 mb-3">
        <span className={`w-2 h-2 rounded-full animate-pulse ${
          isUrgent ? 'bg-rose-400' : isWarning ? 'bg-amber-400' : 'bg-emerald-400'
        }`} />
        <span className="text-xs font-medium text-dark-400 uppercase tracking-wider">
          {isUrgent ? 'Closing Soon' : 'Time Remaining'}
        </span>
      </div>
      <div className="grid grid-cols-4 gap-2 text-center">
        {[
          { val: timeLeft.days, label: 'Days' },
          { val: timeLeft.hours, label: 'Hours' },
          { val: timeLeft.minutes, label: 'Min' },
          { val: timeLeft.seconds, label: 'Sec' },
        ].map(({ val, label }) => (
          <div key={label}>
            <div className={`text-xl font-bold font-mono ${
              isUrgent ? 'text-rose-400' : isWarning ? 'text-amber-400' : 'text-dark-100'
            }`}>
              {String(val).padStart(2, '0')}
            </div>
            <div className="text-[10px] text-dark-500 uppercase tracking-wider">{label}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
