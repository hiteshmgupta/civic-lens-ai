import { useState } from 'react'
import { createAmendment } from '../../api/amendmentApi'
import { CATEGORIES } from '../../utils/constants'

export default function CreateAmendmentForm({ onCreated }) {
  const [form, setForm] = useState({
    title: '',
    body: '',
    category: 'HEALTHCARE',
    closesAt: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const handleChange = (field, value) => {
    setForm(prev => ({ ...prev, [field]: value }))
    setError(null)
    setSuccess(false)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.title.trim() || !form.body.trim()) {
      setError('Title and body are required')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const payload = {
        ...form,
        closesAt: form.closesAt ? new Date(form.closesAt).toISOString() : null,
      }
      await createAmendment(payload)
      setSuccess(true)
      setForm({ title: '', body: '', category: 'HEALTHCARE', closesAt: '' })
      onCreated?.()
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to create amendment')
    } finally {
      setLoading(false)
    }
  }

  // Default to 7 days from now for the timer
  const defaultClosesAt = () => {
    const d = new Date()
    d.setDate(d.getDate() + 7)
    return d.toISOString().slice(0, 16)
  }

  return (
    <div className="glass-card p-4 sm:p-6">
      <h3 className="section-title flex items-center gap-2 text-sm sm:text-lg">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#c8ee44" strokeWidth="2" className="sm:w-[18px] sm:h-[18px]">
          <path d="M12 5v14M5 12h14" />
        </svg>
        Create New Amendment
      </h3>

      <form onSubmit={handleSubmit} className="space-y-3 sm:space-y-4">
        {error && (
          <div className="p-2.5 sm:p-3 bg-rose-500/10 border border-rose-500/20 rounded-xl text-rose-400 text-xs sm:text-sm">
            {error}
          </div>
        )}
        {success && (
          <div className="p-2.5 sm:p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-400 text-xs sm:text-sm">
            ✓ Amendment created successfully!
          </div>
        )}

        {/* Title */}
        <div>
          <label className="block text-xs sm:text-sm font-medium text-dark-300 mb-1.5 sm:mb-2">Title</label>
          <input
            type="text"
            value={form.title}
            onChange={(e) => handleChange('title', e.target.value)}
            className="input-field text-sm"
            placeholder="E.g., Environmental Protection Clause"
            required
          />
        </div>

        {/* Body */}
        <div>
          <label className="block text-xs sm:text-sm font-medium text-dark-300 mb-1.5 sm:mb-2">Amendment Text</label>
          <textarea
            value={form.body}
            onChange={(e) => handleChange('body', e.target.value)}
            className="input-field min-h-[120px] sm:min-h-[150px] resize-y text-sm"
            placeholder="Full text of the proposed amendment..."
            required
          />
        </div>

        {/* Category + Timer row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
          <div>
            <label className="block text-xs sm:text-sm font-medium text-dark-300 mb-1.5 sm:mb-2">Category</label>
            <div className="relative">
              <select
                value={form.category}
                onChange={(e) => handleChange('category', e.target.value)}
                className="input-field appearance-none pr-10 text-sm"
              >
                {CATEGORIES.map(cat => (
                  <option key={cat} value={cat}>{cat.replace('_', ' ')}</option>
                ))}
              </select>
              <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" className="text-dark-400">
                  <path d="M6 9l6 6 6-6" />
                </svg>
              </div>
            </div>
          </div>

          <div>
            <label className="block text-xs sm:text-sm font-medium text-dark-300 mb-1.5 sm:mb-2">
              Closes At
              <button
                type="button"
                onClick={() => handleChange('closesAt', defaultClosesAt())}
                className="ml-2 text-[10px] sm:text-xs text-civic-400 hover:text-civic-300"
              >
                (Set 7 days)
              </button>
            </label>
            <input
              type="datetime-local"
              value={form.closesAt}
              onChange={(e) => handleChange('closesAt', e.target.value)}
              className="input-field text-sm"
              min={new Date().toISOString().slice(0, 16)}
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="btn-primary w-full disabled:opacity-50 text-sm"
        >
          {loading ? 'Creating...' : 'Create Amendment'}
        </button>
      </form>
    </div>
  )
}
