import { useLanguage } from '../context/LanguageContext'
import { useEffect, useState } from 'react'
import { ArrowUpRight, ArrowDownRight, ClipboardList, TrendingUp, AlertTriangle, Users, BarChart3 } from 'lucide-react'
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
    {
      icon: ClipboardList,
      label: 'Total Cases',
      value: formatNumber(totals.cases ?? dashStats?.total_cases),
      trend: loading ? '…' : `${byStatus.active ?? 0} active`,
      trendLabel: 'open investigations',
      trendDir: 'up',
    },
    {
      icon: TrendingUp,
      label: 'Investigation Rate',
      value: totals.cases
        ? `${Math.round(((byStatus.active || 0) / Math.max(totals.cases, 1)) * 1000) / 10}%`
        : '—',
      trend: loading ? '…' : `${byStatus.pending ?? 0} pending`,
      trendLabel: 'awaiting action',
      trendDir: 'up',
    },
    {
      icon: AlertTriangle,
      label: 'Active Alerts',
      value: formatNumber(totals.alerts ?? dashStats?.active_alerts),
      trend: loading ? '…' : `${byStatus.closed ?? 0} closed cases`,
      trendLabel: 'resolved',
      trendDir: 'down',
    },
    {
      icon: Users,
      label: 'Suspects',
      value: formatNumber(totals.suspects ?? dashStats?.suspects),
      trend: loading ? '…' : `${totals.users ?? 0} users`,
      trendLabel: 'in system',
      trendDir: 'up',
    },
    {
      icon: BarChart3,
      label: 'Resolution Rate',
      value: resolution != null ? `${resolution}%` : '—',
      trend: loading ? '…' : `${byStatus.closed ?? 0} closed`,
      trendLabel: 'of all cases',
      trendDir: 'up',
    },
  ]

  const now = new Date()
  const lastUpdated = now.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })

  return (
    <div className="analytics-dashboard">
      <div className="dashboard-header">
        <h1 className="dashboard-title">{t('Crime Analytics')}</h1>
        <span className="dashboard-updated">
          Last updated: {lastUpdated}
        </span>
      </div>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 mb-4">{error}</div>
      )}

      <div className="stats-row">
        {cards.map((stat, i) => (
          <div key={i} className="stat-card-v2">
            <div className="stat-v2-icon">
              <stat.icon size={18} strokeWidth={1.8} />
            </div>
            <div className="stat-v2-label">{stat.label}</div>
            <div className="stat-v2-value">{stat.value}</div>
            <div className={`stat-v2-trend ${stat.trendDir}`}>
              {stat.trendDir === 'up' ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}
              <span>{stat.trend}</span>
              <span className="stat-v2-trend-label">{stat.trendLabel}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="dashboard-charts-row">
        <CaseTrendChart />
        <CrimeTypeChart />
        <DistrictDonut />
      </div>

      <div className="dashboard-bottom-row">
        <StatusBars />
        <InvestmentCalendar />
        <RecommendationsPanel />
      </div>
    </div>
  )
}
