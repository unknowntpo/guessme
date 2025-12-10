import { ref, computed, onUnmounted } from 'vue'
import { WebSocketClient } from '@/services/websocket'
import type { GameState, Prediction, Stroke } from '@/types'

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8080'

export function useGame() {
  const gameState = ref<GameState>('idle')
  const predictions = ref<Prediction[]>([])
  const finalResult = ref<Prediction | null>(null)

  let wsClient: WebSocketClient | null = null

  const isConnected = computed(() => wsClient?.isConnected ?? false)
  const isPlaying = computed(() => gameState.value === 'playing')
  const isGameOver = computed(() => gameState.value === 'gameOver')

  function connect() {
    wsClient = new WebSocketClient(WS_URL)

    wsClient.onPredictions = (preds) => {
      predictions.value = preds
    }

    wsClient.onFinal = (result) => {
      finalResult.value = result
      gameState.value = 'gameOver'
    }
  }

  function disconnect() {
    wsClient?.disconnect()
    wsClient = null
  }

  function startGame() {
    gameState.value = 'playing'
    predictions.value = []
    finalResult.value = null
    connect()
  }

  function handleStroke(stroke: Stroke) {
    if (!isPlaying.value) return
    wsClient?.sendStroke(stroke)
  }

  function handleSubmit() {
    if (!isPlaying.value) return
    wsClient?.sendSubmit()
  }

  function handleClear() {
    if (!isPlaying.value) return
    wsClient?.sendClear()
    predictions.value = []
  }

  function handleTimeout() {
    handleSubmit()
  }

  function newGame() {
    disconnect()
    predictions.value = []
    finalResult.value = null
    startGame()
  }

  onUnmounted(() => {
    disconnect()
  })

  return {
    gameState,
    predictions,
    finalResult,
    isConnected,
    isPlaying,
    isGameOver,
    startGame,
    handleStroke,
    handleSubmit,
    handleClear,
    handleTimeout,
    newGame
  }
}
