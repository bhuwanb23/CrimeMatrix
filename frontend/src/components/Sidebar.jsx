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
} from 'lucide-react'
import LogoIcon from './icons/LogoIcon'

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard', id: 'dashboard' },
  { icon: FileText, label: 'FIR & Cases', id: 'cases', badge: true },
  { icon: BarChart3, label: 'Analytics', id: 'analytics' },
  { icon: Building2, label: 'Stations', id: 'stations' },
  { icon: Users, label: 'Suspects', id: 'suspects' },
  { icon: ClipboardList, label: 'Investigations', id: 'investigations' },
]

const bottomItems = [
  { icon: Settings, label: 'Settings', id: 'settings' },
  { icon: LogOut, label: 'Logout', id: 'logout' },
]

export default function Sidebar({ isOpen }) {
  const [activeItem, setActiveItem] = useState('dashboard')
  const [hoveredItem, setHoveredItem] = useState(null)

  return (
    <aside className={`sidebar ${isOpen ? 'expanded' : 'collapsed'}`}>
      <div className="sidebar-inner">
        {/* Brand Logo */}
        <div className="sidebar-logo">
          <div className="sidebar-logo-mark">
            <LogoIcon size={22} />
          </div>
          {isOpen && <span className="sidebar-logo-text">CrimeMatrix</span>}
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
                onClick={() => setActiveItem(item.id)}
                aria-label={item.label}
              >
                <item.icon size={18} strokeWidth={1.8} />
                {isOpen && <span className="sidebar-nav-label">{item.label}</span>}
                {item.badge && <span className="sidebar-nav-badge" />}
              </button>

              {/* Tooltip when collapsed */}
              {!isOpen && (
                <span className={`sidebar-tooltip ${hoveredItem === item.id ? 'visible' : ''}`}>
                  {item.label}
                </span>
              )}
            </div>
          ))}
        </nav>

        <div className="sidebar-divider" />

        {/* Spacer */}
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
                {isOpen && <span className="sidebar-nav-label">{item.label}</span>}
              </button>

              {!isOpen && (
                <span className={`sidebar-tooltip ${hoveredItem === item.id ? 'visible' : ''}`}>
                  {item.label}
                </span>
              )}
            </div>
          ))}

          {/* User Avatar */}
          <div className="sidebar-avatar">
            <div className="sidebar-avatar-circle">SK</div>
            {isOpen && (
              <div className="sidebar-avatar-info">
                <span className="sidebar-avatar-name">SI Karthik</span>
                <span className="sidebar-avatar-role">Investigation Officer</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </aside>
  )
}
