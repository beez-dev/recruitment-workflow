import type { ReactNode } from 'react'

interface AuthCardProps {
  title: string
  subtitle: string
  children: ReactNode
}

export function AuthCard({ title, subtitle, children }: AuthCardProps) {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight">TechCraft</h1>
          <p className="text-sm text-gray-500 mt-1">Hiring Review Platform</p>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 px-8 py-10">
          <h2 className="text-xl font-semibold text-gray-900 mb-1">{title}</h2>
          <p className="text-sm text-gray-500 mb-6">{subtitle}</p>
          {children}
        </div>
      </div>
    </div>
  )
}
