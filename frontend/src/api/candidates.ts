import { apiFetch } from './client'
import type { CandidateFilters, CandidateListResponse } from '../types/candidate'

export function fetchCandidates(
  filters: CandidateFilters,
  page: number,
  pageSize = 20,
): Promise<CandidateListResponse> {
  const params = new URLSearchParams()
  if (filters.status) params.set('status', filters.status)
  if (filters.role_applied) params.set('role_applied', filters.role_applied)
  if (filters.skill) params.set('skill', filters.skill)
  if (filters.keyword) params.set('keyword', filters.keyword)
  params.set('page', String(page))
  params.set('page_size', String(pageSize))

  return apiFetch<CandidateListResponse>(`/candidates?${params}`)
}
