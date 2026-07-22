import { MessageSquare } from 'lucide-react'
import { useState, useEffect } from 'react'
import { getEvaluationFeedback } from '../../services/analytics'

export default function FeedbackSummary() {
  const [feedback, setFeedback] = useState([])

  useEffect(() => {
    async function loadFeedback() {
      try {
        const res = await getEvaluationFeedback()
        setFeedback(res?.data?.items || [])
      } catch (e) { console.error(e) }
    }
    loadFeedback()
  }, [])

  const correct = feedback.filter(f => f.feedback_type === 'correct').length
  const incorrect = feedback.filter(f => f.feedback_type === 'incorrect').length
  const avgRating = feedback.length > 0 ? (feedback.reduce((s, f) => s + (f.rating || 0), 0) / feedback.length).toFixed(1) : 0

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4">
      <div className="flex items-center gap-2 mb-3">
        <MessageSquare size={14} className="text-amber-500" />
        <h3 className="text-sm font-semibold text-slate-900">Feedback Summary</h3>
      </div>

      <div className="grid grid-cols-3 gap-2 mb-3">
        <div className="text-center p-2 bg-green-50 rounded-lg">
          <span className="block text-lg font-bold text-green-600">{correct}</span>
          <span className="text-[9px] text-green-500">Correct</span>
        </div>
        <div className="text-center p-2 bg-red-50 rounded-lg">
          <span className="block text-lg font-bold text-red-600">{incorrect}</span>
          <span className="text-[9px] text-red-500">Incorrect</span>
        </div>
        <div className="text-center p-2 bg-amber-50 rounded-lg">
          <span className="block text-lg font-bold text-amber-600">{avgRating}</span>
          <span className="text-[9px] text-amber-500">Avg Rating</span>
        </div>
      </div>

      {feedback.length > 0 && (
        <div className="space-y-1">
          {feedback.slice(0, 3).map((f, i) => (
            <div key={i} className="p-1.5 bg-slate-50 rounded text-[10px]">
              <span className="font-semibold text-slate-700">{f.feedback_type}</span>
              <span className="text-slate-400 ml-2">Rating: {f.rating}/5</span>
              {f.comment && <span className="text-slate-500 ml-2">— {f.comment}</span>}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
