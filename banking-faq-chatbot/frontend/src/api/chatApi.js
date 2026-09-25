const API_BASE = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api').replace(/\/$/, '')

export async function sendChatMessage(message, recentMessages = []) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, recent_messages: recentMessages }),
  })
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}