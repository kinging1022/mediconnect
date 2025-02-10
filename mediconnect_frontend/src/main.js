import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useUserStore } from './stores/user'

import App from './App.vue'
import router from './router'
import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/'

const app = createApp(App)

app.use(createPinia())
app.use(router)

const userStore = useUserStore(); 

// Request interceptor to attach access token
axios.interceptors.request.use(
    (config) => {
        const token = userStore.user.access; 
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor to handle token refresh and expiration
axios.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            
            try {
                await userStore.refreshToken(); 
                originalRequest.headers['Authorization'] = `Bearer ${userStore.user.access}`;
                return axios(originalRequest); 
            } catch (error) {
                userStore.removeToken();
                alert('Your session has expired. Please log in again.');

                router.push('/login');
            }
        }
        return Promise.reject(error);
    }
);

app.mount('#app')


