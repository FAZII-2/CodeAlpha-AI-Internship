import { useState } from 'react'
import WelcomeScreen from './screens/WelcomeScreen'
import VoiceScreen from './screens/VoiceScreen'
import ChatScreen from './screens/ChatScreen'
import { sendChatMessage } from './api/chatApi'

const SCREENS = { WELCOME: 'welcome', VOICE: 'voice', CHAT: 'chat' }
const MIN_RESPONSE_DELAY = 1400
let nextId = 1

const wait = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds))

function App() {
  const [screen, setScreen] = useState(SCREENS.WELCOME)
  const [messages, setMessages] = useState([])
  const [isWorking, setIsWorking] = useState(false)

  const addMessage = (role, text, suggestions) => {
    setMessages((prev) => [...prev, { id: nextId++, role, text, suggestions }])
  }

  const handleSend = async (text) => {
    if (!text.trim()) return
    setScreen(SCREENS.CHAT)
    addMessage('user', text)
    setIsWorking(true)

    const recent = messages.filter((m) => m.role === 'user').slice(-1).map((m) => m.text)

    try {
      const [data] = await Promise.all([
        sendChatMessage(text, recent),
        wait(MIN_RESPONSE_DELAY),
      ])
      addMessage('ai', data.answer, data.suggestions?.length ? data.suggestions : undefined)
    } catch {
      await wait(MIN_RESPONSE_DELAY)
      addMessage('ai', "Sorry, I couldn't reach the server. Please check your connection and try again.")
    } finally {
      setIsWorking(false)
    }
  }

  const handleMicClick = () => setScreen(SCREENS.VOICE)
  const handleVoiceResult = (transcript) => {
    if (transcript && transcript.trim()) handleSend(transcript)
    else setScreen(SCREENS.WELCOME)
  }
  const handleCloseChat = () => setScreen(SCREENS.WELCOME)

  if (screen === SCREENS.VOICE) {
    return <VoiceScreen onClose={() => setScreen(SCREENS.WELCOME)} onResult={handleVoiceResult} />
  }
  if (screen === SCREENS.CHAT) {
    return (
      <ChatScreen
        messages={messages}
        isWorking={isWorking}
        onSend={handleSend}
        onMicClick={handleMicClick}
        onSelectSuggestion={handleSend}
        onClose={handleCloseChat}
      />
    )
  }
  return <WelcomeScreen onSend={handleSend} onMicClick={handleMicClick} />
}

export default App