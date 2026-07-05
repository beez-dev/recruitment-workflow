import type { CandidateFilters, CandidateStatus } from '../../types/candidate'

interface Props {
  filters: CandidateFilters
  onChange: (filters: CandidateFilters) => void
}

const STATUS_OPTIONS: { label: string; value: CandidateStatus | '' }[] = [
  { label: 'All statuses', value: '' },
  { label: 'New', value: 'new' },
  { label: 'Reviewed', value: 'reviewed' },
  { label: 'Hired', value: 'hired' },
  { label: 'Rejected', value: 'rejected' },
]

const inputClass =
  'rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white'

export function CandidateFilters({ filters, onChange }: Props) {
  function set(key: keyof CandidateFilters, value: string) {
    onChange({ ...filters, [key]: value })
  }

  return (
    <div className="flex flex-wrap gap-3">
      <select
        value={filters.status}
        onChange={(e) => set('status', e.target.value)}
        className={inputClass}
      >
        {STATUS_OPTIONS.map((o) => (
          <option key={o.value} value={o.value}>{o.label}</option>
        ))}
      </select>

      <input
        type="text"
        placeholder="Role applied"
        value={filters.role_applied}
        onChange={(e) => set('role_applied', e.target.value)}
        className={inputClass}
      />

      <input
        type="text"
        placeholder="Skill"
        value={filters.skill}
        onChange={(e) => set('skill', e.target.value)}
        className={inputClass}
      />

      <input
        type="text"
        placeholder="Search name or email"
        value={filters.keyword}
        onChange={(e) => set('keyword', e.target.value)}
        className={`${inputClass} min-w-56`}
      />
    </div>
  )
}
