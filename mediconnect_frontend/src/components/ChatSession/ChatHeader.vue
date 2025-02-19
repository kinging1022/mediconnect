<template>
    <div class="bg-white border-b px-6 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <div class="relative">
            <div class="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-semibold text-lg">
              {{ displayInitials }}
            </div>
            <div class="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-white"></div>
          </div>
          <div>
            <h2 class="text-lg font-semibold text-gray-900">{{ displayName }}</h2>
          </div>
        </div>
        <!-- Show call buttons and options only for the doctor -->
        <div v-if="userStore.user.role === 'doctor'" class="flex items-center space-x-4">
          <button class="p-2 hover:bg-gray-100 rounded-full transition-colors">
            <phone-icon class="w-5 h-5 text-blue-600" />
          </button>
          <button class="p-2 hover:bg-gray-100 rounded-full transition-colors">
            <video-icon class="w-5 h-5 text-blue-600" />
          </button>
          <button 
            @click="$emit('open-options')" 
            class="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <more-vertical-icon class="w-5 h-5 text-gray-600" />
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { Phone, Video, MoreVertical } from 'lucide-vue-next'
  
  export default {
    name: 'ChatHeader',
    
    components: {
      PhoneIcon: Phone,
      VideoIcon: Video,
      MoreVerticalIcon: MoreVertical
    },
    
    props: {
      doctor: {
        type: Object,
        required: true,
        validator: (prop) => {
          return prop.hasOwnProperty('first_name') && prop.hasOwnProperty('last_name')
        }
      },
      patient: {
        type: Object,
        required: true,
        validator: (prop) => {
          return prop.hasOwnProperty('first_name') && prop.hasOwnProperty('last_name')
        }
      },
      userStore: {
        type: Object,
        required: true,
        validator: (prop) => {
          return prop.hasOwnProperty('user') && prop.user.hasOwnProperty('role')
        }
      }
    },
  
    computed: {
      displayName() {
        if (this.userStore.user.role === 'doctor') {
          return `${this.patient.first_name} ${this.patient.last_name}`
        } else {
          return `Dr. ${this.doctor.first_name} ${this.doctor.last_name}`
        }
      },
  
      displayInitials() {
        if (this.userStore.user.role === 'doctor') {
          return `${this.patient.first_name[0]}${this.patient.last_name[0]}`
        } else {
          return `${this.doctor.first_name[0]}${this.doctor.last_name[0]}`
        }
      }
    }
  }
  </script>
  