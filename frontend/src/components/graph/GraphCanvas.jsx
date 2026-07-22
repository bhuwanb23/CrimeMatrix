import { useState, useRef, useEffect, useCallback, useMemo } from 'react'
import GraphNode from './GraphNode'
import GraphEdge from './GraphEdge'
import { nodes as fallbackNodes, edges as fallbackEdges } from './graphData'

// Force-directed layout — memoized to prevent recalculation on zoom/pan/hover
function forceLayout(nodes, edges, width = 800, height = 500) {
  if (!nodes.length) return { positionedNodes: [], positionedEdges: [] }

  const nodeMap = {}
  const cx = width / 2, cy = height / 2

  // Initialize positions in a circle
  nodes.forEach((n, i) => {
    const angle = (2 * Math.PI * i) / nodes.length
    const r = 150 + (((i * 7 + 13) % 50)) // deterministic spread
    nodeMap[n.id || n.node_id] = {
      ...n,
      x: cx + r * Math.cos(angle),
      y: cy + r * Math.sin(angle),
    }
  })

  // Force simulation (30 iterations)
  for (let iter = 0; iter < 30; iter++) {
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

    keys.forEach((k) => {
      nodeMap[k].x += (cx - nodeMap[k].x) * 0.01
      nodeMap[k].y += (cy - nodeMap[k].y) * 0.01
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

export default function GraphCanvas({ selectedNode, onNodeSelect, activeView: _activeView, nodes: realNodes, edges: realEdges }) {
  const svgRef = useRef(null)
  const containerRef = useRef(null)
  const [zoom, setZoom] = useState(1)
  const [pan, setPan] = useState({ x: 0, y: 0 })
  const [isPanning, setIsPanning] = useState(false)
  const [panStart, setPanStart] = useState({ x: 0, y: 0 })
  const [hoveredNode, setHoveredNode] = useState(null)
  const [containerSize, setContainerSize] = useState({ width: 800, height: 500 })

  // Use real data if provided, fallback to hardcoded
  const useRealData = realNodes && realNodes.length > 0
  const rawNodes = useRealData ? realNodes : fallbackNodes
  const rawEdges = useRealData ? realEdges : fallbackEdges

  // KEY FIX: Memoize force layout — only recalculates when nodes/edges change
  const { positionedNodes, positionedEdges } = useMemo(
    () => forceLayout(rawNodes, rawEdges, containerSize.width, containerSize.height),
    [rawNodes, rawEdges, containerSize.width, containerSize.height]
  )

  // Responsive container sizing
  useEffect(() => {
    const updateSize = () => {
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect()
        setContainerSize({ width: rect.width || 800, height: rect.height || 500 })
      }
    }
    updateSize()
    window.addEventListener('resize', updateSize)
    return () => window.removeEventListener('resize', updateSize)
  }, [])

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

  const handleZoomIn = useCallback(() => setZoom((z) => Math.min(3, z + 0.2)), [])
  const handleZoomOut = useCallback(() => setZoom((z) => Math.max(0.3, z - 0.2)), [])
  const handleReset = useCallback(() => { setZoom(1); setPan({ x: 0, y: 0 }) }, [])

  useEffect(() => {
    if (svgRef.current) {
      svgRef.current.zoomIn = handleZoomIn
      svgRef.current.zoomOut = handleZoomOut
      svgRef.current.resetView = handleReset
    }
  }, [handleZoomIn, handleZoomOut, handleReset])

  const connectedNodeIds = useMemo(() => {
    const ids = new Set()
    if (selectedNode) {
      const selId = selectedNode.id || selectedNode.node_id
      positionedEdges.forEach((e) => {
        const src = e.source || e.source_id
        const tgt = e.target || e.target_id
        if (src === selId) ids.add(tgt)
        if (tgt === selId) ids.add(src)
      })
    }
    return ids
  }, [selectedNode, positionedEdges])

  return (
    <div ref={containerRef} className="w-full h-full min-h-[400px]">
      <svg
        ref={svgRef}
        className="w-full h-full"
        style={{ cursor: isPanning ? 'grabbing' : 'grab' }}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      >
        <rect className="graph-bg" width="100%" height="100%" fill="transparent" />

        <g transform={`translate(${pan.x}, ${pan.y}) scale(${zoom})`}>
          {positionedEdges.map((edge, i) => {
            if (!edge.sourceNode || !edge.targetNode) return null
            const srcId = edge.source || edge.source_id
            const tgtId = edge.target || edge.target_id
            const selId = selectedNode?.id || selectedNode?.node_id
            const isHighlighted = selId && (srcId === selId || tgtId === selId)
            return (
              <GraphEdge key={i} edge={edge} sourceNode={edge.sourceNode} targetNode={edge.targetNode} isHighlighted={isHighlighted} />
            )
          })}

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

        {hoveredNode && !selectedNode && (
          <div className="graph-tooltip" style={{ left: (hoveredNode.x || 0) * zoom + pan.x + 20, top: (hoveredNode.y || 0) * zoom + pan.y - 10 }}>
            {hoveredNode.label || hoveredNode.name || hoveredNode.node_id}
          </div>
        )}
      </svg>
    </div>
  )
}
