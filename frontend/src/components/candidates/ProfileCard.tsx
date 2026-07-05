import type { CandidateDetail, CandidateStatus } from '../../types/candidate'

interface Props {
  candidate: CandidateDetail
  isAdmin: boolean
}

const STATUS_STYLES: Record<CandidateStatus, string> = {
  new: 'bg-blue-50 text-blue-700 ring-1 ring-blue-200',
  reviewed: 'bg-yellow-50 text-yellow-700 ring-1 ring-yellow-200',
  hired: 'bg-green-50 text-green-700 ring-1 ring-green-200',
  rejected: 'bg-red-50 text-red-700 ring-1 ring-red-200',
}

export function ProfileCard({ candidate, isAdmin }: Props) {
  return (
    <div className="rounded-2xl border border-gray-200 bg-white p-6">
      <div className="flex items-start justify-between gap-4 mb-4">
        <div>
          <h2 className="text-xl font-semibold text-gray-900">{candidate.name}</h2>
          <p className="text-sm text-gray-500 mt-0.5">{candidate.email}</p>
        </div>
        <span className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-medium capitalize shrink-0 ${STATUS_STYLES[candidate.status]}`}>
          {candidate.status}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4 text-sm mb-4">
        <div>
          <p className="text-gray-400 text-xs uppercase tracking-wide mb-0.5">Role Applied</p>
          <p className="text-gray-800 font-medium">{candidate.role_applied}</p>
        </div>
        <div>
          <p className="text-gray-400 text-xs uppercase tracking-wide mb-0.5">Applied On</p>
          <p className="text-gray-800 font-medium">
            {new Date(candidate.created_at).toLocaleDateString('en-US', {
              year: 'numeric', month: 'short', day: 'numeric',
            })}
          </p>
        </div>
      </div>

      <div className="mb-4">
        <p className="text-gray-400 text-xs uppercase tracking-wide mb-1.5">Skills</p>
        <div className="flex flex-wrap gap-1.5">
          {candidate.skills.map((s) => (
            <span key={s} className="rounded-md bg-gray-100 px-2.5 py-1 text-xs font-medium text-gray-700">
              {s}
            </span>
          ))}
        </div>
      </div>

      {isAdmin && candidate.internal_notes && (
        <div className="rounded-lg bg-amber-50 border border-amber-200 px-4 py-3">
          <p className="text-xs font-medium text-amber-700 uppercase tracking-wide mb-1">Internal Notes</p>
          <p className="text-sm text-amber-900">{candidate.internal_notes}</p>
        </div>
      )}
    </div>
  )
}
