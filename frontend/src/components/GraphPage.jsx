import { useState, useRef } from 'react'
import GraphCanvas from './graph/GraphCanvas'
import NodeDetailsPanel from './graph/NodeDetailsPanel'
import GraphControls from './graph/GraphControls'
import { nodes, edges } from './graph/graphData'

export default function GraphPage() {
  const [selectedNode, setSelectedNode] = useState(null)
  const [activeView, setActiveView] = useState('all')
  const canvasRef = useRef(null)

  const handleNodeSelect = (node) => {
    setSelectedNode((prev) => (prev?.id === node.id ? null : node))
  }

  const handleCloseDetails = () => {
    setSelectedNode(null)
  }

  const handleZoomIn = () => {
    canvasRef.current?.zoomIn?.()
  }

  const handleZoomOut = () => {
    canvasRef.current?.zoomOut?.()
  }

  const handleReset = () => {
    canvasRef.current?.resetView?.()
  }

  return (
    <div className="graph-page">
      <div className="graph-main">
        <div className="graph-header">
          <div>
            <h1 className="graph-title">Knowledge Graph</h1>
            <p className="graph-subtitle">Interactive relationship explorer</p>
          </div>
        </div>

        <GraphControls
          activeView={activeView}
          onViewChange={setActiveView}
          onZoomIn={handleZoomIn}
          onZoomOut={handleZoomOut}
          onReset={handleReset}
        />

        <div className="graph-canvas-container">
          <GraphCanvas
            ref={canvasRef}
            selectedNode={selectedNode}
            onNodeSelect={handleNodeSelect}
            activeView={activeView}
          />

          {/* Legend */}
          <div className="graph-legend">
            <span className="legend-title">Legend</span>
            <div className="legend-items">
              <div className="legend-item">
                <span className="legend-line" style={{ background: '#ef4444' }} />
                <span>Accomplice</span>
              </div>
              <div className="legend-item">
                <span className="legend-line" style={{ background: '#3b82f6' }} />
                <span>Evidence</span>
              </div>
              <div className="legend-item">
                <span className="legend-line dashed" style={{ background: '#10b981' }} />
                <span>Phone</span>
              </div>
              <div className="legend-item">
                <span className="legend-line" style={{ background: '#8b5cf6' }} />
                <span>Vehicle</span>
              </div>
              <div className="legend-item">
                <span className="legend-line" style={{ background: '#f59e0b' }} />
                <span>Fence</span>
              </div>
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
