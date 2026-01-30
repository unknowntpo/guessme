<script setup lang="ts">
import { ref } from 'vue'
import DrawingCanvas from './components/DrawingCanvas.vue'
import SimpleGameControls from './components/SimpleGameControls.vue'
import ResultDisplay from './components/ResultDisplay.vue'
import { useSimpleGame } from './composables/useSimpleGame'
import type { Stroke } from './types'

const canvasRef = ref<InstanceType<typeof DrawingCanvas> | null>(null)

const {
  gameState,
  result,
  error,
  canSubmit,
  isLoading,
  addStroke,
  clearCanvas,
  submitDrawing,
  newGame,
  retry
} = useSimpleGame()

function onStroke(stroke: Stroke) {
  addStroke(stroke)
}

function onClear() {
  canvasRef.value?.clearCanvas()
  clearCanvas()
}

async function onSend() {
  await submitDrawing()
}

function onTryAgain() {
  if (error.value) {
    // On error: keep drawing, just retry
    retry()
  } else {
    // On success: clear canvas for new game
    canvasRef.value?.clearCanvas()
    newGame()
  }
}

const isCanvasDisabled = () => gameState.value === 'loading' || gameState.value === 'result'
</script>

<template>
  <div class="min-h-screen bg-bg text-text">
    <!-- Header -->
    <header class="py-6 border-b-2 border-text">
      <div class="max-w-[1302px] mx-auto px-6 md:px-[30px]">
        <h1 class="font-mono font-normal text-[30px] leading-[140%] uppercase tracking-wide md:text-[56px] md:leading-[120%] lg:text-[80px]">
          Guessme
        </h1>
      </div>
    </header>

    <!-- Main Game Area -->
    <main class="max-w-[1302px] mx-auto px-6 py-6 flex flex-col items-center gap-5 md:py-12 md:gap-8 md:px-[30px]">
      <!-- Prompt Section -->
      <div class="text-center">
        <p class="font-mono text-sm uppercase text-gray mb-2 tracking-wide">
          Draw a digit (0-9)
        </p>
        <p class="font-mono text-sm uppercase tracking-wide text-text max-w-[400px] leading-[160%] md:text-base">
          Draw any single digit and we'll try to recognize it!
        </p>
      </div>

      <!-- Canvas -->
      <DrawingCanvas
        ref="canvasRef"
        :disabled="isCanvasDisabled()"
        @stroke="onStroke"
      />

      <!-- Controls (when not showing result) -->
      <SimpleGameControls
        v-if="gameState !== 'result'"
        :can-submit="canSubmit"
        :is-loading="isLoading"
        @clear="onClear"
        @send="onSend"
      />

      <!-- Result Display -->
      <ResultDisplay
        :digit="result?.digit ?? null"
        :confidence="result?.confidence ?? 0"
        :visible="gameState === 'result'"
        :error="error"
        @try-again="onTryAgain"
      />
    </main>

    <!-- Footer -->
    <footer class="py-6 border-t-2 border-text text-center">
      <div class="max-w-[1302px] mx-auto px-6 md:px-[30px]">
        <p class="text-sm text-gray">GUESSME - AI Drawing Game</p>
      </div>
    </footer>
  </div>
</template>
