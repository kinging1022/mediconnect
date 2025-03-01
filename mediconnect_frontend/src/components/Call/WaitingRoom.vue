<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 flex items-center justify-center p-4">
    <!-- Main Container -->
    <div class="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 relative overflow-hidden">
      <!-- Background Pattern using Lucide Icons -->
      <div class="absolute inset-0 opacity-5 grid grid-cols-4 gap-4 p-4">
        <grid-icon 
          v-for="n in 16" 
          :key="n" 
          class="w-12 h-12 text-gray-400"
        />
      </div>

      <!-- Content -->
      <div class="relative z-10 text-center space-y-8">
        <!-- Avatar Circle with Pulsing Rings -->
        <div class="relative mx-auto w-32 h-32">
          <div class="absolute inset-0 bg-emerald-500/20 rounded-full animate-ping"></div>
          <div class="absolute inset-0 bg-emerald-500/20 rounded-full animate-ping" style="animation-delay: 0.5s"></div>
          <div class="absolute inset-0 bg-emerald-500/20 rounded-full animate-ping" style="animation-delay: 1s"></div>
          <div class="relative w-full h-full bg-white rounded-full shadow-lg flex items-center justify-center border-4 border-emerald-500">
            <span class="text-3xl font-semibold text-emerald-600">
              {{ getInitials }}
            </span>
          </div>
        </div>

        <!-- Patient Name -->
        <div class="space-y-2">
          <h1 class="text-2xl font-bold text-gray-900">
            {{ patient.first_name }} {{ patient.last_name }}
          </h1>
          <p class="text-emerald-600 font-medium flex items-center justify-center gap-2">
            <phone-call-icon class="w-5 h-5" />
            Connecting...
          </p>
        </div>

        <!-- Timer -->
        <div class="text-gray-500 font-medium">
          {{ formattedTime }}
        </div>

        <!-- Loading Indicator -->
        <div class="flex justify-center">
          <loader2-icon class="w-8 h-8 text-emerald-500 animate-spin" />
        </div>

        <!-- Cancel Button -->
        <button 
          @click="$emit('cancel-call')"
          class="mt-6 px-6 py-3 bg-red-50 text-red-600 rounded-full font-medium hover:bg-red-100 transition-colors duration-200 inline-flex items-center gap-2"
        >
          <phone-off-icon class="w-4 h-4" />
          End Call
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { Loader2, PhoneCall, PhoneOff, Grid } from 'lucide-vue-next'

export default {
  name: 'DialingRoom',
  components: {
    Loader2Icon: Loader2,
    PhoneCallIcon: PhoneCall,
    PhoneOffIcon: PhoneOff,
    GridIcon: Grid
  },
  props: {
    patient: {
      type: Object,
      required: true,
      default: () => ({ first_name: '', last_name: '' }),
      validator: (prop) => {
        return prop.hasOwnProperty('first_name') && prop.hasOwnProperty('last_name')
      }
    }
  },
  data() {
    return {
      seconds: 0,
      timerInterval: null
    }
  },
  computed: {
    getInitials() {
      const first = this.patient.first_name.charAt(0)
      const last = this.patient.last_name.charAt(0)
      return `${first}${last}`
    },
    formattedTime() {
      const minutes = Math.floor(this.seconds / 60)
      const remainingSeconds = this.seconds % 60
      return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
    }
  },
  mounted() {
    this.timerInterval = setInterval(() => {
      this.seconds++
    }, 1000)
  },
  beforeUnmount() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval)
    }
  }
}
</script>

<style scoped>
@keyframes ping {
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}
</style>