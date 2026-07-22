import { useState, useRef, useEffect, useCallback } from 'react'
import { RefreshCw, Plus } from 'lucide-react'
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

  // Filter nodes by type
  const filteredNodes = typeFilter.length > 0
    ? nodes.filter((n) => typeFilter.includes(n.node_type || n.type))
    : nodes

  // Filter edges to only include connected nodes
  const filteredNodeIds = new Set(filteredNodes.map((n) => n.id || n.node_id))
  const filteredEdges = edges.filter((e) => {
    const src = e.source || e.source_id
    const tgt = e.target || e.target_id
    if (typeFilter.length === 0) return true
    return filteredNodeIds.has(src) && filteredNodeIds.has(tgt)
  })

  return (
    <div className="graph-page">
      <div className="graph-main">
        <div className="graph-header">
          <div>
            <h1 className="graph-title">Criminal Network Graph</h1>
            <p className="graph-subtitle">
              {stats ? `${stats.total_nodes || 0} nodes · ${stats.total_edges || 0} edges` : 'Interactive relationship explorer'}
            </p>
          </div>
          <div className="graph-header-actions">
            <button className="graph-build-btn" onClick={handleBuildGraph} disabled={building}>
              <Plus size={14} />
              {building ? 'Building...' : 'Build from Crimes'}
            </button>
            <button className="graph-refresh-btn" onClick={loadGraph} disabled={loading}>
              <RefreshCw size={14} className={loading ? 'similar-spinning' : ''} />
            </button>
          </div>
        </div>

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
            <div className="similar-loading">
              <div className="similar-spinner" />
              <span>Loading graph...</span>
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
  )
}
