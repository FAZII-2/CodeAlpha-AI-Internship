export default function MessageInput({
  value,
  onChange,
  onSend,
  onMicClick,
  placeholder = 'Ask a banking question…',
}) {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && value.trim()) {
      onSend()
    }
  }

  return (
    <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 backdrop-blur-md">
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        className="flex-1 bg-transparent text-white placeholder-white/40 outline-none"
      />
      <button
        onClick={onMicClick}
        aria-label="Voice input"
        className="flex h-10 shrink-0 items-center justify-center rounded-full border border-ember-400/50 bg-ember-500/15 px-3 text-xs font-semibold uppercase tracking-[0.12em] text-ember-50 transition hover:bg-ember-500/30 active:scale-95"
      >
        Voice
      </button>
    </div>
  )
}