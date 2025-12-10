<script setup lang="ts">
defineProps<{
  result: string
  confidence: number
  visible?: boolean
}>()
</script>

<template>
  <div
    v-show="visible"
    class="p-5 bg-white border-2 border-text shadow-offset-md w-full max-w-[400px] box-border fade-in md:p-6"
  >
    <div class="flex justify-between items-center py-3 border-b border-text">
      <span class="font-mono text-sm uppercase text-gray tracking-wide">
        Result
      </span>
      <span
        class="font-mono text-2xl uppercase tracking-wide text-success md:text-[28px]"
        data-testid="result-value"
      >
        {{ result }}
      </span>
    </div>
    <div class="flex justify-between items-center py-3">
      <span class="font-mono text-sm uppercase text-gray tracking-wide">
        Confidence
      </span>
      <span
        class="font-mono text-2xl uppercase tracking-wide text-success md:text-[28px]"
        data-testid="result-value"
      >
        {{ confidence }}%
      </span>
    </div>
  </div>
</template>
