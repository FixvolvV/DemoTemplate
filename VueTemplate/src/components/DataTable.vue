<template>
  <div class="card" style="padding: 0; overflow: hidden;">
    <!-- Заголовок таблицы -->
    <div style="display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; border-bottom: 1px solid var(--border);">
      <h3 style="font-size: 16px; font-weight: 600;">{{ title }}</h3>
      <button v-if="canCreate" class="btn btn-primary" @click="$emit('create')">+ Добавить</button>
    </div>

    <!-- Таблица -->
    <div style="overflow-x: auto;">
      <table class="data-table">
        <thead>
          <tr>
            <th v-for="col in columns" :key="col.key">{{ col.label }}</th>
            <th v-if="canEdit || canDelete" style="width: 120px;">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td :colspan="totalCols" style="text-align: center; color: var(--text-secondary); padding: 32px;">
              Загрузка...
            </td>
          </tr>
          <tr v-else-if="rows.length === 0">
            <td :colspan="totalCols" style="text-align: center; color: var(--text-secondary); padding: 32px;">
              Нет данных
            </td>
          </tr>
          <tr v-for="row in rows" :key="row.id">
            <td v-for="col in columns" :key="col.key">
              <slot :name="`cell-${col.key}`" :row="row" :value="row[col.key]">
                {{ row[col.key] }}
              </slot>
            </td>
            <td v-if="canEdit || canDelete">
              <div style="display: flex; gap: 6px;">
                <button v-if="canEdit" class="btn btn-outline" style="padding: 5px 12px; font-size: 12px;" @click="$emit('edit', row)">✎</button>
                <button v-if="canDelete" class="btn btn-danger" style="padding: 5px 12px; font-size: 12px;" @click="$emit('delete', row)">✕</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

export interface Column {
  key: string
  label: string
}

const props = defineProps<{
  title: string
  columns: Column[]
  rows: any[]
  loading?: boolean
  canCreate?: boolean
  canEdit?: boolean
  canDelete?: boolean
}>()

defineEmits<{
  create: []
  edit: [row: any]
  delete: [row: any]
}>()

const totalCols = computed(() => {
  let c = props.columns.length
  if (props.canEdit || props.canDelete) c++
  return c
})
</script>
