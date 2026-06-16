import { createRouter, createWebHashHistory } from 'vue-router'
import { useAuthStore } from '@/services/auth.store'

import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import HomeView from '@/views/HomeView.vue'
import Table1View from '@/views/Table1View.vue'
import Table2View from '@/views/Table2View.vue'
import Table3View from '@/views/Table3View.vue'

const routes = [
  // ===== Публичные =====
  { path: '/login', name: 'Login', component: LoginView, meta: { guest: true } },
  { path: '/register', name: 'Register', component: RegisterView, meta: { guest: true } },

  // ===== Защищённые =====
  { path: '/', name: 'Home', component: HomeView, meta: { auth: true } },
  { path: '/table1', name: 'Table1', component: Table1View, meta: { auth: true } },
  { path: '/table2', name: 'Table2', component: Table2View, meta: { auth: true } },
  { path: '/table3', name: 'Table3', component: Table3View, meta: { auth: true } },

  // ===== ДОБАВЛЯЙ НОВЫЕ РОУТЫ ЗДЕСЬ =====
  // { path: '/table4', name: 'Table4', component: Table4View, meta: { auth: true } },
  // { path: '/admin-only', name: 'AdminOnly', component: AdminView, meta: { auth: true, role: 'admin' } },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

// ===== Guard =====
router.beforeEach((to, _from, next) => {
  const auth = useAuthStore()

  // Требуется авторизация?
  if (to.meta.auth && !auth.isAuthenticated) {
    return next('/login')
  }

  // Только для гостей (уже залогинен — на главную)
  if (to.meta.guest && auth.isAuthenticated) {
    return next('/')
  }

  // Проверка роли
  if (to.meta.role && auth.user?.role !== to.meta.role) {
    return next('/')
  }

  next()
})

export default router
