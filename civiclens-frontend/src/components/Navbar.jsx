import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout, isAdmin } = useAuth()
  const location = useLocation()
  const [mobileOpen, setMobileOpen] = useState(false)

  const closeMobile = () => setMobileOpen(false)

  return (
    <nav className="sticky top-0 z-50 bg-dark-950/80 backdrop-blur-xl border-b border-dark-800/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14 sm:h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 sm:gap-3 flex-shrink-0" onClick={closeMobile}>
            <div className="w-7 h-7 sm:w-8 sm:h-8 bg-civic-400 rounded-lg flex items-center justify-center">
              <span className="text-dark-950 font-bold text-xs sm:text-sm">CL</span>
            </div>
            <div>
              <span className="text-base sm:text-lg font-bold text-dark-100">CivicLens</span>
              <span className="hidden md:inline text-xs text-dark-500 ml-2">INTELLIGENCE PLATFORM</span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-1">
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
                  <span className="text-sm text-dark-300">{user.username}</span>
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

          {/* Mobile Hamburger */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden p-2 rounded-lg text-dark-300 hover:text-dark-100 hover:bg-dark-800/50 transition-colors"
            aria-label="Toggle menu"
          >
            {mobileOpen ? (
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                <path d="M18 6L6 18M6 6l12 12" />
              </svg>
            ) : (
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                <path d="M3 12h18M3 6h18M3 18h18" />
              </svg>
            )}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      <div
        className={`md:hidden border-t border-dark-800/50 bg-dark-950/95 backdrop-blur-xl overflow-hidden transition-all duration-300 ease-in-out ${
          mobileOpen ? 'max-h-80 opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <div className="px-4 py-3 space-y-1">
          <MobileNavLink
            to="/"
            active={location.pathname === '/' || location.pathname === '/amendments'}
            onClick={closeMobile}
          >
            📋 Amendments
          </MobileNavLink>

          {isAdmin && (
            <MobileNavLink to="/admin" active={location.pathname === '/admin'} onClick={closeMobile}>
              ⚙️ Admin Dashboard
            </MobileNavLink>
          )}

          <div className="border-t border-dark-800/50 my-2 pt-2">
            {user ? (
              <>
                <div className="flex items-center gap-3 px-3 py-2">
                  <div className="w-8 h-8 bg-dark-700 rounded-full flex items-center justify-center">
                    <span className="text-sm font-medium text-civic-400">
                      {user.username?.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-dark-200">{user.username}</span>
                    <span className="block text-xs text-dark-500">{user.email}</span>
                  </div>
                </div>
                <button
                  onClick={() => { logout(); closeMobile(); }}
                  className="w-full text-left px-3 py-2.5 text-sm text-rose-400 hover:bg-dark-800/50 rounded-lg transition-colors"
                >
                  Logout
                </button>
              </>
            ) : (
              <div className="flex flex-col gap-2">
                <Link to="/login" onClick={closeMobile} className="btn-ghost text-sm text-center">
                  Login
                </Link>
                <Link to="/register" onClick={closeMobile} className="btn-primary text-sm text-center">
                  Register
                </Link>
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

function MobileNavLink({ to, active, onClick, children }) {
  return (
    <Link
      to={to}
      onClick={onClick}
      className={`block px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${
        active
          ? 'bg-dark-800 text-civic-400'
          : 'text-dark-300 hover:text-dark-100 hover:bg-dark-800/50'
      }`}
    >
      {children}
    </Link>
  )
}
