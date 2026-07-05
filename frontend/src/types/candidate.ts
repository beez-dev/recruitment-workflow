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

export interface Score {
  id: number
  candidate_id: number
  category: string
  score: number
  reviewer_id: number
  note: string | null
  created_at: string
}

export interface CandidateDetail extends Candidate {
  scores: Score[]
  internal_notes?: string | null
}

export interface ScoreRequest {
  category: string
  score: number
  note?: string
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
