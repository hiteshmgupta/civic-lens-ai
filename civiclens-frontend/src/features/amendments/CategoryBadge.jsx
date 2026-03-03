import { CATEGORY_COLORS } from '../../utils/constants'

const CATEGORY_ICONS = {
  HEALTHCARE: '🏥',
  AGRICULTURE: '🌾',
  EDUCATION: '📚',
  INFRASTRUCTURE: '🏗️',
  DIGITAL_PRIVACY: '🔒',
  ENVIRONMENT: '🌿',
  TAXATION: '💰',
  DEFENSE: '🛡️',
  OTHER: '📋',
}

export default function CategoryBadge({ category, size = 'sm' }) {
  const colorClass = CATEGORY_COLORS[category] || CATEGORY_COLORS.OTHER
  const icon = CATEGORY_ICONS[category] || CATEGORY_ICONS.OTHER
  const label = category?.replace('_', ' ') || 'Other'

  const sizeClasses = {
    sm: 'px-2.5 py-0.5 text-xs',
    md: 'px-3 py-1 text-sm',
    lg: 'px-4 py-1.5 text-sm',
  }

  return (
    <span
      className={`inline-flex items-center gap-1.5 font-semibold rounded-full border
        ${colorClass} ${sizeClasses[size]} transition-all duration-200 hover:scale-105`}
    >
      <span>{icon}</span>
      <span>{label}</span>
    </span>
  )
}
