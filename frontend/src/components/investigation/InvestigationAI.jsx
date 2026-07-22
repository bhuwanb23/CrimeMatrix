import { useState } from 'react'
import { Bot, Send, FileText, Search, Link2, BarChart3, ClipboardList, Loader2 } from 'lucide-react'
import { analyzeInvestigation } from '../../services/investigationAI'

const quickActions = [
  { id: 'summary', label: 'Summarize', icon: FileText, description: 'Overview of findings' },
  { id: 'leads', label: 'Find Leads', icon: Search, description: 'Suggest next steps' },
  { id: 'evidence', label: 'Evidence', icon: ClipboardList, description: 'Review evidence' },
  { id: 'similar', label: 'Similar Cases', icon: Link2, description: 'Related crimes' },
  { id: 'full', label: 'Full Report', icon: BarChart3, description: 'Comprehensive report' },
]

export default function InvestigationAI({ investigationId, investigation }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [activeAction, setActiveAction] = useState(null)

  async function handleQuickAction(action) {
    if (loading) return
    setLoading(true)
    setActiveAction(action.id)

    setMessages((prev) => [...prev, {
      role: 'user',
      content: `Analyze this investigation: ${action.label}`,
      type: 'action',
    }])

    try {
      const res = await analyzeInvestigation(investigationId, action.id)
      const data = res?.data || res
      const context = data?.context || 'No analysis available.'

      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: context,
        type: 'analysis',
        analysisType: action.id,
      }])
    } catch {
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: 'Failed to generate analysis. Please try again.',
        type: 'error',
      }])
    } finally {
      setLoading(false)
      setActiveAction(null)
    }
  }

  async function handleSend() {
    if (!input.trim() || loading) return
    const question = input.trim()
    setInput('')

    setMessages((prev) => [...prev, { role: 'user', content: question }])
    setLoading(true)

    try {
      const res = await analyzeInvestigation(investigationId, 'summary', question)
      const data = res?.data || res
      const context = data?.context || 'No response available.'

      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: context,
        type: 'analysis',
      }])
    } catch {
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: 'Failed to process your question. Please try again.',
        type: 'error',
      }])
    } finally {
      setLoading(false)
    }
  }

  function formatContent(text) {
    if (!text) return null
    return text.split('\n').map((line, i) => {
      if (line.startsWith('## ')) return <h4 key={i} className="ai-msg-heading">{line.replace('## ', '')}</h4>
      if (line.startsWith('### ')) return <h5 key={i} className="ai-msg-subheading">{line.replace('### ', '')}</h5>
      if (line.startsWith('- ')) return <li key={i} className="ai-msg-list-item">{line.replace('- ', '')}</li>
      if (line.startsWith('#### ')) return <h6 key={i} className="ai-msg-subheading">{line.replace('#### ', '')}</h6>
      if (line.trim() === '') return <br key={i} />
      return <p key={i} className="ai-msg-text">{line}</p>
    })
  }

  return (
    <div className="investigation-ai">
      <div className="ai-header">
        <Bot size={18} />
        <div>
          <h4>AI Investigation Assistant</h4>
          <span className="ai-header-sub">
            INV-{String(investigationId).padStart(3, '0')}
            {investigation && ` — ${investigation.status || 'Active'}`}
          </span>
        </div>
      </div>

      {messages.length === 0 && !loading && (
        <div className="ai-empty">
          <div className="ai-empty-icon">🤖</div>
          <p>Ask me anything about this investigation</p>
          <span>I can summarize evidence, suggest leads, find similar cases, and more.</span>
        </div>
      )}

      <div className="ai-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`ai-message ai-message-${msg.role}`}>
            {msg.role === 'assistant' && <div className="ai-avatar"><Bot size={14} /></div>}
            <div className={`ai-msg-content ${msg.type === 'error' ? 'ai-msg-error' : ''}`}>
              {msg.type === 'action' ? (
                <span className="ai-msg-action">{msg.content}</span>
              ) : (
                <div className="ai-msg-body">{formatContent(msg.content)}</div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="ai-message ai-message-assistant">
            <div className="ai-avatar"><Bot size={14} /></div>
            <div className="ai-msg-content ai-msg-thinking">
              <Loader2 size={14} className="similar-spinning" />
              <span>Analyzing investigation data...</span>
            </div>
          </div>
        )}
      </div>

      <div className="ai-quick-actions">
        {quickActions.map((action) => (
          <button
            key={action.id}
            className={`ai-quick-btn ${activeAction === action.id ? 'active' : ''}`}
            onClick={() => handleQuickAction(action)}
            disabled={loading}
            title={action.description}
          >
            <action.icon size={12} />
            {action.label}
          </button>
        ))}
      </div>

      <div className="ai-input-area">
        <input
          className="ai-input"
          placeholder="Ask about this investigation..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
          disabled={loading}
        />
        <button className="ai-send-btn" onClick={handleSend} disabled={loading || !input.trim()}>
          <Send size={14} />
        </button>
      </div>
    </div>
  )
}
