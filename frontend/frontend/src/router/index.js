import { createRouter, createWebHistory } from 'vue-router'

import authRoutes from './auth.routes'
import studentRoutes from './student.routes'
import companyRoutes from './company.routes'
import adminRoutes from './admin.routes'

const router = createRouter({
  history: createWebHistory(),
  routes: [...authRoutes, ...studentRoutes, ...companyRoutes, ...adminRoutes],
})

export default router
