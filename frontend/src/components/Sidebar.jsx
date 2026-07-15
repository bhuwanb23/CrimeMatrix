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
  { icon: FileText, label: 'FIR & Cases', id: 'cases' },
  { icon: BarChart3, label: 'Analytics', id: 'analytics' },
  { icon: Building2, label: 'Stations', id: 'stations' },
  { icon: Users, label: 'Suspects', id: 'suspects' },
  { icon: ClipboardList, label: 'Investigations', id: 'investigations' },
]

const bottomItems = [
  { icon: Settings, label: 'Settings', id: 'settings' },
  { icon: LogOut, label: 'Logout', id: 'logout' },
]

function Tooltip({ children, label, visible }) {
  return (
    <div className="sidebar-tooltip-wrapper">
      {children}
      <span className={`sidebar-tooltip ${visible ? 'visible' : ''}`}>
        {label}
      </span>
    </div>
  )
}

export default function Sidebar({ isOpen, onToggle }) {
  const [activeItem, setActiveItem] = useState('dashboard')
  const [hoveredItem, setHoveredItem] = useState(null)

  return (
    <aside className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
      <div className="sidebar-inner">
        {/* Brand Logo */}
        <div className="sidebar-logo">
          <div className="sidebar-logo-circle">
            <LogoIcon size={28} />
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <Tooltip key={item.id} label={item.label} visible={!isOpen && hoveredItem === item.id}>
              <button
                className={`sidebar-nav-item ${activeItem === item.id ? 'active' : ''}`}
                onClick={() => setActiveItem(item.id)}
                onMouseEnter={() => setHoveredItem(item.id)}
                onMouseLeave={() => setHoveredItem(null)}
                aria-label={item.label}
              >
                <item.icon size={20} strokeWidth={1.8} />
              </button>
            </Tooltip>
          ))}
        </nav>

        {/* Spacer */}
        <div className="sidebar-spacer" />

        {/* Bottom Items */}
        <div className="sidebar-bottom">
          {bottomItems.map((item) => (
            <Tooltip key={item.id} label={item.label} visible={!isOpen && hoveredItem === item.id}>
              <button
                className={`sidebar-nav-item ${activeItem === item.id ? 'active' : ''}`}
                onClick={() => setActiveItem(item.id)}
                onMouseEnter={() => setHoveredItem(item.id)}
                onMouseLeave={() => setHoveredItem(null)}
                aria-label={item.label}
              >
                <item.icon size={20} strokeWidth={1.8} />
              </button>
            </Tooltip>
          ))}

          {/* User Avatar */}
          <div className="sidebar-avatar">
            <div className="sidebar-avatar-img">
              <span>Officer</span>
            </div>
          </div>
        </div>
      </div>
    </aside>
  )
}
