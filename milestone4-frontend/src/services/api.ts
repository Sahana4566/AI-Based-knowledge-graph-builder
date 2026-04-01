import type { GraphRow, SemanticMatch } from '../data/mockData'

const API_BASE = import.meta.env.VITE_API_BASE_URL || ''

interface GraphQueryParams {
  entity?: string
  relation?: string
  limit?: number
}

interface SemanticSearchParams {
  query?: string
  topK?: number
}

interface GraphQueryResponse {
  rows: GraphRow[]
}

interface SemanticSearchResponse {
  matches: SemanticMatch[]
}

interface HealthResponse {
  status: string
  neo4j: string
  pinecone: string
}

async function fetchJson<T>(url: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(url, options)
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`)
  }
  return (await response.json()) as T
}

export async function queryGraph({ entity = '', relation = '', limit = 20 }: GraphQueryParams): Promise<GraphQueryResponse> {
  if (!API_BASE) {
    throw new Error('API base URL not configured')
  }
  const params = new URLSearchParams({ entity, relation, limit: String(limit) })
  return fetchJson<GraphQueryResponse>(`${API_BASE}/graph/query?${params.toString()}`)
}

export async function semanticSearch({ query = '', topK = 3 }: SemanticSearchParams): Promise<SemanticSearchResponse> {
  if (!API_BASE) {
    throw new Error('API base URL not configured')
  }
  return fetchJson<SemanticSearchResponse>(`${API_BASE}/semantic/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, topK }),
  })
}

export async function checkApiHealth(): Promise<HealthResponse> {
  if (!API_BASE) {
    throw new Error('API base URL not configured')
  }
  return fetchJson<HealthResponse>(`${API_BASE}/health`)
}
