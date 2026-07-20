import { useState, useRef, useEffect, useCallback } from 'react'
import GraphNode from './GraphNode'
import GraphEdge from './GraphEdge'
import { nodes as fallbackNodes, edges as fallbackEdges } from './graphData'

// Force-directed layout for real data
function forceLayout(nodes, edges, width = 800, height = 500) {
  if (!nodes.length) return { positionedNodes: [], positionedEdges: [] }

  const nodeMap = {}
  const cx = width / 2, cy = height / 2

  // Initialize positions in a circle
  nodes.forEach((n, i) => {
    const angle = (2 * Math.PI * i) / nodes.length
    const r = 150 + Math.random() * 50
    nodeMap[n.id || n.node_id] = {
      ...n,
      x: cx + r * Math.cos(angle),
      y: cy + r * Math.sin(angle),
    }
  })

  // Simple force simulation (30 iterations)
  for (let iter = 0; iter < 30; iter++) {
    // Repulsion between all nodes
    const keys = Object.keys(nodeMap)
    for (let i = 0; i < keys.length; i++) {
      for (let j = i + 1; j < keys.length; j++) {
        const a = nodeMap[keys[i]], b = nodeMap[keys[j]]
        let dx = a.x - b.x, dy = a.y - b.y
        let dist = Math.sqrt(dx * dx + dy * dy) || 1
        let force = 2000 / (dist * dist)
        let fx = (dx / dist) * force, fy = (dy / dist) * force
        a.x += fx; a.y += fy
        b.x -= fx; b.y -= fy
      }
    }

    // Attraction along edges
    edges.forEach((e) => {
      const src = nodeMap[e.source || e.source_id]
      const tgt = nodeMap[e.target || e.target_id]
      if (!src || !tgt) return
      let dx = tgt.x - src.x, dy = tgt.y - src.y
      let dist = Math.sqrt(dx * dx + dy * dy) || 1
      let force = (dist - 100) * 0.01
      let fx = (dx / dist) * force, fy = (dy / dist) * force
      src.x += fx; src.y += fy
      tgt.x -= fx; tgt.y -= fy
    })

    // Center gravity
    keys.forEach((k) => {
      nodeMap[k].x += (cx - nodeMap[k].x) * 0.01
      nodeMap[k].y += (cy - nodeMap[k].y) * 0.01
      // Keep in bounds
      nodeMap[k].x = Math.max(40, Math.min(width - 40, nodeMap[k].x))
      nodeMap[k].y = Math.max(40, Math.min(height - 40, nodeMap[k].y))
    })
  }

  return {
    positionedNodes: Object.values(nodeMap),
    positionedEdges: edges.map((e) => ({
      ...e,
      sourceNode: nodeMap[e.source || e.source_id],
      targetNode: nodeMap[e.target || e.target_id],
    })).filter((e) => e.sourceNode && e.targetNode),
  }
}

const edgeColors = {
  accomplice: '#ef4444', fence: '#f59e0b', evidence: '#3b82f6',
  vehicle: '#8b5cf6', phone: '#10b981', is_criminal: '#f59e0b',
  has_evidence: '#3b82f6', uses: '#8b5cf6', owns: '#10b981',
}

const nodeColors = {
  suspect: '#ef4444', criminal: '#f59e0b', evidence: '#3b82f6',
  vehicle: '#8b5cf6', phone: '#10b981', victim: '#64748b', witness: '#64748b',
}

