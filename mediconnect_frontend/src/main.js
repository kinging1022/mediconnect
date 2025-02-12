import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useUserStore } from './stores/user'
import googleLogin from 'vue3-google-login'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// Configuration constants
const API_BASE_URL = 'http://127.0.0.1:8000/api/'
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID

// Configure axios defaults
axios.defaults.baseURL = API_BASE_URL

// Create and configure Vue app
const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)
app.use(googleLogin, {
  clientId: GOOGLE_CLIENT_ID,
  scope: 'email profile',
  prompt: 'select_account'
})

// Initialize store after Pinia is installed
const userStore = useUserStore()

// Configure axios interceptors
axios.interceptors.request.use(
  (config) => {
    const token = userStore.user.access
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        await userStore.refreshToken()
        originalRequest.headers.Authorization = `Bearer ${userStore.user.access}`
        return axios(originalRequest)
      } catch (refreshError) {
        userStore.removeToken()
        router.push('/login')
        throw refreshError // Allow error handling up the chain
      }
    }
    
    return Promise.reject(error)
  }
)

app.mount('#app')