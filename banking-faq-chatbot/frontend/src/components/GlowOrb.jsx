import { motion } from 'framer-motion'

export default function GlowOrb({ listening = false }) {
  return (
    <div className="relative flex h-64 w-64 items-center justify-center">
      {/* Outer pulsing rings, only animate while actively listening */}
      {listening && (
        <>
          <div className="voice-aura voice-aura-pulse" />
          <div className="voice-aura voice-aura-ring" />
          <motion.div
            className="absolute inset-0 rounded-full"
            style={{ backgroundColor: 'var(--color-ember-500)' }}
            initial={{ opacity: 0.6, scale: 1 }}
            animate={{ opacity: 0, scale: 1.7 }}
            transition={{ duration: 1.05, repeat: Infinity, ease: 'easeOut' }}
          />
          <motion.div
            className="absolute inset-0 rounded-full"
            style={{ backgroundColor: 'var(--color-ember-500)' }}
            initial={{ opacity: 0.5, scale: 1 }}
            animate={{ opacity: 0, scale: 1.5 }}
            transition={{ duration: 1.05, repeat: Infinity, ease: 'easeOut', delay: 0.35 }}
          />
        </>
      )}

      {/* The orb itself: a soft radial gradient sphere, always gently breathing */}
      <motion.div
        className="relative h-40 w-40 rounded-full"
        style={{
          background:
            'radial-gradient(circle at 35% 30%, var(--color-ember-50) 0%, var(--color-ember-400) 35%, var(--color-ember-600) 70%, var(--color-ember-900) 100%)',
          boxShadow: '0 0 60px 10px rgba(255, 107, 26, 0.45)',
        }}
        animate={{
          scale: listening ? [1, 1.06, 1] : [1, 1.02, 1],
        }}
        transition={{
          duration: listening ? 1.4 : 3,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />

      {listening && (
        <div className="absolute bottom-3 flex h-8 items-center gap-1" aria-hidden="true">
          {[0, 1, 2, 3, 4, 5, 6].map((bar) => (
            <motion.span
              key={bar}
              className="w-1 rounded-full bg-ember-50/80"
                  animate={{ height: ['8px', `${18 + ((bar * 9) % 20)}px`, '8px'] }}
              transition={{
                    duration: 0.42 + bar * 0.04,
                repeat: Infinity,
                ease: 'easeInOut',
                delay: bar * 0.05,
              }}
            />
          ))}
        </div>
      )}
    </div>
  )
}