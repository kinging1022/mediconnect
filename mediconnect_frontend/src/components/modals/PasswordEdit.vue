<template>
    <div v-if="isOpen" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
        <div class="p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Change Password</h3>
          <form @submit.prevent="updatePassword">
            <div class="space-y-4">
              <div>
                <label for="currentPassword" class="block text-sm font-medium text-gray-700">Current Password</label>
                <input 
                  type="password" 
                  id="currentPassword" 
                  v-model="passwordForm.currentPassword" 
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm" 
                  required
                />
              </div>
              <div>
                <label for="newPassword" class="block text-sm font-medium text-gray-700">New Password</label>
                <input 
                  type="password" 
                  id="newPassword" 
                  v-model="passwordForm.newPassword" 
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm" 
                  required
                />
              </div>
              <div>
                <label for="confirmPassword" class="block text-sm font-medium text-gray-700">Confirm New Password</label>
                <input 
                  type="password" 
                  id="confirmPassword" 
                  v-model="passwordForm.confirmPassword" 
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm" 
                  required
                />
              </div>
            </div>
            <div class="mt-6 flex justify-end space-x-3">
              <button 
                type="button" 
                @click="closeModal" 
                class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Cancel
              </button>
              <button 
                type="submit" 
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Update Password
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    props: {
      isOpen: Boolean,
    },
    data() {
      return {
        passwordForm: {
          currentPassword: '',
          newPassword: '',
          confirmPassword: '',
        },
        errorMessage: '',
      };
    },
    methods: {
      closeModal(message = null) {
        this.$emit('close', message);
        this.passwordForm = {
          currentPassword: '',
          newPassword: '',
          confirmPassword: '',
        };
        this.errorMessage = '';
      },
      async updatePassword() {
        try {
          this.errorMessage = '';
          const response = await axios.post('edit/password/', this.passwordForm);
          if (response.status === 200) {
            this.closeModal('Password updated successfully');
          }
        } catch (error) {
          if (error?.response?.data) {
            this.errorMessage = error.response.data.error;
            this.$emit('close', this.errorMessage);
          }
          this.passwordForm = {
            currentPassword: '',
            newPassword: '',
            confirmPassword: '',
          };
        }
      },
    },
  };
  </script>
  