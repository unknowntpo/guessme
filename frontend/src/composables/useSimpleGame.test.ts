import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { useSimpleGame } from '@/composables/useSimpleGame'
import * as api from '@/services/api'
import type { Point } from '@/types'

vi.mock('@/services/api', () => ({
  predictDigit: vi.fn(),
  ApiError: class ApiError extends Error {
    constructor(message: string, public status?: number) {
      super(message)
      this.name = 'ApiError'
    }
  }
}))

describe('useSimpleGame', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('initial state', () => {
    it('should start in idle state', () => {
      const game = useSimpleGame()
      expect(game.gameState.value).toBe('idle')
    })

    it('should have empty strokes', () => {
      const game = useSimpleGame()
      expect(game.strokes.value).toEqual([])
    })

    it('should have null result', () => {
      const game = useSimpleGame()
      expect(game.result.value).toBeNull()
    })

    it('should have null error', () => {
      const game = useSimpleGame()
      expect(game.error.value).toBeNull()
    })

    it('should not allow submit when no strokes', () => {
      const game = useSimpleGame()
      expect(game.canSubmit.value).toBe(false)
    })
  })

  describe('startDrawing', () => {
    it('should transition to drawing state', () => {
      const game = useSimpleGame()
      game.startDrawing()
      expect(game.gameState.value).toBe('drawing')
    })

    it('should clear previous result', () => {
      const game = useSimpleGame()
      game.result.value = { digit: 7, confidence: 87 }
      game.startDrawing()
      expect(game.result.value).toBeNull()
    })

    it('should clear previous error', () => {
      const game = useSimpleGame()
      game.error.value = 'Previous error'
      game.startDrawing()
      expect(game.error.value).toBeNull()
    })
  })

  describe('addStroke', () => {
    it('should add stroke to strokes array', () => {
      const game = useSimpleGame()
      game.startDrawing()
      const stroke: Point[] = [{ x: 10, y: 10 }, { x: 20, y: 20 }]
      game.addStroke(stroke)
      expect(game.strokes.value).toEqual([stroke])
    })

    it('should allow submit after adding stroke', () => {
      const game = useSimpleGame()
      game.startDrawing()
      game.addStroke([{ x: 10, y: 10 }])
      expect(game.canSubmit.value).toBe(true)
    })

    it('should auto-transition to drawing if in idle', () => {
      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }])
      expect(game.gameState.value).toBe('drawing')
    })
  })

  describe('clearCanvas', () => {
    it('should clear strokes', () => {
      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }])
      game.clearCanvas()
      expect(game.strokes.value).toEqual([])
    })

    it('should not allow submit after clear', () => {
      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }])
      game.clearCanvas()
      expect(game.canSubmit.value).toBe(false)
    })

    it('should stay in drawing state', () => {
      const game = useSimpleGame()
      game.startDrawing()
      game.addStroke([{ x: 10, y: 10 }])
      game.clearCanvas()
      expect(game.gameState.value).toBe('drawing')
    })
  })

  describe('submitDrawing', () => {
    it('should transition to loading state', async () => {
      vi.mocked(api.predictDigit).mockImplementation(() => new Promise(() => {}))

      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }])
      game.submitDrawing()

      expect(game.gameState.value).toBe('loading')
    })

    it('should call API with all strokes flattened to points', async () => {
      vi.mocked(api.predictDigit).mockResolvedValueOnce({ digit: 7, confidence: 87 })

      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }, { x: 20, y: 20 }])
      game.addStroke([{ x: 30, y: 30 }])
      await game.submitDrawing()

      expect(api.predictDigit).toHaveBeenCalledWith([
        { x: 10, y: 10 },
        { x: 20, y: 20 },
        { x: 30, y: 30 }
      ])
    })

    it('should transition to result state on success', async () => {
      vi.mocked(api.predictDigit).mockResolvedValueOnce({ digit: 7, confidence: 87 })

      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }])
      await game.submitDrawing()

      expect(game.gameState.value).toBe('result')
    })

    it('should store result on success', async () => {
      vi.mocked(api.predictDigit).mockResolvedValueOnce({ digit: 7, confidence: 87 })

      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }])
      await game.submitDrawing()

      expect(game.result.value).toEqual({ digit: 7, confidence: 87 })
    })

    it('should store error on API failure', async () => {
      vi.mocked(api.predictDigit).mockRejectedValueOnce(new api.ApiError('API error: 500'))

      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }])
      await game.submitDrawing()

      expect(game.error.value).toBe('API error: 500')
    })

    it('should transition to result state even on error', async () => {
      vi.mocked(api.predictDigit).mockRejectedValueOnce(new api.ApiError('API error: 500'))

      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }])
      await game.submitDrawing()

      expect(game.gameState.value).toBe('result')
    })

    it('should not submit if no strokes', async () => {
      const game = useSimpleGame()
      await game.submitDrawing()

      expect(api.predictDigit).not.toHaveBeenCalled()
      expect(game.gameState.value).toBe('idle')
    })

    it('should not submit if already loading', async () => {
      vi.mocked(api.predictDigit).mockImplementation(() => new Promise(() => {}))

      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }])
      game.submitDrawing()
      await game.submitDrawing()

      expect(api.predictDigit).toHaveBeenCalledTimes(1)
    })
  })

  describe('newGame (tryAgain)', () => {
    it('should reset to idle state', async () => {
      vi.mocked(api.predictDigit).mockResolvedValueOnce({ digit: 7, confidence: 87 })

      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }])
      await game.submitDrawing()
      game.newGame()

      expect(game.gameState.value).toBe('idle')
    })

    it('should clear strokes', async () => {
      vi.mocked(api.predictDigit).mockResolvedValueOnce({ digit: 7, confidence: 87 })

      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }])
      await game.submitDrawing()
      game.newGame()

      expect(game.strokes.value).toEqual([])
    })

    it('should clear result', async () => {
      vi.mocked(api.predictDigit).mockResolvedValueOnce({ digit: 7, confidence: 87 })

      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }])
      await game.submitDrawing()
      game.newGame()

      expect(game.result.value).toBeNull()
    })

    it('should clear error', async () => {
      vi.mocked(api.predictDigit).mockRejectedValueOnce(new api.ApiError('Error'))

      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }])
      await game.submitDrawing()
      game.newGame()

      expect(game.error.value).toBeNull()
    })
  })

  describe('retry', () => {
    it('should transition from result to drawing state', async () => {
      vi.mocked(api.predictDigit).mockRejectedValueOnce(new api.ApiError('Network error'))

      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }])
      await game.submitDrawing()

      expect(game.gameState.value).toBe('result')
      game.retry()
      expect(game.gameState.value).toBe('drawing')
    })

    it('should clear error', async () => {
      vi.mocked(api.predictDigit).mockRejectedValueOnce(new api.ApiError('Network error'))

      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }])
      await game.submitDrawing()

      expect(game.error.value).toBe('Network error')
      game.retry()
      expect(game.error.value).toBeNull()
    })

    it('should keep strokes intact', async () => {
      vi.mocked(api.predictDigit).mockRejectedValueOnce(new api.ApiError('Network error'))

      const game = useSimpleGame()
      const stroke = [{ x: 10, y: 10 }, { x: 20, y: 20 }]
      game.addStroke(stroke)
      await game.submitDrawing()

      game.retry()
      expect(game.strokes.value).toEqual([stroke])
    })

    it('should clear result', async () => {
      vi.mocked(api.predictDigit).mockResolvedValueOnce({ digit: 7, confidence: 87 })

      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }])
      await game.submitDrawing()

      expect(game.result.value).toEqual({ digit: 7, confidence: 87 })
      game.retry()
      expect(game.result.value).toBeNull()
    })
  })

  describe('computed properties', () => {
    it('isLoading should be true in loading state', () => {
      vi.mocked(api.predictDigit).mockImplementation(() => new Promise(() => {}))

      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }])
      game.submitDrawing()

      expect(game.isLoading.value).toBe(true)
    })

    it('isLoading should be false in other states', () => {
      const game = useSimpleGame()
      expect(game.isLoading.value).toBe(false)
    })

    it('hasResult should be true when result exists', async () => {
      vi.mocked(api.predictDigit).mockResolvedValueOnce({ digit: 7, confidence: 87 })

      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }])
      await game.submitDrawing()

      expect(game.hasResult.value).toBe(true)
    })

    it('hasError should be true when error exists', async () => {
      vi.mocked(api.predictDigit).mockRejectedValueOnce(new api.ApiError('Error'))

      const game = useSimpleGame()
      game.addStroke([{ x: 10, y: 10 }])
      await game.submitDrawing()

      expect(game.hasError.value).toBe(true)
    })
  })
})
