import { NavLink } from 'react-router-dom'
import { Bot, BarChart3, Network, Bell, PanelRightOpen, PanelRightClose } from 'lucide-react'

const headerNav = [
  { icon: Bot, label: 'AI Copilot', to: '/copilot', id: 'copilot' },
  { icon: BarChart3, label: 'Analytics', to: '/analytics', id: 'analytics' },
  { icon: Network, label: 'Knowledge Graph', to: '/knowledge-graph', id: 'knowledge-graph' },
  { icon: Bell, label: 'Alerts', to: '/alerts', id: 'alerts' },
]

import { useLanguage } from '../context/LanguageContext'
import { t } from '../utils/translate'

export default function Header({ rightPanelOpen, onToggleRightPanel }) {
  const { lang } = useLanguage()
  return (
    <header className="header">
      <div className="header-left">
        <div className="header-breadcrumb">
          <span className="header-breadcrumb-brand">CrimeMatrix</span>
          <span className="header-breadcrumb-sep">/</span>
          <span className="header-breadcrumb-page">{t('dashboard', lang)}</span>
        </div>
      </div>

      <nav className="header-nav">
        {headerNav.map((item) => (
          <NavLink
            key={item.id}
            to={item.to}
            className={({ isActive }) =>
              `header-nav-item ${isActive ? 'active' : ''}`
            }
          >
            <item.icon size={16} strokeWidth={1.8} />
            <span>{t(item.id.replace(/-/g, '_'), lang) || item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="header-right">
        <button
          className={`header-icon-btn ${rightPanelOpen ? 'active' : ''}`}
          onClick={onToggleRightPanel}
          aria-label="Toggle panel"
        >
          {rightPanelOpen ? (
            <PanelRightClose size={18} strokeWidth={1.8} />
          ) : (
            <PanelRightOpen size={18} strokeWidth={1.8} />
          )}
        </button>

        <div className="header-user">
          <div className="header-user-avatar">SK</div>
        </div>
      </div>
    </header>
  )
}
