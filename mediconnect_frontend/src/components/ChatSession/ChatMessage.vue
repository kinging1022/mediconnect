<template>
    <div class="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50">
      <div
        v-for="message in messages"
        :key="message.id"
        :class="[
          'flex',
          message.created_by.role === 'patient' ? 'justify-end' : 'justify-start',
          message.type === 'notification' ? 'justify-center' : ''
        ]"
      >
        <template v-if="message.type !== 'notification'">
          <!-- Doctor Icon (White Background) -->
          <div
            v-if="message.created_by.role === 'doctor'"
            class="w-8 h-8 rounded-full bg-white flex items-center justify-center border border-gray-300 mr-2 self-end"
          >
            <UserIcon class="w-4 h-4 text-gray-500" />
          </div>
  
          <div
            :class="[
              'max-w-[70%] rounded-2xl px-4 py-2',
              message.created_by.role === 'patient'
                ? 'bg-blue-600 text-white rounded-br-none'
                : 'bg-white text-gray-900 rounded-bl-none shadow-sm'
            ]"
          >
            <!-- Text message -->
            <p v-if="message.type === 'text'" class="whitespace-pre-wrap">{{ message.body }}</p>
            
            <!-- Image message -->
            <img v-else-if="message.type === 'image'" :src="message.body" alt="Image message" class="max-w-full rounded-lg" />
            
            <!-- Video message -->
            <video v-else-if="message.type === 'video'" controls class="max-w-full rounded-lg">
              <source :src="message.body" type="video/mp4">
              Your browser does not support the video tag.
            </video>
  
            <div class="flex items-center justify-end space-x-1 mt-1">
              <span
                :class="[
                  'text-xs',
                  message.created_by.role === 'patient' ? 'text-blue-100' : 'text-gray-500'
                ]"
              >
                {{ formatTimestamp(message.created_at_formatted) }}
              </span>
              <div v-if="message.created_by.role === 'patient'" class="text-blue-100">
                <div v-if="message.status === 'read'" class="flex">
                  <CheckIcon class="w-3 h-3" />
                  <CheckIcon class="w-3 h-3 -ml-1" />
                </div>
                <CheckIcon v-else class="w-3 h-3" />
              </div>
            </div>
          </div>
  
          <!-- Patient Icon (Blue Background) -->
          <div
            v-if="message.created_by.role === 'patient'"
            class="w-8 h-8 rounded-full bg-blue-600 ml-2 flex items-center justify-center self-end"
          >
            <UserIcon class="w-4 h-4 text-white" />
          </div>
        </template>
  
        <!-- Notification message -->
        <div
          v-else
          class="w-full bg-yellow-100 text-yellow-800 px-4 py-2 rounded-lg flex items-center"
        >
          <BellIcon class="w-5 h-5 mr-2 flex-shrink-0" />
          <p class="flex-grow">{{ message.body }}</p>
          <span class="text-xs text-yellow-600 ml-2">{{ formatTimestamp(message.created_at_formatted) }}</span>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { Check, User, Bell } from 'lucide-vue-next'
  
  export default {
    name: 'ChatMessages',
    components: {
      CheckIcon: Check,
      UserIcon: User,
      BellIcon: Bell
    },
    props: {
      messages: {
        type: Array,
        required: true,
        validator: (value) => {
          return value.every(message => 
            ['text', 'notification', 'image', 'video'].includes(message.type)
          );
        }
      }
    },
    methods: {
      formatTimestamp(timestamp) {
        const createdAt = new Date(timestamp);
        if (isNaN(createdAt.getTime())) {
          console.error("Invalid timestamp:", timestamp);
          return "Invalid date";
        }
  
        const now = new Date();
        const diffInMinutes = Math.floor((now - createdAt) / (1000 * 60)); 
  
        if (diffInMinutes < 1) return "Just now";
        if (diffInMinutes === 1) return "1 minute ago";
        if (diffInMinutes < 60) return `${diffInMinutes} minutes ago`;
  
        const diffInHours = Math.floor(diffInMinutes / 60);
        if (diffInHours === 1) return "1 hour ago";
        if (diffInHours < 24) return `${diffInHours} hours ago`;
  
        const diffInDays = Math.floor(diffInHours / 24);
        if (diffInDays === 1) return "1 day ago";
        if (diffInDays < 7) {
          return `${createdAt.toLocaleDateString(undefined, { weekday: "long" })}, ${createdAt.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' })}`;
        }
  
        return createdAt.toLocaleDateString(undefined, { month: "long", day: "numeric" });
      },
    }
  }
  </script>