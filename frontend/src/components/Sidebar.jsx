import { useState } from 'react'
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
  { icon: LayoutDashboard, label: 'Dashboard', id: 'dashboard', page: 'dashboard' },
  { icon: Bot, label: 'AI Copilot', id: 'copilot', page: 'copilot' },
  { icon: FileText, label: 'FIR & Cases', id: 'cases', badge: true, page: 'dashboard' },
  { icon: BarChart3, label: 'Analytics', id: 'analytics', page: 'dashboard' },
  { icon: Building2, label: 'Stations', id: 'stations', page: 'dashboard' },
  { icon: Users, label: 'Suspects', id: 'suspects', page: 'dashboard' },
  { icon: ClipboardList, label: 'Investigations', id: 'investigations', page: 'dashboard' },
]

const bottomItems = [
  { icon: Settings, label: 'Settings', id: 'settings' },
  { icon: LogOut, label: 'Logout', id: 'logout' },
]

export default function Sidebar({ onNavigate, currentPage }) {
  const [activeItem, setActiveItem] = useState('dashboard')
  const [hoveredItem, setHoveredItem] = useState(null)

  const handleNavClick = (item) => {
    setActiveItem(item.id)
    if (item.page && onNavigate) {
      onNavigate(item.page)
    }
  }

  return (
    <aside className="sidebar collapsed">
      <div className="sidebar-inner">
        {/* Brand Logo */}
        <div className="sidebar-logo">
          <div className="sidebar-logo-mark">
            <LogoIcon size={22} />
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <div
              key={item.id}
              className="sidebar-nav-item-wrapper"
              onMouseEnter={() => setHoveredItem(item.id)}
              onMouseLeave={() => setHoveredItem(null)}
            >
              <button
                className={`sidebar-nav-item ${activeItem === item.id ? 'active' : ''}`}
                onClick={() => handleNavClick(item)}
                aria-label={item.label}
              >
                <item.icon size={18} strokeWidth={1.8} />
                {item.badge && <span className="sidebar-nav-badge" />}
              </button>

              <span className={`sidebar-tooltip ${hoveredItem === item.id ? 'visible' : ''}`}>
                {item.label}
              </span>
            </div>
          ))}
        </nav>

        <div className="sidebar-divider" />

        <div className="sidebar-spacer" />

        {/* Bottom Items */}
        <div className="sidebar-bottom">
          {bottomItems.map((item) => (
            <div
              key={item.id}
              className="sidebar-nav-item-wrapper"
              onMouseEnter={() => setHoveredItem(item.id)}
              onMouseLeave={() => setHoveredItem(null)}
            >
              <button
                className={`sidebar-nav-item ${activeItem === item.id ? 'active' : ''}`}
                onClick={() => setActiveItem(item.id)}
                aria-label={item.label}
              >
                <item.icon size={18} strokeWidth={1.8} />
              </button>

              <span className={`sidebar-tooltip ${hoveredItem === item.id ? 'visible' : ''}`}>
                {item.label}
              </span>
            </div>
          ))}

          <div className="sidebar-avatar">
            <div className="sidebar-avatar-circle">SK</div>
          </div>
        </div>
      </div>
    </aside>
  )
}
