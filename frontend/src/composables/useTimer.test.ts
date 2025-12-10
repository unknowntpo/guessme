import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { useTimer } from './useTimer'

describe('useTimer', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('should initialize with given time', () => {
    const { timeLeft, isWarning, isRunning } = useTimer(30)

    expect(timeLeft.value).toBe(30)
    expect(isWarning.value).toBe(false)
    expect(isRunning.value).toBe(false)
  })

  it('should countdown when started', () => {
    const { timeLeft, start } = useTimer(30)

    start()
    vi.advanceTimersByTime(1000)

    expect(timeLeft.value).toBe(29)

    vi.advanceTimersByTime(5000)
    expect(timeLeft.value).toBe(24)
  })

  it('should set isWarning when time <= 10', () => {
    const { timeLeft, isWarning, start } = useTimer(12)

    start()

    vi.advanceTimersByTime(1000)
    expect(timeLeft.value).toBe(11)
    expect(isWarning.value).toBe(false)

    vi.advanceTimersByTime(1000)
    expect(timeLeft.value).toBe(10)
    expect(isWarning.value).toBe(true)
  })

  it('should call onTimeout when time reaches 0', () => {
    const onTimeout = vi.fn()
    const { start } = useTimer(3, { onTimeout })

    start()

    vi.advanceTimersByTime(3000)

    expect(onTimeout).toHaveBeenCalledTimes(1)
  })

  it('should stop countdown when stopped', () => {
    const { timeLeft, start, stop, isRunning } = useTimer(30)

    start()
    expect(isRunning.value).toBe(true)

    vi.advanceTimersByTime(2000)
    expect(timeLeft.value).toBe(28)

    stop()
    expect(isRunning.value).toBe(false)

    vi.advanceTimersByTime(5000)
    expect(timeLeft.value).toBe(28) // Should not change after stop
  })

  it('should reset timer to initial value', () => {
    const { timeLeft, isWarning, start, reset, isRunning } = useTimer(30)

    start()
    vi.advanceTimersByTime(25000)
    expect(timeLeft.value).toBe(5)
    expect(isWarning.value).toBe(true)

    reset()

    expect(timeLeft.value).toBe(30)
    expect(isWarning.value).toBe(false)
    expect(isRunning.value).toBe(false)
  })

  it('should not go below 0', () => {
    const { timeLeft, start } = useTimer(2)

    start()
    vi.advanceTimersByTime(5000)

    expect(timeLeft.value).toBe(0)
  })
})
