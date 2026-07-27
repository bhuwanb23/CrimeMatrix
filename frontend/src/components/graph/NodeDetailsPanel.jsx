import { X, FileText, Phone, Car, Users } from 'lucide-react'
import { edgeColors } from './graphData'
import { useLanguage } from '../../context/LanguageContext'

const typeIcons = {
  suspect: Users,
  evidence: FileText,
  vehicle: Car,
  phone: Phone,
}

export default function NodeDetailsPanel({ node, edges, nodes, onClose, className = '' }) {
  const { t } = useLanguage()

  if (!node) {
    return (
      <aside className={`flex w-[280px] shrink-0 flex-col overflow-hidden rounded-xl border border-[var(--border)] bg-[var(--bg-card)] max-lg:order-2 max-lg:w-full max-lg:max-h-60 max-md:max-h-[280px] ${className}`}
        aria-label="Node details">
        <div className="flex flex-col items-center justify-center gap-2 px-4 py-12 text-center text-[var(--text-muted)]">
          <span className="text-2xl" aria-hidden="true">🔍</span>
          <p className="m-0 text-xs font-semibold">{t('Select a Node')}</p>
          <p className="m-0 text-[10px]">{t('Click on any node in the graph to view details')}</p>
        </div>
      </aside>
    )
  }

  const Icon = typeIcons[node.type] || Users
  const connections = edges.filter(
    (e) => e.source === node.id || e.target === node.id
  )

  return (
    <aside className={`flex w-[280px] shrink-0 flex-col overflow-hidden rounded-xl border border-[var(--border)] bg-[var(--bg-card)] max-lg:order-2 max-lg:w-full max-lg:max-h-60 max-md:max-h-[280px] ${className}`}
      aria-label="Node details">
      {/* Header */}
      <div className="flex items-center justify-between gap-2 border-b border-[var(--border)] px-3.5 py-3">
        <div className="flex items-center gap-2 min-w-0">
          <div className={`inline-flex size-6 items-center justify-center rounded-md ${node.type === 'suspect' ? 'bg-red-500/10 text-red-500' : 'bg-blue-500/10 text-blue-500'}`}>
            <Icon size={13} />
          </div>
          <h2 className="m-0 min-w-0 text-[13px] font-semibold text-[var(--text-primary)]">
            {node.label || t(node.type)}
          </h2>
        </div>
        <button type="button" onClick={onClose} aria-label="Close node details"
          className="inline-flex size-7 shrink-0 items-center justify-center rounded-md border-0 bg-transparent text-[var(--text-muted)] cursor-pointer hover:bg-[var(--bg-hover)] hover:text-[var(--text-primary)] focus-visible:outline-2 focus-visible:outline-amber-500 focus-visible:outline-offset-2">
          <X size={16} />
        </button>
      </div>

      {/* Node Info */}
      <div className="flex-1 overflow-y-auto">
        {node.type === 'suspect' ? (
          <div className="border-b border-[var(--border)] p-3.5">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold text-white"
                style={{ background: node.gradient || '#0f172a' }}>
                {node.id}
              </div>
              <div>
                <p className="m-0 text-xs font-semibold text-[var(--text-primary)]">{node.label}</p>
                <p className="m-0 text-[10px] text-[var(--text-muted)] capitalize">{t(node.type)}</p>
              </div>
            </div>
            <div className="flex gap-3">
              <div className="flex flex-col">
                <span className="text-sm font-bold text-[var(--text-primary)]">{node.risk}</span>
                <span className="text-[10px] text-[var(--text-muted)]">{t('Risk')}</span>
              </div>
              <div className="flex flex-col">
                <span className="text-sm font-bold text-[var(--text-primary)]">{node.cases}</span>
                <span className="text-[10px] text-[var(--text-muted)]">{t('Cases')}</span>
              </div>
            </div>
          </div>
        ) : (
          <div className="border-b border-[var(--border)] p-3.5">
            <p className="m-0 text-2xl">{node.icon}</p>
            <p className="m-0 mt-1 text-xs font-semibold text-[var(--text-primary)]">{node.label}</p>
            <p className="m-0 text-[10px] text-[var(--text-muted)] capitalize">{t(node.type)}</p>
          </div>
        )}

        {/* Connections */}
        <section className="p-3.5">
          <h3 className="mb-2 mt-0 flex items-center gap-1.5 text-[11px] font-semibold text-[var(--text-muted)]">
            {t('Connections')} ({connections.length})
          </h3>
          <div className="flex flex-col gap-2">
            {connections.length === 0 ? (
              <p className="m-0 text-xs text-[var(--text-muted)]">{t('No connections')}</p>
            ) : connections.map((conn, i) => {
              const otherNodeId = conn.source === node.id ? conn.target : conn.source
              const otherNode = nodes.find((n) => n.id === otherNodeId)
              return (
                <div key={i} className="flex items-center gap-2 text-xs">
                  <span className="size-2 shrink-0 rounded-full" style={{ background: edgeColors[conn.type] || '#64748b' }} />
                  <div className="flex min-w-0 flex-col gap-px">
                    <span className="text-[var(--text-primary)] truncate">{otherNode?.label || otherNodeId}</span>
                    <span className="text-[11px] text-[var(--text-muted)]">{conn.label || conn.type}</span>
                  </div>
                </div>
              )
            })}
          </div>
        </section>

        {/* Actions */}
        {node.type === 'suspect' && (
          <div className="border-t border-[var(--border)] p-3.5 flex gap-2">
            <button className="flex-1 px-3 py-1.5 text-[11px] font-medium text-white bg-blue-500 hover:bg-blue-600 rounded-lg transition-colors cursor-pointer">
              {t('View Full Profile')}
            </button>
            <button className="flex-1 px-3 py-1.5 text-[11px] font-medium text-[var(--text-secondary)] bg-[var(--bg-input)] hover:bg-[var(--bg-input)] rounded-lg transition-colors cursor-pointer">
              {t('Add to Investigation')}
            </button>
          </div>
        )}
      </div>
    </aside>
  )
}
