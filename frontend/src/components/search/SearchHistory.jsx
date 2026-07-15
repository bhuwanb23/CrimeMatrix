import { Clock, Play } from 'lucide-react'

const history = [
  { id: 1, query: 'FIR #4521 theft', time: '2 min ago' },
  { id: 2, query: 'Ravi Kumar suspect network', time: '15 min ago' },
  { id: 3, query: 'Active cases Mysuru', time: '1 hr ago' },
  { id: 4, query: 'Cyber fraud patterns', time: '2 hrs ago' },
  { id: 5, query: 'Missing person Koramangala', time: 'Yesterday' },
  { id: 6, query: 'Vehicle KA-01-AB-1234', time: 'Yesterday' },
]

export default function SearchHistory({ onRunSearch }) {
  return (
    <div className="sidebar-section">
      <h3 className="sidebar-section-title">
        <Clock size={14} />
        Search History
      </h3>
      <div className="history-list">
        {history.map((item) => (
          <button
            key={item.id}
            className="history-item"
            onClick={() => onRunSearch(item.query)}
          >
            <div className="history-item-info">
              <span className="history-item-query">{item.query}</span>
              <span className="history-item-time">{item.time}</span>
            </div>
            <Play size={12} className="history-item-run" />
          </button>
        ))}
      </div>
    </div>
  )
}
