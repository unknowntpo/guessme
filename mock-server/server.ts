import { WebSocketServer, WebSocket } from 'ws'

const PORT = 8080
const KNOWN_LABELS = ['Cat', 'Dog', 'House', 'Tree', 'Car', 'Sun', 'Flower', 'Fish', 'Bird', 'Apple', 'Star', 'Boat', 'Cup']

interface ClientMessage {
  clientId: string
  type: 'stroke' | 'submit' | 'clear'
  data?: {
    points?: { x: number; y: number }[]
  }
}

interface Prediction {
  label: string
  confidence: number
}

interface ServerMessage {
  clientId: string
  type: 'predictions' | 'final'
  data: Prediction[] | Prediction
}

// Track stroke count per client for prediction simulation
const clientStrokes = new Map<string, number>()

function generatePredictions(strokeCount: number): Prediction[] {
  const strokeFactor = Math.min(strokeCount / 10, 1)

  const results = KNOWN_LABELS.map(label => ({
    label,
    confidence: Math.round(Math.random() * 60 * strokeFactor + Math.random() * 20)
  }))

  return results.sort((a, b) => b.confidence - a.confidence).slice(0, 5)
}

const wss = new WebSocketServer({ port: PORT })

console.log(`Mock WebSocket server running on ws://localhost:${PORT}`)

wss.on('connection', (ws: WebSocket) => {
  console.log('Client connected')

  let predictionInterval: ReturnType<typeof setInterval> | null = null
  let currentClientId: string | null = null

  ws.on('message', (data: Buffer) => {
    try {
      const message: ClientMessage = JSON.parse(data.toString())
      currentClientId = message.clientId

      console.log(`[${message.clientId}] ${message.type}`)

      switch (message.type) {
        case 'stroke':
          // Increment stroke count
          const count = (clientStrokes.get(message.clientId) || 0) + 1
          clientStrokes.set(message.clientId, count)

          // Start prediction stream if not already running
          if (!predictionInterval) {
            predictionInterval = setInterval(() => {
              const strokeCount = clientStrokes.get(currentClientId!) || 0
              if (strokeCount > 0) {
                const predictions = generatePredictions(strokeCount)
                const response: ServerMessage = {
                  clientId: currentClientId!,
                  type: 'predictions',
                  data: predictions
                }
                ws.send(JSON.stringify(response))
              }
            }, 500)
          }
          break

        case 'submit':
          // Stop prediction stream
          if (predictionInterval) {
            clearInterval(predictionInterval)
            predictionInterval = null
          }

          // Send final result
          const strokeCount = clientStrokes.get(message.clientId) || 0
          const predictions = generatePredictions(strokeCount)
          const topPrediction = predictions[0] || { label: '-', confidence: 0 }

          const finalResponse: ServerMessage = {
            clientId: message.clientId,
            type: 'final',
            data: topPrediction
          }
          ws.send(JSON.stringify(finalResponse))
          break

        case 'clear':
          // Reset stroke count
          clientStrokes.set(message.clientId, 0)

          // Stop prediction stream
          if (predictionInterval) {
            clearInterval(predictionInterval)
            predictionInterval = null
          }

          // Send empty predictions
          const clearResponse: ServerMessage = {
            clientId: message.clientId,
            type: 'predictions',
            data: []
          }
          ws.send(JSON.stringify(clearResponse))
          break
      }
    } catch (err) {
      console.error('Failed to parse message:', err)
    }
  })

  ws.on('close', () => {
    console.log('Client disconnected')
    if (predictionInterval) {
      clearInterval(predictionInterval)
    }
    if (currentClientId) {
      clientStrokes.delete(currentClientId)
    }
  })
})
