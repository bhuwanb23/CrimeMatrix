import { useState, useRef, useEffect, useCallback } from 'react'
import GraphNode from './GraphNode'
import GraphEdge from './GraphEdge'
import { nodes as allNodes, edges as allEdges } from './graphData'

export default function GraphCanvas({ selectedNode, onNodeSelect, activeView }) {
  const svgRef = useRef(null)
  const [zoom, setZoom] = useState(1)
  const [pan, setPan] = useState({ x: 0, y: 0 })
  const [isPanning, setIsPanning] = useState(false)
  const [panStart, setPanStart] = useState({ x: 0, y: 0 })
  const [hoveredNode, setHoveredNode] = useState(null)

  // Filter nodes/edges based on view
  const { nodes, edges } = filterByView(allNodes, allEdges, activeView, selectedNode)

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

  const handleMouseUp = () => {
    setIsPanning(false)
  }

  const handleZoomIn = () => setZoom((z) => Math.min(3, z + 0.2))
  const handleZoomOut = () => setZoom((z) => Math.max(0.3, z - 0.2))
  const handleReset = () => { setZoom(1); setPan({ x: 0, y: 0 }) }

  // Expose zoom controls
  useEffect(() => {
    if (svgRef.current) {
      svgRef.current.zoomIn = handleZoomIn
      svgRef.current.zoomOut = handleZoomOut
      svgRef.current.resetView = handleReset
    }
  })

  const connectedNodeIds = new Set()
  if (selectedNode) {
    edges.forEach((e) => {
      if (e.source === selectedNode.id) connectedNodeIds.add(e.target)
      if (e.target === selectedNode.id) connectedNodeIds.add(e.source)
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
        {edges.map((edge, i) => {
          const sourceNode = nodes.find((n) => n.id === edge.source)
          const targetNode = nodes.find((n) => n.id === edge.target)
          if (!sourceNode || !targetNode) return null
          const isHighlighted = selectedNode && (edge.source === selectedNode.id || edge.target === selectedNode.id)
          return (
            <GraphEdge
              key={i}
              edge={edge}
              sourceNode={sourceNode}
              targetNode={targetNode}
              isHighlighted={isHighlighted}
            />
          )
        })}

        {/* Nodes */}
        {nodes.map((node) => (
          <GraphNode
            key={node.id}
            node={node}
            isSelected={selectedNode?.id === node.id}
            isHighlighted={connectedNodeIds.has(node.id)}
            onClick={onNodeSelect}
            onMouseEnter={() => setHoveredNode(node)}
            onMouseLeave={() => setHoveredNode(null)}
          />
        ))}
      </g>

      {/* Tooltip */}
      {hoveredNode && !selectedNode && (
        <div className="graph-tooltip" style={{ left: hoveredNode.x * zoom + pan.x + 20, top: hoveredNode.y * zoom + pan.y - 10 }}>
          {hoveredNode.label}
        </div>
      )}
    </svg>
  )
}

function filterByView(nodes, edges, view, selectedNode) {
  if (view === 'all') return { nodes, edges }

  const filteredEdges = edges.filter((e) => {
    switch (view) {
      case 'criminal': return e.type === 'accomplice' || e.type === 'fence'
      case 'gang': return e.type === 'accomplice'
      case 'evidence': return e.type === 'evidence' || e.type === 'vehicle' || e.type === 'phone'
      default: return true
    }
  })

  const nodeIds = new Set()
  filteredEdges.forEach((e) => { nodeIds.add(e.source); nodeIds.add(e.target) })

  const filteredNodes = nodes.filter((n) => nodeIds.has(n.id) || n.type === 'suspect')

  return { nodes: filteredNodes, edges: filteredEdges }
}
