<script setup lang="ts">
defineProps<{
  gameOver: boolean
}>()

defineEmits<{
  clear: []
  submit: []
  newGame: []
}>()
</script>

<template>
  <div class="flex gap-4 flex-wrap justify-center">
    <template v-if="!gameOver">
      <button
        class="btn btn-outline"
        data-testid="clear-btn"
        @click="$emit('clear')"
      >
        Clear
      </button>
      <button
        class="btn btn-primary"
        data-testid="submit-btn"
        @click="$emit('submit')"
      >
        Submit
      </button>
    </template>
    <template v-else>
      <button
        class="btn btn-success"
        data-testid="new-game-btn"
        @click="$emit('newGame')"
      >
        New Game
      </button>
    </template>
  </div>
</template>
