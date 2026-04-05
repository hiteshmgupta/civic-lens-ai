import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { login as loginApi } from '../../api/authApi'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const res = await loginApi({ email, password })
      login(res.data)
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-dark-950 flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-sm sm:max-w-md">
        {/* Logo */}
        <div className="text-center mb-6 sm:mb-8">
          <div className="inline-flex items-center gap-2 sm:gap-3 mb-3 sm:mb-4">
            <div className="w-8 h-8 sm:w-10 sm:h-10 bg-civic-400 rounded-xl flex items-center justify-center">
              <span className="text-dark-950 font-bold text-sm sm:text-base">CL</span>
            </div>
            <span className="text-xl sm:text-2xl font-bold text-dark-100">CivicLens</span>
          </div>
          <p className="text-dark-400 text-xs sm:text-sm">Sign in to the Intelligence Platform</p>
        </div>

        <div className="glass-card p-5 sm:p-8">
          <form onSubmit={handleSubmit} className="space-y-4 sm:space-y-5">
            {error && (
              <div className="p-2.5 sm:p-3 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-xs sm:text-sm">
                {error}
              </div>
            )}

            <div>
              <label className="block text-xs sm:text-sm font-medium text-dark-300 mb-1.5 sm:mb-2">Email</label>
              <input
                id="login-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input-field text-sm"
                placeholder="you@example.com"
                required
              />
            </div>

            <div>
              <label className="block text-xs sm:text-sm font-medium text-dark-300 mb-1.5 sm:mb-2">Password</label>
              <input
                id="login-password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input-field text-sm"
                placeholder="••••••••"
                required
              />
            </div>

            <button
              id="login-submit"
              type="submit"
              disabled={loading}
              className="btn-primary w-full disabled:opacity-50 text-sm"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <p className="text-center text-xs sm:text-sm text-dark-400 mt-4 sm:mt-6">
            Don't have an account?{' '}
            <Link to="/register" className="text-civic-400 hover:text-civic-300 font-medium">
              Register
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
