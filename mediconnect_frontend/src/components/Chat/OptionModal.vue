<template>
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-20">
      <div class="bg-white rounded-lg w-full max-w-md mx-4">
        <div class="p-4 border-b">
          <h2 class="text-xl font-semibold">Options</h2>
        </div>
        
        <div class="p-4 space-y-2">
          <button
            @click="$emit('addMedication')"
            class="w-full text-left px-4 py-2 hover:bg-gray-100 rounded-lg transition-colors flex items-center gap-2"
          >
            <pill-icon size="20" />
            Add Medications
          </button>
          
          <button
            @click="$emit('createFollowup')"
            class="w-full text-left px-4 py-2 hover:bg-gray-100 rounded-lg transition-colors flex items-center gap-2"
          >
            <calendar-icon size="20" />
            Create Follow-up
          </button>
          
          <button
            @click="$emit('endSession')"
            class="w-full text-left px-4 py-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors flex items-center gap-2"
          >
            <x-circle-icon size="20" />
            End Session
          </button>
        </div>
        
        <div class="p-4 border-t">
          <button
            @click="$emit('close')"
            class="w-full px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { PillIcon, CalendarIcon, XCircleIcon } from 'lucide-vue-next'
  
  export default {
    name: 'OptionsModal',
    components: {
      PillIcon,
      CalendarIcon,
      XCircleIcon
    }
  }
  </script>
  
  