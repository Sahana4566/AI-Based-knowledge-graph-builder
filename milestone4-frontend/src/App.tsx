import { useEffect, useMemo, useRef, useState } from 'react'
import { Network, type Edge, type Node } from 'vis-network'
import './App.css'
import {
  graphPreview,
  kpiCards,
  semanticMatches,
  type GraphRow,
  type SemanticMatch,
} from './data/mockData'
import { checkApiHealth, queryGraph, semanticSearch } from './services/api'

function App() {
  const [entity, setEntity] = useState<string>('')
  const [relation, setRelation] = useState<string>('')
  const [query, setQuery] = useState<string>('Who founded Microsoft?')
  const [graphRows, setGraphRows] = useState<GraphRow[]>(graphPreview)
  const [searchRows, setSearchRows] = useState<SemanticMatch[]>(semanticMatches)
  const [, setStatus] = useState<string>('Using demo data (API not connected yet).')
  const [, setApiConnected] = useState<boolean>(false)
  const graphContainerRef = useRef<HTMLDivElement | null>(null)
  const networkRef = useRef<Network | null>(null)

  const isApiConfigured = Boolean(import.meta.env.VITE_API_BASE_URL)

  useEffect(() => {
    let isMounted = true

    async function bootstrapHealth(): Promise<void> {
      if (!isApiConfigured) {
        if (isMounted) {
          setStatus('API URL missing. Using demo data.')
          setApiConnected(false)
        }
        return
      }

      try {
        const health = await checkApiHealth()
        const neo4jNote = health.neo4j === 'connected' ? 'Neo4j connected' : 'Neo4j disconnected'
        const pineconeNote = health.pinecone === 'connected' ? 'Pinecone connected' : 'Pinecone disconnected'
        if (isMounted) {
          setStatus(`Live API connected. ${neo4jNote}; ${pineconeNote}.`)
          setApiConnected(true)
        }
      } catch {
        if (isMounted) {
          setStatus('Using demo data (API not connected yet).')
          setApiConnected(false)
        }
      }
    }

    void bootstrapHealth()

    const intervalId = window.setInterval(() => {
      void bootstrapHealth()
    }, 8000)

    return () => {
      isMounted = false
      window.clearInterval(intervalId)
    }
  }, [isApiConfigured])

  const filteredRows = useMemo(() => {
    return graphRows.filter((row) => {
      const entityMatch = entity
        ? row.head.toLowerCase().includes(entity.toLowerCase()) ||
          row.tail.toLowerCase().includes(entity.toLowerCase())
        : true
      const relationMatch = relation
        ? row.relation.toLowerCase().includes(relation.toLowerCase())
        : true
      return entityMatch && relationMatch
    })
  }, [entity, relation, graphRows])

  useEffect(() => {
    const container = graphContainerRef.current
    if (!container) {
      return
    }

    if (!filteredRows.length) {
      if (networkRef.current) {
        networkRef.current.destroy()
        networkRef.current = null
      }
      return
    }

    const uniqueNodes = new Set<string>()
    const nodes: Node[] = []
    const edges: Edge[] = []

    filteredRows.forEach((row, index) => {
      if (!uniqueNodes.has(row.head)) {
        uniqueNodes.add(row.head)
        nodes.push({ id: row.head, label: row.head, shape: 'dot', size: 14 })
      }

      if (!uniqueNodes.has(row.tail)) {
        uniqueNodes.add(row.tail)
        nodes.push({ id: row.tail, label: row.tail, shape: 'dot', size: 14 })
      }

      edges.push({
        id: `${row.head}-${row.relation}-${row.tail}-${index}`,
        from: row.head,
        to: row.tail,
        label: row.relation,
        arrows: 'to',
      })
    })

    const data = {
      nodes: nodes,
      edges: edges,
    }

    const options = {
      autoResize: true,
      nodes: {
        color: {
          background: '#1d4ed8',
          border: '#0f172a',
          highlight: {
            background: '#0ea5e9',
            border: '#0f172a',
          },
        },
        font: {
          color: '#0f172a',
          face: 'Segoe UI',
          size: 12,
          background: 'rgba(255,255,255,0.85)',
        },
      },
      edges: {
        color: '#64748b',
        font: {
          align: 'middle' as const,
          size: 10,
          color: '#334155',
          background: 'rgba(255,255,255,0.75)',
        },
        smooth: {
          enabled: true,
          type: 'dynamic' as const,
          roundness: 0.4,
        },
      },
      physics: {
        barnesHut: {
          gravitationalConstant: -2600,
          springLength: 120,
          springConstant: 0.03,
        },
        stabilization: {
          iterations: 140,
        },
      },
      interaction: {
        hover: true,
        tooltipDelay: 180,
      },
    }

    if (networkRef.current) {
      networkRef.current.destroy()
    }

    networkRef.current = new Network(container, data, options)

    return () => {
      if (networkRef.current) {
        networkRef.current.destroy()
        networkRef.current = null
      }
    }
  }, [filteredRows])

  async function handleGraphQuery(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!isApiConfigured) {
      setStatus('API URL missing. Showing filtered demo graph data.')
      return
    }
    try {
      const data = await queryGraph({ entity, relation, limit: 20 })
      setGraphRows(data.rows || [])
      setStatus('Graph query completed from live API.')
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unknown error'
      setStatus(`Graph query failed. Falling back to demo data. (${message})`)
      setGraphRows(graphPreview)
    }
  }

  async function handleSemanticSearch(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!isApiConfigured) {
      setStatus('API URL missing. Showing demo semantic matches.')
      return
    }
    try {
      const data = await semanticSearch({ query, topK: 3 })
      setSearchRows(data.matches || [])
      setStatus('Semantic search completed from live API.')
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unknown error'
      setStatus(`Semantic search failed. Showing demo matches. (${message})`)
      setSearchRows(semanticMatches)
    }
  }

  return (
    <div className="page">
      <header className="masthead">
        <h1>Knowledge Graph Dashboard</h1>
        <p className="subtitle">
          Graph exploration and semantic search.
        </p>
      </header>

      <section className="kpi-grid" aria-label="KPI Overview">
        {kpiCards.map((card) => (
          <article key={card.label} className="kpi-card">
            <p className="kpi-label">{card.label}</p>
            <p className="kpi-value">{card.value}</p>
            <p className="kpi-trend">{card.trend}</p>
          </article>
        ))}
      </section>

      <main className="content-grid">
        <section className="panel">
          <div className="panel-head">
            <h2>Graph Explorer</h2>
            <p>Filter head-tail relationships and preview graph triples.</p>
          </div>

          <form className="controls" onSubmit={handleGraphQuery}>
            <label>
              Entity
              <input
                type="text"
                placeholder="e.g. Microsoft"
                value={entity}
                onChange={(event) => setEntity(event.target.value)}
              />
            </label>
            <label>
              Relation
              <input
                type="text"
                placeholder="e.g. founded_by"
                value={relation}
                onChange={(event) => setRelation(event.target.value)}
              />
            </label>
            <button type="submit">Run Graph Query</button>
          </form>

          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Head</th>
                  <th>Relation</th>
                  <th>Tail</th>
                </tr>
              </thead>
              <tbody>
                {filteredRows.map((row, idx) => (
                  <tr key={`${row.head}-${row.relation}-${row.tail}-${idx}`}>
                    <td>{row.head}</td>
                    <td>{row.relation}</td>
                    <td>{row.tail}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="graph-visual-wrap">
            <h3>Graph View</h3>
            <div ref={graphContainerRef} className="graph-canvas" />
          </div>
        </section>

        <section className="panel">
          <div className="panel-head">
            <h2>Semantic Search</h2>
            <p>Use vector similarity to retrieve top related documents.</p>
          </div>

          <form className="controls" onSubmit={handleSemanticSearch}>
            <label className="wide">
              Search Query
              <input
                type="text"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
              />
            </label>
            <button type="submit">Search</button>
          </form>

          <ul className="match-list">
            {searchRows.map((match) => (
              <li key={match.id}>
                <p>{match.text}</p>
                <span>Score: {Number(match.score).toFixed(2)}</span>
              </li>
            ))}
          </ul>
        </section>

      </main>

    </div>
  )
}

export default App
