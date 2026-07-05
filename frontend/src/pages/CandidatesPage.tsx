import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { fetchCandidates } from '../api/candidates'
import { ApiError } from '../api/client'
import { CandidateFilters } from '../components/candidates/CandidateFilters'
import { CandidateList } from '../components/candidates/CandidateList'
import { Pagination } from '../components/candidates/Pagination'
import type { Candidate, CandidateFilters as Filters } from '../types/candidate'

const PAGE_SIZE = 20

const EMPTY_FILTERS: Filters = {
  status: '',
  role_applied: '',
  skill: '',
  keyword: '',
}

export function CandidatesPage() {
  const navigate = useNavigate()
  const [filters, setFilters] = useState<Filters>(EMPTY_FILTERS)
  const [debouncedFilters, setDebouncedFilters] = useState<Filters>(EMPTY_FILTERS)
  const [page, setPage] = useState(1)
  const [candidates, setCandidates] = useState<Candidate[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Debounce text filter inputs by 400ms
  useEffect(() => {
    const t = setTimeout(() => setDebouncedFilters(filters), 400)
    return () => clearTimeout(t)
  }, [filters])

  // Reset to page 1 when filters change
  useEffect(() => {
    setPage(1)
  }, [debouncedFilters])

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setError(null)

    fetchCandidates(debouncedFilters, page, PAGE_SIZE)
      .then((data) => {
        if (cancelled) return
        setCandidates(data.items)
        setTotal(data.total)
      })
      .catch((err) => {
        if (cancelled) return
        if (err instanceof ApiError && err.status === 401) {
          navigate('/login', { replace: true })
        } else {
          setError(err.message ?? 'Failed to load candidates')
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => { cancelled = true }
  }, [debouncedFilters, page, navigate])

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Candidates</h1>
            {!loading && (
              <p className="text-sm text-gray-500 mt-0.5">{total} total</p>
            )}
          </div>
        </div>

        <div className="mb-4">
          <CandidateFilters filters={filters} onChange={setFilters} />
        </div>

        {error && (
          <div className="mb-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-600">
            {error}
          </div>
        )}

        <div className="mb-4">
          <CandidateList candidates={candidates} loading={loading} />
        </div>

        <Pagination
          page={page}
          pageSize={PAGE_SIZE}
          total={total}
          onPageChange={setPage}
        />
      </div>
    </div>
  )
}
