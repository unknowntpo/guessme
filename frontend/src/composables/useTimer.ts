import { ref, computed } from 'vue'

interface UseTimerOptions {
  onTimeout?: () => void
  warningThreshold?: number
}

export function useTimer(initialTime: number, options: UseTimerOptions = {}) {
  const { onTimeout, warningThreshold = 10 } = options

  const timeLeft = ref(initialTime)
  const isRunning = ref(false)
  let intervalId: ReturnType<typeof setInterval> | null = null

  const isWarning = computed(() => timeLeft.value <= warningThreshold && timeLeft.value > 0)

  function start() {
    if (isRunning.value) return

    isRunning.value = true
    intervalId = setInterval(() => {
      if (timeLeft.value > 0) {
        timeLeft.value--

        if (timeLeft.value === 0) {
          stop()
          onTimeout?.()
        }
      }
    }, 1000)
  }

  function stop() {
    if (intervalId) {
      clearInterval(intervalId)
      intervalId = null
    }
    isRunning.value = false
  }

  function reset() {
    stop()
    timeLeft.value = initialTime
  }

  return {
    timeLeft,
    isWarning,
    isRunning,
    start,
    stop,
    reset
  }
}
