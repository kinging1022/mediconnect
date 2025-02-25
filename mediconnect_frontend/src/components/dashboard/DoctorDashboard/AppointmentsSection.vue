<template>
    <div class="min-h-screen w-full bg-gradient-to-br from-blue-50 via-white to-blue-50 p-4 md:p-8">
      <div class="max-w-7xl mx-auto bg-white rounded-2xl shadow-lg p-6">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Your Consultations</h1>
          </div>
        </div>
        <div class="space-y-4">
          <div
            v-for="appointment in appointments"
            :key="appointment.id"
            class="border rounded-xl p-4 hover:border-blue-500 transition-colors duration-300"
          >
            <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div>
                <h3 class="font-semibold text-gray-900">{{ appointment.created_by.first_name }} {{ appointment.created_by.last_name }}</h3>
                <div class="flex items-center gap-4 mt-2">
                  <div class="flex items-center text-gray-500 text-sm">
                    <Calendar class="w-4 h-4 mr-1" />
                    {{ formatDate(appointment.created_at) }}
                  </div>
                  <div class="flex items-center text-gray-500 text-sm">
                    <Clock class="w-4 h-4 mr-1" />
                    {{ appointment.created_at_formatted }}
                  </div>
                </div>
              </div>
              <div class="flex items-center gap-4">
                <button
                  @click="openModal(appointment.symptoms)"
                  class="px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-700 hover:bg-blue-200 transition-colors duration-300"
                >
                  Symptoms
                </button> 
                <button 
                v-if="!sessionId"
                @click="startSession(appointment.id)"
                class="w-8 h-8 rounded-lg bg-gray-100 flex items-center justify-center text-gray-600">
                  <MessageSquare class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
        <div v-if="appointments.length === 0" class="text-center py-12">
          <p class="text-gray-600">No appointments found</p>
        </div>
      </div>
    </div>
    
    <div v-if="isModalOpen" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
        <div class="p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Symptoms</h3>
          <p class="text-gray-700">{{ selectedSymptoms }}</p>
          <div class="mt-6 flex justify-end">
            <button @click="closeModal" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { Calendar, Clock, MessageSquare } from 'lucide-vue-next';
  import { useUserStore } from "@/stores/user";
  import axios from 'axios';
  export default {
    name: 'DoctorAppointments',
    components: {
      Calendar,
      Clock,
      MessageSquare,
    },
    setup() {
    const userStore = useUserStore();
    return { userStore  };
  },
    props: {
      appointments: {
        type: Array,
        required: true,
      },
      formatDate: {
       type: Function,
       required: true,
     },
    },
    data() {
      return {
        isModalOpen: false,
        selectedSymptoms: '',
      }
    },
    computed:{
      sessionId(){
        return this.userStore.activeSession.id || null;

      }

    },
    
    methods: {
      openModal(symptoms) {
        this.selectedSymptoms = symptoms;
        this.isModalOpen = true;
      },
      closeModal() {
        this.isModalOpen = false;
      },
      async startSession(id){

        try{
            const response = await axios.post('session/start/', {
            appointmentId: id,
            });
            if (response.status === 200) {
              this.$router.push(`/session/${response.data.id}`)

              this.userStore.getActiveSession()
              
            
            } 

        }catch(error){
          console.error(error)
        }

      }
    },
  };
  </script>
  