// Point on canvas
export interface Point {
  x: number
  y: number
}

// Single stroke (array of points)
export type Stroke = Point[]

// ML prediction result
export interface Prediction {
  label: string
  confidence: number
}

// Game state
export type GameState = 'idle' | 'playing' | 'gameOver'

// WebSocket message types
export interface ClientMessage {
  clientId: string
  type: 'stroke' | 'submit' | 'clear'
  data?: {
    points?: Point[]
  }
}

export interface ServerPredictionsMessage {
  clientId: string
  type: 'predictions'
  data: Prediction[]
}

export interface ServerFinalMessage {
  clientId: string
  type: 'final'
  data: Prediction
}

export type ServerMessage = ServerPredictionsMessage | ServerFinalMessage
