import { createRouter, createWebHistory } from 'vue-router'

import authRoutes from './auth.routes'
import studentRoutes from './student.routes'
import companyRoutes from './company.routes'
import adminRoutes from './admin.routes'
import { getCurrentUser, getDashboardRoute, isAuthenticated } from '@/utils/auth.js'

const router = createRouter({
  history: createWebHistory(),
  routes: [...authRoutes, ...studentRoutes, ...companyRoutes, ...adminRoutes],
})
router.beforeEach((to) => {
  // Rule 1
  if (to.meta.guest && isAuthenticated()) {
    const currentUser = getCurrentUser()
    return getDashboardRoute(currentUser.role)
  }

  // Rule 2
  if (to.meta.requiresAuth && !isAuthenticated()) {
    return {
      name: 'login',
    }
  }

  // Rule 3
  if (to.meta.requiresAuth) {
    const currentUser = getCurrentUser()

    if (to.meta.role !== currentUser.role) {
      return getDashboardRoute(currentUser.role)
    }
  }
})
export default router
