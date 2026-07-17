import { Bot, CheckSquare } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import { t } from '../../utils/translate'

export function AssistantCard() {
  const { lang } = useLanguage()

  return (
    <div className="suggestion-card suggestion-card-dark">
      <div className="suggestion-card-header">
        <div className="suggestion-card-avatar">
          <Bot size={16} strokeWidth={2} />
        </div>
        <span className="suggestion-card-badge">{t('ai_copilot', lang)}</span>
      </div>
      <p className="suggestion-card-text">
        {t('copilot_assistant_desc', lang)}
      </p>
    </div>
  )
}

export function TasksCard({ onSend }) {
  const { lang } = useLanguage()
  const tasks = [
    { label: 'Analyze suspect connections', key: 'task_analyze_connections' },
    { label: 'Generate investigation report', key: 'task_generate_report' },
    { label: 'Search cross-district cases', key: 'task_search_cross_district' },
  ]

  return (
    <div className="suggestion-card suggestion-card-light">
      <div className="suggestion-card-tasks">
        {tasks.map((task, i) => (
          <button key={i} className="suggestion-task" onClick={() => onSend(task.label)}>
            <CheckSquare size={14} strokeWidth={1.8} />
            {t(task.key, lang)}
          </button>
        ))}
      </div>
      <div className="suggestion-card-footer">
        <span className="suggestion-card-label">{t('quick_tasks', lang)}</span>
      </div>
    </div>
  )
}

export function PromptCard({ onSend }) {
  const { lang } = useLanguage()
  const promptText = t('suggested_prompt_text', lang)

  return (
    <div className="suggestion-card suggestion-card-light" style={{ cursor: 'pointer' }} onClick={() => onSend(promptText)}>
      <p className="suggestion-prompt-text">{promptText}</p>
      <div className="suggestion-card-footer">
        <span className="suggestion-card-label">{t('suggested_prompt', lang)}</span>
      </div>
    </div>
  )
}
