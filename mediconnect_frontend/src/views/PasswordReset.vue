<template>
    <div class="min-h-screen w-full bg-gradient-to-br from-blue-50 via-white to-blue-50 flex items-center justify-center p-4">
      <div class="max-w-md w-full bg-white rounded-2xl shadow-lg p-8 relative overflow-hidden">
        <!-- Success Message -->
        <div v-if="formState === 'success'" class="text-center animate-fade-in">
          <CheckCircle class="w-16 h-16 text-green-500 mx-auto mb-4" />
          <h2 class="text-xl font-semibold text-gray-900 mb-2">
            Password Successfully Reset!
          </h2>
          <p class="text-gray-600 mb-6">
            Your password has been successfully updated. You can now sign in with your new password.
          </p>
          <RouterLink to="/login"
            class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-300"
          >
            Sign In
          </RouterLink>
        </div>
  
        <!-- Password Reset Form -->
        <div v-else>
          <h1 class="text-2xl font-semibold text-gray-900 text-center">
            Reset Your Password
          </h1>
          <p class="mt-2 text-gray-600 text-center">
            Please enter your new password below
          </p>
  
          <form @submit.prevent="handleSubmit" class="space-y-6">
            <!-- New Password -->
            <div>
              <label for="new-password" class="block text-sm font-medium text-gray-700 mb-1">
                New Password
              </label>
              <div class="relative">
                <input
                  id="new-password"
                  :type="showPassword ? 'text' : 'password'"
                  v-model="password"
                  class="w-full px-4 py-2 pl-10 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors duration-300"
                  :class="{ 'border-red-500': password && password.length < 8 }"
                  placeholder="Enter new password"
                />
                <Lock class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  <component :is="showPassword ? EyeOff : Eye" class="w-5 h-5" />
                </button>
              </div>
              <p v-if="password.length < 8" class="mt-2 text-sm text-red-600">
                Password must be at least 8 characters long.
              </p>
            </div>
  
            <!-- Confirm Password -->
            <div>
              <label for="confirm-password" class="block text-sm font-medium text-gray-700 mb-1">
                Confirm Password
              </label>
              <div class="relative">
                <input
                  id="confirm-password"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  v-model="confirmPassword"
                  class="w-full px-4 py-2 pl-10 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors duration-300"
                  :class="{ 'border-red-500': confirmPassword && password !== confirmPassword }"
                  placeholder="Confirm new password"
                />
                <Lock class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <button
                  type="button"
                  @click="showConfirmPassword = !showConfirmPassword"
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  <component :is="showConfirmPassword ? EyeOff : Eye" class="w-5 h-5" />
                </button>
              </div>
              <p v-if="confirmPassword && password !== confirmPassword" class="mt-2 text-sm text-red-600">
                Passwords do not match.
              </p>
            </div>
  
            <!-- Submit Button -->
            <button
              type="submit"
              :disabled="!isFormValid || isLoading"
              class="w-full bg-blue-600 text-white px-6 py-2 rounded-lg transition-all duration-300 flex items-center justify-center"
              :class="{
                'hover:bg-blue-700': isFormValid && !isLoading,
                'opacity-50 cursor-not-allowed': !isFormValid || isLoading
              }"
            >
              <Loader2 v-if="isLoading" class="w-5 h-5 animate-spin mr-2" />
              <span v-else>Reset Password</span>
            </button>
          </form>
  
          <p v-if="errorMessage" class="mt-4 text-sm text-red-600 text-center animate-fade-in">
            {{ errorMessage }}
          </p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { Eye, EyeOff, Lock, CheckCircle, Loader2 } from 'lucide-vue-next';
  import axios from 'axios';
  
  export default {
    components: { Eye, EyeOff, Lock, CheckCircle, Loader2 },
    data() {
      return {
        password: '',
        confirmPassword: '',
        showPassword: false,
        showConfirmPassword: false,
        formState: 'idle',
        errorMessage: '',
        isLoading: false
      };
    },
    computed: {
      passwordsMatch() {
        return this.password && this.confirmPassword && this.password === this.confirmPassword;
      },
      isFormValid() {
        return this.password.length >= 8 && this.passwordsMatch;
      }
    },
    methods: {
      async handleSubmit() {
        if (!this.isFormValid) return;
        this.isLoading = true;
        this.errorMessage = '';
  
        try {
          const token = this.$route.params.token;
          await axios.post('reset/password/', {
            token: token,
            new_password: this.password,
            confirm_password: this.confirmPassword
          });
          this.formState = 'success';
        } catch (error) {
          this.errorMessage = 'The password reset link has expired or is invalid. Please request a new one.';
        } finally {
          this.isLoading = false;
        }
      },
     
    }
  };
  </script>
  