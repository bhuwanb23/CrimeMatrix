import { Database, MapPin, BarChart3, FileText } from 'lucide-react'
import { useState, useEffect } from 'react'
import { getPredictionSources } from '../../services/predictions'
import { useLanguage } from '../../context/LanguageContext'


const sourceIcons = { district: MapPin, crime_type: BarChart3, model: Database, historical_data: FileText }

export default function SourceReferences({ predictionId }) {
  const { t } = useLanguage()
  const [sources, setSources] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!predictionId) return

    async function loadSources() {
      setLoading(true)
      try {
        const res = await getPredictionSources(predictionId)
        setSources(res?.data?.items || [])
      } catch (e) { console.error(e) } finally { setLoading(false) }
    }

    loadSources()
  }, [predictionId])

  if (sources.length === 0 && !loading) return null

  return (
    <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-4">
      <div className="flex items-center gap-2 mb-3">
        <Database size={14} className="text-amber-500" />
        <h3 className="text-sm font-semibold text-[var(--text-primary)]">{t('Data Sources')}</h3>
      </div>

      {loading ? (
        <p className="text-[10px] text-[var(--text-muted)]">{t('Loading sources...')}</p>
      ) : (
        <div className="space-y-1.5">
          {sources.map((s, i) => {
            const Icon = sourceIcons[s.source_type] || Database
            return (
              <div key={i} className="flex items-center gap-2 p-1.5 bg-[var(--bg-muted)] rounded">
                <Icon size={10} className="text-[var(--text-muted)]" />
                <span className="text-[10px] text-[var(--text-secondary)] flex-1">{s.source_name}</span>
                <span className="text-[10px] text-[var(--text-muted)]">{Math.round((s.relevance_score || 0) * 100)}%</span>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
