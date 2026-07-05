import { apiFetch } from './client'
import type {
  CandidateDetail,
  CandidateFilters,
  CandidateListResponse,
  Score,
  ScoreRequest,
} from '../types/candidate'

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

export function fetchCandidate(id: number): Promise<CandidateDetail> {
  return apiFetch<CandidateDetail>(`/candidates/${id}`)
}

export function submitScore(id: number, data: ScoreRequest): Promise<Score> {
  return apiFetch<Score>(`/candidates/${id}/scores`, {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function fetchSummary(id: number): Promise<{ candidate_id: number; summary: string }> {
  return apiFetch(`/candidates/${id}/summary`, { method: 'POST' })
}
