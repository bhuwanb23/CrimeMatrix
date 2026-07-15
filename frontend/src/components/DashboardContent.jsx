import { FileText, AlertTriangle, Clock, TrendingUp, ArrowUpRight, Zap, Eye, Shield } from 'lucide-react'

const stats = [
  {
    icon: FileText,
    color: '#3b82f6',
    bg: 'rgba(59, 130, 246, 0.1)',
    value: '1,284',
    label: 'Total Cases',
    trend: '+12%',
    trendDir: 'up',
  },
  {
    icon: AlertTriangle,
    color: '#f59e0b',
    bg: 'rgba(245, 158, 11, 0.1)',
    value: '47',
    label: 'Active Investigations',
    trend: '+8%',
    trendDir: 'up',
  },
  {
    icon: Zap,
    color: '#ef4444',
    bg: 'rgba(239, 68, 68, 0.1)',
    value: '23',
    label: 'Whisper Alerts',
    trend: '+15%',
    trendDir: 'up',
  },
  {
    icon: TrendingUp,
    color: '#10b981',
    bg: 'rgba(16, 185, 129, 0.1)',
    value: '73%',
    label: 'Resolution Rate',
    trend: '+3%',
    trendDir: 'up',
  },
]

const recentCases = [
  { id: 'FIR #4521', title: 'Theft at Malleshwaram, Bengaluru', status: 'active', date: 'Today' },
  { id: 'FIR #4519', title: 'Vehicle accident — Mysuru Road', status: 'pending', date: 'Today' },
  { id: 'FIR #4515', title: 'Cyber fraud — Electronic City', status: 'active', date: 'Yesterday' },
  { id: 'FIR #4512', title: 'Missing person — Koramangala', status: 'active', date: 'Yesterday' },
  { id: 'FIR #4508', title: 'Robbery attempt — Whitefield', status: 'closed', date: 'Jul 13' },
]

const aiInsights = [
  {
    icon: Eye,
    color: '#8b5cf6',
    bg: 'rgba(139, 92, 246, 0.1)',
    title: 'Serial Pattern Detected',
    text: 'MO fingerprint matches 3 unsolved cases in Bengaluru North across the last 6 months.',
    time: '2 hrs ago',
  },
  {
    icon: Shield,
    color: '#f59e0b',
    bg: 'rgba(245, 158, 11, 0.1)',
    title: 'High-Risk Suspect Alert',
    text: 'Ravi Kumar linked to new FIR — recommended priority investigation.',
    time: '4 hrs ago',
  },
]

export default function DashboardContent() {
  return (
    <div>
      <div className="dashboard-welcome">
        <h1>Good evening, SI Karthik</h1>
        <p>Here's what's happening across your jurisdiction today.</p>
      </div>

      {/* Stat Cards */}
      <div className="stats-grid">
        {stats.map((stat, i) => (
          <div key={i} className="stat-card">
            <div className="stat-card-icon" style={{ background: stat.bg, color: stat.color }}>
              <stat.icon size={22} strokeWidth={1.8} />
            </div>
            <div className="stat-card-info">
              <div className="stat-card-value">{stat.value}</div>
              <div className="stat-card-label">{stat.label}</div>
              <div className={`stat-card-trend ${stat.trendDir}`}>
                <ArrowUpRight size={12} />
                {stat.trend} this month
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Content Grid */}
      <div className="content-grid">
        {/* Recent Cases */}
        <div className="content-card">
          <div className="content-card-header">
            <h3 className="content-card-title">Recent Cases</h3>
            <span className="content-card-action">View all →</span>
          </div>
          <div className="content-card-body">
            <div className="cases-table">
              {recentCases.map((c, i) => (
                <div key={i} className="cases-table-row">
                  <span className="case-id">{c.id}</span>
                  <span className="case-title">{c.title}</span>
                  <span className={`case-status ${c.status}`}>{c.status}</span>
                  <span className="case-date">{c.date}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* AI Insights */}
        <div className="content-card">
          <div className="content-card-header">
            <h3 className="content-card-title">AI Insights</h3>
            <span className="content-card-action">View all →</span>
          </div>
          <div className="content-card-body">
            {aiInsights.map((insight, i) => (
              <div key={i} className="insight-card">
                <div className="insight-icon" style={{ background: insight.bg, color: insight.color }}>
                  <insight.icon size={18} strokeWidth={1.8} />
                </div>
                <div className="insight-content">
                  <div className="insight-title">{insight.title}</div>
                  <div className="insight-text">{insight.text}</div>
                  <div className="insight-time">{insight.time}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
