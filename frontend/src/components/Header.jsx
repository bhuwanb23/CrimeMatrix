import { Search, Bell, PanelLeftClose, PanelLeftOpen, X } from 'lucide-react'

export default function Header({
  sidebarOpen,
  onToggleSidebar,
  rightPanelOpen,
  onToggleRightPanel,
}) {
  return (
    <header className="header">
      <div className="header-left">
        <button
          className="header-toggle-btn"
          onClick={onToggleSidebar}
          aria-label={sidebarOpen ? 'Close sidebar' : 'Open sidebar'}
        >
          {sidebarOpen ? (
            <PanelLeftClose size={18} strokeWidth={1.8} />
          ) : (
            <PanelLeftOpen size={18} strokeWidth={1.8} />
          )}
        </button>
        <div className="header-title">
          <span className="header-title-main">CrimeMatrix</span>
          <span className="header-title-sep">/</span>
          <span className="header-title-sub">Dashboard</span>
        </div>
      </div>

      <div className="header-center">
        <div className="header-search">
          <Search size={16} strokeWidth={1.8} className="header-search-icon" />
          <input
            type="text"
            placeholder="Search cases, suspects..."
            className="header-search-input"
          />
          <kbd className="header-search-kbd">⌘K</kbd>
        </div>
      </div>

      <div className="header-right">
        <button
          className={`header-icon-btn ${rightPanelOpen ? 'active' : ''}`}
          onClick={onToggleRightPanel}
          aria-label="Toggle notifications panel"
        >
          <Bell size={18} strokeWidth={1.8} />
          <span className="header-badge">3</span>
        </button>
        <div className="header-user">
          <div className="header-user-avatar">
            <span>SK</span>
          </div>
          <div className="header-user-info">
            <span className="header-user-name">SI Karthik</span>
            <span className="header-user-role">Investigation Officer</span>
          </div>
        </div>
      </div>
    </header>
  )
}
