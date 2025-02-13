<template>
    <section class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
      <div class="p-6">
        <h3 class="text-xl font-semibold text-gray-900 mb-4">Today's Appointments</h3>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Patient</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Symptoms</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="appointment in appointments" :key="appointment.id">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900">{{ appointment.created_by.first_name }} {{ appointment.created_by.last_name }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-500">{{ appointment.created_at_formatted }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <button 
                    @click="showSymptoms(appointment.symptoms)"
                    class="px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800 hover:bg-blue-200"
                  >
                    Show Symptoms
                  </button>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <button class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                    Start Session
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
  
      <!-- Modal for showing symptoms -->
      <div v-if="isModalOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="bg-white p-6 rounded-lg max-w-md w-full">
          <h4 class="text-lg font-semibold mb-2">Symptoms</h4>
          <p class="text-sm text-gray-600 mb-4">{{ selectedSymptoms }}</p>
          <button @click="closeModal" class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300">
            Close
          </button>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    name: 'AppointmentsSection',
    props: {
      appointments: {
        type: Array,
        required: true,
      },
      formatDate: {
       type: Function,
       required: true,
     },
    },
    data() {
      return {
        isModalOpen: false,
        selectedSymptoms: '',
      }
    },
    methods: {
      showSymptoms(symptoms) {
        this.selectedSymptoms = symptoms
        this.isModalOpen = true
      },
      closeModal() {
        this.isModalOpen = false
      },
    },
  }
  </script>
  
  