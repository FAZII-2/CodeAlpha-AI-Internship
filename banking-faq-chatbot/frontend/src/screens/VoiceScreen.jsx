import { useEffect } from 'react'
import Background from '../components/Background'
import GlowOrb from '../components/GlowOrb'
import { useSpeechRecognition } from '../hooks/useSpeechRecognition'

export default function VoiceScreen({ onClose, onResult }) {
  const { transcript, listening, supported, start, stop, reset, setTranscript } = useSpeechRecognition()

  useEffect(() => {
    if (supported) start()
    return () => stop()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const handleSend = () => {
    stop()
    onResult(transcript)
    reset()
  }

  return (
    <Background>
      <div className="flex items-center justify-between px-6 pt-6 sm:px-10">
        <span className="text-sm font-semibold uppercase tracking-[0.22em] text-ember-400">BankID</span>
        <button onClick={onClose} className="rounded-full border border-white/15 bg-white/5 px-4 py-2 text-sm text-white/80 backdrop-blur-md">
          Close chat
        </button>
      </div>

      <div className="flex flex-1 flex-col items-center justify-center gap-8 px-6 text-center">
        <GlowOrb listening={listening} />
        <p className="text-sm text-white/40">
          {supported ? (listening ? 'BankID is listening…' : 'Paused') : 'Voice not supported in this browser'}
        </p>
        <p className="max-w-sm text-lg text-white/70">
          {transcript || (supported ? 'Say something…' : 'Type below instead.')}
        </p>
      </div>

      <div className="flex items-center justify-center gap-6 px-6 pb-10">
        <input
          type="text"
          value={transcript}
          onChange={(event) => setTranscript(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter' && transcript.trim()) handleSend()
          }}
          placeholder="Or type here"
          className="w-full max-w-xs rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-white outline-none placeholder-white/30"
        />
        <button onClick={handleSend} className="flex h-14 shrink-0 items-center justify-center rounded-full bg-ember-500 px-5 text-xs font-semibold uppercase tracking-[0.14em] text-white transition hover:bg-ember-400">Send</button>
      </div>
    </Background>
  )
}