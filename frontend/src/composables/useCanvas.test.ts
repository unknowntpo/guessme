import { describe, it, expect, vi, beforeEach } from 'vitest'
import { ref } from 'vue'
import { useCanvas } from './useCanvas'

// Mock canvas context
function createMockContext() {
  return {
    fillStyle: '',
    strokeStyle: '',
    lineWidth: 0,
    lineCap: '',
    lineJoin: '',
    fillRect: vi.fn(),
    beginPath: vi.fn(),
    moveTo: vi.fn(),
    lineTo: vi.fn(),
    stroke: vi.fn()
  }
}

function createMockCanvas(ctx: ReturnType<typeof createMockContext>) {
  return {
    width: 400,
    height: 400,
    getContext: vi.fn().mockReturnValue(ctx),
    getBoundingClientRect: vi.fn().mockReturnValue({
      left: 0,
      top: 0,
      width: 400,
      height: 400
    })
  } as unknown as HTMLCanvasElement
}

describe('useCanvas', () => {
  let mockCtx: ReturnType<typeof createMockContext>
  let mockCanvas: HTMLCanvasElement

  beforeEach(() => {
    mockCtx = createMockContext()
    mockCanvas = createMockCanvas(mockCtx)
  })

  it('should initialize canvas on setup', () => {
    const canvasRef = ref<HTMLCanvasElement | null>(mockCanvas)
    useCanvas(canvasRef)

    expect(mockCanvas.getContext).toHaveBeenCalledWith('2d')
    expect(mockCtx.fillRect).toHaveBeenCalledWith(0, 0, 400, 400)
  })

  it('should track strokes', () => {
    const canvasRef = ref<HTMLCanvasElement | null>(mockCanvas)
    const { strokes } = useCanvas(canvasRef)

    expect(strokes.value).toEqual([])
  })

  it('should clear canvas and strokes', () => {
    const canvasRef = ref<HTMLCanvasElement | null>(mockCanvas)
    const { strokes, clearCanvas } = useCanvas(canvasRef)

    // Simulate some strokes
    strokes.value.push([{ x: 10, y: 10 }, { x: 20, y: 20 }])

    clearCanvas()

    expect(strokes.value).toEqual([])
    expect(mockCtx.fillRect).toHaveBeenCalled()
  })

  it('should emit stroke when drawing ends', () => {
    const onStroke = vi.fn()
    const canvasRef = ref<HTMLCanvasElement | null>(mockCanvas)
    const { startDrawing, draw, stopDrawing } = useCanvas(canvasRef, { onStroke })

    // Create mock mouse events
    const startEvent = {
      clientX: 10,
      clientY: 10,
      preventDefault: vi.fn()
    } as unknown as MouseEvent

    const moveEvent = {
      clientX: 50,
      clientY: 50,
      preventDefault: vi.fn()
    } as unknown as MouseEvent

    const endEvent = {
      preventDefault: vi.fn()
    } as unknown as MouseEvent

    startDrawing(startEvent)
    draw(moveEvent)
    stopDrawing(endEvent)

    expect(onStroke).toHaveBeenCalled()
    const strokePoints = onStroke.mock.calls[0][0]
    expect(strokePoints.length).toBeGreaterThan(0)
  })

  it('should not draw when disabled', () => {
    const onStroke = vi.fn()
    const canvasRef = ref<HTMLCanvasElement | null>(mockCanvas)
    const { startDrawing, draw, stopDrawing, setDisabled } = useCanvas(canvasRef, { onStroke })

    setDisabled(true)

    const startEvent = {
      clientX: 10,
      clientY: 10,
      preventDefault: vi.fn()
    } as unknown as MouseEvent

    const moveEvent = {
      clientX: 50,
      clientY: 50,
      preventDefault: vi.fn()
    } as unknown as MouseEvent

    const endEvent = {
      preventDefault: vi.fn()
    } as unknown as MouseEvent

    startDrawing(startEvent)
    draw(moveEvent)
    stopDrawing(endEvent)

    expect(onStroke).not.toHaveBeenCalled()
  })

  it('should handle touch events', () => {
    const onStroke = vi.fn()
    const canvasRef = ref<HTMLCanvasElement | null>(mockCanvas)
    const { startDrawing, draw, stopDrawing } = useCanvas(canvasRef, { onStroke })

    // Create mock touch events
    const startEvent = {
      touches: [{ clientX: 10, clientY: 10 }],
      preventDefault: vi.fn()
    } as unknown as TouchEvent

    const moveEvent = {
      touches: [{ clientX: 50, clientY: 50 }],
      preventDefault: vi.fn()
    } as unknown as TouchEvent

    const endEvent = {
      preventDefault: vi.fn()
    } as unknown as TouchEvent

    startDrawing(startEvent)
    draw(moveEvent)
    stopDrawing(endEvent)

    expect(onStroke).toHaveBeenCalled()
  })

  it('should scale coordinates for responsive canvas', () => {
    // Canvas internal size is 400x400 but displayed at 200x200
    const scaledCanvas = {
      ...mockCanvas,
      getBoundingClientRect: vi.fn().mockReturnValue({
        left: 0,
        top: 0,
        width: 200,
        height: 200
      })
    } as unknown as HTMLCanvasElement

    const onStroke = vi.fn()
    const canvasRef = ref<HTMLCanvasElement | null>(scaledCanvas)
    const { startDrawing, stopDrawing } = useCanvas(canvasRef, { onStroke })

    // Click at display coordinate (100, 100) should map to canvas (200, 200)
    const startEvent = {
      clientX: 100,
      clientY: 100,
      preventDefault: vi.fn()
    } as unknown as MouseEvent

    const endEvent = {
      preventDefault: vi.fn()
    } as unknown as MouseEvent

    startDrawing(startEvent)
    stopDrawing(endEvent)

    expect(onStroke).toHaveBeenCalled()
    const strokePoints = onStroke.mock.calls[0][0]
    expect(strokePoints[0].x).toBe(200)
    expect(strokePoints[0].y).toBe(200)
  })
})
