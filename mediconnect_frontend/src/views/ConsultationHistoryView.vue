
<template>
    <div class="flex flex-col h-screen w-full bg-white">
      <ChatHeader
        :doctor="doctor"
        :patient="patient"
        :user-store="userStore"
        @toggleModal="isModalOpen = !isModalOpen"
      />
      <ChatMessage
        :messages="messages"
      />
      
    </div>
  </template>
  
  <script>
   import ChatHeader from '@/components/Chat/ChatHeader.vue';
   import ChatMessage from '@/components/Chat/ChatMessage.vue';
  import axios from 'axios'
  import { useUserStore } from '@/stores/user'
  import { useToastStore } from '@/stores/toast'
  
  export default {
    name: 'ChatPage',
    components: {
      ChatHeader,
      ChatMessage,
      
    },
  
    setup() {
      const userStore = useUserStore()
      const toastStore = useToastStore()
      return {
        userStore,
        toastStore
      }
    },
  
    data() {
      return {
        messages: [],
        patient:{first_name:'', last_name:''},
        doctor: {first_name:'', last_name:''},
        
      }
    },
  
    computed: {
      sessionId() {
        return this.userStore.activeSession.id || null
      }
    },
  
    mounted() {
      this.getMessages()
    },
  
    methods: {
      async getMessages() {
        try {
          const response = await axios.get('session/', {
            params: {
              sessionId: this.$route.params.id
            }
          })
  
          if (response.status === 200) {
            const users = response.data.users
            this.patient = users.find(user => user.role === "patient");
            this.doctor = users.find(user => user.role === "doctor")
            this.messages = response.data.messages
          }
        } catch (error) {
          console.error('Error fetching messages:', error)
        }
      },
  
      
      
    }
  }
  </script>
  
  