<template>
  <div v-if="visible" class="modal-overlay">
    <div class="modal-body" style="max-width: 440px;">
      <h3 style="margin-bottom: 8px; font-size: 18px;">Соберите картинку</h3>
      <p style="color: var(--text-secondary); font-size: 13px; margin-bottom: 20px;">
        Кликните на два фрагмента чтобы поменять их местами
      </p>

      <!-- Сетка 2x2 -->
      <div class="puzzle-grid">
        <div
          v-for="(piece, idx) in slots"
          :key="idx"
          class="puzzle-cell"
          :class="{
            selected: selectedIndex === idx,
            correct: piece === idx + 1,
          }"
          @click="handleClick(idx)"
        >
          <img :src="getImageSrc(piece)" draggable="false" />
        </div>
      </div>

      <p v-if="error" style="color: var(--error); font-size: 13px; margin-top: 12px;">{{ error }}</p>

      <div style="display: flex; gap: 10px; margin-top: 24px; justify-content: flex-end;">
        <button class="btn btn-outline" @click="$emit('cancel')">Отмена</button>
        <button class="btn btn-primary" @click="submit">Подтвердить</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { verifyCaptcha, getImageSrc } from '@/services/captcha'

const props = defineProps<{
  visible: boolean
  initialSlots: number[] // перемешанный порядок [3,1,4,2]
}>()

const emit = defineEmits<{
  cancel: []
  success: []
  fail: []
}>()

const slots = ref<number[]>([])
const selectedIndex = ref<number | null>(null)
const error = ref('')

// Сброс при открытии
watch(() => props.visible, (val) => {
  if (val) {
    slots.value = [...props.initialSlots]
    selectedIndex.value = null
    error.value = ''
  }
})

function handleClick(idx: number) {
  if (selectedIndex.value === null) {
    // Первый клик — выбираем
    selectedIndex.value = idx
  } else if (selectedIndex.value === idx) {
    // Кликнули на тот же — снимаем выделение
    selectedIndex.value = null
  } else {
    // Второй клик — меняем местами
    const a = selectedIndex.value
    const b = idx
    const temp = slots.value[a]
    slots.value[a] = slots.value[b]
    slots.value[b] = temp
    selectedIndex.value = null
    error.value = ''
  }
}

function submit() {
  if (verifyCaptcha(slots.value)) {
    emit('success')
  } else {
    error.value = 'Картинка собрана неправильно'
    emit('fail')
  }
}
</script>

<style scoped>
.puzzle-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
  max-width: 320px;
  margin: 0 auto;
  background: var(--bg-surface-3);
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid var(--border);
}

.puzzle-cell {
  aspect-ratio: 1;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: outline 0.15s, transform 0.15s;
  outline: 3px solid transparent;
  outline-offset: -3px;
}

.puzzle-cell img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  pointer-events: none;
}

.puzzle-cell:hover {
  outline-color: rgba(187, 134, 252, 0.4);
}

.puzzle-cell.selected {
  outline-color: var(--accent);
  transform: scale(0.94);
}

.puzzle-cell.correct {
  /* можно убрать подсказку если не нужна */
}
</style>
