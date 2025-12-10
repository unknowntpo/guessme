import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useGame } from './useGame'
import type { Prediction } from '@/types'

// Mock WebSocket
class MockWebSocket {
  static readonly CONNECTING = 0
  static readonly OPEN = 1
  static readonly CLOSING = 2
  static readonly CLOSED = 3

  static instances: MockWebSocket[] = []

  readonly CONNECTING = 0
  readonly OPEN = 1
  readonly CLOSING = 2
  readonly CLOSED = 3

  readyState = MockWebSocket.CONNECTING
  onopen: (() => void) | null = null
  onmessage: ((event: { data: string }) => void) | null = null
  onclose: (() => void) | null = null
  onerror: ((error: Event) => void) | null = null
  sentMessages: string[] = []

  constructor(public url: string) {
    MockWebSocket.instances.push(this)
    setTimeout(() => {
      this.readyState = MockWebSocket.OPEN
      this.onopen?.()
    }, 0)
  }

  send(data: string) {
    this.sentMessages.push(data)
  }

  close() {
    this.readyState = MockWebSocket.CLOSED
    this.onclose?.()
  }

  simulateMessage(data: object) {
    this.onmessage?.({ data: JSON.stringify(data) })
  }

  static getLastInstance(): MockWebSocket {
    return MockWebSocket.instances[MockWebSocket.instances.length - 1]
  }

  static clearInstances() {
    MockWebSocket.instances = []
  }
}

vi.stubGlobal('WebSocket', MockWebSocket)

describe('useGame', () => {
  beforeEach(() => {
    vi.useFakeTimers()
    localStorage.clear()
    MockWebSocket.clearInstances()
  })

  it('should initialize with idle state', () => {
    const game = useGame()

    expect(game.gameState.value).toBe('idle')
    expect(game.predictions.value).toEqual([])
    expect(game.finalResult.value).toBeNull()
  })

  it('should start game and connect to WebSocket', async () => {
    const game = useGame()

    game.startGame()
    await vi.waitFor(() => {
      expect(MockWebSocket.getLastInstance().readyState).toBe(MockWebSocket.OPEN)
    })

    expect(game.gameState.value).toBe('playing')
    expect(game.isConnected.value).toBe(true)
  })

  it('should handle stroke and send to WebSocket', async () => {
    const game = useGame()
    game.startGame()

    await vi.waitFor(() => {
      expect(MockWebSocket.getLastInstance().readyState).toBe(MockWebSocket.OPEN)
    })

    const mockWs = MockWebSocket.getLastInstance()
    const stroke = [{ x: 10, y: 10 }, { x: 20, y: 20 }]
    game.handleStroke(stroke)

    expect(mockWs.sentMessages).toHaveLength(1)
    const sent = JSON.parse(mockWs.sentMessages[0])
    expect(sent.type).toBe('stroke')
    expect(sent.data.points).toEqual(stroke)
  })

  it('should update predictions when receiving from WebSocket', async () => {
    const game = useGame()
    game.startGame()

    await vi.waitFor(() => {
      expect(MockWebSocket.getLastInstance().readyState).toBe(MockWebSocket.OPEN)
    })

    const mockWs = MockWebSocket.getLastInstance()
    const predictions: Prediction[] = [
      { label: 'Cat', confidence: 87 },
      { label: 'Dog', confidence: 45 }
    ]

    const clientId = localStorage.getItem('clientToken')
    mockWs.simulateMessage({
      clientId,
      type: 'predictions',
      data: predictions
    })

    expect(game.predictions.value).toEqual(predictions)
  })

  it('should handle submit and receive final result', async () => {
    const game = useGame()
    game.startGame()

    await vi.waitFor(() => {
      expect(MockWebSocket.getLastInstance().readyState).toBe(MockWebSocket.OPEN)
    })

    const mockWs = MockWebSocket.getLastInstance()
    game.handleSubmit()

    // Check submit was sent
    expect(mockWs.sentMessages.some(m => JSON.parse(m).type === 'submit')).toBe(true)

    // Simulate final result from server
    const clientId = localStorage.getItem('clientToken')
    mockWs.simulateMessage({
      clientId,
      type: 'final',
      data: { label: 'Cat', confidence: 87 }
    })

    expect(game.gameState.value).toBe('gameOver')
    expect(game.finalResult.value).toEqual({ label: 'Cat', confidence: 87 })
  })

  it('should handle clear and send to WebSocket', async () => {
    const game = useGame()
    game.startGame()

    await vi.waitFor(() => {
      expect(MockWebSocket.getLastInstance().readyState).toBe(MockWebSocket.OPEN)
    })

    const mockWs = MockWebSocket.getLastInstance()
    game.handleClear()

    expect(mockWs.sentMessages.some(m => JSON.parse(m).type === 'clear')).toBe(true)
    expect(game.predictions.value).toEqual([])
  })

  it('should reset game on newGame', async () => {
    const game = useGame()
    game.startGame()

    await vi.waitFor(() => {
      expect(MockWebSocket.getLastInstance().readyState).toBe(MockWebSocket.OPEN)
    })

    // Simulate game over
    const mockWs = MockWebSocket.getLastInstance()
    game.handleSubmit()
    const clientId = localStorage.getItem('clientToken')
    mockWs.simulateMessage({
      clientId,
      type: 'final',
      data: { label: 'Cat', confidence: 87 }
    })

    expect(game.gameState.value).toBe('gameOver')

    // Start new game
    game.newGame()

    expect(game.gameState.value).toBe('playing')
    expect(game.predictions.value).toEqual([])
    expect(game.finalResult.value).toBeNull()
  })
})
