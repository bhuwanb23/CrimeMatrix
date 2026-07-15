import { useState, useCallback } from 'react'
import ChatHistory from './copilot/ChatHistory'
import ChatArea from './copilot/ChatArea'
import ContextPanel from './copilot/ContextPanel'
import { ArrowLeft } from 'lucide-react'

const aiResponses = [
  'Based on my analysis of FIR #4521 and related cases, I found 3 similar MO patterns in the Bengaluru North district over the past 6 months. The suspect appears to target residential areas between 2-4 AM, using forced entry through rear doors. Would you like me to generate a detailed connection report?',
  'I\'ve cross-referenced the suspect\'s phone records with cell tower data. Ravi Kumar was active near the crime scene at 2:15 AM on the night of the incident. This aligns with the CCTV footage timestamp. I recommend adding this to the evidence chain.',
  'The investigation report for Case #1089 has been compiled. It includes: evidence summary, witness statements, timeline of events, and AI reasoning chain. The report is court-ready and follows KSP formatting guidelines. Shall I export it as PDF?',
  'I\'ve identified a potential link between the theft pattern in Malleshwaram and a similar series in Indiranagar. Both show the same entry method and timing signature. This could indicate a serial offender operating across districts.',
]

export default function CopilotPage({ onBack }) {
  const [activeChatId, setActiveChatId] = useState(null)
  const [messages, setMessages] = useState([])
  const [isTyping, setIsTyping] = useState(false)

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
      const aiMsg = {
        role: 'assistant',
        content: response,
        time: new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' }),
      }
      setMessages((prev) => [...prev, aiMsg])
      setIsTyping(false)
    }, 1500)
  }, [])

  const handleNewChat = () => {
    setMessages([])
    setActiveChatId(null)
  }

  const handleSelectChat = (id) => {
    setActiveChatId(id)
    // In a real app, load messages for this chat
    setMessages([])
  }

  return (
    <div className="copilot-page">
      {/* Back to Dashboard */}
      <button className="copilot-back" onClick={onBack}>
        <ArrowLeft size={16} strokeWidth={1.8} />
        Dashboard
      </button>

      <div className="copilot-layout">
        <ChatHistory
          activeChatId={activeChatId}
          onSelectChat={handleSelectChat}
          onNewChat={handleNewChat}
        />

        <ChatArea
          messages={messages}
          onSend={handleSend}
          isTyping={isTyping}
        />

        <ContextPanel />
      </div>
    </div>
  )
}
