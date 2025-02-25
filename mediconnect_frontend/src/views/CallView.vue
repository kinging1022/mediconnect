<template>
    <main class="w-full h-screen bg-gray-50">
      <waiting-room v-if="callState === 'waiting'" />
      <video-call 
        v-if="callState === 'connected'" 
        @connection-lost="handleConnectionLost" 
      />
      <reconnecting-screen 
        v-if="callState === 'reconnecting'" 
        @reconnect="handleReconnect" 
      />
    </main>
  </template>
  
  <script>
  import WaitingRoom from '@/components/Call/WaitingRoom.vue';
  import ReconnectingScreen from '@/components/Call/ReconnectingScreen.vue';
  import VideoCall from '@/components/Call/VideoCall.vue';
  
  export default {
    name: 'App',
    components: {
      WaitingRoom,
      VideoCall,
      ReconnectingScreen,
      
      

    },
    data() {
      return {
        callState: 'waiting',
      }
    },
    watch: {
      callState: {
        immediate: true,
        handler(newState) {
          if (newState === 'waiting') {
            setTimeout(() => {
              this.callState = 'connected'
            }, 5000)
          }
        }
      }
    },
    methods: {
      handleConnectionLost() {
        this.callState = 'reconnecting'
      },
      handleReconnect() {
        this.callState = 'connected'
      }
    }
  }
  </script>