import { useState, useCallback } from 'react'
import ChatArea from './copilot/ChatArea'
import ChatHistory from './copilot/ChatHistory'
import ContextPanel from './copilot/ContextPanel'

const aiResponses = [
  'Based on my analysis of FIR #4521 and related cases, I found 3 similar MO patterns in the Bengaluru North district over the past 6 months. The suspect appears to target residential areas between 2-4 AM, using forced entry through rear doors. Would you like me to generate a detailed connection report?',
  'I\'ve cross-referenced the suspect\'s phone records with cell tower data. Ravi Kumar was active near the crime scene at 2:15 AM on the night of the incident. This aligns with the CCTV footage timestamp. I recommend adding this to the evidence chain.',
  'The investigation report for Case #1089 has been compiled. It includes: evidence summary, witness statements, timeline of events, and AI reasoning chain. The report is court-ready and follows KSP formatting guidelines. Shall I export it as PDF?',
  'I\'ve identified a potential link between the theft pattern in Malleshwaram and a similar series in Indiranagar. Both show the same entry method and timing signature. This could indicate a serial offender operating across districts.',
]

import { useLanguage } from '../context/LanguageContext'
import { t } from '../utils/translate'

export default function CopilotPage() {
  const { lang } = useLanguage()
  const [activeChatId, setActiveChatId] = useState(null)
  const [messages, setMessages] = useState([])
  const [isTyping, setIsTyping] = useState(false)
  const [historyOpen, setHistoryOpen] = useState(false)
  const [contextOpen, setContextOpen] = useState(false)

  const handleSend = useCallback((content, source) => {
    const userMsg = {
      role: 'user',
      content,
      time: new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' }),
    }
    setMessages((prev) => [...prev, userMsg])
    setIsTyping(true)

    setTimeout(() => {
      const response = aiResponses[Math.floor(Math.random() * aiResponses.length)]
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: response,
        time: new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' }),
      }])
      setIsTyping(false)
    }, 1500)
  }, [])

  const handleNewChat = () => {
    setMessages([])
    setActiveChatId(null)
  }

  return (
    <div className="copilot-page">
      <ChatArea
        messages={messages}
        onSend={handleSend}
        isTyping={isTyping}
        onToggleHistory={() => setHistoryOpen(!historyOpen)}
        onToggleContext={() => setContextOpen(!contextOpen)}
        historyOpen={historyOpen}
        contextOpen={contextOpen}
      />

      {/* History Overlay */}
      {historyOpen && (
        <>
          <div className="copilot-overlay" onClick={() => setHistoryOpen(false)} />
          <div className="copilot-slide-panel left">
            <ChatHistory
              activeChatId={activeChatId}
              onSelectChat={(id) => { setActiveChatId(id); setHistoryOpen(false) }}
              onNewChat={() => { handleNewChat(); setHistoryOpen(false) }}
              onClose={() => setHistoryOpen(false)}
            />
          </div>
        </>
      )}

      {/* Context Overlay */}
      {contextOpen && (
        <>
          <div className="copilot-overlay" onClick={() => setContextOpen(false)} />
          <div className="copilot-slide-panel right">
            <ContextPanel onClose={() => setContextOpen(false)} />
          </div>
        </>
      )}
    </div>
  )
}
