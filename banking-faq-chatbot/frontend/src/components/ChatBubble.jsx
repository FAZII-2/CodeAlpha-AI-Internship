export default function ChatBubble({ role, text }) {
  const isUser = role === 'user'

  return (
    <div className={`message-enter ${isUser ? 'message-enter-user justify-end' : 'message-enter-bot justify-start'} flex`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed sm:text-base ${
          isUser
            ? 'bg-ember-500 text-white'
            : 'border border-white/10 bg-white/5 text-white/90 backdrop-blur-md'
        }`}
      >
        {text}
      </div>
    </div>
  )
}