import { defineStore } from 'pinia';
import { useUserStore } from './user';

export const useAppointmentStore = defineStore('appointment', {
  state: () => ({
    appointments: [],
    wsConnection: null,
  }),

  actions: {
    async initWebSocket() {
      const userStore = useUserStore();
      let token = userStore.user.access;
      let userType = userStore.user.role;
      let userId = userStore.user.id;

      // Close existing connection before creating a new one
      if (this.wsConnection) {
        this.wsConnection.close();
      }

      this.wsConnection = new WebSocket(
        `ws://localhost:8000/ws/appointments/${userType}/${userId}/?token=${token}`
      );

      this.wsConnection.onopen = () => {
        console.log('WebSocket Connected');
      };

      this.wsConnection.onmessage = (e) => {
        const data = JSON.parse(e.data);
        console.log('WebSocket message received:', data);

        switch (data.event) {
          case 'list_appointments':
            console.log(data.data)
            this.updateAppointments(data.data);
            break;

          case 'new_appointment':
            this.addNewAppointment(data.data);
            break;

          case 'update_appointment':
            this.updateAppointmentStatus(data.data);
            break;
        }
      };

      this.wsConnection.onerror = (error) => {
        console.error('WebSocket Error:', error);
      };

      this.wsConnection.onclose = () => {
        console.log('WebSocket Disconnected');
        setTimeout(() => this.initWebSocket(), 5000); // Reconnect after 5 seconds
      };
    },

    updateAppointments(newAppointments) {
      this.appointments = newAppointments;
    },

    addNewAppointment(appointment) {
      this.appointments.push(appointment);
    },

    updateAppointmentStatus(updatedAppointment) {
      const index = this.appointments.findIndex((app) => app.id === updatedAppointment.id);
      if (index !== -1) {
        this.appointments[index] = { ...this.appointments[index], ...updatedAppointment };
      }
    },

    clearAppointments() {
      this.appointments = [];
      if (this.wsConnection) {
        this.wsConnection.close();
        this.wsConnection = null;
      }
    },
  },
});
