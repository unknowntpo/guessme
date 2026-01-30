import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { predictDigit, ApiError } from './api'
import type { Point } from '@/types'

describe('api service', () => {
  const mockPoints: Point[] = [
    { x: 10, y: 10 },
    { x: 20, y: 20 },
    { x: 30, y: 30 }
  ]

  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn())
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  describe('predictDigit', () => {
    it('should send points to /predict and return result', async () => {
      const mockResponse = { digit: 7, confidence: 87 }
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      } as Response)

      const result = await predictDigit(mockPoints)

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/predict',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ points: mockPoints })
        })
      )
      expect(result).toEqual(mockResponse)
    })

    it('should throw ApiError on non-ok response', async () => {
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error'
      } as Response)

      await expect(predictDigit(mockPoints)).rejects.toThrow(ApiError)
    })

    it('should include status code in ApiError message', async () => {
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found'
      } as Response)

      await expect(predictDigit(mockPoints)).rejects.toThrow('API error: 404 Not Found')
    })

    it('should throw ApiError on network error', async () => {
      vi.mocked(fetch).mockRejectedValueOnce(new TypeError('Failed to fetch'))

      await expect(predictDigit(mockPoints)).rejects.toThrow(ApiError)
    })

    it('should include original error message in ApiError', async () => {
      vi.mocked(fetch).mockRejectedValueOnce(new TypeError('Failed to fetch'))

      await expect(predictDigit(mockPoints)).rejects.toThrow('Network error: Failed to fetch')
    })

    it('should handle empty points array', async () => {
      const mockResponse = { digit: 0, confidence: 10 }
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      } as Response)

      const result = await predictDigit([])

      expect(result).toEqual(mockResponse)
    })
  })
})
