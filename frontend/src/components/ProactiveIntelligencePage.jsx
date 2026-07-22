import { useState, useEffect } from 'react'
import { Radar, RefreshCw, Search, Zap, AlertTriangle, Brain, CheckCircle } from 'lucide-react'
import { getProactiveStats, scanData, processEvents, getActivity } from '../services/proactive'
import { batchProcess } from '../services/proactive'
import IntelligenceSummaryCards from './proactive/IntelligenceSummaryCards'
import ActivityFeed from './proactive/ActivityFeed'
import NotificationCenter from './proactive/NotificationCenter'

export default function ProactiveIntelligencePage() {
  const [stats, setStats] = useState(null)
  const [activity, setActivity] = useState([])
  const [loading, setLoading] = useState(true)
  const [scanning, setScanning] = useState(false)
  const [processing, setProcessing] = useState(false)

  useEffect(() => { loadAll(); autoProcess() }, [])

  async function autoProcess() {
    try { await batchProcess() } catch (e) { /* silent */ }
  }

  async function loadAll() {
    setLoading(true)
    try {
      const [statsRes, activityRes] = await Promise.all([
        getProactiveStats(),
        getActivity(20),
      ])
      setStats(statsRes?.data || statsRes)
      setActivity(activityRes?.data?.items || [])
    } catch (e) { console.error(e) } finally { setLoading(false) }
  }

  async function handleScan() {
    setScanning(true)
    try { await scanData(); await loadAll() } catch (e) { console.error(e) } finally { setScanning(false) }
  }

  async function handleProcess() {
    setProcessing(true)
    try { await processEvents(); await loadAll() } catch (e) { console.error(e) } finally { setProcessing(false) }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Hero Header */}
        <div className="bg-gradient-to-r from-cyan-500 via-blue-500 to-indigo-500 rounded-2xl p-6 text-white shadow-lg shadow-blue-500/20">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-white/20 backdrop-blur rounded-2xl flex items-center justify-center">
                <Radar size={28} />
              </div>
              <div>
                <h1 className="text-2xl font-bold">Proactive Intelligence</h1>
                <p className="text-white/80 text-sm mt-0.5">AI continuously monitors and surfaces hidden intelligence</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button onClick={handleScan} disabled={scanning}
                className="flex items-center gap-2 px-5 py-2.5 bg-white/20 backdrop-blur hover:bg-white/30 rounded-xl text-sm font-semibold transition-all disabled:opacity-50">
                {scanning ? <RefreshCw size={14} className="animate-spin" /> : <Search size={14} />}
                {scanning ? 'Scanning...' : 'Scan Now'}
              </button>
              <button onClick={handleProcess} disabled={processing}
                className="flex items-center gap-2 px-5 py-2.5 bg-white/20 backdrop-blur hover:bg-white/30 rounded-xl text-sm font-semibold transition-all disabled:opacity-50">
                {processing ? <RefreshCw size={14} className="animate-spin" /> : <Zap size={14} />}
                {processing ? 'Processing...' : 'Process Queue'}
              </button>
              <button onClick={loadAll} disabled={loading}
                className="p-2.5 bg-white/20 backdrop-blur hover:bg-white/30 rounded-xl transition-all">
                <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
              </button>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <IntelligenceSummaryCards stats={stats} />

        {/* Main Content */}
        <div className="grid grid-cols-12 gap-5">
          {/* Activity Feed (7 cols) */}
          <div className="col-span-7">
            <ActivityFeed events={activity} />
          </div>

          {/* Notifications + AI Summary (5 cols) */}
          <div className="col-span-5 space-y-5">
            <NotificationCenter events={activity} />

            {/* AI Intelligence Summary */}
            <div className="bg-white border border-slate-200 rounded-xl p-4">
              <div className="flex items-center gap-2 mb-3">
                <Brain size={14} className="text-amber-500" />
                <h3 className="text-sm font-semibold text-slate-900">AI Intelligence Summary</h3>
              </div>
              <div className="space-y-2">
                <div className="p-2 bg-blue-50 rounded-lg">
                  <p className="text-xs text-blue-700">
                    The AI Intelligence Engine continuously monitors incoming FIRs, evidence updates, and case changes to detect hidden relationships and recommend immediate actions.
                  </p>
                </div>
                <div className="flex items-center gap-2 text-[10px] text-slate-500">
                  <AlertTriangle size={10} className="text-amber-500" />
                  <span>{stats?.pending || 0} events waiting for processing</span>
                </div>
                <div className="flex items-center gap-2 text-[10px] text-slate-500">
                  <CheckCircle size={10} className="text-green-500" />
                  <span>{stats?.processed || 0} events processed automatically</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
