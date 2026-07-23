import { useState, useRef, useEffect, useCallback } from 'react'
import { RefreshCw, Plus, Network } from 'lucide-react'
import GraphCanvas from './graph/GraphCanvas'
import NodeDetailsPanel from './graph/NodeDetailsPanel'
import GraphControls from './graph/GraphControls'
import { getGraphNodes, getGraphEdges, getGraphStats, buildGraphFromCrimes } from '../services/graph'
import { useLanguage } from '../context/LanguageContext'

export default function GraphPage() {
  const [selectedNode, setSelectedNode] = useState(null)
  const [activeView, setActiveView] = useState('all')
  const [nodes, setNodes] = useState([])
  const [edges, setEdges] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [building, setBuilding] = useState(false)
  const [typeFilter, setTypeFilter] = useState([])
  const { t } = useLanguage()
  const canvasRef = useRef(null)

  const loadGraph = useCallback(async () => {
    setLoading(true)
    try {
      const [nodesRes, edgesRes, statsRes] = await Promise.all([
        getGraphNodes(),
        getGraphEdges(),
        getGraphStats(),
      ])
      const nodesData = nodesRes?.data || nodesRes
      const edgesData = edgesRes?.data || edgesRes
      setNodes(Array.isArray(nodesData) ? nodesData : nodesData?.nodes || [])
      setEdges(Array.isArray(edgesData) ? edgesData : edgesData?.edges || [])
      setStats(statsRes?.data || statsRes)
    } catch (e) {
      console.error('Failed to load graph', e)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { loadGraph() }, [loadGraph])

  async function handleBuildGraph() {
    setBuilding(true)
    try { await buildGraphFromCrimes(); await loadGraph() } catch (e) { console.error(e) } finally { setBuilding(false) }
  }

  function handleNodeSelect(node) { setSelectedNode((prev) => (prev?.id === node.id ? null : node)) }
  function handleCloseDetails() { setSelectedNode(null) }
  function handleZoomIn() { canvasRef.current?.zoomIn?.() }
  function handleZoomOut() { canvasRef.current?.zoomOut?.() }
  function handleReset() { canvasRef.current?.resetView?.() }

  function toggleTypeFilter(type) {
    setTypeFilter((prev) => prev.includes(type) ? prev.filter((t) => t !== type) : [...prev, type])
  }

  const filteredNodes = typeFilter.length > 0
    ? nodes.filter((n) => typeFilter.includes(n.node_type || n.type))
    : nodes

  const filteredNodeIds = new Set(filteredNodes.map((n) => n.id || n.node_id))
  const filteredEdges = edges.filter((e) => {
    const src = e.source || e.source_id
    const tgt = e.target || e.target_id
    if (typeFilter.length === 0) return true
    return filteredNodeIds.has(src) && filteredNodeIds.has(tgt)
  })

  const statItems = [
    { key: 'total_nodes', label: 'Nodes' },
    { key: 'total_edges', label: 'Edges' },
  ]

  return (
    <div className="flex flex-col gap-3 -m-6 p-4 h-[calc(100vh-var(--header-height))] min-h-0 overflow-hidden max-md:-m-4 max-md:p-3 max-md:h-auto max-md:min-h-[calc(100vh-var(--header-height))]">
      {/* Hero Header — compact like MapPage */}
      <div className="bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 rounded-2xl p-4 text-white shadow-lg shadow-orange-500/20 shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white/20 backdrop-blur rounded-xl flex items-center justify-center">
              <Network size={20} />
            </div>
            <div>
              <h1 className="text-lg font-bold">{t('Criminal Network Graph')}</h1>
              <p className="text-white/80 text-xs">
                {stats ? `${stats.total_nodes || 0} ${t('nodes')} · ${stats.total_edges || 0} ${t('edges')}` : t('Interactive relationship explorer')}
              </p>
            </div>
          </div>
          {stats && (
            <dl className="flex items-center m-0 min-w-0 overflow-x-auto">
              {statItems.map((item, i) => (
                <div key={item.key} className={`flex flex-col gap-0.5 px-3 whitespace-nowrap ${i > 0 ? 'border-l border-white/30' : ''}`}>
                  <dt className="m-0 text-[10px] font-medium uppercase tracking-wide text-white/60">{item.label}</dt>
                  <dd className="m-0 text-[15px] font-bold tabular-nums text-white">{stats[item.key] ?? 0}</dd>
                </div>
              ))}
            </dl>
          )}
          <div className="flex items-center gap-2 shrink-0">
            <button onClick={handleBuildGraph} disabled={building}
              className="flex items-center gap-1.5 px-3 py-2 bg-white/20 backdrop-blur hover:bg-white/30 rounded-lg text-xs font-medium text-white whitespace-nowrap transition-colors disabled:opacity-60">
              <Plus size={14} />
              {building ? t('Building...') : t('Build from Crimes')}
            </button>
            <button onClick={loadGraph} disabled={loading}
              className="inline-flex items-center justify-center gap-1.5 px-3 py-2 bg-white/20 backdrop-blur hover:bg-white/30 rounded-lg text-xs font-medium text-white whitespace-nowrap transition-colors disabled:opacity-60">
              <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
              {t('Refresh')}
            </button>
          </div>
        </div>
      </div>

      {/* Controls Bar — white toolbar like MapPage */}
      <div role="toolbar" aria-label="Graph controls"
        className="flex items-center gap-3 flex-wrap px-3 py-2.5 bg-white border border-slate-200 rounded-[10px] shrink-0">
        <GraphControls
          activeView={activeView}
          onViewChange={setActiveView}
          onZoomIn={handleZoomIn}
          onZoomOut={handleZoomOut}
          onReset={handleReset}
          typeFilter={typeFilter}
          onToggleType={toggleTypeFilter}
        />
      </div>

      {/* Canvas + Details Panel — same layout as MapPage */}
      <div className="flex gap-3 flex-1 min-h-0 min-w-0 max-lg:flex-col">
        <div className="flex flex-1 flex-col min-w-0 min-h-0 bg-white border border-slate-200 rounded-xl overflow-hidden max-lg:min-h-[min(52vh,480px)] max-lg:order-1 max-md:min-h-[360px]">
          {loading ? (
            <div className="flex items-center justify-center h-full">
              <div className="w-6 h-6 border-2 border-slate-200 border-t-orange-500 rounded-full animate-spin" />
              <span className="ml-3 text-sm text-slate-500">{t('Loading graph...')}</span>
            </div>
          ) : (
            <GraphCanvas
              ref={canvasRef}
              selectedNode={selectedNode}
              onNodeSelect={handleNodeSelect}
              activeView={activeView}
              nodes={filteredNodes}
              edges={filteredEdges}
            />
          )}

          {/* Legend overlay */}
          <div className="absolute bottom-3 left-3 bg-white/90 backdrop-blur-sm border border-slate-200 rounded-lg px-3 py-2 shadow-sm">
            <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">{t('Legend')}</span>
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-red-500" /><span className="text-[10px] text-slate-600">{t('Suspect')}</span></div>
              <div className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-blue-500" /><span className="text-[10px] text-slate-600">{t('Evidence')}</span></div>
              <div className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-violet-500" /><span className="text-[10px] text-slate-600">{t('Vehicle')}</span></div>
              <div className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-emerald-500" /><span className="text-[10px] text-slate-600">{t('Phone')}</span></div>
              <div className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-amber-500" /><span className="text-[10px] text-slate-600">{t('Criminal')}</span></div>
            </div>
          </div>
        </div>

        <NodeDetailsPanel
          node={selectedNode}
          edges={edges}
          nodes={nodes}
          onClose={handleCloseDetails}
        />
      </div>
    </div>
  )
}
