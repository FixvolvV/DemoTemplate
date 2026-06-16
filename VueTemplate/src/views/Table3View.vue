<template>
  <div style="padding: 32px;">
    <DataTable
      title="Заказы"
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
      <template #cell-status="{ value }">
        <span :style="{ color: value === 'Выполнен' ? 'var(--success)' : value === 'Отменён' ? 'var(--error)' : 'var(--accent)' }">
          {{ value }}
        </span>
      </template>
    </DataTable>

    <FormModal
      :visible="showModal"
      :title="editingItem ? 'Редактировать заказ' : 'Создать заказ'"
      :loading="saving"
      @close="showModal = false"
      @submit="handleSave"
    >
      <div style="display: flex; flex-direction: column; gap: 12px;">
        <input v-model="formData.client" class="input" placeholder="Клиент" />
        <input v-model="formData.product" class="input" placeholder="Товар" />
        <select v-model="formData.status" class="input">
          <option value="В работе">В работе</option>
          <option value="Выполнен">Выполнен</option>
          <option value="Отменён">Отменён</option>
        </select>
      </div>
    </FormModal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/services/auth.store'
import DataTable from '@/components/DataTable.vue'
import FormModal from '@/components/FormModal.vue'

const auth = useAuthStore()

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'client', label: 'Клиент' },
  { key: 'product', label: 'Товар' },
  { key: 'status', label: 'Статус' },
]

const rows = ref([
  { id: 1, client: 'ООО Рога', product: 'Ноутбук', status: 'Выполнен' },
  { id: 2, client: 'ИП Иванов', product: 'Монитор', status: 'В работе' },
  { id: 3, client: 'ООО Копыта', product: 'Клавиатура', status: 'Отменён' },
])
const loading = ref(false)
const showModal = ref(false)
const saving = ref(false)
const editingItem = ref<any>(null)
const formData = reactive({ client: '', product: '', status: 'В работе' })

function openCreate() {
  editingItem.value = null
  formData.client = ''
  formData.product = ''
  formData.status = 'В работе'
  showModal.value = true
}

function openEdit(row: any) {
  editingItem.value = row
  formData.client = row.client
  formData.product = row.product
  formData.status = row.status
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
