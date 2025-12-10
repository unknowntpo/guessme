import { ref, watch, type Ref } from 'vue'
import type { Point, Stroke } from '@/types'

interface UseCanvasOptions {
  onStroke?: (stroke: Stroke) => void
  strokeColor?: string
  strokeWidth?: number
  backgroundColor?: string
}

export function useCanvas(
  canvasRef: Ref<HTMLCanvasElement | null>,
  options: UseCanvasOptions = {}
) {
  const {
    onStroke,
    strokeColor = '#383838',
    strokeWidth = 3,
    backgroundColor = '#FFFFFF'
  } = options

  const strokes = ref<Stroke[]>([])
  const isDrawing = ref(false)
  const disabled = ref(false)
  let currentStroke: Point[] = []
  let ctx: CanvasRenderingContext2D | null = null

  function initCanvas() {
    const canvas = canvasRef.value
    if (!canvas) return

    ctx = canvas.getContext('2d')
    if (!ctx) return

    ctx.fillStyle = backgroundColor
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    ctx.strokeStyle = strokeColor
    ctx.lineWidth = strokeWidth
    ctx.lineCap = 'round'
    ctx.lineJoin = 'round'
  }

  function getPos(e: MouseEvent | TouchEvent): Point {
    const canvas = canvasRef.value
    if (!canvas) return { x: 0, y: 0 }

    const rect = canvas.getBoundingClientRect()
    let clientX: number, clientY: number

    if ('touches' in e && e.touches.length > 0) {
      clientX = e.touches[0]!.clientX
      clientY = e.touches[0]!.clientY
    } else if ('clientX' in e) {
      clientX = e.clientX
      clientY = e.clientY
    } else {
      return { x: 0, y: 0 }
    }

    // Scale coordinates to canvas internal size
    const scaleX = canvas.width / rect.width
    const scaleY = canvas.height / rect.height
    const x = (clientX - rect.left) * scaleX
    const y = (clientY - rect.top) * scaleY

    return { x, y }
  }

  function startDrawing(e: MouseEvent | TouchEvent) {
    if (disabled.value) return
    e.preventDefault()

    isDrawing.value = true
    currentStroke = []
    const pos = getPos(e)
    currentStroke.push(pos)

    if (ctx) {
      ctx.beginPath()
      ctx.moveTo(pos.x, pos.y)
    }
  }

  function draw(e: MouseEvent | TouchEvent) {
    if (!isDrawing.value || disabled.value) return
    e.preventDefault()

    const pos = getPos(e)
    currentStroke.push(pos)

    if (ctx) {
      ctx.lineTo(pos.x, pos.y)
      ctx.stroke()
    }
  }

  function stopDrawing(e: MouseEvent | TouchEvent) {
    if (!isDrawing.value || disabled.value) return
    e.preventDefault()

    isDrawing.value = false

    if (currentStroke.length > 0) {
      strokes.value.push([...currentStroke])
      onStroke?.(currentStroke)
    }
    currentStroke = []
  }

  function clearCanvas() {
    strokes.value = []
    currentStroke = []
    initCanvas()
  }

  function setDisabled(value: boolean) {
    disabled.value = value
  }

  // Initialize when canvas ref is set
  watch(canvasRef, (canvas) => {
    if (canvas) {
      initCanvas()
    }
  }, { immediate: true })

  return {
    strokes,
    isDrawing,
    startDrawing,
    draw,
    stopDrawing,
    clearCanvas,
    setDisabled
  }
}
