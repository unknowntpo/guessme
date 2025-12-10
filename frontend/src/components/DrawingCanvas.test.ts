import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import DrawingCanvas from './DrawingCanvas.vue'

// Mock canvas context
const mockContext = {
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

// Mock HTMLCanvasElement.getContext
HTMLCanvasElement.prototype.getContext = vi.fn().mockReturnValue(mockContext)

describe('DrawingCanvas', () => {
  it('should render canvas element', () => {
    const wrapper = mount(DrawingCanvas)

    const canvas = wrapper.find('canvas')
    expect(canvas.exists()).toBe(true)
    expect(canvas.attributes('width')).toBe('400')
    expect(canvas.attributes('height')).toBe('400')
  })

  it('should emit stroke event on drawing', async () => {
    const wrapper = mount(DrawingCanvas)
    const canvas = wrapper.find('canvas')

    // Simulate mouse events
    await canvas.trigger('mousedown', { clientX: 10, clientY: 10 })
    await canvas.trigger('mousemove', { clientX: 50, clientY: 50 })
    await canvas.trigger('mouseup')

    expect(wrapper.emitted('stroke')).toBeTruthy()
  })

  it('should have disabled styling when disabled prop is true', async () => {
    const wrapper = mount(DrawingCanvas, {
      props: { disabled: true }
    })

    const canvas = wrapper.find('canvas')
    expect(canvas.classes()).toContain('opacity-70')
    expect(canvas.classes()).toContain('pointer-events-none')
  })

  it('should expose clearCanvas method', () => {
    const wrapper = mount(DrawingCanvas)

    expect(wrapper.vm.clearCanvas).toBeDefined()
    expect(typeof wrapper.vm.clearCanvas).toBe('function')
  })
})
