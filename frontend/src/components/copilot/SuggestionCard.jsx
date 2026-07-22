import { Bot, CheckSquare } from 'lucide-react'

export function AssistantCard() {
  return (
    <div className="suggestion-card suggestion-card-dark">
      <div className="suggestion-card-header">
        <div className="suggestion-card-avatar">
          <Bot size={16} strokeWidth={2} />
        </div>
        <span className="suggestion-card-badge">AI Copilot</span>
      </div>
      <p className="suggestion-card-text">
        Your AI Investigation Assistant — trained on Karnataka police protocols, criminal databases, and legal frameworks.
      </p>
    </div>
  )
}

export function TasksCard({ onSend }) {
  const tasks = [
    'Analyze suspect connections',
    'Generate investigation report',
    'Search cross-district cases',
  ]

  return (
    <div className="suggestion-card suggestion-card-light">
      <div className="suggestion-card-tasks">
        {tasks.map((task, i) => (
          <button key={i} className="suggestion-task" onClick={() => onSend(task)}>
            <CheckSquare size={14} strokeWidth={1.8} />
            {task}
          </button>
        ))}
      </div>
      <div className="suggestion-card-footer">
        <span className="suggestion-card-label">Quick Tasks</span>
      </div>
    </div>
  )
}

export function PromptCard({ onSend: _onSend }) {
  const prompt = 'What are the common MO patterns in theft cases across Bengaluru district this month?'

  return (
    <div className="suggestion-card suggestion-card-light">
      <p className="suggestion-prompt-text">{prompt}</p>
      <div className="suggestion-card-footer">
        <span className="suggestion-card-label">Suggested prompt</span>
      </div>
    </div>
  )
}
