<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Timer from './components/Timer.vue'
import DrawingCanvas from './components/DrawingCanvas.vue'
import PredictionsList from './components/PredictionsList.vue'
import FinalResult from './components/FinalResult.vue'
import GameControls from './components/GameControls.vue'
import { useTimer } from './composables/useTimer'
import { useGame } from './composables/useGame'
import type { Stroke } from './types'

const INITIAL_TIME = 30

const canvasRef = ref<InstanceType<typeof DrawingCanvas> | null>(null)

const {
  predictions,
  finalResult,
  isGameOver,
  startGame,
  handleStroke,
  handleSubmit,
  handleClear,
  handleTimeout,
  newGame
} = useGame()

const { timeLeft, isWarning, start: startTimer, stop: stopTimer, reset: resetTimer } = useTimer(INITIAL_TIME, {
  onTimeout: handleTimeout
})

function onStroke(stroke: Stroke) {
  handleStroke(stroke)
}

function onClear() {
  canvasRef.value?.clearCanvas()
  handleClear()
}

function onSubmit() {
  stopTimer()
  handleSubmit()
}

function onNewGame() {
  resetTimer()
  canvasRef.value?.clearCanvas()
  newGame()
  startTimer()
}

onMounted(() => {
  startGame()
  startTimer()
})
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
          Draw something like:
        </p>
        <p class="font-mono text-sm uppercase tracking-wide text-text max-w-[400px] leading-[160%] md:text-base">
          Cat, House, Tree, Car, Sun, Flower, Fish, Bird, Apple, Star...
        </p>
      </div>

      <!-- Timer -->
      <Timer :time-left="timeLeft" :is-warning="isWarning" />

      <!-- Canvas -->
      <DrawingCanvas
        ref="canvasRef"
        :disabled="isGameOver"
        @stroke="onStroke"
      />

      <!-- Live Predictions -->
      <PredictionsList
        v-if="!isGameOver"
        :predictions="predictions"
      />

      <!-- Final Result -->
      <FinalResult
        :result="finalResult?.label ?? '-'"
        :confidence="finalResult?.confidence ?? 0"
        :visible="isGameOver"
      />

      <!-- Controls -->
      <GameControls
        :game-over="isGameOver"
        @clear="onClear"
        @submit="onSubmit"
        @new-game="onNewGame"
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
