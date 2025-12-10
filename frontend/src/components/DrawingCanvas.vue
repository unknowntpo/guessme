<script setup lang="ts">
import { ref, watch } from 'vue'
import { useCanvas } from '@/composables/useCanvas'
import type { Stroke } from '@/types'

const props = defineProps<{
  disabled?: boolean
}>()

const emit = defineEmits<{
  stroke: [stroke: Stroke]
}>()

const canvasRef = ref<HTMLCanvasElement | null>(null)

const { strokes, startDrawing, draw, stopDrawing, clearCanvas, setDisabled } = useCanvas(
  canvasRef,
  {
    onStroke: (stroke) => emit('stroke', stroke)
  }
)

watch(() => props.disabled, (value) => {
  setDisabled(value ?? false)
}, { immediate: true })

defineExpose({
  clearCanvas,
  strokes
})
</script>

<template>
  <div
    class="bg-white border-2 border-text shadow-offset-md p-3 w-full max-w-[424px] box-border md:p-6 md:shadow-offset-lg md:w-auto md:max-w-none"
  >
    <canvas
      ref="canvasRef"
      width="400"
      height="400"
      class="block cursor-crosshair touch-none w-full h-auto max-w-[400px]"
      :class="{ 'opacity-70 pointer-events-none': disabled }"
      @mousedown="startDrawing"
      @mousemove="draw"
      @mouseup="stopDrawing"
      @mouseleave="stopDrawing"
      @touchstart.passive="false"
      @touchmove.passive="false"
      @touchend="stopDrawing"
      v-on="{
        touchstart: startDrawing,
        touchmove: draw
      }"
    />
  </div>
</template>
