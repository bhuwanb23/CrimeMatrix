import { useLanguage } from '../context/LanguageContext'
import { useEffect, useState } from 'react'
import { ArrowUpRight, ArrowDownRight, ClipboardList, TrendingUp, AlertTriangle, Users, BarChart3, LayoutDashboard } from 'lucide-react'
import CaseTrendChart from './charts/CaseTrendChart'
import CrimeTypeChart from './charts/CrimeTypeChart'
import DistrictDonut from './charts/DistrictDonut'
import StatusBars from './charts/StatusBars'
import InvestmentCalendar from './charts/InvestmentCalendar'
import RecommendationsPanel from './recommendations/RecommendationsPanel'
import { get } from '../services/api'
import { getDashboardStats, getDashboardSummary } from '../services/analyticsDashboard'

function formatNumber(n) {
  if (n == null || Number.isNaN(n)) return '—'
  return Number(n).toLocaleString()
}

export default function DashboardContent() {
  const { t } = useLanguage()
  const [stats, setStats] = useState(null)
  const [dashStats, setDashStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false
    async function load() {
      setLoading(true)
      setError(null)
      try {
        const [statsRes, dashRes, summaryRes] = await Promise.all([
          get('/statistics'),
          getDashboardStats().catch(() => null),
          getDashboardSummary().catch(() => null),
        ])
        if (cancelled) return
        setStats(statsRes?.data || null)
        setDashStats(dashRes?.data || summaryRes?.data || null)
      } catch (e) {
        if (!cancelled) setError(e?.message || 'Failed to load dashboard')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [])

  const totals = stats?.totals || {}
  const byStatus = stats?.cases_by_status || {}
  const resolution = stats?.resolution_rate ?? dashStats?.resolution_rate

  const cards = [
    { icon: ClipboardList, label: 'Total Cases', value: formatNumber(totals.cases ?? dashStats?.total_cases), trend: loading ? '…' : `${byStatus.active ?? 0} active`, trendLabel: 'open', trendDir: 'up' },
    { icon: TrendingUp, label: 'Investigation Rate', value: totals.cases ? `${Math.round(((byStatus.active || 0) / Math.max(totals.cases, 1)) * 1000) / 10}%` : '—', trend: loading ? '…' : `${byStatus.pending ?? 0} pending`, trendLabel: 'awaiting', trendDir: 'up' },
    { icon: AlertTriangle, label: 'Active Alerts', value: formatNumber(totals.alerts ?? dashStats?.active_alerts), trend: loading ? '…' : `${byStatus.closed ?? 0} closed`, trendLabel: 'resolved', trendDir: 'down' },
    { icon: Users, label: 'Suspects', value: formatNumber(totals.suspects ?? dashStats?.suspects), trend: loading ? '…' : `${totals.users ?? 0} users`, trendLabel: 'in system', trendDir: 'up' },
    { icon: BarChart3, label: 'Resolution Rate', value: resolution != null ? `${resolution}%` : '—', trend: loading ? '…' : `${byStatus.closed ?? 0} closed`, trendLabel: 'of all', trendDir: 'up' },
  ]

  const lastUpdated = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6 space-y-5">
      {/* Hero Header */}
      <div className="bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 rounded-2xl p-4 px-6 text-white shadow-lg shadow-orange-500/20 shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white/20 backdrop-blur rounded-xl flex items-center justify-center">
              <LayoutDashboard size={20} />
            </div>
            <div>
              <h1 className="text-lg font-bold">{t('Crime Analytics')}</h1>
              <p className="text-white/80 text-xs">Last updated: {lastUpdated}</p>
            </div>
          </div>
        </div>
      </div>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>
      )}

      {/* Stats Cards — 5 columns */}
      <div className="grid grid-cols-5 gap-4">
        {cards.map((stat, i) => (
          <div key={i} className="bg-white rounded-2xl p-4 shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-9 h-9 rounded-xl bg-slate-50 flex items-center justify-center">
                <stat.icon size={16} className="text-slate-500" strokeWidth={1.8} />
              </div>
              <span className="text-[10px] text-slate-400 font-medium uppercase tracking-wide">{stat.label}</span>
            </div>
            <div className="text-xl font-bold text-slate-900">{stat.value}</div>
            <div className={`flex items-center gap-1 mt-1 text-[10px] font-medium ${stat.trendDir === 'up' ? 'text-emerald-600' : 'text-red-500'}`}>
              {stat.trendDir === 'up' ? <ArrowUpRight size={12} /> : <ArrowDownRight size={12} />}
              <span>{stat.trend}</span>
              <span className="text-slate-400 ml-0.5">{stat.trendLabel}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Charts Row 1 — Trend + Crime Type */}
      <div className="grid grid-cols-12 gap-5">
        <div className="col-span-8">
          <CaseTrendChart />
        </div>
        <div className="col-span-4">
          <CrimeTypeChart />
        </div>
      </div>

      {/* Charts Row 2 — Status + District + Calendar (3-col equal height) */}
      <div className="grid grid-cols-3 gap-5" style={{ gridAutoRows: '1fr' }}>
        <StatusBars />
        <DistrictDonut />
        <InvestmentCalendar />
      </div>

      {/* Recommendations — Full Width */}
      <RecommendationsPanel />
    </div>
  )
}
