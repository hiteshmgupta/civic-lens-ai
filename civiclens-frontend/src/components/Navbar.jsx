import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout, isAdmin } = useAuth()
  const location = useLocation()

  return (
    <nav className="sticky top-0 z-50 bg-dark-950/80 backdrop-blur-xl border-b border-dark-800/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3">
            <div className="w-8 h-8 bg-civic-400 rounded-lg flex items-center justify-center">
              <span className="text-dark-950 font-bold text-sm">CL</span>
            </div>
            <div>
              <span className="text-lg font-bold text-dark-100">CivicLens</span>
              <span className="hidden sm:inline text-xs text-dark-500 ml-2">INTELLIGENCE PLATFORM</span>
            </div>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center gap-1">
            <NavLink to="/" active={location.pathname === '/' || location.pathname === '/amendments'}>
              Amendments
            </NavLink>

            {isAdmin && (
              <NavLink to="/admin" active={location.pathname === '/admin'}>
                Admin
              </NavLink>
            )}

            {user ? (
              <div className="flex items-center gap-3 ml-4">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 bg-dark-700 rounded-full flex items-center justify-center">
                    <span className="text-sm font-medium text-civic-400">
                      {user.username?.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <span className="hidden sm:inline text-sm text-dark-300">{user.username}</span>
                </div>
                <button onClick={logout} className="btn-ghost text-sm">
                  Logout
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2 ml-4">
                <Link to="/login" className="btn-ghost text-sm">Login</Link>
                <Link to="/register" className="btn-primary text-sm">Register</Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}

function NavLink({ to, active, children }) {
  return (
    <Link
      to={to}
      className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
        active
          ? 'bg-dark-800 text-civic-400'
          : 'text-dark-400 hover:text-dark-100 hover:bg-dark-800/50'
      }`}
    >
      {children}
    </Link>
  )
}
