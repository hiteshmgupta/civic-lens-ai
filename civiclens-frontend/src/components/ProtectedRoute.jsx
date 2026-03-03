import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function ProtectedRoute({ children, requiredRole }) {
  const { user, loading } = useAuth()

  if (loading) return <div className="flex items-center justify-center h-screen"><LoadingSpinner /></div>
  if (!user) return <Navigate to="/login" replace />
  if (requiredRole && user.role !== requiredRole) return <Navigate to="/" replace />

  return children
}

function LoadingSpinner() {
  return (
    <div className="animate-spin h-8 w-8 border-4 border-civic-400 border-t-transparent rounded-full" />
  )
}
