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
    // Skip authentication for refresh token requests
    if (config._skipAuthRefresh) {
      return config;
    }
    
    const token = userStore.user.access;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);


axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Only attempt refresh if it's a 401 error, not already retried, and we have a refresh token
    if (error.response?.status === 401 && !originalRequest._retry && userStore.user.refresh) {
      originalRequest._retry = true;
      
      try {
        const newAccessToken = await userStore.refreshToken();
        if (newAccessToken) {
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
          return axios(originalRequest);
        } else {
          // If refreshToken() returns falsy value, handle as expired session
          throw new Error("Failed to refresh token");
        }
      } catch (refreshError) {
        console.error("Session expired, redirecting to login:", refreshError);
        userStore.removeToken();
        router.push('/login');
        return Promise.reject(refreshError);
      }
    }
    
    // Handle other errors or retried 401s that still failed
    return Promise.reject(error);
  }
);



app.mount('#app')