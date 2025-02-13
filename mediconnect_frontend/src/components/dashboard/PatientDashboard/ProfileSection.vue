<template>
  <section class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
    <div class="p-6">
      <div class="flex flex-col md:flex-row justify-between items-center md:items-start">
        <div class="flex flex-col md:flex-row items-center mb-4 md:mb-0">
          <div class="w-24 h-24 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold text-3xl mb-4 md:mb-0 md:mr-6">
            {{ patient.initials }}
          </div>
          <div class="text-center md:text-left">
            <h2 class="text-2xl font-semibold text-gray-900">{{ patient.name }}</h2>
            <div v-if="patient.age && patient.gender" class="text-md text-gray-600">
              {{ patient.age }} years old, {{ patient.gender }}
            </div>
            <div v-if="patient.email || patient.phone" class="text-sm text-gray-500">
              <span v-if="patient.email">{{ patient.email }}</span>
              <span v-if="patient.email && patient.phone"> | </span>
              <span v-if="patient.phone">{{ patient.phone }}</span>
            </div>
            <div v-if="patient.blood_type" class="text-sm text-gray-500 mt-2">
              Blood Type: {{ patient.blood_type }}
            </div>
            <div v-if="patient.weight || patient.height" class="text-sm text-gray-500">
              <span v-if="patient.weight">Weight: {{ patient.weight }} kg</span>
              <span v-if="patient.weight && patient.height"> | </span>
              <span v-if="patient.height">Height: {{ patient.height }} cm</span>
            </div>
            <div v-if="patient.allergies && patient.allergies.length > 0 && patient.allergies[0] !== 'Not specified'" class="text-sm text-gray-500">
              Allergies: {{ patient.allergies.join(', ') }}
            </div>
            <div v-if="patient.emergencyContact && patient.emergencyContact !== 'Not specified'" class="text-sm text-gray-500 mt-2">
              Emergency Contact: {{ patient.emergencyContact }}
            </div>
          </div>
        </div>
        <div class="flex flex-wrap justify-center md:justify-end gap-2 mt-4 md:mt-0">
          <RouterLink :to="{ name: 'update-profile' }" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors">Edit Profile</RouterLink>
          <RouterLink
            :to="latestAppointment && latestAppointment.status !== 'done' ? null : { name: 'appointment' }"
            :class="{ 'disabled-link': latestAppointment && latestAppointment.status !== 'done' }"
            class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
          >
              Book Appointment
          </RouterLink>
          <button class="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition-colors">Chat with AI Doctor</button>
          <button @click="$emit('logout')" class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors">Logout</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { useAppointmentStore } from '@/stores/appointment';
export default {
  name: 'ProfileSection',
  setup() {
    const appointmentStore = useAppointmentStore();
    return { appointmentStore };
  },
  computed: {
    // Get latest appointment
    latestAppointment() {
      return this.appointmentStore.appointments.length > 0
        ? this.appointmentStore.appointments[0]
        : null;
    },
  },
  props: {
    patient: {
      type: Object,
      required: true,
    },
  },
  
};
</script>
<style>
/* Disable the link when the class is applied */
.disabled-link {
  pointer-events: none;  /* Prevent clicking */
  opacity: 0.5;         /* Make it look disabled */
  background-color: gray !important; /* Change color */
}
</style>
