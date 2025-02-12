<template>
    <div class="min-h-screen bg-gray-50 flex flex-col">
      <header class="bg-white border-b border-gray-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between items-center h-16">
            <h1 class="text-xl font-semibold text-gray-900">Update Profile</h1>
            <button @click="goBack" class="text-blue-600 hover:text-blue-700 font-medium">
              <ArrowLeft class="w-5 h-5 inline-block mr-1" />
              Back to Dashboard
            </button>
          </div>
        </div>
      </header>
  
      <main class="flex-grow">
        <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <form @submit.prevent="updateProfile" class="bg-white rounded-xl shadow-sm border border-gray-200">
            <div class="p-6 space-y-6">
              <div class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-2">
                <div>
                  <label for="firstName" class="block text-sm font-medium text-gray-700">First Name</label>
                  <input type="text" id="firstName" v-model="form.firstName" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm py-2 px-3 text-base focus:ring-blue-500 focus:border-blue-500">
                </div>
                <div>
                  <label for="lastName" class="block text-sm font-medium text-gray-700">Last Name</label>
                  <input type="text" id="lastName" v-model="form.lastName" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm py-2 px-3 text-base focus:ring-blue-500 focus:border-blue-500">
                </div>
                <div>
                  <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
                  <input type="email" id="email" v-model="form.email" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm py-2 px-3 text-base focus:ring-blue-500 focus:border-blue-500">
                </div>
                <div>
                  <label for="phone" class="block text-sm font-medium text-gray-700">Phone</label>
                  <input type="tel" id="phone" v-model="form.phone" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm py-2 px-3 text-base focus:ring-blue-500 focus:border-blue-500">
                </div>
                <div>
                  <label for="dateOfBirth" class="block text-sm font-medium text-gray-700">Date of Birth</label>
                  <input type="date" id="dateOfBirth" v-model="form.dateOfBirth" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm py-2 px-3 text-base focus:ring-blue-500 focus:border-blue-500">
                </div>
                <div>
                  <label for="gender" class="block text-sm font-medium text-gray-700">Gender</label>
                  <select id="gender" v-model="form.gender" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm py-2 px-3 text-base focus:ring-blue-500 focus:border-blue-500">
                    <option value="">Select gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                <div>
                  <label for="weight" class="block text-sm font-medium text-gray-700">Weight (kg)</label>
                  <input type="number" id="weight" v-model="form.weight" min="1" max="300" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm py-2 px-3 text-base focus:ring-blue-500 focus:border-blue-500">
                </div>
                <div>
                  <label for="height" class="block text-sm font-medium text-gray-700">Height (cm)</label>
                  <input type="number" id="height" v-model="form.height" min="50" max="300" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm py-2 px-3 text-base focus:ring-blue-500 focus:border-blue-500">
                </div>
                <div>
                  <label for="bloodType" class="block text-sm font-medium text-gray-700">Blood Group</label>
                  <select id="bloodType" v-model="form.bloodType" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm py-2 px-3 text-base focus:ring-blue-500 focus:border-blue-500">
                    <option value="">Select blood type</option>
                    <option v-for="blood in bloodTypes" :key="blood" :value="blood">{{ blood }}</option>
                  </select>
                </div>
              </div>
              <div>
                <label for="allergies" class="block text-sm font-medium text-gray-700">Allergies</label>
                <textarea id="allergies" v-model="form.allergies" rows="3" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm py-2 px-3 text-base focus:ring-blue-500 focus:border-blue-500"></textarea>
              </div>
              <div class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-2">
                <div>
                  <label for="emergencyContactName" class="block text-sm font-medium text-gray-700">Emergency Contact Name</label>
                  <input type="text" id="emergencyContactName" v-model="form.emergencyContactName" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm py-2 px-3 text-base focus:ring-blue-500 focus:border-blue-500">
                </div>
                <div>
                  <label for="emergencyContactNumber" class="block text-sm font-medium text-gray-700">Emergency Contact Number</label>
                  <input type="tel" id="emergencyContactNumber" v-model="form.emergencyContactNumber" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm py-2 px-3 text-base focus:ring-blue-500 focus:border-blue-500">
                </div>
              </div>
            </div>
            <div class="px-6 py-3 bg-gray-50 flex items-center justify-between rounded-b-xl">
              <button type="button" @click="openPasswordModal" class="text-gray-700 bg-white border border-gray-300 shadow-sm rounded-md py-2 px-4 text-base hover:bg-gray-50">
                Edit Password
              </button>
              <button type="submit" class="text-white bg-blue-600 border border-transparent shadow-sm rounded-md py-2 px-4 text-base hover:bg-blue-700">
                Update Profile
              </button>
            </div>
          </form>
        </div>
      </main>
  
      <PasswordEdit :is-open="isPasswordModalOpen" @close="closePasswordModal" />
    </div>
  </template>
  
  <script>
  import { ArrowLeft } from 'lucide-vue-next'
  import PasswordEdit from '@/components/modals/PasswordEdit.vue'
  import { useToastStore } from '@/stores/toast'
  import { useUserStore } from '@/stores/user'
  import axios from 'axios'
  
  export default {
    name: 'UpdateProfileForm',
    components: {
      ArrowLeft,
      PasswordEdit
    },
    setup() {
      const userStore = useUserStore()
      const toastStore = useToastStore()
  
      return {
        userStore,
        toastStore,
      }
    },
    data() {
      return {
        form: {
          firstName: this.userStore.user.first_name,
          lastName: this.userStore.user.last_name,
          email: this.userStore.user.email,
          phone: this.userStore.user.phone || "",
          dateOfBirth: this.userStore.user.dob || null,
          gender: this.userStore.user.gender || "",
          weight: this.userStore.user.weight || "",
          height: this.userStore.user.height || "",
          allergies: this.userStore.user.allergies || "",
          emergencyContactNumber: this.userStore.user.emergency_contact_number || "",
          emergencyContactName: this.userStore.user.emergency_contact_name || "",
          bloodType: this.userStore.user.blood_type || ""
        },
        isPasswordModalOpen: false,
        bloodTypes: ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
      }
    },
    methods: {
      openPasswordModal() {
        this.isPasswordModalOpen = true
      },
      closePasswordModal(message) {
        this.isPasswordModalOpen = false
        if (message) {
          console.log(message)
          this.toastStore.showToast(5000, message, message.includes('successful') ? 'bg-blue-700 text-white' : 'bg-red-500 text-white')
        }
      },
      async updateProfile() {
        if (this.form.dateOfBirth) {
          this.form.dateOfBirth = new Date(this.form.dateOfBirth).toISOString().split('T')[0] // Convert to YYYY-MM-DD
        }
        try {
          console.log('Profile update submitted:', this.form)
          const response = await axios.patch('dashboard/profile/update/', this.form)
          this.userStore.setUserInfo(response.data)
          this.toastStore.showToast(5000, 'Profile successfully updated', 'bg-blue-700 text-white')
          this.goBack()
        } catch (error) {
          console.error(error)
          this.toastStore.showToast(5000, 'Failed to update profile', 'bg-red-500 text-white')
        }
      },
      goBack() {
        this.$router.push('/dashboard')
      }
    }
  }
  </script>
  
  