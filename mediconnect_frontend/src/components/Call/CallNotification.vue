<template>
    <div 
      class="fixed inset-0 flex items-start justify-center z-50 p-4 sm:pt-16"
      v-if="show"
    >
      <!-- Backdrop -->
      <div 
        class="absolute inset-0 bg-black/40 backdrop-blur-sm"
        @click="$emit('decline')"
      ></div>
  
      <!-- Notification Card -->
      <div 
        class="w-full max-w-md bg-white rounded-2xl shadow-2xl relative z-10 animate-notification"
      >
        <!-- Top Pattern -->
        <div class="bg-emerald-500 h-24 rounded-t-2xl relative overflow-hidden">
          <div class="absolute inset-0 opacity-10">
            <activity-icon 
              v-for="n in 8" 
              :key="n" 
              class="w-12 h-12 text-white transform rotate-45"
              :style="{
                position: 'absolute',
                top: `${Math.random() * 100}%`,
                left: `${Math.random() * 100}%`
              }"
            />
          </div>
        </div>
  
        <!-- Caller Avatar -->
        <div class="relative -mt-12 mb-4 px-6">
          <div class="relative w-24 h-24 mx-auto">
            <div class="absolute inset-0 bg-white/80 rounded-full animate-ping"></div>
            <div class="relative w-full h-full bg-white rounded-full shadow-lg border-4 border-emerald-500 flex items-center justify-center">
              <user-icon class="w-12 h-12 text-emerald-500" />
            </div>
          </div>
        </div>
  
        <!-- Call Information -->
        <div class="px-6 pb-6 text-center space-y-4">
          <div class="space-y-1">
            <h2 class="text-xl font-bold text-gray-900">
              Incoming Call from
            </h2>
            <h3 class="text-2xl font-bold text-emerald-600">
              Dr. {{ doctor.first_name }} {{ doctor.last_name }}
            </h3>
            <p class="text-gray-500 flex items-center justify-center gap-2">
              <stethoscope-icon class="w-4 h-4" />
              {{ doctor.speciality }}
            </p>
          </div>
  
          
  
          <!-- Action Buttons -->
          <div class="grid grid-cols-2 gap-4 pt-4">
            <button 
              @click="$emit('decline')"
              class="flex items-center justify-center gap-2 px-6 py-3 rounded-full bg-red-50 text-red-600 hover:bg-red-100 transition-colors duration-200 group"
            >
              <phone-off-icon class="w-5 h-5 group-hover:rotate-12 transition-transform" />
              Decline
            </button>
            <button 
              @click="$emit('accept')"
              class="flex items-center justify-center gap-2 px-6 py-3 rounded-full bg-emerald-500 text-white hover:bg-emerald-600 transition-colors duration-200 group"
            >
              <phone-icon class="w-5 h-5 group-hover:rotate-12 transition-transform" />
              Accept
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { 
    Phone, 
    PhoneOff, 
    User, 
    Activity,
    Clock,
    Stethoscope
  } from 'lucide-vue-next'
  
  export default {
    name: 'CallNotification',
    components: {
      PhoneIcon: Phone,
      PhoneOffIcon: PhoneOff,
      UserIcon: User,
      ActivityIcon: Activity,
      ClockIcon: Clock,
      StethoscopeIcon: Stethoscope
    },
    props: {
      show: {
        type: Boolean,
        default: false
      },
      doctor: {
        type: Object,
        required: true,
        default: () => ({ first_name: '', last_name: '' }), // Default values
        validator: (prop) => {
          return prop.hasOwnProperty('first_name') && prop.hasOwnProperty('last_name');
        },
      },
      userStore: {
        type: Object,
        required: true,
        validator: (prop) => {
          return prop.hasOwnProperty('user') && prop.user.hasOwnProperty('role');
        },
      },
    },
    methods: {
      formatTime(date) {
        return new Date(date).toLocaleTimeString([], {
          hour: '2-digit',
          minute: '2-digit'
        })
      }
    },
    mounted() {
      // Trigger vibration if supported
      if ('vibrate' in navigator) {
        navigator.vibrate([200, 100, 200])
      }
    }
  }
  </script>
  
  <style scoped>
  @keyframes notification-appear {
    0% {
      transform: translateY(-20px);
      opacity: 0;
    }
    100% {
      transform: translateY(0);
      opacity: 1;
    }
  }
  
  .animate-notification {
    animation: notification-appear 0.3s ease-out forwards;
  }
  </style>