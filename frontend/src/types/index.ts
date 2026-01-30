// Point on canvas
export interface Point {
  x: number
  y: number
}

// Single stroke (array of points)
export type Stroke = Point[]

// ML prediction result (WebSocket)
export interface Prediction {
  label: string
  confidence: number
}

// REST API types
export interface PredictRequest {
  points: Point[]
}

export interface PredictResponse {
  digit: number
  confidence: number  // 0-100
}

// Game state (WebSocket mode - deprecated)
export type GameState = 'idle' | 'playing' | 'gameOver'

// Simple game state (REST mode)
export type SimpleGameState = 'idle' | 'drawing' | 'loading' | 'result'

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
