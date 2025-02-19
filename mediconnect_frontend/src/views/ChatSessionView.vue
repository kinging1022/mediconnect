<!-- ChatPage.vue -->
<template>
    <div class="w-full min-h-screen bg-gray-50">
      <div class="max-w-4xl mx-auto h-screen flex flex-col">
        <chat-header
          :doctor="doctor"
          :patient="patient"
          :user-store="userStore"
          @open-options="isOptionsModalOpen = true"
        />
        <chat-message :messages="messages" />
        <chat-input
          v-model="newMessage"
          :session-ended="sessionEnded"
          @send="sendText"
        />
      </div>
      <option-modal
        v-if="isOptionsModalOpen"
        @close="isOptionsModalOpen = false"
        @open-medication="openMedicationModal"
        @add-followup="addFollowup"
        @end-session="endSession"
      />
      <medication-modal
        v-if="isMedicationModalOpen"
        :medications="medications"
        @close="isMedicationModalOpen = false"
        @add-medication="handleAddMedication"
        @remove-medication="handleRemoveMedication"
        @change-medication="handleMedicationChange"
        @submit-medications="handleSubmitMedications"
      />
    </div>
  </template>
  
  <script>
  import ChatHeader from '@/components/ChatSession/ChatHeader.vue'
  import ChatMessage from '@/components/ChatSession/ChatMessage.vue'
  import ChatInput from '@/components/ChatSession/ChatInput.vue'
  import OptionModal from '@/components/ChatSession/OptionModal.vue'
  import MedicationModal from '@/components/ChatSession/MedicationModal.vue'
  import axios from 'axios'
  import { useUserStore } from '@/stores/user'
  import { useToastStore } from '@/stores/toast'
  
  export default {
    name: 'ChatPage',
    components: {
      ChatHeader,
      ChatMessage,
      ChatInput,
      OptionModal,
      MedicationModal
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
        newMessage: '',
        isOptionsModalOpen: false,
        isMedicationModalOpen: false,
        medications: [{
          name: "",
          weight: "",
          dosage: "",
        }],
        socket: null,
        isConnecting: false,
        reconnectAttempts: 0,
        maxReconnectAttempts: 5,
        messageQueue: [],
        sessionEnded: false
      }
    },
  
    computed: {
      doctor() {
        if(this.userStore.activeSession){
          const users = this.userStore.activeSession.users 
          return users.find(user => user.role === "doctor") || null
        }
        
      },
      patient() {
        if(this.userStore.activeSession){
          const users = this.userStore.activeSession.users 
          return users.find(user => user.role === "patient") || null
        }
        
      },
      sessionId() {
        return this.userStore.activeSession.id || null
      }
    },
  
    mounted() {
      this.getMessages()
      this.connectWebsocket()
    },
  
    methods: {
      async getMessages() {
        try {
          const response = await axios.get('session/messages/', {
            params: {
              sessionId: this.$route.params.id
            }
          })
  
          if (response.status === 200) {
            this.messages = response.data
          }
        } catch (error) {
          console.error('Error fetching messages:', error)
        }
      },
  
      connectWebsocket() {
        if (!this.sessionId || this.isConnecting) return;
        
        this.isConnecting = true;
        const token = this.userStore.user.access;
        const wsUrl = `ws://localhost:8000/ws/chat/${this.sessionId}/?token=${token}`;
        
        try {
          this.socket = new WebSocket(wsUrl);
          
          this.socket.onopen = () => {
            console.log("Connected to WebSocket");
            this.isConnecting = false;
            this.reconnectAttempts = 0;
            
            // Send any queued messages
            while (this.messageQueue.length > 0) {
              const queuedMessage = this.messageQueue.shift();
              this.sendMessage(queuedMessage.message, queuedMessage.type);
            }
          };
  
          this.socket.onmessage = (event) => {
            try {
              const data = JSON.parse(event.data);
              
              // Handle session ended event
              if (data.type === 'session_ended') {
                this.handleSessionEnded(data);
                return;
              }
  
              // Handle error messages
              if (data.type === 'error') {
                console.error(data.message);
                this.toastStore.showToast(5000, data.message, "bg-red-500");
                return;
              }
  
              // Handle regular messages
              if (data?.data) {
                this.messages.push(data.data);
              }
            } catch (error) {
              console.error("Error parsing WebSocket message:", error);
            }
          };

          
          this.socket.onclose = (event) => {
            this.isConnecting = false;
            console.log(`WebSocket disconnected. Code: ${event.code}, Reason: ${event.reason}`);
            
            if (!this.sessionEnded && this.reconnectAttempts < this.maxReconnectAttempts) {
              const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 10000);
              setTimeout(() => {
                this.reconnectAttempts++;
                console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
                this.connectWebsocket();
              }, delay);
            }
          };
  
          this.socket.onerror = (error) => {
            console.error("WebSocket error:", error);
          };
          
        } catch (error) {
          this.isConnecting = false;
          console.error("Error creating WebSocket connection:", error);
        }
      },
  
      async sendMessage(message, type) {
        if (this.sessionEnded) {
          console.log("Cannot send message - session has ended");
          return;
        }
  
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
          this.messageQueue.push({ message, type });
          console.log("Message queued - WebSocket is not connected");
          return;
        }
  
        try {
          const payload = {
            message: message,
            type: type,
            timestamp: new Date().toISOString()
          };
          
          await this.socket.send(JSON.stringify(payload));
          this.newMessage = ""; 
        } catch (error) {
          console.error("Error sending message:", error);
        }
      },
  
      async sendText() {
        const message = this.newMessage.trim();
        if (message) {
          await this.sendMessage(message, 'text');
        }
      },
  
      async addFollowup() {
        try {
          const response = await axios.post(`sessions/followup/${this.sessionId}/`, {});
  
          if (response.status === 201) {
            this.newMessage = response.data.message;
            await this.sendMessage(this.newMessage, 'notification');
          }
          this.isOptionsModalOpen = false;
        } catch (error) {
          console.error(error);
        }
      },
  
      openMedicationModal() {
        this.isOptionsModalOpen = false;
        this.isMedicationModalOpen = true;
      },
  
      handleAddMedication() {
        this.medications.push({
          name: "",
          weight: "",
          dosage: "",
        });
      },
  
      handleRemoveMedication(index) {
        this.medications.splice(index, 1);
      },
  
      handleMedicationChange(index, field, value) {
        this.medications[index][field] = value;
      },
  
      async handleSubmitMedications() {
        try {
          const response = await axios.post(
            `sessions/medications/${this.sessionId}/`,
            this.medications
          );
  
          if (response.status === 201) {
            this.newMessage = response.data.message;
            await this.sendMessage(this.newMessage, 'notification');
          }
  
          // Reset form
          this.medications = [{
            name: "",
            weight: "",
            dosage: "",
          }];
          this.isMedicationModalOpen = false;
  
        } catch (error) {
          if (error.response?.data?.error) {
            const errorMessage = error.response.data.error;
            this.toastStore.showToast(5000, errorMessage, "bg-red-500");
          }
        }
      },
  
      async endSession() {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
          console.error("Cannot end session - WebSocket is not connected");
          return;
        }

        console.log('This is trying to end session')
  
        try {
          const payload = {
            type: 'end_session',
            message: 'Ending session'
          };
          
          console.log("Sending end session payload:", payload);
          await this.socket.send(JSON.stringify(payload));
          console.log("End session message sent");
          this.isOptionsModalOpen = false;
        } catch (error) {
          console.error("Error ending session:", error);
        }
      },
  
      handleSessionEnded(data) {
        this.sessionEnded = true;
        
        // Add the end session message to the chat
        if (data.data?.message) {
          this.messages.push(data.data.message);
        }
        this.userStore.clearActiveSession()
        // Show notification to users
        this.toastStore.showToast(
          5000, 
          "This session has ended", 
          "bg-blue-500"
        );
  
        // Disable input
        this.newMessage = '';
        
        // Emit event to parent component
        this.$emit('session-ended');
      },
  
      beforeUnmount() {
        if (this.socket) {
          this.socket.close(1000, "Component unmounting");
        }
      }
    }
  }
  </script>
  
  