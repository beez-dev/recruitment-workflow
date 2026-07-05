import { useNavigate } from 'react-router-dom'
import type { Candidate, CandidateStatus } from '../../types/candidate'

interface Props {
  candidates: Candidate[]
  loading: boolean
}

const STATUS_STYLES: Record<CandidateStatus, string> = {
  new: 'bg-blue-50 text-blue-700 ring-1 ring-blue-200',
  reviewed: 'bg-yellow-50 text-yellow-700 ring-1 ring-yellow-200',
  hired: 'bg-green-50 text-green-700 ring-1 ring-green-200',
  rejected: 'bg-red-50 text-red-700 ring-1 ring-red-200',
}

export function CandidateList({ candidates, loading }: Props) {
  const navigate = useNavigate()

  if (loading) {
    return (
      <div className="flex justify-center py-16 text-sm text-gray-400">
        Loading…
      </div>
    )
  }

  if (candidates.length === 0) {
    return (
      <div className="flex justify-center py-16 text-sm text-gray-400">
        No candidates found.
      </div>
    )
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-gray-200">
      <table className="w-full text-sm text-left">
        <thead className="bg-gray-50 text-gray-500 uppercase text-xs tracking-wide">
          <tr>
            <th className="px-4 py-3 font-medium">Name</th>
            <th className="px-4 py-3 font-medium">Email</th>
            <th className="px-4 py-3 font-medium">Role Applied</th>
            <th className="px-4 py-3 font-medium">Status</th>
            <th className="px-4 py-3 font-medium">Skills</th>
            <th className="px-4 py-3 font-medium">Applied</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100 bg-white">
          {candidates.map((c) => (
            <tr
              key={c.id}
              onClick={() => navigate(`/candidates/${c.id}`)}
              className="hover:bg-gray-50 transition-colors cursor-pointer"
            >
              <td className="px-4 py-3 font-medium text-gray-900">{c.name}</td>
              <td className="px-4 py-3 text-gray-600">{c.email}</td>
              <td className="px-4 py-3 text-gray-600">{c.role_applied}</td>
              <td className="px-4 py-3">
                <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium capitalize ${STATUS_STYLES[c.status]}`}>
                  {c.status}
                </span>
              </td>
              <td className="px-4 py-3">
                <div className="flex flex-wrap gap-1">
                  {c.skills.map((s) => (
                    <span key={s} className="rounded-md bg-gray-100 px-2 py-0.5 text-xs text-gray-600">
                      {s}
                    </span>
                  ))}
                </div>
              </td>
              <td className="px-4 py-3 text-gray-500">
                {new Date(c.created_at).toLocaleDateString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
