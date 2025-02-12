import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import DashboardView from '@/views/DashboardView.vue'
import AccountActivate from '@/views/AccountActivate.vue'
import ForgotPasswordResetView from '@/views/ForgotPasswordResetView.vue'
import PasswordReset from '@/views/PasswordReset.vue'
import updateProfileView from '@/views/updateProfileView.vue'
import UpdateProfileView from '@/views/updateProfileView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
    },
    {
      path: '/acount/activate/:token',
      name: 'activate',
      component: AccountActivate,
    },
    {
      path: '/reset/password/request',
      name: 'reset-password',
      component: ForgotPasswordResetView,
    },
    {
      path: '/reset-password/:token',
      name: 'edit-password',
      component: PasswordReset,
    },
    {
      path: '/dashboard/profile/update',
      name: 'update-profile',
      component: UpdateProfileView,
    },
    
  ],
})

export default router
