import { Search, Bell, PanelRightOpen, PanelRightClose, ChevronDown } from 'lucide-react'

export default function Header({ rightPanelOpen, onToggleRightPanel }) {
  return (
    <header className="header">
      <div className="header-left">
        <div className="header-breadcrumb">
          <span className="header-breadcrumb-brand">CrimeMatrix</span>
          <span className="header-breadcrumb-sep">/</span>
          <span className="header-breadcrumb-page">Dashboard</span>
        </div>
      </div>

      <div className="header-center">
        <div className="header-search">
          <Search size={16} strokeWidth={1.8} className="header-search-icon" />
          <input
            type="text"
            placeholder="Search cases, suspects, stations..."
            className="header-search-input"
          />
          <kbd className="header-search-kbd">⌘K</kbd>
        </div>
      </div>

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

        <button className="header-icon-btn" aria-label="Notifications">
          <Bell size={18} strokeWidth={1.8} />
          <span className="header-badge">3</span>
        </button>

        <div className="header-user">
          <div className="header-user-avatar">SK</div>
          <div className="header-user-info">
            <span className="header-user-name">SI Karthik</span>
            <span className="header-user-role">Investigation Officer</span>
          </div>
          <ChevronDown size={14} className="header-user-chevron" />
        </div>
      </div>
    </header>
  )
}
