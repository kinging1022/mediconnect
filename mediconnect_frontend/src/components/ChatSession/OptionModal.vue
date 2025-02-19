<template>
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 w-full max-w-[360px] mx-auto">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-xl font-semibold text-gray-900">Options</h3>
          <button
            @click="$emit('close')"
            class="text-gray-500 hover:text-gray-700"
          >
            <x-icon class="w-5 h-5" />
          </button>
        </div>
        <div class="space-y-4">
          <button
            @click="$emit('open-medication')"
            class="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-50 text-gray-700 font-medium"
          >
            Add Medication
          </button>
          <button 
          @click="$emit('add-followup')"
          class="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-50 text-gray-700 font-medium">
            Schedule Follow-up
          </button>
          <button 
          @click="$emit('end-session')"
          class="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-50 text-red-600 font-medium">
            End Session
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { X } from 'lucide-vue-next'
  
  export default {
    name: 'OptionsModal',
    components: {
      XIcon: X
    }
  }
  </script>