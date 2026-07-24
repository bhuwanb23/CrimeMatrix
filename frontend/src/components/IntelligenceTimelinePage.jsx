import { useState, useEffect } from 'react'
import { useLanguage } from '../context/LanguageContext'
import {
  Clock, Activity, AlertTriangle, Link2, Sparkles, Shield, Globe,
  RefreshCw, Calendar, ChevronRight,
} from 'lucide-react'
import {
  getUnifiedTimeline, getTimelineStats,
} from '../services/intelligenceTimeline'

const sourceConfig = {
  event: { icon: Activity, label: 'Event', color: 'text-emerald-400', bg: 'bg-emerald-500/10', dot: 'bg-emerald-400' },
  alert: { icon: AlertTriangle, label: 'Alert', color: 'text-red-400', bg: 'bg-red-500/10', dot: 'bg-red-400' },
  evidence: { icon: Link2, label: 'Evidence', color: 'text-blue-400', bg: 'bg-blue-500/10', dot: 'bg-blue-400' },
  recommendation: { icon: Sparkles, label: 'Recommendation', color: 'text-amber-400', bg: 'bg-amber-500/10', dot: 'bg-amber-400' },
  risk: { icon: Shield, label: 'Risk/Priority', color: 'text-purple-400', bg: 'bg-purple-500/10', dot: 'bg-purple-400' },
  match: { icon: Globe, label: 'Cross-District', color: 'text-cyan-400', bg: 'bg-cyan-500/10', dot: 'bg-cyan-400' },
}

const tabs = [
  { key: null, label: 'All', icon: Clock },
  { key: 'event', label: 'Events', icon: Activity },
  { key: 'alert', label: 'Alerts', icon: AlertTriangle },
  { key: 'evidence', label: 'Evidence', icon: Link2 },
  { key: 'recommendation', label: 'Recommendations', icon: Sparkles },
  { key: 'risk', label: 'Risk', icon: Shield },
  { key: 'match', label: 'Matches', icon: Globe },
]

