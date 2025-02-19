<template>
    <div class="bg-white border-t p-4">
      <div class="flex items-center space-x-4">
        <div class="flex-1 relative">
          <textarea
            :value="modelValue"
            @input="$emit('update:modelValue', $event.target.value)"
            @keypress="handleKeyPress"
            :placeholder="sessionEnded ? 'This session has ended' : 'Type your message...'"
            :disabled="sessionEnded"
            class="w-full resize-none rounded-2xl border border-gray-200 px-4 py-3 text-gray-900 focus:border-blue-600 focus:ring-1 focus:ring-blue-600 focus:outline-none min-h-[48px] max-h-32 disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed"
            rows="1"
          ></textarea>
        </div>
        <button
          @click="$emit('send')"
          :disabled="sessionEnded || !modelValue.trim()"
          :class="[
            'p-3 rounded-full transition-colors',
            !sessionEnded && modelValue.trim()
              ? 'bg-blue-600 text-white hover:bg-blue-700'
              : 'bg-gray-100 text-gray-400',
            sessionEnded && 'cursor-not-allowed opacity-50'
          ]"
        >
          <send-icon class="w-5 h-5" />
        </button>
      </div>
    </div>
  </template>
  
  <script>
  import { Send } from 'lucide-vue-next'
  
  export default {
    name: 'ChatInput',
    components: {
      SendIcon: Send
    },
    props: {
      modelValue: {
        type: String,
        required: true
      },
      sessionEnded: {
        type: Boolean,
        default: false
      }
    },
    methods: {
      handleKeyPress(e) {
        if (e.key === 'Enter' && !e.shiftKey && !this.sessionEnded) {
          e.preventDefault()
          this.$emit('send')
        }
      }
    }
  }
  </script>