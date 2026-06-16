<template>
  <div style="padding: 32px;">
    <DataTable
      title="Пользователи"
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
      <!-- Пример кастомной ячейки -->
      <template #cell-role="{ value }">
        <span class="badge" :class="value === 'admin' ? 'badge-admin' : 'badge-user'">{{ value }}</span>
      </template>
    </DataTable>

    <!-- Модалка создания/редактирования -->
    <FormModal
      :visible="showModal"
      :title="editingItem ? 'Редактировать' : 'Создать'"
      :loading="saving"
      @close="showModal = false"
      @submit="handleSave"
    >
      <div style="display: flex; flex-direction: column; gap: 12px;">
        <input v-model="formData.name" class="input" placeholder="Имя" />
        <input v-model="formData.email" class="input" placeholder="Email" />
        <select v-model="formData.role" class="input">
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>
      </div>
    </FormModal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/services/auth.store'
import DataTable from '@/components/DataTable.vue'
import FormModal from '@/components/FormModal.vue'
// import * as api from '@/api/example.api'  // Раскомментируй для реального API

const auth = useAuthStore()

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'name', label: 'Имя' },
  { key: 'email', label: 'Email' },
  { key: 'role', label: 'Роль' },
]

// ===== Моковые данные (замени на API) =====
const rows = ref([
  { id: 1, name: 'Иван', email: 'ivan@mail.ru', role: 'admin' },
  { id: 2, name: 'Мария', email: 'maria@mail.ru', role: 'user' },
  { id: 3, name: 'Пётр', email: 'petr@mail.ru', role: 'user' },
])
const loading = ref(false)
const showModal = ref(false)
const saving = ref(false)
const editingItem = ref<any>(null)
const formData = reactive({ name: '', email: '', role: 'user' })

// ===== Загрузка данных =====
onMounted(async () => {
  // loading.value = true
  // try {
  //   const res = await api.getAll()
  //   rows.value = res.data
  // } catch (e) { console.error(e) }
  // loading.value = false
})

// ===== CRUD =====
function openCreate() {
  editingItem.value = null
  formData.name = ''
  formData.email = ''
  formData.role = 'user'
  showModal.value = true
}

function openEdit(row: any) {
  editingItem.value = row
  formData.name = row.name
  formData.email = row.email
  formData.role = row.role
  showModal.value = true
}

async function handleSave() {
  saving.value = true
  try {
    if (editingItem.value) {
      // await api.update(editingItem.value.id, { ...formData })
      Object.assign(editingItem.value, { ...formData })
    } else {
      // const res = await api.create({ ...formData })
      // rows.value.push(res.data)
      rows.value.push({ id: Date.now(), ...formData })
    }
    showModal.value = false
  } catch (e) { console.error(e) }
  saving.value = false
}

async function handleDelete(row: any) {
  if (!confirm('Удалить запись?')) return
  try {
    // await api.remove(row.id)
    rows.value = rows.value.filter(r => r.id !== row.id)
  } catch (e) { console.error(e) }
}
</script>
