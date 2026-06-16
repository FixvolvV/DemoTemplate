<template>
  <div style="min-height: 100vh; display: flex; align-items: center; justify-content: center;">
    <div class="card" style="width: 100%; max-width: 400px;">
      <h2 style="margin-bottom: 24px; text-align: center; color: var(--accent);">Вход в систему</h2>

      <div style="display: flex; flex-direction: column; gap: 14px;">
        <input
          v-model="form.username"
          class="input"
          placeholder="Логин"
          @keyup.enter="handleLogin"
        />
        <input
          v-model="form.password"
          class="input"
          type="password"
          placeholder="Пароль"
          @keyup.enter="handleLogin"
        />

        <p v-if="error" style="color: var(--error); font-size: 13px;">{{ error }}</p>

        <button class="btn btn-primary" @click="handleLogin" :disabled="loading" style="width: 100%;">
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>

        <p style="text-align: center; color: var(--text-secondary); font-size: 13px;">
          Нет аккаунта?
          <router-link to="/register" style="color: var(--accent);">Регистрация</router-link>
        </p>
      </div>
    </div>

    <!-- Капча: собрать картинку 2x2 -->
    <CaptchaModal
      :visible="showCaptcha"
      :initial-slots="captchaSlots"
      @cancel="showCaptcha = false"
      @success="handleCaptchaSuccess"
      @fail="handleCaptchaFail"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/services/auth.store'
import { generateCaptcha } from '@/services/captcha'
import CaptchaModal from '@/components/CaptchaModal.vue'
// import { loginApi } from '@/api/auth.api'

const router = useRouter()
const auth = useAuthStore()

const form = reactive({ username: '', password: '' })
const error = ref('')
const loading = ref(false)

const showCaptcha = ref(false)
const captchaSlots = ref<number[]>([])

function handleLogin() {
  if (!form.username || !form.password) {
    error.value = 'Заполните все поля'
    return
  }
  error.value = ''

  // Генерируем капчу и показываем
  const captcha = generateCaptcha()
  captchaSlots.value = captcha.slots
  showCaptcha.value = true
}

async function handleCaptchaSuccess() {
  loading.value = true
  showCaptcha.value = false

  try {
    // ===== РЕАЛЬНЫЙ API =====
    // const res = await loginApi({ username: form.username, password: form.password })
    // auth.login(res.data.access_token, res.data.refresh_token, res.data.user)

    // ===== ДЕМО (без API) =====
    const fakeUser = {
      id: 1,
      username: form.username,
      role: form.username.toLowerCase() === 'admin' ? 'admin' as const : 'user' as const
    }
    auth.login('fake_access_token', 'fake_refresh_token', fakeUser)

    router.push('/')
  } catch (e: any) {
    error.value = e.response?.data?.message || 'Ошибка входа'
  } finally {
    loading.value = false
  }
}

function handleCaptchaFail() {
  // Можно перегенерировать или оставить — пользователь продолжает собирать
}
</script>
