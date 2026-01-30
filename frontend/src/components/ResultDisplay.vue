<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  digit: number | null
  confidence: number
  visible: boolean
  error?: string | null
}>()

defineEmits<{
  tryAgain: []
}>()

const confidenceColor = computed(() => {
  if (props.confidence >= 70) return 'text-success'
  if (props.confidence >= 40) return 'text-accent'
  return 'text-error'
})

const digitColor = computed(() => {
  if (props.confidence >= 70) return 'text-success'
  if (props.confidence >= 40) return 'text-accent'
  return 'text-error'
})
</script>

<template>
  <div
    v-if="visible"
    data-testid="result-card"
    class="p-5 md:p-6 bg-white border-2 border-text shadow-offset-md w-[calc(100%-12px)] max-w-[400px] fade-in"
  >
    <!-- Error State -->
    <template v-if="error">
      <div class="flex flex-col items-center gap-4 py-3">
        <span class="font-mono text-sm uppercase text-error tracking-wide text-center">
          {{ error }}
        </span>
      </div>
    </template>

    <!-- Success State -->
    <template v-else>
      <!-- Digit result -->
      <div class="flex justify-between items-center py-3 border-b border-text">
        <span class="font-mono text-sm uppercase text-gray tracking-wide">Digit</span>
        <span
          data-testid="digit-value"
          class="font-mono text-5xl uppercase tracking-wide"
          :class="digitColor"
        >
          {{ digit }}
        </span>
      </div>

      <!-- Confidence with progress bar -->
      <div class="flex justify-between items-center py-3">
        <span class="font-mono text-sm uppercase text-gray tracking-wide">Confidence</span>
        <div class="flex items-center gap-3">
          <div class="w-[100px] h-2 bg-white border border-text overflow-hidden">
            <div
              data-testid="confidence-bar"
              class="h-full bg-primary transition-[width] duration-200 ease-out"
              :style="{ width: `${confidence}%` }"
            />
          </div>
          <span
            data-testid="confidence-value"
            class="font-mono text-2xl"
            :class="confidenceColor"
          >
            {{ confidence }}%
          </span>
        </div>
      </div>
    </template>

    <!-- Try Again button -->
    <button
      data-testid="try-again-btn"
      class="btn btn-success w-full mt-4"
      @click="$emit('tryAgain')"
    >
      Try Again
    </button>
  </div>
</template>
