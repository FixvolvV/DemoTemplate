<template>
  <div style="padding: 32px;">
    <h1 style="font-size: 24px; margin-bottom: 8px;">Добро пожаловать, {{ auth.user?.username }}</h1>
    <p style="color: var(--text-secondary); margin-bottom: 24px;">
      Роль: <span class="badge" :class="auth.isAdmin ? 'badge-admin' : 'badge-user'">{{ auth.role }}</span>
    </p>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; max-width: 800px;">
      <router-link to="/table1" class="card" style="text-decoration: none; color: var(--text-primary); transition: border-color 0.2s;" onmouseover="this.style.borderColor='var(--accent)'" onmouseout="this.style.borderColor='var(--border)'">
        <h3 style="color: var(--accent); margin-bottom: 8px;">Таблица 1</h3>
        <p style="color: var(--text-secondary); font-size: 13px;">Пример работы с данными</p>
      </router-link>

      <router-link to="/table2" class="card" style="text-decoration: none; color: var(--text-primary); transition: border-color 0.2s;" onmouseover="this.style.borderColor='var(--accent)'" onmouseout="this.style.borderColor='var(--border)'">
        <h3 style="color: var(--accent); margin-bottom: 8px;">Таблица 2</h3>
        <p style="color: var(--text-secondary); font-size: 13px;">Пример работы с данными</p>
      </router-link>

      <router-link to="/table3" class="card" style="text-decoration: none; color: var(--text-primary); transition: border-color 0.2s;" onmouseover="this.style.borderColor='var(--accent)'" onmouseout="this.style.borderColor='var(--border)'">
        <h3 style="color: var(--accent); margin-bottom: 8px;">Таблица 3</h3>
        <p style="color: var(--text-secondary); font-size: 13px;">Пример работы с данными</p>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/services/auth.store'
const auth = useAuthStore()
</script>
