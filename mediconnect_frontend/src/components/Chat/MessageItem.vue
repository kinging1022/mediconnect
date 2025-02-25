<template>
    <div :class="[
      'flex mb-4 items-end gap-2',
      message.created_by.role === 'patient' ? 'justify-end' : 'justify-start'
    ]">
      <!-- Avatar for doctor -->
      <div v-if="message.created_by.role === 'doctor'" 
        class="w-8 h-8 rounded-full bg-white border-2 border-blue-500 flex items-center justify-center flex-shrink-0"
      >
        <user-icon size="16" class="text-blue-500" />
      </div>
  
      <div :class="messageClasses">
        <!-- Text Message -->
        <div v-if="message.type === 'text'">
          {{ message.body }}
        </div>
  
        <!-- Notification Message -->
        <div v-else-if="message.type === 'notification'"
          class="flex items-center gap-2 text-white"
        >
          <bell-icon size="16" />
          {{ message.body }}
        </div>
  
        <!-- Image Message -->
        <img
          v-else-if="message.type === 'image'"
          :src="message.get_file"
          class="rounded-lg max-w-[200px]"
          alt="Shared image"
        />
  
        <!-- Video Message -->
        <video
          v-else-if="message.type === 'video'"
          :src="message.get_file"
          class="rounded-lg max-w-[200px]"
          controls
        />
      </div>
  
      <!-- Avatar for patient -->
      <div v-if="message.created_by.role === 'patient'"
        class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center flex-shrink-0"
      >
        <user-icon size="16" class="text-white" />
      </div>
    </div>
  </template>
  
  <script>
  import { UserIcon, BellIcon } from 'lucide-vue-next'
  
  export default {
    name: 'MessageItem',
    components: {
      UserIcon,
      BellIcon
    },
    props: {
      message: {
        type: Object,
        required: true
      }
    },
    computed: {
      messageClasses() {
        const baseClasses = 'max-w-[80%] rounded-lg px-4 py-2'
        
        // Notification messages
        if (this.message.type === 'notification') {
          return `${baseClasses} bg-amber-500 w-full max-w-[90%] mx-auto text-center shadow-sm`
        }
        
        // Patient messages (blue background, white text, rounded on the right)
        if (this.message.created_by.role === 'patient') {
          return `${baseClasses} bg-blue-500 text-white rounded-tr-none`
        }
        
        // Doctor messages (gray background, rounded on the left)
        return `${baseClasses} bg-gray-100 rounded-tl-none`
      }
    }
  }
  </script>