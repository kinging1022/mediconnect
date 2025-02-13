import { defineStore } from 'pinia';
import { useUserStore } from './user';

export const useAppointmentStore = defineStore('appointment', {
  state: () => ({
    appointments: [], 
  }),

  actions: {
    hydrate() {
      const savedAppointments = localStorage.getItem('appointments');
      if (savedAppointments) {
        this.appointments = JSON.parse(savedAppointments);
      }
    },

    updateAppointments(newAppointments) {
      this.appointments = newAppointments;
      localStorage.setItem('appointments', JSON.stringify(newAppointments)); 
    },

    initWebSocket(appointmentsArray) {
      const userStore = useUserStore(); 
      const token = userStore.user.access;
      const ws = new WebSocket(`ws://localhost:8000/ws/appointments/?token=${token}`);

      ws.onopen = () => {
        ws.send(
          JSON.stringify({
            action: "list",
            request_id: new Date().getTime(),
          })
        );
      };

      ws.onmessage = (e) => {
        const allData = JSON.parse(e.data);

        if (allData.action === 'list') {
          appointmentsArray.splice(0, appointmentsArray.length, ...allData.data); 
          this.updateAppointments(allData.data); 

        } else if (allData.action === "create") {
          appointmentsArray.push(allData.data);
          this.updateAppointments([...appointmentsArray]); 
        }
      };
    },

    clearAppointments() {
      this.appointments = [];
      localStorage.removeItem('appointments');
    },
  },
});
