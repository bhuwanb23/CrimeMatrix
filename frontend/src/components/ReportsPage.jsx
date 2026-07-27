import { useState, useEffect, useCallback, useMemo } from 'react'
import { FileText, RefreshCw, Plus } from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'
import { listAllCrimes } from '../services/search'
import {
  listReportTemplates,
  listReportQueue,
  queueReport,
  generateSummaryReport,
} from '../services/reports'
import { dedupeByKey } from '../utils/dedupeByKey'

const TYPE_COLORS = {
  summary: '#3b82f6',
  timeline: '#8b5cf6',
  evidence: '#f59e0b',
  investigation: '#10b981',
}

const STATUS_COLORS = {
  queued: '#64748b',
  pending: '#f59e0b',
  processing: '#3b82f6',
  completed: '#10b981',
  failed: '#ef4444',
  cancelled: '#94a3b8',
}

export default function ReportsPage() {
  const { t } = useLanguage()
  const [templates, setTemplates] = useState([])
  const [jobs, setJobs] = useState([])
  const [crimes, setCrimes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [crimeId, setCrimeId] = useState('')
  const [reportType, setReportType] = useState('summary')
  const [busy, setBusy] = useState(false)
  const [filter, setFilter] = useState('')

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const [tplRes, queueRes, crimesRes] = await Promise.all([
        listReportTemplates(),
        listReportQueue(),
        listAllCrimes(1, 50),
      ])
      const tplData = tplRes?.data
      setTemplates(Array.isArray(tplData) ? tplData : tplData?.items || [])
      const queueData = queueRes?.data
      setJobs(Array.isArray(queueData) ? queueData : queueData?.items || queueData?.jobs || [])
      setCrimes(dedupeByKey(crimesRes?.data?.items || [], 'id'))
    } catch (e) {
      setError(e?.message || 'Failed to load reports')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  const filteredJobs = useMemo(() => {
    if (!filter.trim()) return jobs
    const q = filter.toLowerCase()
    return jobs.filter((j) =>
      String(j.id || '').toLowerCase().includes(q) ||
      String(j.report_type || j.type || '').toLowerCase().includes(q) ||
      String(j.status || '').toLowerCase().includes(q) ||
      String(j.params?.crime_id || j.crime_id || '').includes(q)
    )
  }, [jobs, filter])

  async function handleQueue() {
    const id = Number(crimeId)
    if (!id) return
    setBusy(true)
    try {
      await queueReport(reportType, id)
      await load()
    } catch (e) {
      setError(e?.message || 'Failed to queue report')
    } finally {
      setBusy(false)
    }
  }

  async function handleGenerate() {
    const id = Number(crimeId)
    if (!id) return
    setBusy(true)
    try {
      await generateSummaryReport(id)
      await load()
    } catch (e) {
      setError(e?.message || 'Failed to generate report')
    } finally {
      setBusy(false)
    }
  }

  const stats = {
    templates: templates.length,
    queued: jobs.filter((j) => ['queued', 'pending', 'processing'].includes(j.status)).length,
    completed: jobs.filter((j) => j.status === 'completed').length,
    failed: jobs.filter((j) => j.status === 'failed').length,
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[var(--bg-gradient-from)] to-[var(--bg-gradient-to)] p-6">
      <div className="max-w-7xl mx-auto space-y-5">
        <div className="bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 rounded-2xl p-4 px-6 text-white shadow-lg shadow-orange-500/20 shrink-0">
          <div className="flex items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-white/20 backdrop-blur rounded-xl flex items-center justify-center">
                <FileText size={20} />
              </div>
              <div>
                <h1 className="text-lg font-bold">{t('Reports & Documentation')}</h1>
                <p className="text-white/80 text-xs">{t('Investigation reports, court documents, and exports')}</p>
              </div>
            </div>
            <button
              type="button"
              onClick={load}
              disabled={loading}
              className="inline-flex items-center gap-1.5 px-3 py-2 bg-white/20 hover:bg-white/30 rounded-lg text-xs font-medium"
            >
              <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
              {t('Refresh')}
            </button>
          </div>
        </div>

        {error && (
          <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>
        )}

        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            { label: 'Templates', value: stats.templates },
            { label: 'In queue', value: stats.queued },
            { label: 'Completed', value: stats.completed },
            { label: 'Failed', value: stats.failed },
          ].map((s) => (
            <div key={s.label} className="rounded-xl border border-[var(--border)] bg-[var(--bg-card)] p-4">
              <div className="text-xs text-[var(--text-muted)] font-medium">{s.label}</div>
              <div className="text-2xl font-bold text-[var(--text-primary)] mt-1">{s.value}</div>
            </div>
          ))}
        </div>

        <div className="rounded-xl border border-[var(--border)] bg-[var(--bg-card)] p-4 space-y-3">
          <h2 className="text-sm font-semibold text-[var(--text-primary)]">Generate / queue report</h2>
          <div className="flex flex-wrap gap-3 items-end">
            <label className="flex flex-col gap-1 text-xs text-[var(--text-muted)]">
              Crime
              <select
                className="rounded-lg border border-[var(--border)] px-3 py-2 text-sm text-[var(--text-primary)] min-w-[220px]"
                value={crimeId}
                onChange={(e) => setCrimeId(e.target.value)}
              >
                <option value="">Select crime…</option>
                {crimes.map((c, index) => (
                  <option key={`${c.id ?? 'crime'}-${index}`} value={c.id}>#{c.id} — {c.title}</option>
                ))}
              </select>
            </label>
            <label className="flex flex-col gap-1 text-xs text-[var(--text-muted)]">
              Type
              <select
                className="rounded-lg border border-[var(--border)] px-3 py-2 text-sm text-[var(--text-primary)]"
                value={reportType}
                onChange={(e) => setReportType(e.target.value)}
              >
                <option value="summary">Summary</option>
                <option value="timeline">Timeline</option>
                <option value="evidence">Evidence</option>
                <option value="investigation">Investigation</option>
              </select>
            </label>
            <button
              type="button"
              disabled={!crimeId || busy}
              onClick={handleQueue}
              className="inline-flex items-center gap-1.5 rounded-lg bg-[var(--color-primary)] text-white px-4 py-2 text-sm font-medium disabled:opacity-50"
            >
              <Plus size={14} /> Queue
            </button>
            <button
              type="button"
              disabled={!crimeId || busy}
              onClick={handleGenerate}
              className="inline-flex items-center gap-1.5 rounded-lg border border-[var(--border)] bg-[var(--bg-card)] px-4 py-2 text-sm font-medium text-[var(--text-primary)] disabled:opacity-50"
            >
              Generate summary PDF
            </button>
          </div>
          {templates.length > 0 && (
            <p className="text-xs text-[var(--text-muted)]">{templates.length} template(s) available from API</p>
          )}
        </div>

        <div className="rounded-xl border border-[var(--border)] bg-[var(--bg-card)] overflow-hidden">
          <div className="flex items-center justify-between gap-3 px-4 py-3 border-b border-[var(--border)]">
            <h2 className="text-sm font-semibold text-[var(--text-primary)]">Report queue</h2>
            <input
              className="rounded-lg border border-[var(--border)] px-3 py-1.5 text-sm"
              placeholder="Filter jobs…"
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
            />
          </div>
          {loading ? (
            <p className="p-6 text-sm text-[var(--text-muted)]">Loading…</p>
          ) : filteredJobs.length === 0 ? (
            <p className="p-6 text-sm text-[var(--text-muted)]">No report jobs yet. Queue a report above.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-xs text-[var(--text-muted)] border-b border-[var(--border)]">
                    <th className="px-4 py-2 font-medium">Job ID</th>
                    <th className="px-4 py-2 font-medium">Type</th>
                    <th className="px-4 py-2 font-medium">Crime</th>
                    <th className="px-4 py-2 font-medium">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredJobs.map((job) => {
                    const type = job.report_type || job.type || 'summary'
                    const status = job.status || 'queued'
                    return (
                      <tr key={job.id} className="border-b border-[var(--border)]">
                        <td className="px-4 py-2 font-mono text-xs">{job.id}</td>
                        <td className="px-4 py-2">
                          <span
                            className="inline-flex rounded-md px-2 py-0.5 text-[11px] font-semibold"
                            style={{ background: `${TYPE_COLORS[type] || '#64748b'}18`, color: TYPE_COLORS[type] || '#64748b' }}
                          >
                            {type}
                          </span>
                        </td>
                        <td className="px-4 py-2">#{job.params?.crime_id || job.crime_id || '—'}</td>
                        <td className="px-4 py-2">
                          <span
                            className="inline-flex rounded-md px-2 py-0.5 text-[11px] font-semibold capitalize"
                            style={{ background: `${STATUS_COLORS[status] || '#64748b'}18`, color: STATUS_COLORS[status] || '#64748b' }}
                          >
                            {status}
                          </span>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
