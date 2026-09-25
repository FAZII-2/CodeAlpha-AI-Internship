export default function QuickActionCard({ label, title, onClick }) {
  return (
    <button
      onClick={onClick}
      className="flex min-w-[160px] flex-1 flex-col items-start gap-3 rounded-2xl border border-white/10 bg-white/5 p-4 text-left backdrop-blur-md transition hover:bg-white/10 active:scale-[0.98]"
    >
      <span className="text-[0.65rem] font-semibold uppercase tracking-[0.18em] text-ember-400">{label}</span>
      <span className="text-sm font-medium text-white/90">{title}</span>
    </button>
  )
}