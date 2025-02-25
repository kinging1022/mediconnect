<template>
    <div class="w-80 bg-white border-l border-gray-200 flex flex-col">
      <div class="p-4 border-b border-gray-200">
        <h2 class="text-lg font-semibold">Chat</h2>
      </div>
      <div class="flex-1 p-4 overflow-y-auto">
        <div class="space-y-4">
          <div class="bg-gray-100 p-3 rounded-lg">
            <p class="text-sm text-gray-900">
              Hi, how are you feeling today?
            </p>
            <span class="text-xs text-gray-500">Doctor • 10:30 AM</span>
          </div>
        </div>
      </div>
      <div class="p-4 border-t border-gray-200">
        <input
          type="text"
          placeholder="Type a message..."
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ChatSidebar'
  }
  </script>