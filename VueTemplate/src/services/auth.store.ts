import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface User {
  id: number
  username: string
  role: 'admin' | 'user'
}

export const useAuthStore = defineStore('auth', () => {
  // ===== State =====
  const user = ref<User | null>(loadUser())
  const accessToken = ref<string | null>(localStorage.getItem('access_token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'))

  // ===== Getters =====
  const isAuthenticated = computed(() => !!accessToken.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const role = computed(() => user.value?.role ?? 'user')

  // ===== Actions =====
  function setTokens(access: string, refresh: string) {
    accessToken.value = access
    refreshToken.value = refresh
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
  }

  function setUser(u: User) {
    user.value = u
    localStorage.setItem('user', JSON.stringify(u))
  }

  function login(access: string, refresh: string, u: User) {
    setTokens(access, refresh)
    setUser(u)
  }

  function logout() {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  }

  function loadUser(): User | null {
    const raw = localStorage.getItem('user')
    if (!raw) return null
    try { return JSON.parse(raw) } catch { return null }
  }

  return {
    user, accessToken, refreshToken,
    isAuthenticated, isAdmin, role,
    setTokens, setUser, login, logout
  }
})
