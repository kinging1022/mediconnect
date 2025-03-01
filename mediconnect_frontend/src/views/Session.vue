<template>
    <div v-if="state === 'chat'">
        <div class="flex flex-col h-screen w-full bg-white">
            <ChatHeader
                :doctor="doctor"
                :patient="patient"
                :user-store="userStore"
                @toggleModal="isModalOpen = !isModalOpen"
                @videoCall = "startCall"
            />
            <ChatMessage
                :messages="messages"
                :isTyping="isTyping"
            />
            <ChatInput
                v-model="newMessage"
                :session-ended="sessionEnded"
                @send="sendChatMessage"
                @typing="handleTyping"
            />
        
            <OptionModal
                v-if="isModalOpen"
                @close="isModalOpen = false"
                @addMedication="openMedicationModal"
                @createFollowup="handleCreateFollowup"
                @endSession="endSession"
            />
        
            <MedicationModal
                v-if="isMedicationModalOpen"
                :medications="medications"
                @close="isMedicationModalOpen = false"
                @add-medication="handleAddMedication"
                @remove-medication="handleRemoveMedication"
                @change-medication="handleMedicationChange"
                @submit-medications="handleSubmitMedications"
            />
            <CallNotification  :doctor="doctor" :user-store="userStore" :show="showIncommingCall" @accept="handleAccept" @decline=" handleEndCall"/>

        </div>
        

    </div>

    <div v-if="state === 'call'">
        <WaitingRoom v-if="callState === 'dialing'":patient = "patient"/>
        <VideoCall v-if="callState === 'incall'"   :token="callToken"  :uid="callUid" :channel="channelName" @end-call="handleEndCall"/>
    </div>
    
  </template>
  
  <script>
  import ChatHeader from '@/components/Chat/ChatHeader.vue';
  import ChatMessage from '@/components/Chat/ChatMessage.vue';
  import ChatInput from '@/components/Chat/Chatinput.vue';
  import OptionModal from '@/components/Chat/OptionModal.vue';
  import MedicationModal from '@/components/Chat/MedicationModal.vue';
  import WaitingRoom from '@/components/Call/WaitingRoom.vue'
  import CallNotification from '@/components/Call/CallNotification.vue';
  import { useUserStore } from '@/stores/user';
  import { useToastStore } from '@/stores/toast';
  import VideoCall from '@/components/Call/VideoCall.vue';

  import axios from 'axios';
  
  export default {
    name: 'ChatLayout',
    components: {
      ChatHeader,
      ChatMessage,
      ChatInput,
      OptionModal,
      WaitingRoom,
      CallNotification,
      MedicationModal,
      VideoCall

    },
    setup() {
      const userStore = useUserStore();
      const toastStore = useToastStore();
      return {
        userStore,
        toastStore,
      };
    },
    data() {
      return {
        state: 'chat',
        callState: null,
        callToken: null,
        callUid: null,
        channelName:null,
        showIncommingCall: false,
        messages: [],
        isTyping: false,
        isModalOpen: false,
        isMedicationModalOpen: false,
        medications: [{
          name: '',
          weight: '',
          dosage: '',
        }],
        newMessage: '',
        socket: null,
        isConnecting: false,
        reconnectAttempts: 0,
        maxReconnectAttempts: 5,
        messageQueue: [],
        sessionEnded: false,
        reconnectTimeout: null,
      };
    },
    computed: {
      doctor() {
        if (this.userStore.activeSession) {
          const users = this.userStore.activeSession.users;
          return users.find(user => user.role === 'doctor') || null;
        }
        return null;
      },
      patient() {
        if (this.userStore.activeSession) {
          const users = this.userStore.activeSession.users;
          return users.find(user => user.role === 'patient') || null;
        }
        return null;
      },
      sessionId() {
        return this.userStore.activeSession?.id || null;
      },
    },
    mounted() {
      this.initializeChat();
    },
    beforeUnmount() {
      this.cleanup();
    },
    methods: {
      // Initialization and cleanup
      async initializeChat() {
        await this.getMessages();
        this.connectWebsocket();
      },
      cleanup() {
        if (this.socket) {
          this.socket.close(1000, 'Component unmounting');
        }
        if (this.reconnectTimeout) {
          clearTimeout(this.reconnectTimeout);
        }
      },
  
      // WebSocket handling
      connectWebsocket() {
        if (!this.sessionId || this.isConnecting || this.sessionEnded) return;
  
        this.isConnecting = true;
        const token = this.userStore.user.access;
        const wsUrl = `ws://localhost:8000/ws/chat/${this.sessionId}/?token=${token}`;
  
        try {
          this.socket = new WebSocket(wsUrl);
          this.setupWebSocketListeners();
        } catch (error) {
          this.handleConnectionError(error);
        }
      },
      setupWebSocketListeners() {
        this.socket.onopen = this.handleWebSocketOpen;
        this.socket.onmessage = this.handleWebSocketMessage;
        this.socket.onclose = this.handleWebSocketClose;
        this.socket.onerror = this.handleWebSocketError;
      },
      handleWebSocketOpen() {
        console.log('Connected to WebSocket');
        this.isConnecting = false;
        this.reconnectAttempts = 0;
        this.processMessageQueue();
      },
      handleWebSocketMessage(event) {
        try {
          const data = JSON.parse(event.data);
  
          switch (data.type) {
            case 'call_notification_status':
                if(data.user_id !== this.userStore.user.id){
                    this.showIncommingCall = data.incoming_call
                }
            case 'typing_status':
              if (data.user_id !== this.userStore.user.id) {
                this.isTyping = data.is_typing;
              }
              break;
            case 'session_ended':
              this.reconnectAttempts = this.maxReconnectAttempts;
              this.handleSessionEnded(data);
              break;
            case 'error':
              console.error(data.message);
              this.toastStore.showToast(5000, data.message, 'bg-red-500');
              break;
            default:
              if (data?.data) {
                this.messages.push(data.data);
              }
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      },
      handleWebSocketClose(event) {
        this.isConnecting = false;
        console.log(`WebSocket disconnected. Code: ${event.code}, Reason: ${event.reason}`);
  
        if (!this.sessionEnded && this.reconnectAttempts < this.maxReconnectAttempts) {
          this.handleReconnection();
        }
      },
      handleWebSocketError(error) {
        console.error('WebSocket error:', error);
        this.socket?.close();
      },
      handleConnectionError(error) {
        this.isConnecting = false;
        console.error('Error creating WebSocket connection:', error);
        this.toastStore.showToast(5000, 'Connection failed', 'bg-red-500');
      },
      handleReconnection() {
        const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 10000);
        this.reconnectTimeout = setTimeout(() => {
          this.reconnectAttempts++;
          console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
          this.connectWebsocket();
        }, delay);
      },
  
      // Message handling
      async getMessages() {
        try {
          const response = await axios.get('session/messages/', {
            params: {
              sessionId: this.sessionId,
            },
          });
  
          if (response.status === 200) {
            this.messages = response.data;
          }
        } catch (error) {
          console.error('Error fetching messages:', error);
          this.toastStore.showToast(5000, 'Failed to load messages', 'bg-red-500');
        }
      },
      processMessageQueue() {
        console.log('Processing message queue, items:', this.messageQueue.length);
        while (this.messageQueue.length > 0) {
          const queuedMessage = this.messageQueue.shift();
          console.log('Processing queued message:', queuedMessage);
  
          if (queuedMessage.type === 'media' && queuedMessage.file_id) {
            this.sendWebSocketMessage(queuedMessage);
          } else {
            this.sendWebSocketMessage(queuedMessage);
          }
        }
      },
      async uploadFiles(formData) {
        try {
          console.log('Uploading files to API endpoint');
          const uploadUrl = `/sessions/${this.sessionId}/upload/`;
          console.log(`Upload URL: ${uploadUrl}`);
  
          const response = await axios.post(uploadUrl, formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
  
          console.log('File upload response:', response.data);
  
          if (response.data?.files && response.data.files.length > 0) {
            for (const fileData of response.data.files) {
              await this.sendWebSocketMessage({
                type: 'media',
                file_id: fileData.id,
              });
            }
          }
  
          this.newMessage = '';
        } catch (error) {
          console.error('Error uploading files:', error);
          this.toastStore.showToast(5000, 'Failed to upload files', 'bg-red-500');
        }
      },
      async sendWebSocketMessage(payload) {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
          if (payload.type !== 'typing_indicator') {
            console.log('Message queued - WebSocket is not connected', payload);
            this.messageQueue.push(payload);
            if (this.socket?.readyState === WebSocket.CLOSED) {
              this.connectWebsocket();
            }
          }
          return;
        }
  
        try {
          payload.timestamp = new Date().toISOString();
          console.log('Sending WebSocket message:', payload);
          await this.socket.send(JSON.stringify(payload));
        } catch (error) {
          console.error('Error sending message:', error);
          if (payload.type !== 'typing_indicator') {
            this.messageQueue.push(payload);
            this.toastStore.showToast(5000, 'Failed to send message', 'bg-red-500');
          }
        }
      },
      async sendChatMessage(data) {
        if (data instanceof FormData) {
          await this.uploadFiles(data);
        } else if (typeof data === 'string') {
          const message = data.trim();
          if (message) {
            await this.sendWebSocketMessage({
              type: 'text',
              message: message,
            });
          }
        }
        this.newMessage = '';
      },
  
      // Typing indicator
      handleTyping(isTyping) {
        if (!this.sessionEnded && this.socket?.readyState === WebSocket.OPEN) {
          const payload = {
            type: 'typing_indicator',
            is_typing: isTyping,
            timestamp: new Date().toISOString(),
          };
  
          try {
            this.socket.send(JSON.stringify(payload));
          } catch (error) {
            console.error('Error sending typing status:', error);
          }
        }
      },
  
      // Medication handling
      openMedicationModal() {
        this.isModalOpen = false;
        this.isMedicationModalOpen = true;
      },
      handleAddMedication() {
        this.medications.push({
          name: '',
          weight: '',
          dosage: '',
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
            await this.sendWebSocketMessage({
              type: 'notification',
              message: response.data.message,
            });
  
            this.medications = [{
              name: '',
              weight: '',
              dosage: '',
            }];
            this.isMedicationModalOpen = false;
          }
        } catch (error) {
          const errorMessage = error.response?.data?.error || 'Failed to submit medications';
          this.toastStore.showToast(5000, errorMessage, 'bg-red-500');
        }
      },
  
      // Followup handling
      async handleCreateFollowup() {
        try {
          const response = await axios.post(`sessions/followup/${this.sessionId}/`, {});
  
          if (response.status === 201) {
            await this.sendWebSocketMessage({
              type: 'notification',
              message: response.data.message,
            });
          }
          this.isModalOpen = false;
        } catch (error) {
          console.error(error);
          this.toastStore.showToast(5000, 'Failed to add followup', 'bg-red-500');
        }
      },
  
      // Session handling
      async endSession() {
        console.log('Attempting to end session');
  
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
          console.log('Socket not connected - queueing end session message');
          this.messageQueue.push({
            type: 'end_session',
            message: 'Ending session',
          });
          this.connectWebsocket();
          return;
        }
  
        try {
          this.sessionEnded = true;
  
          const payload = {
            type: 'end_session',
            message: 'Ending session',
          };
  
          console.log('Sending end session payload:', payload);
          await this.sendWebSocketMessage(payload);
          this.isModalOpen = false;
        } catch (error) {
          console.error('Error ending session:', error);
          this.sessionEnded = false;
          this.toastStore.showToast(5000, 'Failed to end session', 'bg-red-500');
        }
      },
      handleSessionEnded(data) {
        this.sessionEnded = true;
  
        if (data.data?.message) {
          this.messages.push(data.data.message);
        }
  
        this.userStore.clearActiveSession();
  
        this.toastStore.showToast(
          5000,
          'This session has ended',
          'bg-blue-500'
        );
  
        this.newMessage = '';
        this.isModalOpen = false;
        this.isMedicationModalOpen = false;
        setTimeout(() => {
          this.$router.push('/dashboard');
        }, 2000);
  
        this.$emit('session-ended');
      },
      async startCall(){
        this.state = 'call'
        this.callState = 'dialing'
        await this.getCallToken()
        setTimeout(() => {
                this.sendWebSocketMessage({
                type : 'call_notification_indicator',
                message: 'Call Notification'
            })
        }, 2000);

        
       
      },
      async getCallToken() {
        try {
            const response = await axios.get('session/agora/token/', {
                params: {
                    sessionId: this.sessionId,
                },
            });

            if (response.status === 200) {
                console.log(response.data);
                console.log(response.data.token);
                console.log(response.data.uid);
                console.log(response.data.channel)

                const uid = response.data.uid;
                if (typeof uid === 'number' && uid >= 0 && uid <= 10000) {
                    this.callToken = response.data.token;
                    this.channelName = response.data.channel
                    this.callUid = uid;
                    setTimeout(() => {
                        this.callState = 'incall';
                    }, 2000);
                } else {
                    console.error('Invalid uid:', uid);
                }
            }
        } catch (error) {
            console.error(error);
        }
      },
      async handleAccept(){
        this.showIncommingCall =  false
        this.state = 'call'
        await this.getCallToken()

      },
      handleEndCall(){
        this.showIncommingCall =  false
        this.state = 'chat'
      }
    },
  };
  </script>