import { useState } from 'react'
import { NavLink } from 'react-router-dom'
import { createPortal } from 'react-dom'
import {
  LayoutDashboard,
  FileText,
  BarChart3,
  Building2,
  Users,
  ClipboardList,
  Settings,
  LogOut,
  Bot,
  Network,
  BookOpen,
  Brain,
  GitBranch,
  Clock,
  LineChart,
  Shield,
  Zap,
  Search,
} from 'lucide-react'
import LogoIcon from './icons/LogoIcon'

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard', to: '/', id: 'dashboard' },
  { icon: Brain, label: 'Intelligence', to: '/intelligence', id: 'intelligence' },
  { icon: GitBranch, label: 'Pattern-Timeline', to: '/pattern-timeline', id: 'pattern-timeline' },
  { icon: BarChart3, label: 'Analytics', to: '/analytics-dashboard', id: 'analytics-dashboard' },
  { icon: LineChart, label: 'Predictions', to: '/predictions', id: 'predictions' },

  { icon: Shield, label: 'Risk Score', to: '/suspect-risk', id: 'suspect-risk' },
  { icon: Zap, label: 'Priority', to: '/prioritizations', id: 'prioritizations' },
  { icon: Search, label: 'Search', to: '/search', id: 'search' },
  { icon: Building2, label: 'Stations', to: '/stations', id: 'stations' },

  { icon: ClipboardList, label: 'Investigations', to: '/investigations', id: 'investigations' },
  { icon: BookOpen, label: 'Reports', to: '/reports', id: 'reports' },
]

const bottomItems = [
  { icon: Settings, label: 'Settings', id: 'settings', to: '/settings' },
]

export default function Sidebar() {
  const [hoveredItem, setHoveredItem] = useState(null)
  const [tooltipPos, setTooltipPos] = useState({ top: 0, left: 0 })

  const handleMouseEnter = (e, label) => {
    const rect = e.currentTarget.getBoundingClientRect()
    setTooltipPos({
      top: rect.top + rect.height / 2,
      left: rect.right + 10,
    })
    setHoveredItem(label)
  }

  const handleMouseLeave = () => {
    setHoveredItem(null)
  }

  return (
    <>
      <aside className="sidebar">
        <div className="sidebar-inner">
          <nav className="sidebar-nav">
            {navItems.map((item) => (
              <div
                key={item.label}
                className="sidebar-nav-item-wrapper"
                onMouseEnter={(e) => handleMouseEnter(e, item.label)}
                onMouseLeave={handleMouseLeave}
              >
                <NavLink
                  to={item.to}
                  end={item.to !== '/search/cases'}
                  className={({ isActive }) =>
                    `sidebar-nav-item ${isActive ? 'active' : ''}`
                  }
                >
                  <item.icon size={18} strokeWidth={1.8} />
                  {item.badge && <span className="sidebar-nav-badge" />}
                </NavLink>
              </div>
            ))}
          </nav>

          <div className="sidebar-divider" />
          <div className="sidebar-spacer" />

          <div className="sidebar-bottom">
            {bottomItems.map((item) => (
              <div
                key={item.id}
                className="sidebar-nav-item-wrapper"
                onMouseEnter={(e) => handleMouseEnter(e, item.label)}
                onMouseLeave={handleMouseLeave}
              >
                {item.to ? (
                  <NavLink
                    to={item.to}
                    className={({ isActive }) =>
                      `sidebar-nav-item ${isActive ? 'active' : ''}`
                    }
                  >
                    <item.icon size={18} strokeWidth={1.8} />
                  </NavLink>
                ) : (
                  <button className="sidebar-nav-item" aria-label={item.label}>
                    <item.icon size={18} strokeWidth={1.8} />
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      </aside>

      {/* Portal-rendered tooltip — not clipped by sidebar overflow */}
      {hoveredItem && createPortal(
        <span
          className="sidebar-tooltip visible"
          style={{ top: tooltipPos.top, left: tooltipPos.left }}
        >
          {hoveredItem}
        </span>,
        document.body
      )}
    </>
  )
}
