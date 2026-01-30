<script setup lang="ts">
defineProps<{
  canSubmit: boolean
  isLoading: boolean
}>()

defineEmits<{
  clear: []
  send: []
}>()
</script>

<template>
  <div class="flex gap-4 flex-wrap justify-center">
    <button
      class="btn btn-outline"
      data-testid="clear-btn"
      :disabled="isLoading"
      @click="$emit('clear')"
    >
      Clear
    </button>
    <button
      class="btn btn-primary"
      data-testid="send-btn"
      :disabled="!canSubmit || isLoading"
      @click="$emit('send')"
    >
      {{ isLoading ? 'Sending...' : 'Send' }}
    </button>
  </div>
</template>
