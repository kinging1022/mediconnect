<template>
  <div class="min-h-screen w-full bg-gradient-to-br from-blue-50 via-white to-blue-50 flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-white rounded-2xl shadow-lg p-8 relative overflow-hidden">
      <div class="mb-8">
        <div class="text-2xl font-bold text-blue-600 flex items-center justify-center mb-6">
          <div class="w-8 h-8 bg-blue-600 rounded-lg mr-2"></div>
          MediConnect
        </div>
        <template v-if="status !== 'success'">
          <h1 class="text-2xl font-semibold text-gray-900 text-center">Reset Your Password</h1>
          <p class="mt-2 text-gray-600 text-center">
            Enter your email address and we'll send you instructions to reset your password.
          </p>
        </template>
      </div>
      <div v-if="status === 'success'" class="text-center animate-fade-in">
        <CheckCircle class="w-16 h-16 text-green-500 mx-auto mb-4" />
        <h2 class="text-xl font-semibold text-gray-900 mb-2">Check Your Email</h2>
        <p class="text-gray-600 mb-6">
          We've sent password reset instructions to <span class="font-medium">{{ email }}</span>
        </p>
        <button @click="status = 'idle'" class="text-blue-600 hover:text-blue-700 font-medium flex items-center justify-center mx-auto">
          <ArrowLeft class="w-4 h-4 mr-2" />
          Back to reset password
        </button>
      </div>
      <form v-else @submit.prevent="handleSubmit" class="space-y-6">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
          <div class="relative">
            <input
              type="email"
              id="email"
              v-model="email"
              :class="[
                'w-full px-4 py-2 pl-10 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors duration-300',
                errorMessage ? 'border-red-500' : 'border-gray-300'
              ]"
              placeholder="Enter your email"
              :disabled="status === 'loading'"
            />
            <Mail class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
          </div>
          <p v-if="errorMessage" class="mt-1 text-sm text-red-500 animate-fade-in">{{ errorMessage }}</p>
        </div>
        <button
          type="submit"
          :disabled="status === 'loading' || !email"
          :class="[
            'w-full bg-blue-600 text-white px-6 py-2 rounded-lg transition-all duration-300 flex items-center justify-center',
            status === 'loading' ? 'bg-blue-500 cursor-not-allowed' : 'hover:bg-blue-700',
            !email && 'opacity-50 cursor-not-allowed'
          ]"
        >
          <Loader2 v-if="status === 'loading'" class="w-5 h-5 animate-spin" />
          <span v-else>Reset Password</span>
        </button>
        <button
          type="button"
          @click="$router.back()"
          class="w-full text-gray-600 hover:text-blue-600 font-medium flex items-center justify-center"
        >
          <ArrowLeft class="w-4 h-4 mr-2" />
          Back to sign in
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { Loader2, ArrowLeft, Mail, CheckCircle } from 'lucide-vue-next';
import axios from 'axios';
import { useToastStore } from '@/stores/toast';

export default {
  name: 'PasswordResetRequest',
  components: {
    Loader2,
    ArrowLeft,
    Mail,
    CheckCircle
  },
  data() {
    return {
      email: '',
      status: 'idle',
      errorMessage: '',
      toastStore: useToastStore()
    };
  },
  methods: {
    validateEmail(email) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    },
    async handleSubmit() {
      if (!this.validateEmail(this.email)) {
        this.errorMessage = 'Please enter a valid email address';
        return;
      }
      this.status = 'loading';
      this.errorMessage = '';
      try {
        await new Promise((resolve) => setTimeout(resolve, 1500));
        await axios.post('request/password/reset/', { email: this.email });
        this.status = 'success';
      } catch (error) {
        if (error?.response?.data?.error) {
          this.status = 'error';
          this.errorMessage = error.response.data.error;
          if (error.response.data.error.includes('inactive')) {
            await this.sendActivationEmail(this.email);
          }
        } else {
          this.status = 'error';
          this.errorMessage = 'Something went wrong, please try again';
        }
      }
    },
    async sendActivationEmail(email) {
      try {
        await axios.post('activate/email/', { email });
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
