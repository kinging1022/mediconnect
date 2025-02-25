<template>
    <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg shadow-xl w-full max-w-md">
        <div class="flex justify-between items-center p-6 border-b">
          <h2 class="text-xl font-semibold text-gray-900">Set Medication Reminder</h2>
          <button @click="$emit('close')" class="text-gray-400 hover:text-gray-500">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
          <div>
            <label for="time" class="block text-sm font-medium text-gray-700 mb-1">Reminder Time</label>
            <div class="relative">
              <svg xmlns="http://www.w3.org/2000/svg" class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <input
                type="time"
                id="time"
                v-model="time"
                required
                class="pl-10 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <div class="relative">
              <svg xmlns="http://www.w3.org/2000/svg" class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <input
                type="email"
                id="email"
                v-model="email"
                required
                class="pl-10 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="your@email.com"
              />
            </div>
          </div>
          <div>
            <label for="phoneNumber" class="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
            <div class="flex">
              <div class="relative w-1/3 mr-2">
                <select
                  v-model="countryCode"
                  class="w-full pl-3 pr-10 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option v-for="code in countryCodes" :key="code.code" :value="code.code">
                    {{ code.code }} ({{ code.country }})
                  </option>
                </select>
              </div>
              <div class="relative flex-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
                <input
                  type="tel"
                  id="phoneNumber"
                  v-model="phoneNumber"
                  required
                  class="pl-10 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="(123) 456-7890"
                />
              </div>
            </div>
          </div>
          <div class="mt-6">
            <button
              type="submit"
              class="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-300"
            >
              Set Reminder
            </button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { countries } from 'countries-list';
  import axios from 'axios';
  
  export default {
    name: 'MedicationReminderModal',
    props: {
      isOpen: {
        type: Boolean,
        required: true
      },
      medicationId: {
        type: String,
      },
      
    },
    data() {
      return {
        time: '',
        email: '',
        phoneNumber: '',
        countryCode: '+1',
        countryCodes: []
      }
    },
    methods: {
      async handleSubmit() {
          if (!this.time || !this.email || !this.phoneNumber) {
            console.error("All fields are required.");
            return;
          }
  
          const payload = {
            time: this.time,
            email: this.email,
            phoneNumber: `${this.countryCode}${this.phoneNumber}`
          };
  
  
          try {
            const response = await axios.post(`reminder/create/${this.medicationId}/`, payload);
            if (response.status === 201) {
              this.$emit('reminderSuccess', response.data.id);
            }
          } catch (error) {
            console.error("Error submitting reminder:", error.response || error.message);
          }
        },
  
      generateCountryCodes() {
        this.countryCodes = Object.entries(countries).map(([code, country]) => ({
          code: `+${country.phone}`,
          country: country.name
        }));
  
        // Sort country codes alphabetically by country name
        this.countryCodes.sort((a, b) => a.country.localeCompare(b.country));
  
        // Set default country code to United States (+1)
        const usCode = this.countryCodes.find(c => c.code === '+1');
        if (usCode) {
          this.countryCode = usCode.code;
        }
      }
    },
    mounted() {
      this.generateCountryCodes()
    }
  }
  </script>
  
  