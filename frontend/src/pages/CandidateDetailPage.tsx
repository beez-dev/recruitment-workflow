import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { fetchCandidate } from '../api/candidates'
import { ApiError } from '../api/client'
import { AISummary } from '../components/candidates/AISummary'
import { ProfileCard } from '../components/candidates/ProfileCard'
import { ScoreForm } from '../components/candidates/ScoreForm'
import { ScoresList } from '../components/candidates/ScoresList'
import { useAuth } from '../context/AuthContext'
import type { CandidateDetail, Score } from '../types/candidate'

export function CandidateDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { user } = useAuth()
  const navigate = useNavigate()
  const isAdmin = user?.role === 'admin'

  const [candidate, setCandidate] = useState<CandidateDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return
    setLoading(true)

    fetchCandidate(Number(id))
      .then(setCandidate)
      .catch((err) => {
        if (err instanceof ApiError && err.status === 401) {
          navigate('/login', { replace: true })
        } else {
          setError(err.message ?? 'Failed to load candidate')
        }
      })
      .finally(() => setLoading(false))
  }, [id, navigate])

  function handleScoreAdded(score: Score) {
    setCandidate((prev) => prev ? { ...prev, scores: [...prev.scores, score] } : prev)
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center text-sm text-gray-400">
        Loading…
      </div>
    )
  }

  if (error || !candidate) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-sm text-red-600 mb-3">{error ?? 'Candidate not found'}</p>
          <Link to="/candidates" className="text-sm text-indigo-600 hover:underline">← Back to candidates</Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-5xl mx-auto px-6 py-8">
        <Link to="/candidates" className="inline-flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-700 mb-6">
          ← Back to candidates
        </Link>

        <div className="space-y-6">
          <ProfileCard candidate={candidate} isAdmin={isAdmin} />

          <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
            <div className="lg:col-span-3 rounded-2xl border border-gray-200 bg-white p-6">
              <h3 className="text-sm font-semibold text-gray-900 mb-4">
                {isAdmin ? 'All Scores' : 'Your Scores'}
              </h3>
              <ScoresList scores={candidate.scores} isAdmin={isAdmin} />
            </div>

            <div className="lg:col-span-2 rounded-2xl border border-gray-200 bg-white p-6">
              <h3 className="text-sm font-semibold text-gray-900 mb-4">Submit Score</h3>
              <ScoreForm candidateId={candidate.id} onScoreAdded={handleScoreAdded} />
            </div>
          </div>

          <AISummary candidateId={candidate.id} />
        </div>
      </div>
    </div>
  )
}
