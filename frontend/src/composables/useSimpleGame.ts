import { ref, computed } from 'vue'
import { predictDigit } from '@/services/api'
import type { SimpleGameState, Point, Stroke, PredictResponse } from '@/types'

export function useSimpleGame() {
  const gameState = ref<SimpleGameState>('idle')
  const strokes = ref<Stroke[]>([])
  const result = ref<PredictResponse | null>(null)
  const error = ref<string | null>(null)

  const canSubmit = computed(() => strokes.value.length > 0)
  const isLoading = computed(() => gameState.value === 'loading')
  const hasResult = computed(() => result.value !== null)
  const hasError = computed(() => error.value !== null)

  function startDrawing() {
    gameState.value = 'drawing'
    result.value = null
    error.value = null
  }

  function addStroke(stroke: Stroke) {
    if (gameState.value === 'idle') {
      startDrawing()
    }
    strokes.value.push(stroke)
  }

  function clearCanvas() {
    strokes.value = []
  }

  async function submitDrawing() {
    if (!canSubmit.value || gameState.value === 'loading') {
      return
    }

    gameState.value = 'loading'
    error.value = null

    try {
      const points: Point[] = strokes.value.flat()
      const response = await predictDigit(points)
      result.value = response
    } catch (err) {
      error.value = (err as Error).message
    } finally {
      gameState.value = 'result'
    }
  }

  function newGame() {
    gameState.value = 'idle'
    strokes.value = []
    result.value = null
    error.value = null
  }

  function retry() {
    gameState.value = 'drawing'
    error.value = null
    result.value = null
  }

  return {
    // State
    gameState,
    strokes,
    result,
    error,
    // Computed
    canSubmit,
    isLoading,
    hasResult,
    hasError,
    // Actions
    startDrawing,
    addStroke,
    clearCanvas,
    submitDrawing,
    newGame,
    retry
  }
}
