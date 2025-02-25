<template>
    <div class="flex justify-start mb-4">
      <div class="bg-gray-100 rounded-lg px-4 py-2 rounded-tl-none">
        <div class="flex space-x-2">
          <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
          <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
          <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'TypingIndicator'
  }
  </script>
  
  <style scoped>
  .animate-bounce {
    animation: bounce 1s infinite;
  }
  
  @keyframes bounce {
    0%, 100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(-25%);
    }
  }
  
  [animation-delay="-0.3s"] {
    animation-delay: -0.3s;
  }
  
  [animation-delay="-0.15s"] {
    animation-delay: -0.15s;
  }
  </style>
  
  