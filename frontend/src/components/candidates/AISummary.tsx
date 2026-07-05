import { useState } from 'react'
import { fetchSummary } from '../../api/candidates'
import { ApiError } from '../../api/client'

interface Props {
  candidateId: number
}

export function AISummary({ candidateId }: Props) {
  const [summary, setSummary] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function generate() {
    setLoading(true)
    setError(null)

    try {
      const data = await fetchSummary(candidateId)
      setSummary(data.summary)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Failed to generate summary')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="rounded-2xl border border-gray-200 bg-white p-6">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-gray-900">AI Summary</h3>
          <p className="text-xs text-gray-400 mt-0.5">Generated on demand — not stored</p>
        </div>
        <button
          onClick={generate}
          disabled={loading}
          className="inline-flex items-center gap-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 disabled:cursor-not-allowed text-white text-sm font-medium px-4 py-2 transition-colors"
        >
          {loading ? (
            <>
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
              </svg>
              Generating…
            </>
          ) : (
            <>✦ {summary ? 'Regenerate' : 'Generate Summary'}</>
          )}
        </button>
      </div>

      {loading && (
        <div className="rounded-lg bg-gray-50 border border-gray-100 px-4 py-6 flex items-center justify-center gap-2 text-sm text-gray-400">
          <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
          </svg>
          Analyzing candidate profile…
        </div>
      )}

      {!loading && summary && (
        <div className="rounded-lg bg-indigo-50 border border-indigo-100 px-4 py-4">
          <p className="text-sm text-indigo-900 leading-relaxed">{summary}</p>
        </div>
      )}

      {!loading && error && (
        <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-4 py-3">{error}</p>
      )}

      {!loading && !summary && !error && (
        <p className="text-sm text-gray-400 text-center py-4">
          Click "Generate Summary" to get an AI-generated overview of this candidate.
        </p>
      )}
    </div>
  )
}
