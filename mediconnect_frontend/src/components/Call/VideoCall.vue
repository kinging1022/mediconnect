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

      <!-- Local Video Feed - Increased size -->
      <video
        ref="localVideo"
        autoplay
        muted
        class="absolute top-4 right-4 w-40 h-30 md:w-64 md:h-48 bg-gray-700 rounded-lg overflow-hidden shadow-lg"
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
        <button
          @click="endCall"
          class="p-3 md:p-4 rounded-full bg-red-500 hover:bg-red-600"
        >
          <phone-icon class="w-5 h-5 md:w-6 md:h-6 text-white transform rotate-135" />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { markRaw } from 'vue'

import { 
  Mic, MicOff, Video, VideoOff, Phone, Share2, 
  MessageSquare, Headphones 
} from 'lucide-vue-next'
import { useUserStore } from '@/stores/user';
import AgoraRTC from "agora-rtc-sdk-ng";

export default {
  name: 'VideoCall',
  components: {
    MicIcon: Mic,
    MicOffIcon: MicOff,
    VideoIcon: Video,
    VideoOffIcon: VideoOff,
    PhoneIcon: Phone,
    Share2Icon: Share2,
    MessageSquareIcon: MessageSquare,
    HeadphonesIcon: Headphones
  },
  props: {
    channel: {
      type: String,
      required: true,
    },
    token: {
      type: String,
      required: true,
    },
    uid: {
      type: Number,
      required: true,
    },
  },
  setup() {
    const userStore = useUserStore()
    return { userStore }
  },
  data() {
    return {
      client: null,
      localAudioTrack: null,
      localVideoTrack: null,
      appId: import.meta.env.VITE_AGORA_APP_ID,
      isMuted: false,
      isVideoEnabled: true,
      isAudioOnly: false,
      savedVideoTrack: null, // To store video track when toggling
    }
  },
  mounted() {
    this.initializeClient();
    this.joinChannel().catch(err => {
      console.error("Join channel error:", err);
    });
  },
  methods: {
    initializeClient() {
      this.client = markRaw(AgoraRTC.createClient({ mode: 'rtc', codec: 'vp8' }))
      this.setupEventListeners();
    },

    setupEventListeners() {
      this.client.on("user-published", async (user, mediaType) => {
        await this.client.subscribe(user, mediaType);
        console.log("subscribe success");
        
        if (mediaType === "video" && !this.isAudioOnly) {
          // Play remote video in the remoteVideo ref instead of creating a new container
          const remoteVideoElement = this.$refs.remoteVideo;
          if (remoteVideoElement) {
            user.videoTrack.play(remoteVideoElement);
          }
        }
        
        if (mediaType === "audio") {
          user.audioTrack.play();
        }
      });
      
      this.client.on("user-unpublished", (user, mediaType) => {
        // Handle user unpublished event
        if (mediaType === "video") {
          const remoteVideoElement = this.$refs.remoteVideo;
          
          // Check if the remote video element exists and if it's playing the user's video
          if (remoteVideoElement && remoteVideoElement.srcObject) {
            // Stop the video track
            user.videoTrack?.stop();
            
            // Clear the video element
            remoteVideoElement.srcObject = null;
          }
        }
      });
    },

    async joinChannel() {
      // Validate channel name before attempting to join
      if (!this.channel) {
        throw new Error("Channel name is undefined or empty");
      }
      
      await this.client.join(this.appId, this.channel, this.token, this.uid);
      await this.createLocalTracks();
      await this.publishLocalTracks();
      this.displayLocalVideo();
      console.log("Publish success!");
    },

    // Create local audio and video tracks
    async createLocalTracks() {
      this.localAudioTrack = await AgoraRTC.createMicrophoneAudioTrack();
      this.localVideoTrack = await AgoraRTC.createCameraVideoTrack();
    },

    // Publish local audio and video tracks
    async publishLocalTracks() {
      const tracksToPublish = [];
      
      if (this.localAudioTrack) {
        tracksToPublish.push(this.localAudioTrack);
      }
      
      if (this.localVideoTrack && this.isVideoEnabled) {
        tracksToPublish.push(this.localVideoTrack);
      }
      
      if (tracksToPublish.length > 0) {
        await this.client.publish(tracksToPublish);
      } else {
        console.error("No tracks to publish");
      }
    },

    // Display local video
    displayLocalVideo() {
      if (this.localVideoTrack && this.isVideoEnabled) {
        const localVideoElement = this.$refs.localVideo;
        this.localVideoTrack.play(localVideoElement);
      }
    },

    // Display remote video
    displayRemoteVideo(user) {
      const remoteVideoTrack = user.videoTrack;
      const remoteVideoElement = this.$refs.remoteVideo;
      
      // Play the remote video in the existing video element
      if (remoteVideoTrack && remoteVideoElement) {
        remoteVideoTrack.play(remoteVideoElement);
      }
    },

    async endCall() {
      if (this.localAudioTrack) {
        this.localAudioTrack.close();
      }
      if (this.localVideoTrack) {
        this.localVideoTrack.close();
      }
      if (this.savedVideoTrack) {
        this.savedVideoTrack.close();
      }
      
      // Leave the channel
      if (this.client) {
        await this.client.leave();
      }
      
      this.$emit('endCall') 
    },

    async toggleMute() {
      this.isMuted = !this.isMuted;
      
      if (this.localAudioTrack) {
        // Properly mute/unmute the audio track
        this.localAudioTrack.setEnabled(!this.isMuted);
      }
    },

    async toggleVideo() {
      this.isVideoEnabled = !this.isVideoEnabled;
      
      if (this.isVideoEnabled) {
        // Re-enable video
        if (!this.localVideoTrack && this.savedVideoTrack) {
          // Restore from saved track
          this.localVideoTrack = this.savedVideoTrack;
          this.savedVideoTrack = null;
          
          // Publish the video track
          await this.client.publish([this.localVideoTrack]);
          
          // Display local video
          this.displayLocalVideo();
        } else if (!this.localVideoTrack) {
          // Create new video track if none exists
          this.localVideoTrack = await AgoraRTC.createCameraVideoTrack();
          await this.client.publish([this.localVideoTrack]);
          this.displayLocalVideo();
        } else {
          // Just enable the existing track
          this.localVideoTrack.setEnabled(true);
        }
      } else {
        // Disable video
        if (this.localVideoTrack) {
          // Stop the video track from playing
          this.localVideoTrack.stop();
          
          // Save the track for later re-enabling
          this.savedVideoTrack = this.localVideoTrack;
          
          // Unpublish the video track
          await this.client.unpublish([this.localVideoTrack]);
          
          // Clear the local video track reference
          this.localVideoTrack = null;
          
          // Clear the video element
          const localVideoElement = this.$refs.localVideo;
          if (localVideoElement && localVideoElement.srcObject) {
            localVideoElement.srcObject = null;
          }
        }
      }
    },
    
    async toggleAudioOnly() {
      this.isAudioOnly = !this.isAudioOnly;

      if (this.isAudioOnly) {
        // Save current video state before switching to audio-only
        if (this.localVideoTrack) {
          this.savedVideoTrack = this.localVideoTrack;
          await this.client.unpublish([this.localVideoTrack]);
          this.localVideoTrack.stop();
          this.localVideoTrack = null;
          
          // Clear the video element
          const localVideoElement = this.$refs.localVideo;
          if (localVideoElement && localVideoElement.srcObject) {
            localVideoElement.srcObject = null;
          }
        }
      } else {
        // Restore video if we have a saved track
        if (this.savedVideoTrack) {
          this.localVideoTrack = this.savedVideoTrack;
          this.savedVideoTrack = null;
          await this.client.publish([this.localVideoTrack]);
          this.displayLocalVideo();
        } else {
          // Create a new video track if we don't have one saved
          this.localVideoTrack = await AgoraRTC.createCameraVideoTrack();
          await this.client.publish([this.localVideoTrack]);
          this.displayLocalVideo();
        }
        
        // Force re-subscription to remote streams
        this.refreshRemoteStreams();
      }
    },
    
    // Add a new method to refresh remote streams
    async refreshRemoteStreams() {
      // Get the list of remote users
      const remoteUsers = this.client.remoteUsers;
      
      // Re-subscribe to their video tracks if they have them
      for (const user of remoteUsers) {
        if (user.hasVideo) {
          // Unsubscribe first to ensure a clean state
          await this.client.unsubscribe(user, "video");
          
          // Re-subscribe to the video track
          await this.client.subscribe(user, "video");
          
          // Play the video track
          const remoteVideoElement = this.$refs.remoteVideo;
          if (user.videoTrack && remoteVideoElement) {
            user.videoTrack.play(remoteVideoElement);
          }
        }
      }
    }
    ,
    
    // Helper method to create local video track
    async createLocalVideoTrack() {
      this.localVideoTrack = await AgoraRTC.createCameraVideoTrack();
      await this.client.publish([this.localVideoTrack]);
      return this.localVideoTrack;
    },
  },
  beforeUnmount() {
    // Clean up resources when component is destroyed
    this.endCall();
  }
}
</script>