<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <AppHeader />

    <main class="flex-grow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <DoctorProfileSection :doctor="doctor" @logout="logout" />
        <AppointmentsSection :appointments="appointments" />
        <PatientsSection :patients="patients" />
        <ScheduleSection :schedule="schedule" />
      </div>
    </main>
  </div>
</template>

<script>
import { useUserStore } from "@/stores/user";
import AppHeader from "./AppHeader.vue";
import DoctorProfileSection from "./DoctorDashboard/DoctorProfileSection.vue";
import AppointmentsSection from "./DoctorDashboard/AppointmentsSection.vue";
import PatientsSection from "./DoctorDashboard/PatientsSection.vue";
import ScheduleSection from "./DoctorDashboard/ScheduleSection.vue";

export default {
  name: 'DoctorDashboard',
  components: {
    AppHeader,
    DoctorProfileSection,
    AppointmentsSection,
    PatientsSection,
    ScheduleSection,
  },
  setup() {
    const userStore = useUserStore();
    return { userStore };
  },
  data() {
    return {
      doctor: this.getDoctorData(),
      appointments: [
        { patient: "John Doe", date: "2023-06-15", time: "10:00 AM", type: "General Checkup", status: "confirmed" },
        { patient: "Jane Smith", date: "2023-06-15", time: "11:00 AM", type: "Follow-up", status: "confirmed" },
        { patient: "Mike Johnson", date: "2023-06-15", time: "2:00 PM", type: "New Patient", status: "pending" },
      ],
      patients: [
        { name: "John Doe", age: 45, lastVisit: "2023-05-20" },
        { name: "Jane Smith", age: 32, lastVisit: "2023-06-01" },
        { name: "Mike Johnson", age: 58, lastVisit: "2023-05-15" },
      ],
      schedule: [
        { day: "Monday", hours: "9:00 AM - 5:00 PM" },
        { day: "Tuesday", hours: "9:00 AM - 5:00 PM" },
        { day: "Wednesday", hours: "9:00 AM - 1:00 PM" },
        { day: "Thursday", hours: "9:00 AM - 5:00 PM" },
        { day: "Friday", hours: "9:00 AM - 5:00 PM" },
      ]
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
    logout() {
      this.userStore.removeToken();
      this.$router.push('/');
    }
  }
};
</script>

