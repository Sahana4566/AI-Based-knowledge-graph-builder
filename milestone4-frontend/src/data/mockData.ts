export interface KpiCard {
  label: string
  value: string
  trend: string
}

export interface GraphRow {
  head: string
  relation: string
  tail: string
}

export interface SemanticMatch {
  id: string
  score: number
  text: string
}

export const kpiCards: KpiCard[] = [
  { label: 'Entities Indexed', value: '13,781', trend: '+2.1%' },
  { label: 'Relations Tracked', value: '237', trend: '+0.4%' },
  { label: 'Vector Documents', value: '5', trend: '+100%' },
  { label: 'Pipeline Status', value: 'Healthy', trend: 'All checks green' },
]

export const graphPreview: GraphRow[] = [
  { head: 'Barack Obama', relation: 'born_in', tail: 'Hawaii' },
  { head: 'Microsoft', relation: 'founded_by', tail: 'Bill Gates' },
  { head: 'Google', relation: 'headquartered_in', tail: 'California' },
  { head: 'Tesla', relation: 'founded_by', tail: 'Elon Musk' },
  { head: 'Amazon', relation: 'type', tail: 'E-commerce company' },
]

export const semanticMatches: SemanticMatch[] = [
  {
    id: '1',
    score: 0.92,
    text: 'Microsoft was founded by Bill Gates',
  },
  {
    id: '2',
    score: 0.84,
    text: 'Google is headquartered in California',
  },
  {
    id: '3',
    score: 0.73,
    text: 'Barack Obama was the President of the United States',
  },
]

export const deploymentChecklist: string[] = [
  'Create API endpoints for graph query and semantic search',
  'Secure credentials via server-side environment variables',
  'Add authentication for dashboard access',
  'Deploy frontend (Vercel/Netlify) and backend APIs',
  'Enable request logging and uptime monitoring',
]
