import { reportTypes, reportStatuses } from './reportsData'
import { Eye, Download, ChevronLeft, ChevronRight } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'


export default function ReportTable({ reports, page, totalPages, onPageChange }) {
  const { t } = useLanguage()
  return (
    <div className="report-table-card">
      <div className="report-table-wrapper">
        <table className="report-table">
          <thead>
            <tr>
              <th>{t('Report ID')}</th>
              <th>{t('Title')}</th>
              <th>{t('Type')}</th>
              <th>{t('Case')}</th>
              <th>{t('Officer')}</th>
              <th>{t('Date')}</th>
              <th>{t('Pages')}</th>
              <th>{t('Status')}</th>
              <th>{t('Actions')}</th>
            </tr>
          </thead>
          <tbody>
            {reports.map((report) => {
              const typeInfo = reportTypes[report.type]
              const statusInfo = reportStatuses[report.status]
              return (
                <tr key={report.id} className="report-row">
                      <button className="report-action-btn" aria-label={t('Download')}>
                        <Download size={14} />
                      </button>
                    </div>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="report-pagination">
          <button
            className="report-page-btn"
            disabled={page === 1}
            onClick={() => onPageChange(page - 1)}
          >
            <ChevronLeft size={16} />
          </button>
          {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
            <button
              key={p}
              className={`report-page-btn ${p === page ? 'active' : ''}`}
              onClick={() => onPageChange(p)}
            >
              {p}
            </button>
          ))}
          <button
            className="report-page-btn"
            disabled={page === totalPages}
            onClick={() => onPageChange(page + 1)}
          >
            <ChevronRight size={16} />
          </button>
        </div>
      )}
    </div>
  )
}
