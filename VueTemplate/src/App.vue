<template>
  <AppNav v-if="auth.isAuthenticated" />
  <router-view />
</template>

<script setup lang="ts">
import AppNav from '@/components/AppNav.vue'
import { useAuthStore } from '@/services/auth.store'

const auth = useAuthStore()
</script>
