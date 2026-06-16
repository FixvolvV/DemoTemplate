<template>
  <div style="padding: 32px;">
    <DataTable
      title="Товары"
      :columns="columns"
      :rows="rows"
      :loading="loading"
      :can-create="auth.isAdmin"
      :can-edit="auth.isAdmin"
      :can-delete="auth.isAdmin"
      @create="openCreate"
      @edit="openEdit"
      @delete="handleDelete"
    >
      <template #cell-price="{ value }">
        <span style="color: var(--success);">{{ value }} ₽</span>
      </template>
    </DataTable>

    <FormModal
      :visible="showModal"
      :title="editingItem ? 'Редактировать товар' : 'Добавить товар'"
      :loading="saving"
      @close="showModal = false"
      @submit="handleSave"
    >
      <div style="display: flex; flex-direction: column; gap: 12px;">
        <input v-model="formData.name" class="input" placeholder="Название" />
        <input v-model="formData.category" class="input" placeholder="Категория" />
        <input v-model.number="formData.price" class="input" type="number" placeholder="Цена" />
      </div>
    </FormModal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/services/auth.store'
import DataTable from '@/components/DataTable.vue'
import FormModal from '@/components/FormModal.vue'

const auth = useAuthStore()

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'name', label: 'Название' },
  { key: 'category', label: 'Категория' },
  { key: 'price', label: 'Цена' },
]

const rows = ref([
  { id: 1, name: 'Ноутбук', category: 'Электроника', price: 45000 },
  { id: 2, name: 'Клавиатура', category: 'Периферия', price: 3500 },
  { id: 3, name: 'Монитор', category: 'Электроника', price: 22000 },
])
const loading = ref(false)
const showModal = ref(false)
const saving = ref(false)
const editingItem = ref<any>(null)
const formData = reactive({ name: '', category: '', price: 0 })

function openCreate() {
  editingItem.value = null
  formData.name = ''
  formData.category = ''
  formData.price = 0
  showModal.value = true
}

function openEdit(row: any) {
  editingItem.value = row
  formData.name = row.name
  formData.category = row.category
  formData.price = row.price
  showModal.value = true
}

async function handleSave() {
  saving.value = true
  if (editingItem.value) {
    Object.assign(editingItem.value, { ...formData })
  } else {
    rows.value.push({ id: Date.now(), ...formData })
  }
  showModal.value = false
  saving.value = false
}

async function handleDelete(row: any) {
  if (!confirm('Удалить запись?')) return
  rows.value = rows.value.filter(r => r.id !== row.id)
}
</script>
