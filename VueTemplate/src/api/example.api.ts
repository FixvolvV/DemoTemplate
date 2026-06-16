import api from '@/services/axios'

// ===== Пример API для работы с таблицей =====
// Скопируй этот файл и измени под свою таблицу

export interface ExampleItem {
  id: number
  name: string
  description: string
  created_at: string
  [key: string]: any // для дополнительных полей
}

// Получить все записи
export function getAll() {
  return api.get<ExampleItem[]>('/examples')
}

// Получить одну запись
export function getById(id: number) {
  return api.get<ExampleItem>(`/examples/${id}`)
}

// Создать запись
export function create(data: Partial<ExampleItem>) {
  return api.post<ExampleItem>('/examples', data)
}

// Обновить запись
export function update(id: number, data: Partial<ExampleItem>) {
  return api.put<ExampleItem>(`/examples/${id}`, data)
}

// Удалить запись
export function remove(id: number) {
  return api.delete(`/examples/${id}`)
}
