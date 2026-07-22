import { useState, useMemo } from 'react'
import { FileText } from 'lucide-react'
import ReportStats from './reports/ReportStats'
import ReportFilters from './reports/ReportFilters'
import ReportTable from './reports/ReportTable'
import { reports as allReports } from './reports/reportsData'

const ITEMS_PER_PAGE = 8

export default function ReportsPage() {
  const [filters, setFilters] = useState({ search: '', date: '', type: '', status: '' })
  const [page, setPage] = useState(1)

  const filteredReports = useMemo(() => {
    let results = allReports

    if (filters.search) {
      const q = filters.search.toLowerCase()
      results = results.filter(
        (r) =>
          r.id.toLowerCase().includes(q) ||
          r.title.toLowerCase().includes(q) ||
          r.caseId.toLowerCase().includes(q) ||
          r.officer.toLowerCase().includes(q)
      )
    }

    if (filters.type) {
      results = results.filter((r) => r.type === filters.type)
    }

    if (filters.status) {
      results = results.filter((r) => r.status === filters.status)
    }

    return results
  }, [filters])

  const totalPages = Math.ceil(filteredReports.length / ITEMS_PER_PAGE)
  const paginatedReports = filteredReports.slice(
    (page - 1) * ITEMS_PER_PAGE,
    page * ITEMS_PER_PAGE
  )

  const handleExport = () => {
    console.log('Export CSV:', filteredReports)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-5">
        {/* Hero Header */}
        <div className="bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 rounded-2xl p-6 text-white shadow-lg shadow-orange-500/20">
          <div className="flex items-center gap-4">
            <div className="w-14 h-14 bg-white/20 backdrop-blur rounded-2xl flex items-center justify-center">
              <FileText size={28} />
            </div>
            <div>
              <h1 className="text-2xl font-bold">Reports & Documentation</h1>
              <p className="text-white/80 text-sm mt-0.5">Investigation reports, court documents, and exports</p>
            </div>
          </div>
        </div>

      <ReportStats />

      <ReportFilters
        filters={filters}
        onFilterChange={(f) => { setFilters(f); setPage(1) }}
        onExport={handleExport}
      />

      <ReportTable
        reports={paginatedReports}
        page={page}
        totalPages={totalPages}
        onPageChange={setPage}
      />
    </div>
  )
}
