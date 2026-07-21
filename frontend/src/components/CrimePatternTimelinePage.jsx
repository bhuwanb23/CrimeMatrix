import { useState } from 'react'
import { GitBranch, Clock } from 'lucide-react'
import PatternDiscoveryPage from './PatternDiscoveryPage'
import CriminalTimelinePage from './CriminalTimelinePage'

const tabs = [
  { id: 'patterns', label: 'Patterns', icon: GitBranch },
  { id: 'timeline', label: 'Timeline', icon: Clock },
]

export default function CrimePatternTimelinePage() {
  const [activeTab, setActiveTab] = useState('patterns')

  return (
    <div className="flex flex-col gap-4">
      {/* Tab Bar */}
      <div className="flex items-center gap-1 bg-white border border-slate-200 rounded-xl p-1 w-fit">
        {tabs.map((tab) => {
          const Icon = tab.icon
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
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

      {/* Tab Content */}
      {activeTab === 'patterns' && <PatternDiscoveryPage />}
      {activeTab === 'timeline' && <CriminalTimelinePage />}
    </div>
  )
}
