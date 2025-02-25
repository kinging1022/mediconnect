import { defineStore } from 'pinia';
import { useUserStore } from './user';

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    notifications: [],
    wsConnection: null,
    notificationType: null,
    unreadCount: 0,
    userStore: null, 
  }),

  actions: {
    async initWebSocket() {
      this.userStore = useUserStore();

      let token = this.userStore.user.access;
      let userId = this.userStore.user.id;

      if (this.wsConnection) {
        this.wsConnection.close();
      }

      this.wsConnection = new WebSocket(
        `ws://localhost:8000/ws/notifications/${userId}/?token=${token}`
      );

      this.wsConnection.onopen = () => {
        console.log('WebSocket Connected');
      };

      this.wsConnection.onmessage = (e) => {
        const data = JSON.parse(e.data);
        console.log('WebSocket message received:', data);

        switch (data.event) {
          case 'list_notifications':
            this.updateNotifications(data.data);
            this.unreadCount = this.notifications.filter((n) => !n.is_read).length;
            break;

          case 'new_notification':
            this.addNewNotification(data.data);
            if (data.data.type_of_notification === 'session_start') {
              console.log(data.data.type_of_notification);
              this.userStore.getActiveSession(); 
            }
            this.notificationType = data.data.type_of_notification;
            this.unreadCount++;
            break;
        }
      };

      this.wsConnection.onerror = (error) => {
        console.error('WebSocket Error:', error);
      };

      this.wsConnection.onclose = () => {
        console.log('WebSocket Disconnected');
        setTimeout(() => this.initWebSocket(), 5000); 
      };
    },

    updateNotifications(newNotifications) {
      this.notifications = newNotifications;
    },

    addNewNotification(notification) {
      this.notifications.unshift(notification);
    },

    markNotificationAsRead(id) {
      const notification = this.notifications.find((n) => n.id === id);
      if (notification && !notification.is_read) {
        notification.is_read = true;
        this.unreadCount--;
      }
    },

    markAllNotificationsAsRead() {
      this.notifications.forEach((notification) => {
        if (!notification.is_read) {
          notification.is_read = true;
        }
      });
      this.unreadCount = 0;
    },

    incrementUnreadCount() {
      this.unreadCount++;
    },

    decrementUnreadCount(count = 1) {
      this.unreadCount = Math.max(this.unreadCount - count, 0);
    },

    resetUnreadCount() {
      this.unreadCount = 0;
    },

    clearNotifications() {
      this.notifications = [];
      this.notificationType = null;
      this.unreadCount = 0;
      if (this.notificationSocket) {
        this.notificationSocket.close();
        this.notificationSocket = null;
      }
    },
  },

  getters: {
    hasUnreadNotifications: (state) => state.unreadCount > 0,
    getUnreadNotifications: (state) => state.notifications.filter((n) => !n.is_read),
    getAllNotifications: (state) => state.notifications,
  },
});