<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50 py-12 px-4 sm:px-6 lg:px-8 flex items-center">
      <div class="max-w-md w-full mx-auto space-y-8 bg-white p-8 rounded-2xl shadow-lg">
        <div class="text-center">
          <div class="flex items-center justify-center mb-4">
            <div class="w-10 h-10 bg-blue-600 rounded-lg"></div>
            <h2 class="ml-3 text-2xl font-bold text-gray-900">
              MediConnect
            </h2>
          </div>
          <h2 class="text-3xl font-bold text-gray-900">
            Create Patient Account
          </h2>
          <p class="mt-2 text-sm text-gray-600">
            Get connected with healthcare professionals in minutes
          </p>
        </div>
  
        <!-- New error display -->
        <div v-if="Object.keys(errors).length > 0" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <strong class="font-bold">Please correct the following errors:</strong>
          <ul class="mt-2 list-disc list-inside">
            <li v-for="(error, key) in errors" :key="key">{{ error }}</li>
          </ul>
        </div>
  
        <div class="relative">
          <div class="flex justify-between items-center">
            <div
              v-for="i in 2"
              :key="i"
              :class="[
                'w-8 h-8 rounded-full flex items-center justify-center',
                step >= i ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-400'
              ]"
            >
              <component :is="step > i ? 'Check' : 'span'" v-if="step > i" :size="16" />
              <template v-else>{{ i }}</template>
            </div>
          </div>
          <div class="absolute top-4 left-0 right-0 h-0.5 bg-gray-100 -z-10">
            <div
              class="h-full bg-blue-600 transition-all duration-300"
              :style="{ width: step === 1 ? '0%' : '100%' }"
            ></div>
          </div>
        </div>
        <div v-if="step === 1" class="space-y-6">
          <h3 class="text-lg font-medium text-gray-900">
            Personal Information
          </h3>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">
                First Name
              </label>
              <input
                type="text"
                v-model="formData.first_name"
                class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">
                Last Name
              </label>
              <input
                type="text"
                v-model="formData.last_name"
                class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">
              Email
            </label>
            <div class="mt-1 relative rounded-lg">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Mail class="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="email"
                v-model="formData.email"
                class="block w-full pl-10 rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>
          </div>
        </div>
        <div v-if="step === 2" class="space-y-6">
          <h3 class="text-lg font-medium text-gray-900">
            Create Password
          </h3>
          <div>
            <label class="block text-sm font-medium text-gray-700">
              Password
            </label>
            <div class="mt-1 relative rounded-lg">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Lock class="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="password"
                v-model="formData.password"
                class="block w-full pl-10 rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-blue-500"
                required
                minlength="8"
              />
            </div>
            <p class="mt-2 text-sm text-gray-500">
              Password must be at least 8 characters long
            </p>
          </div>
          <!-- New confirm password input -->
          <div>
            <label class="block text-sm font-medium text-gray-700">
              Confirm Password
            </label>
            <div class="mt-1 relative rounded-lg">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Lock class="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="password"
                v-model="formData.password2"
                class="block w-full pl-10 rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-blue-500"
                required
                minlength="8"
              />
            </div>
          </div>
        </div>
        <div class="flex justify-between mt-8">
          <button
            v-if="step > 1"
            @click="prevStep"
            class="flex items-center px-4 py-2 text-sm font-medium text-gray-600 hover:text-blue-600"
          >
            <ChevronLeft class="w-4 h-4 mr-1" />
            Back
          </button>
          <button
            @click="step < 2 ? nextStep() : submitForm()"
            class="flex items-center px-6 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 ml-auto"
          >
            <template v-if="step === 2">
              Create Account
            </template>
            <template v-else>
              Next
              <ChevronRight class="w-4 h-4 ml-1" />
            </template>
          </button>
        </div>
        <div v-if="step === 1" class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-white text-gray-500">
                Or continue with
              </span>
            </div>
          </div>
          <div class="mt-6 grid grid-cols-2 gap-3">
            <button class="w-full px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
              Google
            </button>
            <button class="w-full px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
              Apple
            </button>
          </div>
        </div>
        <p class="text-center text-sm text-gray-600">
          Already have an account?
          <a href="#" class="font-medium text-blue-600 hover:text-blue-500">
            Sign in
          </a>
        </p>
      </div>
    </div>
  </template>
  
  <script>
  import { ChevronLeft, ChevronRight, Check, Mail, Lock } from 'lucide-vue-next';
  import axios from 'axios';
  import { useToastStore } from "@/stores/toast";  
  
  export default {
    name: 'SignUpForm',
    components: {
      ChevronLeft,
      ChevronRight,
      Check,
      Mail,
      Lock
    },
    data() {
      return {
        step: 1,
        formData: {
          first_name: '',
          last_name: '',
          email: '',
          password: '',
          password2: '' 
        },
        toastStore: useToastStore(),
        errors: {} 
      };
    },
    methods: {
      nextStep() {
        if (this.validateStep()) {
          this.step += 1;
        }
      },
      prevStep() {
        this.step -= 1;
      },
      validateStep() {
        this.errors = {};
        
        if (this.step === 1) {
          if (!this.formData.first_name) this.errors.firstName = "First name is required";
          if (!this.formData.last_name) this.errors.lastName = "Last name is required";
          if (!this.formData.email) this.errors.email = "Email is required";
        } else if (this.step === 2) {
          if (!this.formData.password) this.errors.password = "Password is required";
          if (this.formData.password.length < 8) this.errors.password = "Password must be at least 8 characters long";
          if (!this.formData.password) this.errors.password = "Please confirm your password";
          if (this.formData.password !== this.formData.password2) {
            this.errors.password2 = "Passwords do not match";
          }
        }
  
        return Object.keys(this.errors).length === 0;
      },
      async submitForm() {
        if (this.validateStep()) {
          try {
            console.log(this.formData)
            const response = await axios.post('signup/', this.formData);
            if (response.status === 201) {
                await this.sendActivationEmail(this.formData.email)
              this.toastStore.showToast(5000, `${response.data.message}`, 'bg-blue-700 text-white');
              // Reset form data
              Object.keys(this.formData).forEach((key) => {
                this.formData[key] = "";
              });
              // Redirect to login page
              this.$router.push('/login');
            }
          } catch (error) {
            console.error('Signup error:', error.data);
            if (error.status === 400){
                this.toastStore.showToast(5000, `${error.response.data.email[0]}`, 'bg-red-500 text-white');
            }else{
                this.toastStore.showToast(5000, 'An error occured while siging up , contact support', 'bg-red-500 text-white');
            }
           

            
          }
        }
      },
      async sendActivationEmail(email){
        try{
            const response = await axios.post('activate/email/',{email:email})


        }catch(error){
            console.error(error)

        }

      }
    }
  };
  </script>