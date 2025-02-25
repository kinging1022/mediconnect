<template>
    <div class="w-full h-screen bg-gray-50 flex flex-col items-center justify-center">
      <div class="text-center space-y-6">
        <loader2-icon class="w-12 h-12 text-blue-500 animate-spin mx-auto" />
        <h1 class="text-2xl font-semibold text-gray-900">
          Connection Lost
        </h1>
        <p class="text-gray-600">
          Attempting to reconnect automatically...
        </p>
        <button
          @click="handleReconnect"
          class="mt-4 px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          Reconnect Manually
        </button>
      </div>
    </div>
  </template>
  
  <script>
  import { Loader2 } from 'lucide-vue-next'
  
  export default {
    name: 'ReconnectingScreen',
    components: {
      Loader2Icon: Loader2
    },
    methods: {
      handleReconnect() {
        this.$emit('reconnect')
      }
    }
  }
  </script>