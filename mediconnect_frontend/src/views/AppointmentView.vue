<template>
    <div class="min-h-screen w-full bg-gradient-to-br from-blue-50 via-white to-blue-50 flex items-center justify-center p-4">
      <div class="max-w-2xl w-full bg-white rounded-2xl shadow-lg p-8 relative overflow-hidden">
        <div class="mb-8">
          <div class="text-2xl font-bold text-blue-600 flex items-center justify-center mb-6">
            <div class="w-8 h-8 bg-blue-600 rounded-lg mr-2"></div>
            MediConnect
          </div>
          <h1 class="text-2xl font-semibold text-gray-900 text-center">
            Book an Appointment
          </h1>
          <p v-if="status === 'selecting'" class="mt-2 text-gray-600 text-center">
            Choose the type of appointment you'd like to schedule
          </p>
        </div>
        <div class="space-y-6">
          <!-- Selecting appointment type -->
          <div v-if="status === 'selecting'" class="grid md:grid-cols-2 gap-4 animate-fade-in">
            <button
              @click="handleAppointmentTypeSelect('follow-up')"
              class="p-6 border-2 border-gray-200 rounded-xl hover:border-blue-500 hover:bg-blue-50 transition-all duration-300 group"
            >
              <refresh-cw-icon class="w-8 h-8 text-blue-600 mb-4" />
              <h3 class="text-lg font-semibold mb-2">Follow-up Visit</h3>
              <p class="text-gray-600 text-sm">
                Continue your treatment with a follow-up appointment
              </p>
            </button>
            <button
              @click="handleAppointmentTypeSelect('new')"
              class="p-6 border-2 border-gray-200 rounded-xl hover:border-blue-500 hover:bg-blue-50 transition-all duration-300 group"
            >
              <plus-circle-icon class="w-8 h-8 text-blue-600 mb-4" />
              <h3 class="text-lg font-semibold mb-2">New Appointment</h3>
              <p class="text-gray-600 text-sm">
                Schedule a new consultation with our healthcare providers
              </p>
            </button>
          </div>
  
          <!-- Checking availability -->
          <div v-if="status === 'checking'" class="text-center py-8 animate-fade-in">
            <loader2-icon class="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
            <p class="text-gray-600">
              Checking appointment availability...
            </p>
          </div>
  
          <!-- Booking new appointment -->
          <div v-if="status === 'booking'" class="space-y-6 animate-fade-in">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Reason for Visit
              </label>
              <textarea
                v-model="symptoms"
                class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none h-24"
                placeholder="Please describe your symptoms or reason for visit"
              ></textarea>
            </div>
            <button
              @click="handleNewAppointmentSubmit"
              :disabled="isProcessing"
              class="w-full bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors duration-300 flex items-center justify-center"
            >
              <loader2-icon v-if="isProcessing" class="w-5 h-5 animate-spin" />
              <template v-else>
                Book Appointment
                <chevron-right-icon class="ml-2 w-4 h-4" />
              </template>
            </button>
          </div>
  
          <!-- Success message -->
          <div v-if="status === 'success'" class="text-center animate-fade-in">
            <check-circle-icon class="w-16 h-16 text-green-500 mx-auto mb-4" />
            <h2 class="text-xl font-semibold text-gray-900 mb-2">
              {{ appointmentType === 'follow-up' ? 'Your follow-up appointment is confirmed!' : 'Appointment request received!' }}
            </h2>
            <div v-if="appointmentType === 'follow-up' && selectedFollowUp" class="mb-6">
              <p class="text-gray-600">
                Follow-up appointment with Dr {{ selectedFollowUp.created_for.first_name }} {{ selectedFollowUp.created_for.last_name }}
              </p>
              <p class="text-sm text-gray-500 mt-1">
                Please wait for the doctor to join your session
              </p>
            </div>
            <p class="text-gray-600 mb-6">
              {{ appointmentType === 'follow-up' ? 'Your doctor will join you soon. Please wait...' : 'Our team is processing your appointment request.' }}
            </p>
            <div v-if="appointmentType === 'new' && progress < 100" class="w-full max-w-xs mx-auto mb-6">
              <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  class="h-full bg-blue-600 transition-all duration-500"
                  :style="{ width: `${progress}%` }"
                ></div>
              </div>
              <p class="text-sm text-gray-600 mt-2">
                Processing request...
              </p>
            </div>
            <button
              @click="resetBooking"
              class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-300"
            >
              Back to Dashboard
            </button>
          </div>
  
          <!-- Error message -->
          <div v-if="status === 'error'" class="text-center animate-fade-in">
            <alert-circle-icon class="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h2 class="text-xl font-semibold text-gray-900 mb-2">
              No Follow-up Available
            </h2>
            <p class="text-gray-600 mb-6">
              You don't have any scheduled follow-up appointments. Would you
              like to book a new appointment instead?
            </p>
            <div class="space-y-4">
              <button
                @click="handleAppointmentTypeSelect('new')"
                class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-300"
              >
                Book New Appointment
              </button>
              <button
                @click="resetBooking"
                class="block w-full text-gray-600 hover:text-blue-600 font-medium"
              >
                <arrow-left-icon class="w-4 h-4 inline mr-2" />
                Back to Options
              </button>
            </div>
          </div>
  
          <!-- Listing follow-up appointments -->
          <div v-if="status === 'listing'" class="animate-fade-in space-y-6">
            <div class="text-center mb-8">
              <h2 class="text-xl font-semibold text-gray-900 mb-2">
                Available Follow-up Appointments
              </h2>
              <p class="text-gray-600">
                Select a follow-up appointment to confirm
              </p>
            </div>
            <div class="space-y-4">
              <div
                v-for="followUp in followUps"
                :key="followUp.id"
                class="border rounded-xl p-6 hover:border-blue-500 transition-colors duration-300"
              >
                <div class="flex items-start justify-between">
                  <div class="flex items-start space-x-4">
                    <div>
                      <h3 class="font-semibold text-gray-900">
                       Dr {{ followUp.created_for.first_name }} 
                        {{ followUp.created_for.last_name }} 
                      </h3>
                      <p class="text-gray-600 text-sm">
                        {{ followUp.created_for.speciality }}
                      </p>
                      <div class="flex items-center mt-2 text-sm text-gray-500">
                        <calendar-clock-icon class="w-4 h-4 mr-1" />
                        Expires: {{ new Date(followUp.follow_up_expiry_date).toLocaleDateString() }}
                      </div>
                    </div>
                  </div>
                  <button
                    @click="handleConfirmFollowUp(followUp)"
                    class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-300"
                  >
                    Confirm
                  </button>
                </div>
              </div>
            </div>
            <button
              @click="resetBooking"
              class="w-full text-gray-600 hover:text-blue-600 font-medium flex items-center justify-center mt-4"
            >
              <arrow-left-icon class="w-4 h-4 mr-2" />
              Back to Options
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { 
    Calendar, 
    Clock, 
    RefreshCw, 
    PlusCircle, 
    CheckCircle, 
    AlertCircle, 
    Loader2, 
    ArrowLeft, 
    ChevronRight, 
    CalendarClock 
  } from 'lucide-vue-next'
  
  export default {
    components: {
      CalendarIcon: Calendar,
      ClockIcon: Clock,
      RefreshCwIcon: RefreshCw,
      PlusCircleIcon: PlusCircle,
      CheckCircleIcon: CheckCircle,
      AlertCircleIcon: AlertCircle,
      Loader2Icon: Loader2,
      ArrowLeftIcon: ArrowLeft,
      ChevronRightIcon: ChevronRight,
      CalendarClockIcon: CalendarClock
    },
    data() {
      return {
        appointmentType: null,
        symptoms: null,
        status: 'selecting',
        isProcessing: false,
        progress: 0,
        selectedFollowUp: null,
        followUps:[],
      }
    },
    methods: {
      async handleAppointmentTypeSelect(type) {
        try{
            this.appointmentType = type
            this.status = 'checking'
            this.isProcessing = true
            await new Promise(resolve => setTimeout(resolve, 1500))
            if (type === 'follow-up'){
                const response = await axios.post('appointment/',{type:type})
                console.log('data',response.data)
                this.followUps = response.data
                console.log(this.followUps)
                if(this.followUps.length > 0){
                    this.status = 'listing'
                }else{
                    //this.status = 'error'
                }

            }else{
                this.status = 'booking'
            }
            this.isProcessing = false

        }catch(error){
            this.status = 'error'
            this.isProcessing = false
            console.error(error)

        }
    },
    
      async handleConfirmFollowUp(followUp) {
        try{
            this.selectedFollowUp = followUp
            console.log(followUp)
            this.status = 'checking'
            this.isProcessing = true
            await new Promise(resolve => setTimeout(resolve, 1500))
            const response = await axios.post('confirm/follow-up/',{id:this.selectedFollowUp.id})
            if (response.status === 200){
                this.status = 'success'
                this.isProcessing = false
            }

        }catch(error){
            console.error(error)

        }
        
      },
      async handleNewAppointmentSubmit() {
        try{
            this.isProcessing = true
            await new Promise(resolve => setTimeout(resolve, 1500))
            const response = await axios.post('appointment/',{type:'new',symptoms: this.symptoms})
            if(response.status === 200){
                this.status = 'success'
                this.isProcessing = false
                this.progress = 20

            }

        }catch(error){
            console.error(error)
        }
      },
      resetBooking() {
        this.appointmentType = null
        this.status = 'selecting'
        this.isProcessing = false
        this.progress = 0
        this.$router.push('/dashboard')
      }
    },
    watch: {
      status(newStatus) {
        if (newStatus === 'success' && this.appointmentType === 'new') {
          this.progressInterval = setInterval(() => {
            this.progress += 20
            if (this.progress >= 100) {
              clearInterval(this.progressInterval)
              this.progress = 100
            }
          }, 1000)
        }
      }
    },
    beforeUnmount() {
      if (this.progressInterval) {
        clearInterval(this.progressInterval)
      }
    }
  }
  </script>
  
  <style scoped>
  .animate-fade-in {
    animation: fadeIn 0.5s ease-out;
  }
  
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  .animate-spin {
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
  </style>
  
  