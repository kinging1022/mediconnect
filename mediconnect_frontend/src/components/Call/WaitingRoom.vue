<template>
    <div class="w-full h-screen bg-gray-50 flex flex-col items-center justify-center">
      <div class="text-center space-y-6">
        <loader2-icon class="w-12 h-12 text-blue-500 animate-spin mx-auto" />
        <h1 class="text-2xl font-semibold text-gray-900">
          Initaiting call enviroment ..
        </h1>
        <p class="text-gray-600">Estimated wait time: few seconds ...</p>
        
      </div>
    </div>
  </template>
  
  <script>
  import { Loader2 } from 'lucide-vue-next'
  
  export default {
    name: 'WaitingRoom',
    components: {
      Loader2Icon: Loader2
    }
  }
  </script>