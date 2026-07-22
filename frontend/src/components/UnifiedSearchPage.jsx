import { useLocation, useNavigate } from 'react-router-dom'
import { FileText, Users } from 'lucide-react'
import SearchPage from './SearchPage'
import SuspectsPage from './SuspectsPage'

const tabs = [
  { id: 'cases', label: 'Cases', icon: FileText, path: '/search/cases' },
  { id: 'suspects', label: 'Suspects', icon: Users, path: '/search/suspects' },
]

export default function UnifiedSearchPage() {
  const location = useLocation()
  const navigate = useNavigate()
  const activeTab = location.pathname.includes('/suspects') ? 'suspects' : 'cases'

  function handleTabChange(tab) {
    navigate(tab.path)
  }

  return (
    <div className="flex flex-col gap-4">
      {/* Tab Bar */}
      <div className="flex items-center gap-3">
        {/* <div className="flex items-center gap-2">
          <Search size={18} className="text-amber-500" />
          <h1 className="text-lg font-bold text-slate-900">Search</h1>
        </div> */}
        <div className="flex items-center gap-1 bg-white border border-slate-200 rounded-xl p-1">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => handleTabChange(tab)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  activeTab === tab.id
                    ? 'bg-amber-500 text-slate-900'
                    : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
                }`}
              >
                <Icon size={16} />
                {tab.label}
              </button>
            )
          })}
        </div>
      </div>

      {/* Tab Content */}
      {activeTab === 'cases' && <SearchPage />}
      {activeTab === 'suspects' && <SuspectsPage />}
    </div>
  )
}
