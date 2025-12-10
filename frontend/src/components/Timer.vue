<script setup lang="ts">
defineProps<{
  timeLeft: number
  isWarning: boolean
}>()
</script>

<template>
  <div
    class="inline-flex items-center gap-2 border-2 border-text px-4 py-2 font-mono text-2xl font-normal shadow-offset-sm"
    :class="isWarning ? 'bg-error text-white' : 'bg-accent text-text'"
  >
    <span data-testid="timer-value">{{ timeLeft }}</span>s
  </div>
</template>
