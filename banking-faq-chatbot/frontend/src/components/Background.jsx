export default function Background({ children }) {
  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-ink-950">
      <div
        className="ember-field pointer-events-none absolute inset-x-0 bottom-0 h-[75%]"
        style={{
          background:
            "radial-gradient(120% 100% at 50% 100%, var(--color-ember-600) 0%, var(--color-ember-900) 45%, transparent 75%)",
          opacity: 0.76,
        }}
      />

      <div
        className="ember-current pointer-events-none absolute inset-x-[-18%] bottom-[-12%] h-[62%]"
        style={{
          background:
            'radial-gradient(60% 80% at 18% 70%, var(--color-ember-500) 0%, transparent 68%), radial-gradient(52% 70% at 82% 45%, var(--color-ember-900) 0%, transparent 72%)',
          opacity: 0.34,
        }}
      />

      <div
        className="ember-wave ember-wave-one pointer-events-none absolute left-[-30%] top-[34%] h-[42%] w-[78%]"
        style={{
          background:
            'radial-gradient(ellipse at center, var(--color-ember-600) 0%, var(--color-ember-900) 38%, transparent 72%)',
          opacity: 0.35,
        }}
      />

      <div
        className="ember-wave ember-wave-two pointer-events-none absolute right-[-30%] top-[48%] h-[38%] w-[72%]"
        style={{
          background:
            'radial-gradient(ellipse at center, var(--color-ember-500) 0%, var(--color-ember-900) 36%, transparent 70%)',
          opacity: 0.27,
        }}
      />

      <div
        className="ember-flow pointer-events-none absolute inset-[-28%]"
        style={{
          background:
            'radial-gradient(48% 42% at 18% 24%, var(--color-ember-900) 0%, transparent 72%), radial-gradient(46% 48% at 82% 70%, var(--color-ember-600) 0%, transparent 70%), radial-gradient(36% 38% at 56% 42%, var(--color-ember-900) 0%, transparent 74%)',
          opacity: 0.28,
        }}
      />

      <div
        className="ember-drift pointer-events-none absolute -top-40 left-1/2 h-96 w-96 -translate-x-1/2 rounded-full blur-3xl"
        style={{ backgroundColor: "var(--color-ember-500)", opacity: 0.15 }}
      />

      {/* Actual screen content sits above the glow layers */}
      <div className="relative z-10 flex min-h-screen flex-col">
        {children}
      </div>
    </div>
  )
}