import { ArrowUpRight, ArrowDownRight, ClipboardList, TrendingUp, AlertTriangle, Users, BarChart3 } from 'lucide-react'
import CaseTrendChart from './charts/CaseTrendChart'
import CrimeTypeChart from './charts/CrimeTypeChart'
import DistrictDonut from './charts/DistrictDonut'
import StatusBars from './charts/StatusBars'
import InvestmentCalendar from './charts/InvestmentCalendar'

const stats = [
  {
    icon: ClipboardList,
    label: 'Total Cases',
    value: '1,284',
    trend: '+3.5%',
    trendLabel: 'vs last Year',
    trendDir: 'up',
  },
  {
    icon: TrendingUp,
    label: 'Investigation Rate',
    value: '8.3%',
    trend: '+1.2%',
    trendLabel: 'vs last Month',
    trendDir: 'up',
  },
  {
    icon: AlertTriangle,
    label: 'Active FIRs',
    value: '47',
    trend: '-1.7%',
    trendLabel: 'vs last Week',
    trendDir: 'down',
  },
  {
    icon: Users,
    label: 'Officers on Duty',
    value: '156',
    trend: '+2.5%',
    trendLabel: 'vs last Month',
    trendDir: 'up',
  },
  {
    icon: BarChart3,
    label: 'Resolution Rate',
    value: '73%',
    trend: '+4.1%',
    trendLabel: 'vs last Quarter',
    trendDir: 'up',
  },
]

export default function DashboardContent() {
  const now = new Date()
  const lastUpdated = now.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })

  return (
    <div className="analytics-dashboard">
      {/* Page Header */}
      <div className="dashboard-header">
        <h1 className="dashboard-title">Crime Analytics</h1>
        <span className="dashboard-updated">
          Last updated: {lastUpdated}
        </span>
      </div>

      {/* Row 1: 5 Stat Cards */}
      <div className="stats-row">
        {stats.map((stat, i) => (
          <div key={i} className="stat-card-v2">
            <div className="stat-v2-icon">
              <stat.icon size={18} strokeWidth={1.8} />
            </div>
            <div className="stat-v2-label">{stat.label}</div>
            <div className="stat-v2-value">{stat.value}</div>
            <div className={`stat-v2-trend ${stat.trendDir}`}>
              {stat.trendDir === 'up' ? (
                <ArrowUpRight size={12} strokeWidth={2} />
              ) : (
                <ArrowDownRight size={12} strokeWidth={2} />
              )}
              {stat.trend} {stat.trendLabel}
            </div>
          </div>
        ))}
      </div>

      {/* Row 2: Chart + Category */}
      <div className="dashboard-row-2">
        <CaseTrendChart />
        <CrimeTypeChart />
      </div>

      {/* Row 3: 3 Cards */}
      <div className="dashboard-row-3">
        <DistrictDonut />
        <InvestmentCalendar />
        <StatusBars />
      </div>
    </div>
  )
}
