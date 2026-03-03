import { useState, useEffect, useRef } from 'react'

export default function useCountdown(targetDate) {
  const [timeLeft, setTimeLeft] = useState(calcTimeLeft(targetDate))
  const intervalRef = useRef(null)

  useEffect(() => {
    if (!targetDate) return
    intervalRef.current = setInterval(() => {
      setTimeLeft(calcTimeLeft(targetDate))
    }, 1000)
    return () => clearInterval(intervalRef.current)
  }, [targetDate])

  return timeLeft
}

function calcTimeLeft(targetDate) {
  if (!targetDate) return null
  const diff = new Date(targetDate) - new Date()
  if (diff <= 0) return { expired: true, days: 0, hours: 0, minutes: 0, seconds: 0 }
  return {
    expired: false,
    days: Math.floor(diff / (1000 * 60 * 60 * 24)),
    hours: Math.floor((diff / (1000 * 60 * 60)) % 24),
    minutes: Math.floor((diff / (1000 * 60)) % 60),
    seconds: Math.floor((diff / 1000) % 60),
  }
}
