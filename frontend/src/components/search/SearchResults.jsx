import { Eye, ExternalLink, ChevronLeft, ChevronRight } from 'lucide-react'

export default function SearchResults({ results, page, totalPages, onPageChange }) {
  if (results.length === 0) {
    return (
      <div className="search-empty">
        <Search size={48} strokeWidth={1} className="search-empty-icon" />
        <h3>No results found</h3>
        <p>Try adjusting your search or filters</p>
      </div>
    )
  }

  return (
    <div className="search-results">
      <div className="results-header">
        <span className="results-count">{results.length} results found</span>
      </div>

      <div className="results-table-wrapper">
        <table className="results-table">
          <thead>
            <tr>
              <th>Case ID</th>
              <th>Title</th>
              <th>Crime Type</th>
              <th>District</th>
              <th>Status</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {results.map((row) => (
              <tr key={row.id} className="results-row">
                <td>
                  <span className="case-id-badge">{row.id}</span>
                </td>
                <td>
                  <span className="case-title-text">{row.title}</span>
                </td>
                <td>
                  <span className="case-type-tag">{row.type}</span>
                </td>
                <td>{row.district}</td>
                <td>
                  <span className={`status-badge ${row.status}`}>{row.status}</span>
                </td>
                <td className="date-cell">{row.date}</td>
                <td>
                  <div className="action-btns">
                    <button className="action-btn" aria-label="View">
                      <Eye size={14} strokeWidth={1.8} />
                    </button>
                    <button className="action-btn" aria-label="Open">
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
