import { Navigate } from 'react-router-dom'
import { AuthCard } from '../components/auth/AuthCard'
import { LoginForm } from '../components/auth/LoginForm'
import { useAuth } from '../context/AuthContext'

export function LoginPage() {
  const { user } = useAuth()

  if (user) return <Navigate to="/" replace />

  return (
    <AuthCard title="Welcome back" subtitle="Sign in to your account to continue">
      <LoginForm />
    </AuthCard>
  )
}
