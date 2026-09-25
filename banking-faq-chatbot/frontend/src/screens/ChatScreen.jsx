import { useState, useRef, useEffect } from 'react'
import Background from '../components/Background'
import ChatBubble from '../components/ChatBubble'
import SuggestionChips from '../components/SuggestionChips'
import MessageInput from '../components/MessageInput'

export default function ChatScreen({ messages, isWorking, onSend, onMicClick, onSelectSuggestion, onClose }) {
  const [input, setInput] = useState('')
  const scrollRef = useRef(null)

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages, isWorking])

  const handleSend = () => {
    if (!input.trim()) return
    onSend(input)
    setInput('')
  }

  return (
    <Background>
      <div className="flex items-center justify-between px-6 pt-6 sm:px-10">
        <span className="text-sm font-semibold uppercase tracking-[0.22em] text-ember-400">BankID</span>
        <button
          onClick={onClose}
          className="rounded-full border border-white/15 bg-white/5 px-4 py-2 text-sm text-white/80 backdrop-blur-md"
        >
          Close chat
        </button>
      </div>

      <div ref={scrollRef} className="flex-1 space-y-4 overflow-y-auto px-6 py-6 sm:px-10">
        {messages.map((m) => (
          <div key={m.id} className="space-y-2">
            <ChatBubble role={m.role} text={m.text} />
            {m.suggestions && (
              <SuggestionChips suggestions={m.suggestions} onSelect={onSelectSuggestion} />
            )}
          </div>
        ))}

        {isWorking && (
          <div
            className="flex items-center gap-3 pl-1 text-sm text-white/45"
            aria-live="polite"
            aria-label="Preparing an answer"
          >
            <span>Preparing an answer</span>
            <span className="thinking-dots" aria-hidden="true">
              <span />
              <span />
              <span />
            </span>
          </div>
        )}
      </div>

      <div className="px-6 pb-8 pt-2 sm:px-10">
        <MessageInput
          value={input}
          onChange={setInput}
          onSend={handleSend}
          onMicClick={onMicClick}
        />
      </div>
    </Background>
  )
}