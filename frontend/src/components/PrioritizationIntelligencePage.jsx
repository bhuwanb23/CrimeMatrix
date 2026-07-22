import { useState } from 'react'
import { Zap, Radar } from 'lucide-react'
import PrioritizationDashboard from './PrioritizationDashboard'
import ProactiveIntelligencePage from './ProactiveIntelligencePage'

const tabs = [
  { id: 'priority', label: 'Priority', icon: Zap },
  { id: 'proactive', label: 'Proactive Intelligence', icon: Radar },
]

export default function PrioritizationIntelligencePage() {
  const [activeTab, setActiveTab] = useState('priority')

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
      {activeTab === 'priority' && <PrioritizationDashboard />}
      {activeTab === 'proactive' && <ProactiveIntelligencePage />}
    </div>
  )
}
