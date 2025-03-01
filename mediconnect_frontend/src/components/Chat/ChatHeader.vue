<template>
    <header class="fixed top-0 left-0 right-0 flex items-center justify-between p-4 bg-white border-b shadow-sm z-10">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-semibold">
          {{ displayInitials }}
        </div>
        <h1 class="text-xl font-semibold text-gray-800">{{ displayName }}</h1>
      </div>
  
      <div 
        v-if="userStore.user.role === 'doctor'"
        class="flex items-center gap-2"
      >
        <button
          class="p-2 text-gray-600 hover:bg-gray-100 rounded-full transition-colors"
          @click="$emit('videoCall')"
        >
          <video-icon size="20" />
        </button>
        
        <button
          class="p-2 text-gray-600 hover:bg-gray-100 rounded-full transition-colors"
          @click="$emit('toggleModal')"
        >
          <more-vertical-icon size="20" />
        </button>
      </div>
    </header>
  </template>
  
  <script>
  import { Phone, Video, MoreVertical } from 'lucide-vue-next';
  
  export default {
    name: 'ChatHeader',
  
    components: {
      PhoneIcon: Phone,
      VideoIcon: Video,
      MoreVerticalIcon: MoreVertical,
    },
  
    props: {
      doctor: {
        type: Object,
        required: true,
        default: () => ({ first_name: '', last_name: '' }), 
        validator: (prop) => {
          return prop.hasOwnProperty('first_name') && prop.hasOwnProperty('last_name');
        },
      },
      patient: {
        type: Object,
        required: true,
        default: () => ({ first_name: '', last_name: '' }), 
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
  
    computed: {
      displayName() {
        if (this.userStore.user.role === 'doctor') {
          return `${this.patient.first_name || ''} ${this.patient.last_name || ''}`.trim();
        } else {
          return `Dr. ${this.doctor.first_name || ''} ${this.doctor.last_name || ''}`.trim();
        }
      },
  
      displayInitials() {
        if (this.userStore.user.role === 'doctor') {
          return `${this.patient.first_name?.[0]?.toUpperCase() || ''}${this.patient.last_name?.[0]?.toUpperCase() || ''}`;
        } else {
          return `${this.doctor.first_name?.[0]?.toUpperCase() || ''}${this.doctor.last_name?.[0]?.toUpperCase() || ''}`;
        }
      },
    },
  };
  </script>