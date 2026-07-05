import { Navigate } from 'react-router-dom'
import { AuthCard } from '../components/auth/AuthCard'
import { useAuth } from '../context/AuthContext'

export function SignupPage() {
  const { user } = useAuth()

  if (user) return <Navigate to="/" replace />

  return (
    <AuthCard title="Create an account" subtitle="Get started with TechCraft">
      <p className="text-sm text-gray-500 text-center">Sign-up coming soon.</p>
    </AuthCard>
  )
}
