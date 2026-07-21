import { Eye, ExternalLink, ChevronLeft, ChevronRight, Search } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import { t } from '../../utils/translate'

export default function SearchResults({ results, page, totalPages, onPageChange, onViewCase }) {
  const { lang } = useLanguage()
  if (results.length === 0) {
    return (
      <div className="search-empty">
        <Search size={48} strokeWidth={1} className="search-empty-icon" />
        <h3>{t('no_results_found', lang)}</h3>
        <p>{t('try_adjusting_search', lang)}</p>
      </div>
    )
  }

  return (
    <div className="search-results">
      <div className="results-header">
        <span className="results-count">{results.length} {t('results_found', lang)}</span>
      </div>

      <div className="results-table-wrapper">
        <table className="results-table">
          <thead>
            <tr>
              <th>{t('case_id', lang)}</th>
              <th>{t('title', lang)}</th>
              <th>{t('crime_type', lang)}</th>
              <th>{t('district', lang)}</th>
              <th>{t('status', lang)}</th>
              <th>{t('date', lang)}</th>
              <th>{t('actions', lang)}</th>
            </tr>
          </thead>
          <tbody>
            {results.map((row) => (
              <tr
                key={row.id}
                className="results-row"
                onClick={() => onViewCase(row.id)}
              >
                <td>
                  <span className="case-id-badge">{row.id}</span>
                </td>
                <td>
                  <span className="case-title-text">{t(row.title, lang)}</span>
                </td>
                <td>
                  <span className="case-type-tag">{t(row.type.toLowerCase().replace(/ /g, '_'), lang) || row.type}</span>
                </td>
                <td>{t(row.district.toLowerCase().replace(/ /g, '_'), lang) || row.district}</td>
                <td>
                  <span className={`status-badge ${row.status}`}>{t(row.status.toLowerCase(), lang) || row.status}</span>
                </td>
                <td className="date-cell">{row.date}</td>
                <td>
                  <div className="action-btns" onClick={(e) => e.stopPropagation()}>
                    <button
                      className="action-btn"
                      aria-label={t('view', lang)}
                      onClick={() => onViewCase(row.id)}
                    >
                      <Eye size={14} strokeWidth={1.8} />
                    </button>
                    <button
                      className="action-btn"
                      aria-label={t('open', lang)}
                      onClick={() => onViewCase(row.id)}
                    >
                      <ExternalLink size={14} strokeWidth={1.8} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="results-pagination">
          <button
            className="pagination-btn"
            disabled={page === 1}
            onClick={() => onPageChange(page - 1)}
          >
            <ChevronLeft size={16} />
          </button>
          {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
            <button
              key={p}
              className={`pagination-btn ${p === page ? 'active' : ''}`}
              onClick={() => onPageChange(p)}
            >
              {p}
            </button>
          ))}
          <button
            className="pagination-btn"
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
