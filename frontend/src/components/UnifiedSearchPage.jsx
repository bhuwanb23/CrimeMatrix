import { useLocation, useNavigate } from 'react-router-dom'
import { FileText, Users, Search } from 'lucide-react'
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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-5">
        {/* Hero Header */}
        <div className="bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 rounded-2xl p-6 text-white shadow-lg shadow-orange-500/20">
          <div className="flex items-center gap-4">
            <div className="w-14 h-14 bg-white/20 backdrop-blur rounded-2xl flex items-center justify-center">
              <Search size={28} />
            </div>
            <div>
              <h1 className="text-2xl font-bold">Crime Search</h1>
              <p className="text-white/80 text-sm mt-0.5">Search cases, suspects, and investigate connections</p>
            </div>
          </div>
        </div>

        {/* Tab Bar */}
        <div className="flex items-center gap-1 bg-white border border-slate-200 rounded-xl p-1 w-fit">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => handleTabChange(tab)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  activeTab === tab.id
                    ? 'bg-orange-500 text-white shadow-sm'
                    : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
                }`}
              >
                <Icon size={16} />
                {tab.label}
              </button>
            )
          })}
        </div>

        {/* Tab Content */}
        {activeTab === 'cases' && <SearchPage />}
        {activeTab === 'suspects' && <SuspectsPage />}
      </div>
    </div>
  )
}
