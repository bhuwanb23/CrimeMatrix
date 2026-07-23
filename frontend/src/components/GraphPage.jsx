import { useState, useRef, useEffect, useCallback } from 'react'
import { RefreshCw, Plus, Network } from 'lucide-react'
import GraphCanvas from './graph/GraphCanvas'
import NodeDetailsPanel from './graph/NodeDetailsPanel'
import GraphControls from './graph/GraphControls'
import { getGraphNodes, getGraphEdges, getGraphStats, buildGraphFromCrimes } from '../services/graph'

export default function GraphPage() {
  const [selectedNode, setSelectedNode] = useState(null)
  const [activeView, setActiveView] = useState('all')
  const [nodes, setNodes] = useState([])
  const [edges, setEdges] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [building, setBuilding] = useState(false)
  const [typeFilter, setTypeFilter] = useState([])
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

  useEffect(() => {
    loadGraph()
  }, [loadGraph])

  async function handleBuildGraph() {
    setBuilding(true)
    try {
      await buildGraphFromCrimes()
      await loadGraph()
    } catch (e) {
      console.error('Failed to build graph', e)
    } finally {
      setBuilding(false)
    }
  }

  function handleNodeSelect(node) {
    setSelectedNode((prev) => (prev?.id === node.id ? null : node))
  }

  function handleCloseDetails() {
    setSelectedNode(null)
  }

  function handleZoomIn() { canvasRef.current?.zoomIn?.() }
  function handleZoomOut() { canvasRef.current?.zoomOut?.() }
  function handleReset() { canvasRef.current?.resetView?.() }

  function toggleTypeFilter(type) {
    setTypeFilter((prev) =>
      prev.includes(type) ? prev.filter((t) => t !== type) : [...prev, type]
    )
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

  return (
    <div className="flex flex-col" style={{ height: 'calc(100vh - var(--header-height))' }}>
      {/* Hero Header */}
      <div className="bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 p-4 px-6 text-white shrink-0">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 bg-white/20 backdrop-blur rounded-xl flex items-center justify-center">
              <Network size={20} />
            </div>
            <div>
              <h1 className="text-lg font-bold">Criminal Network Graph</h1>
              <p className="text-white/80 text-xs">
                {stats ? `${stats.total_nodes || 0} nodes · ${stats.total_edges || 0} edges` : 'Interactive relationship explorer'}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button onClick={handleBuildGraph} disabled={building}
              className="flex items-center gap-1.5 px-4 py-2 bg-white/20 backdrop-blur hover:bg-white/30 rounded-xl text-sm font-semibold transition-all disabled:opacity-50">
              <Plus size={14} />
              {building ? 'Building...' : 'Build from Crimes'}
            </button>
            <button onClick={loadGraph} disabled={loading}
              className="p-2 bg-white/20 backdrop-blur hover:bg-white/30 rounded-xl transition-all">
              <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
            </button>
          </div>
        </div>
      </div>

      {/* Graph Area */}
      <div className="graph-page flex-1 min-h-0">
        <div className="graph-main">
          <GraphControls
            activeView={activeView}
            onViewChange={setActiveView}
            onZoomIn={handleZoomIn}
            onZoomOut={handleZoomOut}
            onReset={handleReset}
            typeFilter={typeFilter}
            onToggleType={toggleTypeFilter}
          />

          <div className="graph-canvas-container">
            {loading ? (
              <div className="flex items-center justify-center h-full">
                <div className="w-6 h-6 border-2 border-slate-200 border-t-orange-500 rounded-full animate-spin" />
                <span className="ml-3 text-sm text-slate-500">Loading graph...</span>
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

            <div className="graph-legend">
              <span className="legend-title">Legend</span>
              <div className="legend-items">
                <div className="legend-item"><span className="legend-dot" style={{ background: '#ef4444' }} /> Suspect</div>
                <div className="legend-item"><span className="legend-dot" style={{ background: '#3b82f6' }} /> Evidence</div>
                <div className="legend-item"><span className="legend-dot" style={{ background: '#8b5cf6' }} /> Vehicle</div>
                <div className="legend-item"><span className="legend-dot" style={{ background: '#10b981' }} /> Phone</div>
                <div className="legend-item"><span className="legend-dot" style={{ background: '#f59e0b' }} /> Criminal</div>
              </div>
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