export default function GraphCanvas({ selectedNode, onNodeSelect, activeView, nodes: realNodes, edges: realEdges }) {
  const svgRef = useRef(null)
  const [zoom, setZoom] = useState(1)
  const [pan, setPan] = useState({ x: 0, y: 0 })
  const [isPanning, setIsPanning] = useState(false)
  const [panStart, setPanStart] = useState({ x: 0, y: 0 })
  const [hoveredNode, setHoveredNode] = useState(null)

  // Use real data if provided, fallback to hardcoded
  const useRealData = realNodes && realNodes.length > 0
  const rawNodes = useRealData ? realNodes : fallbackNodes
  const rawEdges = useRealData ? realEdges : fallbackEdges

  // Apply force layout to real data
  const { positionedNodes, positionedEdges } = forceLayout(rawNodes, rawEdges)

  const handleWheel = useCallback((e) => {
    e.preventDefault()
    const delta = e.deltaY > 0 ? -0.1 : 0.1
    setZoom((z) => Math.max(0.3, Math.min(3, z + delta)))
  }, [])

  useEffect(() => {
    const svg = svgRef.current
    if (svg) {
      svg.addEventListener('wheel', handleWheel, { passive: false })
      return () => svg.removeEventListener('wheel', handleWheel)
    }
  }, [handleWheel])

  const handleMouseDown = (e) => {
    if (e.target === svgRef.current || e.target.classList.contains('graph-bg')) {
      setIsPanning(true)
      setPanStart({ x: e.clientX - pan.x, y: e.clientY - pan.y })
    }
  }

  const handleMouseMove = (e) => {
    if (isPanning) {
      setPan({ x: e.clientX - panStart.x, y: e.clientY - panStart.y })
    }
  }

  const handleMouseUp = () => setIsPanning(false)

  const handleZoomIn = () => setZoom((z) => Math.min(3, z + 0.2))
  const handleZoomOut = () => setZoom((z) => Math.max(0.3, z - 0.2))
  const handleReset = () => { setZoom(1); setPan({ x: 0, y: 0 }) }

  useEffect(() => {
    if (svgRef.current) {
      svgRef.current.zoomIn = handleZoomIn
      svgRef.current.zoomOut = handleZoomOut
      svgRef.current.resetView = handleReset
    }
  })

  const connectedNodeIds = new Set()
  if (selectedNode) {
    const selId = selectedNode.id || selectedNode.node_id
    positionedEdges.forEach((e) => {
      const src = e.source || e.source_id
      const tgt = e.target || e.target_id
      if (src === selId) connectedNodeIds.add(tgt)
      if (tgt === selId) connectedNodeIds.add(src)
    })
  }

  return (
    <svg
      ref={svgRef}
      className="graph-svg"
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
    >
      <rect className="graph-bg" width="100%" height="100%" fill="transparent" />

      <g transform={`translate(${pan.x}, ${pan.y}) scale(${zoom})`}>
        {/* Edges */}
        {positionedEdges.map((edge, i) => {
          if (!edge.sourceNode || !edge.targetNode) return null
          const srcId = edge.source || edge.source_id
          const tgtId = edge.target || edge.target_id
          const selId = selectedNode?.id || selectedNode?.node_id
          const isHighlighted = selId && (srcId === selId || tgtId === selId)
          return (
            <GraphEdge
              key={i}
              edge={edge}
              sourceNode={edge.sourceNode}
              targetNode={edge.targetNode}
              isHighlighted={isHighlighted}
            />
          )
        })}

        {/* Nodes */}
        {positionedNodes.map((node) => {
          const nodeId = node.id || node.node_id
          return (
            <GraphNode
              key={nodeId}
              node={node}
              isSelected={(selectedNode?.id || selectedNode?.node_id) === nodeId}
              isHighlighted={connectedNodeIds.has(nodeId)}
              onClick={onNodeSelect}
              onMouseEnter={() => setHoveredNode(node)}
              onMouseLeave={() => setHoveredNode(null)}
            />
          )
        })}
      </g>

      {/* Tooltip */}
      {hoveredNode && !selectedNode && (
        <div className="graph-tooltip" style={{ left: (hoveredNode.x || 0) * zoom + pan.x + 20, top: (hoveredNode.y || 0) * zoom + pan.y - 10 }}>
          {hoveredNode.label || hoveredNode.name || hoveredNode.node_id}
        </div>
      )}
    </svg>
  )
}
