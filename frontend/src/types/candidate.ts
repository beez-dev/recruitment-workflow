export type CandidateStatus = 'new' | 'reviewed' | 'hired' | 'rejected'

export interface Candidate {
  id: number
  name: string
  email: string
  role_applied: string
  status: CandidateStatus
  skills: string[]
  created_at: string
}

export interface CandidateListResponse {
  items: Candidate[]
  total: number
  page: number
  page_size: number
}

export interface CandidateFilters {
  status: CandidateStatus | ''
  role_applied: string
  skill: string
  keyword: string
}
