<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50 py-12 px-4 sm:px-6 lg:px-8 flex items-center">
      <div class="max-w-md w-full mx-auto space-y-8 bg-white p-8 rounded-2xl shadow-lg">
        <!-- Logo and Header -->
        <div class="text-center">
          <div class="flex items-center justify-center mb-4">
            <div class="w-10 h-10 bg-blue-600 rounded-lg"></div>
            <h2 class="ml-3 text-2xl font-bold text-gray-900">MediConnect</h2>
          </div>
          <h2 class="text-3xl font-bold text-gray-900">Welcome Back</h2>
          <p class="mt-2 text-sm text-gray-600">Sign in to continue to your account</p>
        </div>
        <!-- Login Form -->
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700">Email</label>
            <div class="mt-1 relative rounded-lg">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Mail class="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="email"
                v-model="formData.email"
                required
                class="block w-full pl-10 rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-blue-500"
                placeholder="Enter your email"
              />
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Password</label>
            <div class="mt-1 relative rounded-lg">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Lock class="h-5 w-5 text-gray-400" />
              </div>
              <input
                :type="showPassword ? 'text' : 'password'"
                v-model="formData.password"
                required
                class="block w-full pl-10 pr-10 rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-blue-500"
                placeholder="Enter your password"
              />
              <button
                type="button"
                @click="togglePasswordVisibility"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <EyeOff v-if="showPassword" class="h-5 w-5 text-gray-400 hover:text-gray-600" />
                <Eye v-else class="h-5 w-5 text-gray-400 hover:text-gray-600" />
              </button>
            </div>
            <div class="flex items-center justify-end mt-2">
                <RouterLink :to="{ name: 'reset-password' }" class="text-sm font-medium text-blue-600 hover:text-blue-500">Forgot password?</RouterLink>
            </div>
          </div>
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          >
            <div v-if="isLoading" class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <span v-else>Sign in</span>
          </button>
        </form>
        <!-- Social Login -->
        <div class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-white text-gray-500">Or continue with</span>
            </div>
          </div>
          <div class="mt-6 grid grid-cols-2 gap-3">
            <GoogleLogin :callback="handleGoogleLogin" />

            <button class="w-full px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200">
              Apple
            </button>
          </div>
        </div>
        <!-- Sign Up Link -->
        <p class="text-center text-sm text-gray-600">
          Don't have an account?
          <a href="#" class="font-medium text-blue-600 hover:text-blue-500">Sign up</a>
        </p>
      </div>
    </div>
  </template>
  
  <script>
  import { Mail, Lock, Eye, EyeOff } from 'lucide-vue-next'
  import { GoogleLogin } from "vue3-google-login";
  import axios from "axios";
  import {useUserStore} from '@/stores/user'
  import { useToastStore } from "@/stores/toast";  

  
  export default {
    name: 'LoginForm',
    components: {
      Mail,
      Lock,
      Eye,
      EyeOff,
      GoogleLogin
      
    },
    data() {
      return {
        showPassword: false,
        formData: {
          email: '',
          password: ''
        },
        isLoading: false,
        userStore: useUserStore(),
        toastStore: useToastStore()
      }
    },
    methods: {
      togglePasswordVisibility() {
        this.showPassword = !this.showPassword
      },
      async handleSubmit() {
        try{
            this.isLoading = true
            // Simulate API call
            console.log('Login:', this.formData)
            const response = await axios.post('login/',this.formData)
            console.log(response.data)
            this.userStore.setToken(response.data)
            await this.fetchUser()
            this.isLoading = false
            this.$router.push('/dashboard')
            this.toastStore.showToast(5000, `welcome back ${this.userStore.user.first_name}`, 'bg-blue-700 text-white');


        }catch(error){
            this.isLoading = false
            console.log(error.response.data)
            const errorMessage = error.response.data.detail[0]
            this.toastStore.showToast(5000, `${errorMessage}`, 'bg-red-500 text-white');

            if (errorMessage === 'Account is inactive, click the link sent to your email to activate your account'){
                await this.sendActivationEmail(this.formData.email)
            }

        }
        
        
      },
      async sendActivationEmail(email){
        try{
            const response = await axios.post('activate/email/',{email:email})


        }catch(error){
            console.error(error)

        }

      },
      async fetchUser() {
        try {
          const response = await axios.get('user/');
          console.log(response)
          this.userStore.setUserInfo(response.data);
        } catch (error) {
          console.error(error);
        }
      },
      async handleGoogleLogin(response) {
      try {
        const { data } = await axios.post("auth/google/", {
          token: response.credential,
        });

        this.userStore.setToken(data)
        await this.fetchUser()
        this.$router.push('/dashboard')
        

        console.log("Login successful", data);
      } catch (error) {
        console.error("Login failed", error);
      }
    },

    }
  }
  </script>
  
  