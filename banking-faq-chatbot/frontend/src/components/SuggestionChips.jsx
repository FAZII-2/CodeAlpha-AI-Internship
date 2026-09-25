export default function SuggestionChips({ suggestions, onSelect }) {
  if (!suggestions || suggestions.length === 0) return null

  return (
    <div className="flex flex-wrap gap-2 pl-1">
      {suggestions.map((s) => (
        <button
          key={s.question}
          onClick={() => onSelect(s.question)}
          className="rounded-full border border-ember-500/40 bg-ember-500/10 px-3 py-1.5 text-xs text-ember-400 transition hover:bg-ember-500/20"
        >
          {s.question}
        </button>
      ))}
    </div>
  )
}