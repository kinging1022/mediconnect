<template>
    <header class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-end items-center h-16">
          <button class="relative p-2 text-gray-400 hover:text-gray-500">
            <Bell class="w-5 h-5" />
            <span class="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>
        </div>
      </div>
    </header>
  </template>
  
  <script>
  import { Bell } from 'lucide-vue-next';
  
  export default {
    name: 'AppHeader',
    components: {
      Bell,
    },
  };
  </script>
  
  