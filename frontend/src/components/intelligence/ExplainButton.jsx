import { Brain } from 'lucide-react'

export default function ExplainButton({ onClick, loading = false, label = 'Why?', size = 'sm' }) {
  const sizeClasses = size === 'sm'
    ? 'text-[10px] px-1.5 py-0.5 gap-0.5'
    : 'text-xs px-2 py-1 gap-1'

  return (
    <button
      onClick={(e) => { e.stopPropagation(); onClick?.(e) }}
      disabled={loading}
      className={`flex items-center ${sizeClasses} bg-purple-500/10 text-purple-400 hover:bg-purple-500/20 hover:text-purple-300 rounded-lg transition-all font-medium disabled:opacity-50`}
      title="Explain with AI"
    >
      {loading ? (
        <div className="w-2.5 h-2.5 border border-purple-400/30 border-t-purple-400 rounded-full animate-spin" />
      ) : (
        <Brain size={size === 'sm' ? 10 : 12} />
      )}
      {label}
    </button>
  )
}
