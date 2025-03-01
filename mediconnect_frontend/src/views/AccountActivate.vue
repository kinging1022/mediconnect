<template>
    <div class="min-h-screen w-full bg-gradient-to-br from-blue-50 via-white to-blue-50 flex items-center justify-center p-4">
      <div class="max-w-md w-full bg-white rounded-2xl shadow-lg p-8 relative overflow-hidden">
        <div class="text-center">
          <div class="mb-6">
            <div class="text-2xl font-bold text-blue-600 flex items-center justify-center mb-2">
              <div class="w-8 h-8 bg-blue-600 rounded-lg mr-2"></div>
              MediConnect
            </div>
            <h1 class="text-2xl font-semibold text-gray-900">
              Account Activation
            </h1>
          </div>
          <div class="space-y-6">
            <div v-if="status === 'loading'" class="animate-fade-in">
              <Loader2 class="w-16 h-16 text-blue-600 animate-spin mx-auto mb-4" />
              <p class="text-gray-600">Verifying your account...</p>
            </div>
            <div v-else-if="status === 'success'" class="animate-fade-in">
              <CheckCircle class="w-16 h-16 text-green-500 mx-auto mb-4" />
              <h2 class="text-xl font-semibold text-gray-900 mb-2">
                Account Activated!
              </h2>
              <p class="text-gray-600 mb-6">
                Your account has been successfully activated. You can now sign
                in to access your account.
              </p>
              <RouterLink to="/login" class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-300">
                Sign In
              </RouterLink>
            </div>
            <div v-else-if="status === 'error'" class="animate-fade-in">
              <XCircle class="w-16 h-16 text-red-500 mx-auto mb-4" />
              <h2 class="text-xl font-semibold text-gray-900 mb-2">
                Activation Failed
              </h2>
              <p class="text-gray-600 mb-6">
                The activation link has expired or is invalid. Please login to request
                a new activation link.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { CheckCircle, XCircle, Loader2 } from 'lucide-vue-next';
  import axios from 'axios';
  
  export default {
    name: 'AccountActivation',
    components: {
      CheckCircle,
      XCircle,
      Loader2
    },
    data() {
      return {
        status: 'loading'
      };
    },
    mounted() {
      this.verifyToken();
    },
    methods: {
        async verifyToken() {
            try {
                await new Promise(resolve => setTimeout(resolve, 2000));
                const token = this.$route.params.token;


                const response = await axios.post('activate/', {token:token }, { timeout: 5000 });

                if (response.status === 200) {
                    this.status = 'success';
                }
                } catch (error) {
                if (error.code === 'ECONNABORTED') {
                    this.status = 'error';
                    console.error('Request timed out.');
                } else {
                    this.status = 'error';
                }
             }
        }
    }
  };
  </script>
  
  <style scoped>
  .animate-fade-in {
    animation: fadeIn 0.5s ease-in-out;
  }
  
  .animate-spin {
    animation: spin 1s linear infinite;
  }
  
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
  </style>
  
  