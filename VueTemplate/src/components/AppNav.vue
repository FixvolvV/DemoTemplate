<template>
  <nav class="nav">
    <router-link to="/" style="font-weight: 700; color: var(--accent); font-size: 16px;">Exam</router-link>

    <template v-if="auth.isAuthenticated">
      <router-link to="/">Главная</router-link>
      <router-link to="/table1">Таблица 1</router-link>
      <router-link to="/table2">Таблица 2</router-link>
      <router-link to="/table3">Таблица 3</router-link>
      <!-- ДОБАВЛЯЙ НОВЫЕ ССЫЛКИ ЗДЕСЬ -->

      <div style="margin-left: auto; display: flex; align-items: center; gap: 12px;">
        <span class="badge" :class="auth.isAdmin ? 'badge-admin' : 'badge-user'">
          {{ auth.role }}
        </span>
        <span style="font-size: 13px; color: var(--text-secondary);">{{ auth.user?.username }}</span>
        <button class="btn btn-outline" style="padding: 5px 14px; font-size: 12px;" @click="handleLogout">Выйти</button>
      </div>
    </template>
  </nav>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/services/auth.store'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>
