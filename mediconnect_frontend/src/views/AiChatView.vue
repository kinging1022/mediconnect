<template>
    <div class="flex flex-col h-screen w-full bg-white">
      <!-- Sticky Header -->
      <header class="fixed top-0 left-0 right-0 flex items-center gap-2 p-4 bg-white border-b shadow-sm z-10">
        <stethoscope-icon class="w-6 h-6 text-blue-500" />
        <h1 class="text-xl font-semibold text-gray-800">Mediconnect AI Doctor</h1>
      </header>
  
      <!-- Messages -->
      <div 
        class="flex-1 overflow-y-auto p-4 mt-16 mb-20" 
        ref="messagesContainer"
      >
        <div v-for="(message, index) in messages" :key="index">
          <div :class="['flex', message.isBot ? 'justify-start' : 'justify-end', 'mb-4']">
            <div
              :class="[
                'max-w-[80%] rounded-lg px-4 py-2',
                message.isBot
                  ? 'bg-gray-100 rounded-tl-none'
                  : 'bg-blue-500 text-white rounded-tr-none',
              ]"
            >
              {{ message.content }}
            </div>
          </div>
        </div>
  
        <!-- Typing Indicator -->
        <div v-if="isTyping" class="flex justify-start mb-4">
          <div class="bg-gray-100 rounded-lg px-4 py-2 rounded-tl-none">
            <div class="flex space-x-2">
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
            </div>
          </div>
        </div>
  
        <div ref="messagesEnd"></div>
      </div>
  
      <!-- Sticky Chat Input -->
      <form 
        @submit.prevent="handleSubmit" 
        class="fixed bottom-0 left-0 right-0 flex gap-2 p-4 border-t bg-white z-10"
      >
        <input
          type="text"
          v-model="message"
          placeholder="Type your message..."
          class="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          class="p-2 text-white bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors"
        >
          <send-icon size="20" />
        </button>
      </form>
    </div>
  </template>
  
  <script>
  import { SendIcon, StethoscopeIcon } from 'lucide-vue-next'
  
  export default {
    name: 'App',
    components: {
      SendIcon,
      StethoscopeIcon
    },
    data() {
      return {
        messages: [],
        isTyping: false,
        message: ''
      }
    },
    methods: {
      scrollToBottom() {
        this.$nextTick(() => {
          this.$refs.messagesEnd.scrollIntoView({ behavior: 'smooth' })
        })
      },
      async simulateBotResponse(userMessage) {
        this.isTyping = true
        await new Promise(resolve => setTimeout(resolve, 2000))
        this.isTyping = false
        this.messages.push({
          content: `Response to: ${userMessage}`,
          isBot: true
        })
      },
      handleSubmit() {
        if (this.message.trim()) {
          this.messages.push({
            content: this.message,
            isBot: false
          })
          this.simulateBotResponse(this.message)
          this.message = ''
        }
      }
    },
    watch: {
      messages: {
        handler() {
          this.scrollToBottom()
        },
        deep: true
      },
      isTyping() {
        this.scrollToBottom()
      }
    }
  }
  </script>
  
  <style>
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