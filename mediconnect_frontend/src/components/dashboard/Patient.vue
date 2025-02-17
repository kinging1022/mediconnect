<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">

    <main class="flex-grow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <ProfileSection :patient="patient" @logout="logout" />
        <VitalsSection :vitals="patient.vitals" />
        <AppointmentsSection :appointments="appointments" :format-date="formatDate"/>
        <MedicationsSection :medications="medications" />
        <ConsultationsSection :consultations="consultations" />
      </div>
    </main>
  </div>
</template>

<script>
import { parseISO, format } from 'date-fns';
import { useUserStore } from "@/stores/user";
import { useAppointmentStore } from "@/stores/appointment";
import { useNotificationStore } from '@/stores/notification';
import ProfileSection from "./PatientDashboard/ProfileSection.vue";
import VitalsSection from "./PatientDashboard/VitalsSection.vue";
import AppointmentsSection from "./PatientDashboard/AppointmentsSection.vue";
import MedicationsSection from './PatientDashboard/MedicationsSection.vue';
import ConsultationsSection from "./PatientDashboard/ConsultationsSection.vue";

export default {
  name: 'PatientDashboard',
  components: {
    ProfileSection,
    VitalsSection,
    AppointmentsSection,
    MedicationsSection,
    ConsultationsSection,
  },
  setup() {
    const userStore = useUserStore();
    const appointmentStore = useAppointmentStore();
    const notificationStore = useNotificationStore();
    return { userStore, appointmentStore, notificationStore };
  },
  mounted(){
    this.appointmentStore.initWebSocket()

  },
  computed:{
    appointments(){
        return this.appointmentStore.appointments
    }
    
  },
  data() {
    return {
      patient: this.getPatientData(),
    };
  },
  methods: {
    getPatientData() {
      const user = this.userStore.user;
      const patientData = {
        name: `${user.first_name} ${user.last_name}`,
        initials: `${user.first_name.charAt(0)}${user.last_name.charAt(0)}`,
      };

      if (user.email) patientData.email = user.email;
      if (user.display_age) patientData.age = user.display_age;
      if (user.gender) patientData.gender = user.gender;
      if (user.weight) patientData.weight = user.weight;
      if (user.height) patientData.height = user.height;
      if (user.allergies && user.allergies !== "Not specified") patientData.allergies = [user.allergies];
      if (user.phone) patientData.phone = user.phone;
      if (user.blood_type) patientData.blood_type = user.blood_type;
      
      if (user.emergency_contact_name && user.emergency_contact_number) {
        patientData.emergencyContact = `${user.emergency_contact_name} - ${user.emergency_contact_number}`;
      }

      patientData.vitals = {
        "Blood Pressure": "120/80 mmHg",
        "Heart Rate": "72 bpm",
        "Temperature": "98.6°F",
        "Oxygen Saturation": "98%"
      };

      return patientData;
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
      this.appointmentStore.clearAppointments();
      this.notificationStore.clearNotifications()
      this.$router.push('/');
    }
  }
};
</script>

