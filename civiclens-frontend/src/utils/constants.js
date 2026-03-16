export const CATEGORIES = [
  'HEALTHCARE', 'AGRICULTURE', 'EDUCATION', 'INFRASTRUCTURE',
  'DIGITAL_PRIVACY', 'ENVIRONMENT', 'TAXATION', 'DEFENSE', 'OTHER'
]

export const SORTS = [
  { value: 'LATEST', label: 'Latest' },
]

export const CATEGORY_COLORS = {
  HEALTHCARE: 'bg-rose-500/20 text-rose-400 border-rose-500/30',
  AGRICULTURE: 'bg-green-500/20 text-green-400 border-green-500/30',
  EDUCATION: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  INFRASTRUCTURE: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
  DIGITAL_PRIVACY: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
  ENVIRONMENT: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
  TAXATION: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  DEFENSE: 'bg-red-500/20 text-red-400 border-red-500/30',
  OTHER: 'bg-gray-500/20 text-gray-400 border-gray-500/30',
}

export function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric'
  })
}

export function formatDateTime(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}
