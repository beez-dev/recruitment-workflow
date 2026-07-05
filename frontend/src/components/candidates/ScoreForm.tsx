import { useState, type FormEvent } from 'react'
import { submitScore } from '../../api/candidates'
import { ApiError } from '../../api/client'
import type { Score } from '../../types/candidate'

interface Props {
  candidateId: number
  onScoreAdded: (score: Score) => void
}

const CATEGORIES = ['Technical', 'Communication', 'Culture Fit', 'Problem Solving', 'Leadership']

export function ScoreForm({ candidateId, onScoreAdded }: Props) {
  const [category, setCategory] = useState(CATEGORIES[0])
  const [score, setScore] = useState(0)
  const [note, setNote] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const inputClass = 'w-full rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white'

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (score === 0) { setError('Please select a score.'); return }
    setError(null)
    setLoading(true)

    try {
      const newScore = await submitScore(candidateId, {
        category,
        score,
        note: note.trim() || undefined,
      })
      onScoreAdded(newScore)
      setScore(0)
      setNote('')
      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Failed to submit score')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <div>
        <label className="block text-xs font-medium text-gray-600 mb-1">Category</label>
        <select value={category} onChange={(e) => setCategory(e.target.value)} className={inputClass}>
          {CATEGORIES.map((c) => <option key={c}>{c}</option>)}
        </select>
      </div>

      <div>
        <label className="block text-xs font-medium text-gray-600 mb-1">Score</label>
        <div className="flex gap-1">
          {[1, 2, 3, 4, 5].map((n) => (
            <button
              key={n}
              type="button"
              onClick={() => setScore(n)}
              className={`text-2xl transition-colors ${n <= score ? 'text-amber-400' : 'text-gray-200 hover:text-amber-200'}`}
            >
              ★
            </button>
          ))}
        </div>
      </div>

      <div>
        <label className="block text-xs font-medium text-gray-600 mb-1">Note <span className="text-gray-400">(optional)</span></label>
        <textarea
          value={note}
          onChange={(e) => setNote(e.target.value)}
          rows={3}
          placeholder="Add a note…"
          className={`${inputClass} resize-none`}
        />
      </div>

      {error && (
        <p className="text-xs text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">{error}</p>
      )}
      {success && (
        <p className="text-xs text-green-600 bg-green-50 border border-green-200 rounded-lg px-3 py-2">Score submitted.</p>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 disabled:cursor-not-allowed text-white text-sm font-medium rounded-lg px-4 py-2 transition-colors"
      >
        {loading ? 'Submitting…' : 'Submit Score'}
      </button>
    </form>
  )
}
