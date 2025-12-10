import { describe, it, expect, vi, beforeEach } from 'vitest'
import type { Prediction } from '@/types'

// Mock WebSocket class
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
    // Simulate async connection
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

  // Test helper to simulate server message
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

// Apply mock globally
vi.stubGlobal('WebSocket', MockWebSocket)

// Import after mock is set up
import { WebSocketClient, getClientId } from './websocket'

describe('getClientId', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('should generate and store clientId if not exists', () => {
    const id = getClientId()
    expect(id).toBeTruthy()
    expect(id.length).toBe(26) // ULID length
    expect(localStorage.getItem('clientToken')).toBe(id)
  })

  it('should return existing clientId from localStorage', () => {
    const existingId = '01ARZ3NDEKTSV4RRFFQ69G5FAV'
    localStorage.setItem('clientToken', existingId)

    const id = getClientId()
    expect(id).toBe(existingId)
  })
})

describe('WebSocketClient', () => {
  beforeEach(() => {
    localStorage.clear()
    MockWebSocket.clearInstances()
  })

  it('should connect to WebSocket server', async () => {
    const client = new WebSocketClient('ws://localhost:8080')
    const mockWs = MockWebSocket.getLastInstance()

    await vi.waitFor(() => {
      expect(mockWs.readyState).toBe(MockWebSocket.OPEN)
    })

    expect(mockWs.url).toBe('ws://localhost:8080')
    client.disconnect()
  })

  it('should send stroke message with clientId', async () => {
    const client = new WebSocketClient('ws://localhost:8080')
    const mockWs = MockWebSocket.getLastInstance()

    await vi.waitFor(() => {
      expect(mockWs.readyState).toBe(MockWebSocket.OPEN)
    })

    const points = [{ x: 10, y: 20 }, { x: 30, y: 40 }]
    client.sendStroke(points)

    expect(mockWs.sentMessages).toHaveLength(1)
    const sent = JSON.parse(mockWs.sentMessages[0])
    expect(sent.type).toBe('stroke')
    expect(sent.clientId).toBeTruthy()
    expect(sent.data.points).toEqual(points)

    client.disconnect()
  })

  it('should send submit message', async () => {
    const client = new WebSocketClient('ws://localhost:8080')
    const mockWs = MockWebSocket.getLastInstance()

    await vi.waitFor(() => {
      expect(mockWs.readyState).toBe(MockWebSocket.OPEN)
    })

    client.sendSubmit()

    expect(mockWs.sentMessages).toHaveLength(1)
    const sent = JSON.parse(mockWs.sentMessages[0])
    expect(sent.type).toBe('submit')
    expect(sent.clientId).toBeTruthy()

    client.disconnect()
  })

  it('should send clear message', async () => {
    const client = new WebSocketClient('ws://localhost:8080')
    const mockWs = MockWebSocket.getLastInstance()

    await vi.waitFor(() => {
      expect(mockWs.readyState).toBe(MockWebSocket.OPEN)
    })

    client.sendClear()

    expect(mockWs.sentMessages).toHaveLength(1)
    const sent = JSON.parse(mockWs.sentMessages[0])
    expect(sent.type).toBe('clear')
    expect(sent.clientId).toBeTruthy()

    client.disconnect()
  })

  it('should call onPredictions callback when receiving predictions', async () => {
    const onPredictions = vi.fn()
    const client = new WebSocketClient('ws://localhost:8080')
    client.onPredictions = onPredictions
    const mockWs = MockWebSocket.getLastInstance()

    await vi.waitFor(() => {
      expect(mockWs.readyState).toBe(MockWebSocket.OPEN)
    })

    const predictions: Prediction[] = [
      { label: 'Cat', confidence: 87 },
      { label: 'Dog', confidence: 45 }
    ]

    mockWs.simulateMessage({
      clientId: getClientId(),
      type: 'predictions',
      data: predictions
    })

    expect(onPredictions).toHaveBeenCalledWith(predictions)

    client.disconnect()
  })

  it('should call onFinal callback when receiving final result', async () => {
    const onFinal = vi.fn()
    const client = new WebSocketClient('ws://localhost:8080')
    client.onFinal = onFinal
    const mockWs = MockWebSocket.getLastInstance()

    await vi.waitFor(() => {
      expect(mockWs.readyState).toBe(MockWebSocket.OPEN)
    })

    const finalResult: Prediction = { label: 'Cat', confidence: 87 }

    mockWs.simulateMessage({
      clientId: getClientId(),
      type: 'final',
      data: finalResult
    })

    expect(onFinal).toHaveBeenCalledWith(finalResult)

    client.disconnect()
  })

  it('should ignore messages with different clientId', async () => {
    const onPredictions = vi.fn()
    const client = new WebSocketClient('ws://localhost:8080')
    client.onPredictions = onPredictions
    const mockWs = MockWebSocket.getLastInstance()

    await vi.waitFor(() => {
      expect(mockWs.readyState).toBe(MockWebSocket.OPEN)
    })

    mockWs.simulateMessage({
      clientId: 'DIFFERENT_CLIENT_ID',
      type: 'predictions',
      data: []
    })

    expect(onPredictions).not.toHaveBeenCalled()

    client.disconnect()
  })
})
