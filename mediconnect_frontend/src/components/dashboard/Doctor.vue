<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">

    <main class="flex-grow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <DoctorProfileSection :doctor="doctor" @logout="logout" />
        <AppointmentsSection :appointments="appointments" :format-date="formatDate"  />
        <PatientsSection :patients="patients" />
        <ScheduleSection :schedule="schedule" />
      </div>
    </main>
  </div>
</template>

<script>
import { parseISO, format } from 'date-fns';

import { useUserStore } from "@/stores/user";
import { useAppointmentStore } from "@/stores/appointment";
import DoctorProfileSection from "./DoctorDashboard/DoctorProfileSection.vue";
import AppointmentsSection from "./DoctorDashboard/AppointmentsSection.vue";
import PatientsSection from "./DoctorDashboard/PatientsSection.vue";
import ScheduleSection from "./DoctorDashboard/ScheduleSection.vue";

export default {
  name: 'DoctorDashboard',
  components: {
    DoctorProfileSection,
    AppointmentsSection,
    PatientsSection,
    ScheduleSection,
  },
  setup() {
    const userStore = useUserStore();
    const appointmentStore = useAppointmentStore();
    return { userStore , appointmentStore };
  },
  mounted(){
    this.appointmentStore.initWebSocket()
  },
  computed:{
    appointments(){
      return this.appointmentStore.appointments
    },
    sesionId(){
      return this.userStore.activeSession.id
    }

  },
  data() {
    return {
      doctor: this.getDoctorData(),
      
    };
  },
  methods: {
    getDoctorData() {
      const user = this.userStore.user;
      return {
        name: `Dr. ${user.first_name} ${user.last_name}`,
        speciality: user.speciality|| "General Practitioner",
        email: user.email,
        phone: user.phone,
        license: user.license_number,
      };
    },
    formatDate(dateString) {
      try {
        return format(parseISO(dateString), 'MMMM dd, yyyy - hh:mm a'); 
      } catch (error) {
        console.error('Date parsing error:', error);
        return 'Invalid Date';
      }
    },
    logout() {
      this.userStore.removeToken();
      this.appointmentStore.clearAppointments()
      this.$router.push('/');
      
    }
  }
};
</script>

