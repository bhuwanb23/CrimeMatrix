import {
  FileText, Download, BookmarkPlus, Share2, X,
} from 'lucide-react'
import SourceCard from './SourceCard'
import { useLanguage } from '../../context/LanguageContext'
import { t, translateNodeLabel } from '../../utils/translate'

const referencedSources = [
  { type: 'fir', title: 'FIR #4521/2026', subtitleKey: 'theft_malleshwaram' },
  { type: 'suspect', titleKey: 'ravi_kumar', subtitleKey: 'suspect_linked_3_cases' },
  { type: 'evidence', subtitleKey: 'captured_at_215_am', titleKey: 'cctv_footage_main_road' },
  { type: 'location', subtitleKey: 'crime_hotspot_zone', titleKey: 'malleshwaram_bengaluru' },
]

const actions = [
  { icon: FileText, labelKey: 'generate_report', color: '#3b82f6' },
  { icon: Download, labelKey: 'export_conversation', color: '#10b981' },
  { icon: BookmarkPlus, labelKey: 'save_to_case', color: '#f59e0b' },
  { icon: Share2, labelKey: 'share_with_team', color: '#8b5cf6' },
]

const relatedCases = [
  { id: 'FIR #4489', titleKey: 'robbery_indiranagar', status: 'active' },
  { id: 'FIR #4501', titleKey: 'theft_koramangala', status: 'pending' },
  { id: 'FIR #4515', titleKey: 'cyber_fraud_ecity', status: 'active' },
]

export default function ContextPanel({ onClose }) {
  const { lang } = useLanguage()

  return (
    <div className="slide-panel-inner">
      <div className="slide-panel-header">
        <h2 className="slide-panel-title">{t('context', lang)}</h2>
        <button className="slide-panel-close" onClick={onClose} aria-label="Close">
          <X size={18} strokeWidth={1.8} />
        </button>
      </div>

      <div className="slide-panel-body">
        <section className="context-section">
          <h3 className="context-section-title">{t('referenced_sources', lang)}</h3>
          <div className="context-sources">
            {referencedSources.map((src, i) => {
              const displayTitle = src.titleKey ? t(src.titleKey, lang) : src.title
              const displaySubtitle = src.subtitleKey ? t(src.subtitleKey, lang) : src.subtitle
              return (
                <SourceCard
                  key={i}
                  type={src.type}
                  title={displayTitle}
                  subtitle={displaySubtitle}
                />
              )
            })}
          </div>
        </section>

        <section className="context-section">
          <h3 className="context-section-title">{t('actions', lang)}</h3>
          <div className="context-actions">
            {actions.map((action, i) => (
              <button key={i} className="context-action-btn">
                <div className="context-action-icon" style={{ background: action.color + '12', color: action.color }}>
                  <action.icon size={14} strokeWidth={1.8} />
                </div>
                <span className="context-action-label">{t(action.labelKey, lang)}</span>
              </button>
            ))}
          </div>
        </section>

        <section className="context-section">
          <h3 className="context-section-title">{t('related_cases', lang)}</h3>
          <div className="context-cases">
            {relatedCases.map((c, i) => (
              <div key={i} className="context-case-card">
                <div className="context-case-header">
                  <span className="context-case-id">{c.id}</span>
                  <span className={`context-case-status ${c.status}`}>{t(c.status, lang)}</span>
                </div>
                <p className="context-case-title">{t(c.titleKey, lang)}</p>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  )
}
