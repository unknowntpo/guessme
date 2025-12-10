<script setup lang="ts">
import type { Prediction } from '@/types'

defineProps<{
  predictions: Prediction[]
}>()
</script>

<template>
  <div
    class="p-4 bg-white border-2 border-text shadow-offset-md w-full max-w-[400px] box-border md:p-6 md:w-auto md:min-w-[320px]"
  >
    <p class="font-mono text-xs uppercase text-gray mb-4 tracking-wide text-center">
      AI Predictions (Live)
    </p>

    <div class="flex flex-col gap-2">
      <!-- Placeholder when no predictions -->
      <div
        v-if="predictions.length === 0"
        class="flex items-center gap-3 px-3 py-2 bg-bg border border-text"
        data-testid="prediction-item"
      >
        <span class="font-mono text-sm uppercase tracking-wide flex-1">
          Start drawing...
        </span>
        <div class="w-[60px] h-2 bg-white border border-text overflow-hidden md:w-[100px]">
          <div class="h-full bg-primary" style="width: 0%" data-testid="progress-fill" />
        </div>
        <span class="font-mono text-xs text-gray min-w-[40px] text-right">-</span>
      </div>

      <!-- Prediction items -->
      <div
        v-for="(prediction, index) in predictions"
        :key="prediction.label"
        class="flex items-center gap-3 px-3 py-2 transition-all duration-150"
        :class="[
          index === 0
            ? 'bg-accent border-2 border-text'
            : 'bg-bg border border-text'
        ]"
        data-testid="prediction-item"
      >
        <span class="font-mono text-sm uppercase tracking-wide flex-1">
          {{ prediction.label }}
        </span>
        <div class="w-[60px] h-2 bg-white border border-text overflow-hidden md:w-[100px]">
          <div
            class="h-full transition-[width] duration-200"
            :class="index === 0 ? 'bg-text' : 'bg-primary'"
            :style="{ width: `${prediction.confidence}%` }"
            data-testid="progress-fill"
          />
        </div>
        <span class="font-mono text-xs text-gray min-w-[40px] text-right">
          {{ prediction.confidence }}%
        </span>
      </div>
    </div>
  </div>
</template>
