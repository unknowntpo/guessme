import { ulid } from 'ulid'
import type { Point, Prediction, ClientMessage, ServerMessage } from '@/types'

const CLIENT_TOKEN_KEY = 'clientToken'

export function getClientId(): string {
  let clientId = localStorage.getItem(CLIENT_TOKEN_KEY)
  if (!clientId) {
    clientId = ulid()
    localStorage.setItem(CLIENT_TOKEN_KEY, clientId)
  }
  return clientId
}

export class WebSocketClient {
  private ws: WebSocket | null = null
  private clientId: string

  onPredictions: ((predictions: Prediction[]) => void) | null = null
  onFinal: ((result: Prediction) => void) | null = null
  onConnect: (() => void) | null = null
  onDisconnect: (() => void) | null = null

  constructor(url: string) {
    this.clientId = getClientId()
    this.connect(url)
  }

  private connect(url: string) {
    this.ws = new WebSocket(url)

    this.ws.onopen = () => {
      this.onConnect?.()
    }

    this.ws.onmessage = (event) => {
      try {
        const message: ServerMessage = JSON.parse(event.data)

        // Ignore messages for other clients
        if (message.clientId !== this.clientId) {
          return
        }

        if (message.type === 'predictions') {
          this.onPredictions?.(message.data)
        } else if (message.type === 'final') {
          this.onFinal?.(message.data)
        }
      } catch (err) {
        console.error('Failed to parse WebSocket message:', err)
      }
    }

    this.ws.onclose = () => {
      this.onDisconnect?.()
    }

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
  }

  private send(message: ClientMessage) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message))
    }
  }

  sendStroke(points: Point[]) {
    this.send({
      clientId: this.clientId,
      type: 'stroke',
      data: { points }
    })
  }

  sendSubmit() {
    this.send({
      clientId: this.clientId,
      type: 'submit'
    })
  }

  sendClear() {
    this.send({
      clientId: this.clientId,
      type: 'clear'
    })
  }

  disconnect() {
    this.ws?.close()
    this.ws = null
  }

  get isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN
  }
}