function groupByDate(entries) {
  const groups = {}
  entries.forEach(entry => {
    const date = entry.created_at
      ? new Date(entry.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
      : 'Unknown Date'
    if (!groups[date]) groups[date] = []
    groups[date].push(entry)
  })
  return groups
}

function timeAgo(dateStr, t) {
  if (!dateStr) return ''
  const now = Date.now()
  const then = new Date(dateStr).getTime()
  const diff = now - then
  if (diff < 60000) return t('Just now')
  if (diff < 3600000) return `${Math.floor(diff / 60000)}${t('m ago')}`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}${t('h ago')}`
  return `${Math.floor(diff / 86400000)}${t('d ago')}`
}

export default function IntelligenceTimelinePage() {
  const { t } = useLanguage()
  const [entries, setEntries] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState(null)
  const [refreshing, setRefreshing] = useState(false)

  async function loadData(source = null) {
    setLoading(true)
    try {
      const [timelineRes, statsRes] = await Promise.all([
        getUnifiedTimeline({ limit: 100, source }),
        getTimelineStats(),
      ])
      const data = timelineRes?.data || timelineRes
      setEntries(data?.entries || [])
      setStats(statsRes?.data || statsRes)
    } catch (e) {
      console.error('Timeline load failed', e)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { loadData() }, [])

  function handleTabChange(key) {
    setActiveTab(key)
    loadData(key)
  }

  async function handleRefresh() {
    setRefreshing(true)
    await loadData(activeTab)
    setRefreshing(false)
  }

  const grouped = groupByDate(entries)

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Hero Header */}
        <div className="bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 rounded-2xl p-4 px-6 text-white shadow-lg shadow-orange-500/20 shrink-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-white/20 backdrop-blur rounded-xl flex items-center justify-center">
                <Clock size={20} />
              </div>
              <div>
                <h1 className="text-lg font-bold">Intelligence Timeline</h1>
                <p className="text-white/80 text-xs">Complete audit trail of AI-generated intelligence</p>
              </div>
            </div>
            <button onClick={handleRefresh} disabled={refreshing}
              className="p-2 bg-white/20 backdrop-blur hover:bg-white/30 rounded-xl transition-all">
              <RefreshCw size={14} className={refreshing ? 'animate-spin' : ''} />
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-5 gap-4">
            {[
              { label: 'Total Entries', value: stats.total_timeline || 0, icon: Clock, color: 'text-violet-500' },
              { label: 'Events', value: stats.events || 0, icon: Activity, color: 'text-emerald-500' },
              { label: 'Alerts', value: (stats.alerts || 0) + (stats.early_warnings || 0), icon: AlertTriangle, color: 'text-red-500' },
              { label: 'Evidence Links', value: (stats.evidence_links || 0) + (stats.link_history || 0), icon: Link2, color: 'text-blue-500' },
              { label: 'Recommendations', value: stats.recommendation_history || 0, icon: Sparkles, color: 'text-amber-500' },
            ].map(({ label, value, icon: Icon, color }) => (
              <div key={label} className="bg-white border border-slate-200 rounded-xl p-4 flex items-center gap-3">
                <div className={`w-10 h-10 rounded-xl bg-slate-50 flex items-center justify-center`}>
                  <Icon size={18} className={color} />
                </div>
                <div>
                  <p className="text-lg font-bold text-slate-900">{value}</p>
                  <p className="text-[10px] text-slate-500">{t(label)}</p>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Tabs */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1">
          {tabs.map(tab => {
            const TabIcon = tab.icon
            const count = tab.key ? entries.filter(e => e.source === tab.key).length : entries.length
            return (
              <button
                key={tab.key || 'all'}
                onClick={() => handleTabChange(tab.key)}
                className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-medium whitespace-nowrap transition-all ${
                  activeTab === tab.key
                    ? 'bg-violet-500/10 text-violet-600 border border-violet-500/30 shadow-sm'
                    : 'text-slate-500 hover:text-slate-700 hover:bg-white border border-transparent'
                }`}
              >
                <TabIcon size={12} />
                {t(tab.label)}
                {count > 0 && (
                  <span className="text-[10px] bg-slate-100 text-slate-500 px-1.5 py-0.5 rounded-full">
                    {count}
                  </span>
                )}
              </button>
            )
          })}
        </div>

        {/* Timeline */}
        {loading ? (
          <div className="flex items-center justify-center py-16">
            <div className="w-6 h-6 border-2 border-violet-400/30 border-t-violet-400 rounded-full animate-spin" />
            <span className="ml-3 text-slate-500 text-sm">{t('Loading timeline...')}</span>
          </div>
        ) : entries.length === 0 ? (
          <div className="text-center py-16 bg-white border border-slate-200 rounded-2xl">
            <Clock size={40} className="mx-auto text-slate-200 mb-3" />
            <p className="text-slate-500 font-medium">{t('No timeline entries')}</p>
            <p className="text-slate-400 text-xs mt-1">{t('Intelligence activity will appear here as events are processed')}</p>
          </div>
        ) : (
          <div className="space-y-6">
            {Object.entries(grouped).map(([date, dateEntries]) => (
              <div key={date}>
                {/* Date header */}
                <div className="flex items-center gap-3 mb-3">
                  <Calendar size={12} className="text-slate-400" />
                  <span className="text-xs font-semibold text-slate-600">{date === 'Unknown Date' ? t('Unknown Date') : date}</span>
                  <div className="flex-1 h-px bg-slate-200" />
                  <span className="text-[10px] text-slate-400">{dateEntries.length} {t('entries')}</span>
                </div>

                {/* Entries */}
                <div className="space-y-1.5 ml-4 border-l-2 border-slate-100 pl-4">
                  {dateEntries.map((entry, i) => {
                    const config = sourceConfig[entry.source] || sourceConfig.event
                    const Icon = config.icon
                    return (
                      <div
                        key={entry.id || i}
                        className="relative flex items-start gap-3 p-3 bg-white border border-slate-100 rounded-xl hover:border-slate-200 hover:shadow-sm transition-all"
                      >
                        {/* Timeline dot */}
                        <div className={`absolute -left-[21px] top-4 w-2.5 h-2.5 rounded-full ${config.dot} ring-2 ring-white`} />

                        {/* Icon */}
                        <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${config.bg}`}>
                          <Icon size={14} className={config.color} />
                        </div>

                        {/* Content */}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2">
                            <span className={`text-[10px] font-semibold uppercase tracking-wider ${config.color}`}>
                              {t(config.label)}
                            </span>
                            {entry.score != null && (
                              <span className="text-[10px] font-mono text-slate-400">{Math.round(entry.score)}%</span>
                            )}
                          </div>
                          <p className="text-xs font-medium text-slate-900 mt-0.5 leading-relaxed">{entry.title}</p>
                          {entry.details && (
                            <p className="text-[11px] text-slate-500 mt-0.5 line-clamp-2">{entry.details}</p>
                          )}
                        </div>

                        {/* Timestamp */}
                        <span className="text-[10px] text-slate-400 whitespace-nowrap flex-shrink-0">
                          {timeAgo(entry.created_at, t)}
                        </span>
                      </div>
                    )
                  })}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
