import { useState } from 'react'
import Background from '../components/Background'
import QuickActionCard from '../components/QuickActionCard'
import MessageInput from '../components/MessageInput'

const QUICK_ACTIONS = [
  { label: 'Cards', title: 'Block a lost card' },
  { label: 'Accounts', title: 'Open an account' },
  { label: 'Transfers', title: 'Send a transfer' },
  { label: 'Planning', title: 'Calculate my EMI' },
]

export default function WelcomeScreen({ onSend, onMicClick }) {
  const [message, setMessage] = useState('')

  const handleSend = (text) => {
    const finalText = text ?? message
    if (!finalText.trim()) return
    onSend(finalText)
    setMessage('')
  }

  return (
    <Background>
      <div className="flex flex-1 flex-col justify-end gap-8 px-6 pb-8 pt-16 sm:px-10">
        <p className="text-sm font-semibold uppercase tracking-[0.22em] text-ember-400">BankID banking assistant</p>
        <h1 className="text-4xl font-bold leading-tight text-white sm:text-5xl">
          What are we<br />banking on today?
        </h1>

        <div className="flex gap-3 overflow-x-auto pb-2">
          {QUICK_ACTIONS.map((action) => (
            <QuickActionCard
              key={action.title}
              label={action.label}
              title={action.title}
              onClick={() => handleSend(action.title)}
            />
          ))}
        </div>

        <MessageInput
          value={message}
          onChange={setMessage}
          onSend={() => handleSend()}
          onMicClick={onMicClick}
        />
      </div>
    </Background>
  )
}