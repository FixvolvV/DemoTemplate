<template>
  <div v-if="visible" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-body">
      <h3 style="margin-bottom: 20px; font-size: 18px;">{{ title }}</h3>
      <slot />
      <div style="display: flex; gap: 10px; margin-top: 24px; justify-content: flex-end;">
        <button class="btn btn-outline" @click="$emit('close')">Отмена</button>
        <button class="btn btn-primary" @click="$emit('submit')" :disabled="loading">
          {{ loading ? 'Сохранение...' : 'Сохранить' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  visible: boolean
  title: string
  loading?: boolean
}>()

defineEmits<{
  close: []
  submit: []
}>()
</script>
