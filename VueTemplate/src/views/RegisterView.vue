<template>
  <div style="min-height: 100vh; display: flex; align-items: center; justify-content: center;">
    <div class="card" style="width: 100%; max-width: 400px;">
      <h2 style="margin-bottom: 24px; text-align: center; color: var(--accent);">Регистрация</h2>

      <div style="display: flex; flex-direction: column; gap: 14px;">
        <input v-model="form.username" class="input" placeholder="Логин" @keyup.enter="handleRegister" />
        <input v-model="form.password" class="input" type="password" placeholder="Пароль" @keyup.enter="handleRegister" />
        <input v-model="form.confirmPassword" class="input" type="password" placeholder="Подтвердите пароль" @keyup.enter="handleRegister" />

        <p v-if="error" style="color: var(--error); font-size: 13px;">{{ error }}</p>

        <button class="btn btn-primary" @click="handleRegister" :disabled="loading" style="width: 100%;">
          {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
        </button>

        <p style="text-align: center; color: var(--text-secondary); font-size: 13px;">
          Уже есть аккаунт?
          <router-link to="/login" style="color: var(--accent);">Войти</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/services/auth.store'
// import { registerApi } from '@/api/auth.api'  // Для реального API

const router = useRouter()
const auth = useAuthStore()

const form = reactive({ username: '', password: '', confirmPassword: '' })
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  if (!form.username || !form.password) {
    error.value = 'Заполните все поля'
    return
  }
  if (form.password !== form.confirmPassword) {
    error.value = 'Пароли не совпадают'
    return
  }
  error.value = ''
  loading.value = true

  try {
    // ===== РЕАЛЬНЫЙ API =====
    // const res = await registerApi({ username: form.username, password: form.password })
    // auth.login(res.data.access_token, res.data.refresh_token, res.data.user)
    
    // ===== ДЕМО (без API) =====
    const fakeUser = {
      id: Date.now(),
      username: form.username,
      role: 'user' as const
    }
    auth.login('fake_access_token', 'fake_refresh_token', fakeUser)
    
    router.push('/')
  } catch (e: any) {
    error.value = e.response?.data?.message || 'Ошибка регистрации'
  } finally {
    loading.value = false
  }
}
</script>
