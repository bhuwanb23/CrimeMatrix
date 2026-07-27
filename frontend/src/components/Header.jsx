import { NavLink } from 'react-router-dom'
import { Bot, BarChart3, Network, Bell, PanelRightOpen, PanelRightClose, Sun, Moon, Monitor } from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'
import { useTheme } from '../context/ThemeContext'

const headerNav = [
  { icon: Bot, label: 'AI Copilot', to: '/copilot', id: 'copilot' },
  { icon: BarChart3, label: 'Analytics', to: '/analytics', id: 'analytics' },
  { icon: Network, label: 'Knowledge Graph', to: '/knowledge-graph', id: 'knowledge-graph' },
  { icon: Bell, label: 'Alerts', to: '/alerts', id: 'alerts' },
]

export default function Header({ rightPanelOpen, onToggleRightPanel }) {
  const { t } = useLanguage()
  const { theme, cycleTheme } = useTheme()

  const ThemeIcon = theme === 'dark' ? Moon : theme === 'light' ? Sun : Monitor
  const themeLabel =
    theme === 'dark' ? 'Dark theme' : theme === 'light' ? 'Light theme' : 'System theme'

  return (
    <header className="header">
      <div className="header-left">
        <div className="header-breadcrumb">
          <span className="header-breadcrumb-brand">{t('CrimeMatrix')}</span>
        </div>
      </div>

      <nav className="header-nav" data-tour="header-nav">
        {headerNav.map((item) => (
          <NavLink
            key={item.id}
            to={item.to}
            className={({ isActive }) =>
              `header-nav-item ${isActive ? 'active' : ''}`
            }
          >
            <item.icon size={16} strokeWidth={1.8} />
            <span>{t(item.label)}</span>
          </NavLink>
        ))}
      </nav>

      <div className="header-right">
        <button
          type="button"
          className="header-icon-btn"
          onClick={cycleTheme}
          aria-label={themeLabel}
          title={`${themeLabel} (click to cycle)`}
        >
          <ThemeIcon size={18} strokeWidth={1.8} />
        </button>

        <button
          type="button"
          data-tour="header-panel-toggle"
          className={`header-icon-btn ${rightPanelOpen ? 'active' : ''}`}
          onClick={onToggleRightPanel}
          aria-label={rightPanelOpen ? 'Close panel' : 'Open panel'}
        >
          {rightPanelOpen ? (
            <PanelRightClose size={18} strokeWidth={1.8} />
          ) : (
            <PanelRightOpen size={18} strokeWidth={1.8} />
          )}
        </button>

        <div className="header-user">
          <div className="header-user-avatar">{t('SK')}</div>
        </div>
      </div>
    </header>
  )
}
