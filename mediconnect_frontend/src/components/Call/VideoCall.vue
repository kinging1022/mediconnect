<template>
    <div class="relative w-full h-screen bg-gray-900 flex flex-col md:flex-row">
      <!-- Video/Audio Feed -->
      <div class="flex-1 relative h-[calc(100vh-5rem)] md:h-full">
        <!-- Remote Video Feed -->
        <video
          ref="remoteVideo"
          autoplay
          class="w-full h-full bg-gray-800"
          v-if="!isAudioOnly"
        ></video>
        <div v-else class="w-full h-full flex items-center justify-center bg-gray-800">
          <div class="text-white text-xl">Audio Only Mode</div>
        </div>
  
        <!-- Local Video Feed -->
        <video
          ref="localVideo"
          autoplay
          muted
          class="absolute top-4 right-4 w-32 h-24 md:w-48 md:h-36 bg-gray-700 rounded-lg overflow-hidden shadow-lg"
        ></video>
      </div>
  
      <!-- Control Bar -->
      <div class="fixed bottom-0 left-0 right-0 md:absolute h-20 bg-gray-800 bg-opacity-90 flex items-center justify-center px-2 md:px-6">
        <div class="flex items-center justify-center space-x-2 md:space-x-6 w-full max-w-screen-lg">
          <button
            @click="toggleMute"
            :class="['p-3 md:p-4 rounded-full', isMuted ? 'bg-red-500' : 'bg-gray-600 hover:bg-gray-700']"
          >
            <mic-off-icon v-if="isMuted" class="w-5 h-5 md:w-6 md:h-6 text-white" />
            <mic-icon v-else class="w-5 h-5 md:w-6 md:h-6 text-white" />
          </button>
          <button
            @click="toggleVideo"
            :class="['p-3 md:p-4 rounded-full', !isVideoEnabled ? 'bg-red-500' : 'bg-gray-600 hover:bg-gray-700']"
          >
            <video-icon v-if="isVideoEnabled" class="w-5 h-5 md:w-6 md:h-6 text-white" />
            <video-off-icon v-else class="w-5 h-5 md:w-6 md:h-6 text-white" />
          </button>
          <button
            @click="toggleAudioOnly"
            :class="['p-3 md:p-4 rounded-full', isAudioOnly ? 'bg-blue-500' : 'bg-gray-600 hover:bg-gray-700']"
          >
            <headphones-icon class="w-5 h-5 md:w-6 md:h-6 text-white" />
          </button>
          <button class="p-3 md:p-4 rounded-full bg-gray-600 hover:bg-gray-700">
            <share2-icon class="w-5 h-5 md:w-6 md:h-6 text-white" />
          </button>
          <button
            @click="toggleChat"
            :class="['p-3 md:p-4 rounded-full', isChatOpen ? 'bg-blue-500' : 'bg-gray-600 hover:bg-gray-700']"
          >
            <message-square-icon class="w-5 h-5 md:w-6 md:h-6 text-white" />
          </button>
          <button
            @click="endCall"
            class="p-3 md:p-4 rounded-full bg-red-500 hover:bg-red-600"
          >
            <phone-icon class="w-5 h-5 md:w-6 md:h-6 text-white transform rotate-135" />
          </button>
        </div>
      </div>
  
      <!-- Chat Sidebar -->
      <div v-if="isChatOpen" class="fixed inset-0 z-50 md:relative md:z-auto">
        <div class="absolute inset-0 bg-black bg-opacity-50 md:hidden" @click="toggleChat"></div>
        <div class="absolute right-0 top-0 bottom-0 w-full max-w-[320px] md:w-80 md:relative">
          <chat-sidebar />
        </div>
      </div>
  
      <!-- Call Notification -->
      <div v-if="incomingCall" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white p-6 rounded-lg shadow-lg">
          <h3 class="text-lg font-bold mb-4">Incoming Call</h3>
          <div class="flex space-x-4">
            <button @click="acceptCall" class="bg-green-500 text-white px-4 py-2 rounded">Accept</button>
            <button @click="rejectCall" class="bg-red-500 text-white px-4 py-2 rounded">Reject</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { 
    Mic, MicOff, Video, VideoOff, Phone, Share2, 
    MessageSquare, Headphones 
  } from 'lucide-vue-next'
  import ChatSidebar from './ChatSidebar.vue'
  import { useUserStore } from '@/stores/user';
  import { onMounted, ref, nextTick } from 'vue';
  
  export default {
    name: 'VideoCall',
    components: {
      ChatSidebar,
      MicIcon: Mic,
      MicOffIcon: MicOff,
      VideoIcon: Video,
      VideoOffIcon: VideoOff,
      PhoneIcon: Phone,
      Share2Icon: Share2,
      MessageSquareIcon: MessageSquare,
      HeadphonesIcon: Headphones
    },
    setup(){
      const userStore = useUserStore()
      return { userStore }
    },
    data() {
      return {
        isMuted: false,
        isVideoEnabled: true,
        isAudioOnly: false,
        isChatOpen: false,
        incomingCall: false,
        peer: null,
        localStream: null,
        remoteStream: null,
        call: null,
        socket: null,
        roomName: null,
        callerId: null,
        connectionReady: false,
        videoRefsReady: false
      }
    },
    computed:{
     
    },
    mounted() {
      
    },
    methods: {

      
      toggleMute() {
        this.isMuted = !this.isMuted;
        if (this.localStream) {
          this.localStream.getAudioTracks().forEach(track => {
            track.enabled = !this.isMuted;
          });
        }
      },
      
      toggleVideo() {
        this.isVideoEnabled = !this.isVideoEnabled;
        if (this.localStream) {
          this.localStream.getVideoTracks().forEach(track => {
            track.enabled = this.isVideoEnabled;
          });
        }
      },
      
      toggleAudioOnly() {
        this.isAudioOnly = !this.isAudioOnly;
      },
      
      toggleChat() {
        this.isChatOpen = !this.isChatOpen;
      }
    },
    beforeUnmount() {
      // Clean up resources when component is destroyed
      this.endCall();
    }
  }
  </script>