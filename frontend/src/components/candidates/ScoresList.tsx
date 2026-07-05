import type { Score } from '../../types/candidate'

interface Props {
  scores: Score[]
  isAdmin: boolean
}

function StarRating({ value }: { value: number }) {
  return (
    <div className="flex gap-0.5">
      {[1, 2, 3, 4, 5].map((n) => (
        <span key={n} className={`text-base ${n <= value ? 'text-amber-400' : 'text-gray-200'}`}>★</span>
      ))}
    </div>
  )
}

export function ScoresList({ scores, isAdmin }: Props) {
  if (scores.length === 0) {
    return (
      <p className="text-sm text-gray-400 py-4 text-center">
        {isAdmin ? 'No scores submitted yet.' : 'You have not submitted any scores yet.'}
      </p>
    )
  }

  return (
    <div className="space-y-3">
      {scores.map((s) => (
        <div key={s.id} className="rounded-xl border border-gray-100 bg-gray-50 px-4 py-3">
          <div className="flex items-center justify-between mb-1">
            <span className="text-sm font-medium text-gray-800">{s.category}</span>
            <StarRating value={s.score} />
          </div>
          {s.note && (
            <p className="text-xs text-gray-500 mt-1">{s.note}</p>
          )}
          <p className="text-xs text-gray-400 mt-1.5">
            {isAdmin ? `Reviewer #${s.reviewer_id} · ` : ''}
            {new Date(s.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
          </p>
        </div>
      ))}
    </div>
  )
}
