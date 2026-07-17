import { useState, useRef } from 'react'
import GraphCanvas from './graph/GraphCanvas'
import NodeDetailsPanel from './graph/NodeDetailsPanel'
import GraphControls from './graph/GraphControls'
import { nodes, edges } from './graph/graphData'

import { useLanguage } from '../context/LanguageContext'
import { t } from '../utils/translate'

export default function GraphPage() {
  const { lang } = useLanguage()
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
            <h1 className="graph-title">{t('knowledge_graph', lang)}</h1>
            <p className="graph-subtitle">{t('interactive_relationship_explorer', lang)}</p>
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
            <span className="legend-title">{t('legend', lang)}</span>
            <div className="legend-items">
              <div className="legend-item">
                <span className="legend-line" style={{ background: '#ef4444' }} />
                <span>{t('accomplice', lang)}</span>
              </div>
              <div className="legend-item">
                <span className="legend-line" style={{ background: '#3b82f6' }} />
                <span>{t('evidence', lang)}</span>
              </div>
              <div className="legend-item">
                <span className="legend-line dashed" style={{ background: '#10b981' }} />
                <span>{t('phone', lang)}</span>
              </div>
              <div className="legend-item">
                <span className="legend-line" style={{ background: '#8b5cf6' }} />
                <span>{t('vehicle', lang)}</span>
              </div>
              <div className="legend-item">
                <span className="legend-line" style={{ background: '#f59e0b' }} />
                <span>{t('fence', lang)}</span>
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
