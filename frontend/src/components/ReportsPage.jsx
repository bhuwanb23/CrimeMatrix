import { useState, useMemo } from 'react'
import ReportStats from './reports/ReportStats'
import ReportFilters from './reports/ReportFilters'
import ReportTable from './reports/ReportTable'
import { reports as allReports } from './reports/reportsData'

const ITEMS_PER_PAGE = 8

import { useLanguage } from '../context/LanguageContext'
import { t } from '../utils/translate'

export default function ReportsPage() {
  const { lang } = useLanguage()
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
    <div className="reports-page">
      <div className="reports-header">
        <div>
          <h1 className="reports-title">{t('reports_and_documentation', lang)}</h1>
          <p className="reports-subtitle">{t('investigation_reports_desc', lang)}</p>
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
