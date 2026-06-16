import api from '@/services/axios'

// ===== Аутентификация =====

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  password: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  user: {
    id: number
    username: string
    role: 'admin' | 'user'
  }
}

// --- Логин (капча проверяется на клиенте, потом вызываем этот метод) ---
export function loginApi(data: LoginRequest) {
  return api.post<AuthResponse>('/auth/login', data)
}

// --- Регистрация ---
export function registerApi(data: RegisterRequest) {
  return api.post<AuthResponse>('/auth/register', data)
}

// --- Обновить токен ---
export function refreshTokenApi(refresh: string) {
  return api.post<AuthResponse>('/auth/refresh', { refresh_token: refresh })
}
