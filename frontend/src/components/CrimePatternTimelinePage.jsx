import { useState } from 'react'
import { GitBranch, Clock, Layers } from 'lucide-react'
import PatternDiscoveryPage from './PatternDiscoveryPage'
import CriminalTimelinePage from './CriminalTimelinePage'

const tabs = [
  { id: 'patterns', label: 'Patterns', icon: GitBranch },
  { id: 'timeline', label: 'Timeline', icon: Clock },
]

import { useLanguage } from '../context/LanguageContext'

export default function CrimePatternTimelinePage() {
  const { t } = useLanguage()
  const [activeTab, setActiveTab] = useState('patterns')

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-5">
        {/* Hero Header */}
        <div className="bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 rounded-2xl p-6 text-white shadow-lg shadow-orange-500/20">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-white/20 backdrop-blur rounded-2xl flex items-center justify-center">
                <Layers size={28} />
              </div>
              <div>
                <h1 className="text-2xl font-bold">{t('Patterns & Timeline')}</h1>
                <p className="text-white/80 text-sm mt-0.5">{t('Crime pattern discovery and criminal timeline tracking')}</p>
              </div>
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
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  activeTab === tab.id
                    ? 'bg-orange-500 text-white shadow-sm'
                    : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
                }`}
              >
                <Icon size={16} />
                {t(tab.label)}
              </button>
            )
          })}
        </div>

        {/* Tab Content */}
        {activeTab === 'patterns' && <PatternDiscoveryPage />}
        {activeTab === 'timeline' && <CriminalTimelinePage />}
      </div>
    </div>
  )
}
