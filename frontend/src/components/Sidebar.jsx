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
} from 'lucide-react'
import LogoIcon from './icons/LogoIcon'

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard', to: '/' },
  { icon: Bot, label: 'AI Copilot', to: '/copilot' },
  { icon: FileText, label: 'FIR & Cases', to: '/', badge: true },
  { icon: BarChart3, label: 'Analytics', to: '/' },
  { icon: Building2, label: 'Stations', to: '/' },
  { icon: Users, label: 'Suspects', to: '/' },
  { icon: ClipboardList, label: 'Investigations', to: '/' },
]

const bottomItems = [
  { icon: Settings, label: 'Settings', id: 'settings' },
  { icon: LogOut, label: 'Logout', id: 'logout' },
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
          <div className="sidebar-logo">
            <div className="sidebar-logo-mark">
              <LogoIcon size={22} />
            </div>
          </div>

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
                  end={item.to === '/'}
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
                <button className="sidebar-nav-item" aria-label={item.label}>
                  <item.icon size={18} strokeWidth={1.8} />
                </button>
              </div>
            ))}

            <div className="sidebar-avatar">
              <div className="sidebar-avatar-circle">SK</div>
            </div>
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
