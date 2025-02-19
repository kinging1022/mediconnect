<template>
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 w-full max-w-[480px] max-h-[80vh] overflow-y-auto mx-auto">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-xl font-semibold text-gray-900">Add Medications</h3>
          <button
            @click="$emit('close')"
            class="text-gray-500 hover:text-gray-700"
          >
            <x-icon class="w-5 h-5" />
          </button>
        </div>
        <div class="space-y-6">
          <div
            v-for="(medication, index) in medications"
            :key="index"
            class="space-y-4 p-4 bg-gray-50 rounded-lg relative"
          >
            <button
              v-if="medications.length > 1"
              @click="$emit('remove-medication', index)"
              class="absolute top-2 right-2 text-gray-400 hover:text-red-500"
            >
              <x-icon class="w-4 h-4" />
            </button>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Medication Name
              </label>
              <input
                type="text"
                :value="medication.name"
                @input="$emit('change-medication', index, 'name', $event.target.value)"
                class="w-full rounded-lg border border-gray-200 px-4 py-2.5 focus:border-blue-600 focus:ring-1 focus:ring-blue-600 focus:outline-none"
                placeholder="Enter medication name"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Weight/Strength
              </label>
              <input
                type="text"
                :value="medication.weight"
                @input="$emit('change-medication', index, 'weight', $event.target.value)"
                class="w-full rounded-lg border border-gray-200 px-4 py-2.5 focus:border-blue-600 focus:ring-1 focus:ring-blue-600 focus:outline-none"
                placeholder="e.g., 500mg"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Dosage Instructions
              </label>
              <input
                type="text"
                :value="medication.dosage"
                @input="$emit('change-medication', index, 'dosage', $event.target.value)"
                class="w-full rounded-lg border border-gray-200 px-4 py-2.5 focus:border-blue-600 focus:ring-1 focus:ring-blue-600 focus:outline-none"
                placeholder="e.g., Take twice daily with meals"
              />
            </div>
          </div>
          <button
            @click="$emit('add-medication')"
            class="w-full py-3 border-2 border-dashed border-gray-200 rounded-lg text-gray-500 hover:border-blue-600 hover:text-blue-600 transition-colors flex items-center justify-center"
          >
            <plus-icon class="w-4 h-4 mr-2" />
            Add Another Medication
          </button>
          <div class="flex flex-col sm:flex-row justify-end space-y-3 sm:space-y-0 sm:space-x-4 mt-6">
            <button
              @click="$emit('close')"
              class="px-6 py-2.5 border border-gray-200 rounded-lg text-gray-600 hover:bg-gray-50 w-full sm:w-auto"
            >
              Cancel
            </button>
            <button
              @click="$emit('submit-medications')"
              class="px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 w-full sm:w-auto"
            >
              Add Medications
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { X, Plus } from 'lucide-vue-next'
  
  export default {
    name: 'MedicationModal',
    components: {
      XIcon: X,
      PlusIcon: Plus
    },
    props: {
      medications: {
        type: Array,
        required: true
      }
    }
  }
  </script>