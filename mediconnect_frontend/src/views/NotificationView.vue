<template>
    <div class="w-full min-h-screen bg-gray-50">
      <div class="max-w-4xl mx-auto px-4 py-8">
        <div class="bg-white rounded-2xl shadow-sm">
          <!-- Header -->
          <div class="border-b border-gray-100 p-6">
            <div class="flex items-center justify-between mb-6">
              <h1 class="text-2xl font-bold text-gray-900">
                Notifications
              </h1>
              <button
                @click="markAllAsRead"
                class="flex items-center text-sm text-blue-600 hover:text-blue-700"
              >
                <check-check-icon class="w-4 h-4 mr-2" />
                Mark all as read
              </button>
            </div>
            <!-- Tabs -->
            <div class="flex space-x-4">
              <button
                @click="activeTab = 'all'"
                :class="[
                  'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                  activeTab === 'all' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'
                ]"
              >
                All
              </button>
              <button
                @click="activeTab = 'unread'"
                :class="[
                  'px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center',
                  activeTab === 'unread' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'
                ]"
              >
                Unread
                <span
                  v-if="unreadCount > 0"
                  :class="[
                    'ml-2 px-2 py-0.5 rounded-full text-xs',
                    activeTab === 'unread' ? 'bg-white text-blue-600' : 'bg-blue-600 text-white'
                  ]"
                >
                  {{ unreadCount }}
                </span>
              </button>
            </div>
          </div>
          <!-- Notifications List -->
          <div class="divide-y divide-gray-100">
            <div v-if="displayedNotifications.length === 0" class="p-8 text-center text-gray-500">
              No notifications to display
            </div>
            <div
              v-else
              v-for="notification in displayedNotifications"
              :key="notification.id"
              :class="[
                'p-6 transition-colors',
                notification.is_read ? 'bg-white' : 'bg-blue-50',
                'hover:bg-gray-50'
              ]"
            >
              <div class="flex items-start gap-4">
                <div
                  :class="[
                    'p-2 rounded-lg',
                    notification.is_read ? 'bg-gray-100' : 'bg-blue-100'
                  ]"
                >
                  <component :is="getIcon(notification.type_of_notification)" class="w-5 h-5" />
                </div>
                <div class="flex-1">
                  <div class="flex items-start justify-between">
                    <div>
                      <p class="mt-1 text-gray-600">
                        {{ notification.body }}
                      </p>
                    </div>
                    <button
                      v-if="!notification.is_read"
                      @click="markAsRead(notification.id)"
                      class="text-blue-600 hover:text-blue-700 text-sm"
                    >
                      Mark as read
                    </button>
                  </div>
                  <span class="text-sm text-gray-500 mt-2 block">
                    {{ formatTimestamp(notification.created_at) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { Bell, CheckCheck, Mail, Calendar, UserPlus, AlertCircle } from 'lucide-vue-next'
  import { useNotificationStore } from '@/stores/notification'
  import { useUserStore } from '@/stores/user'
  import axios from 'axios';  
  export default {
    name: 'NotificationPage',
    components: {
      BellIcon: Bell,
      CheckCheckIcon: CheckCheck,
      MailIcon: Mail,
      CalendarIcon: Calendar,
      UserPlusIcon: UserPlus,
      AlertCircleIcon: AlertCircle
    },
    setup() {
      const notificationStore = useNotificationStore()
      const userStore = useUserStore()
  
      return {
        notificationStore,
        userStore
      }
    },
    data() {
      return {
        activeTab: 'all',
      }
    },
    computed: {
      notifications() {
        return this.notificationStore.notifications
      },
      unreadCount() {
        return this.notifications.filter(n => !n.is_read).length
      },
      displayedNotifications() {
        return this.activeTab === 'unread'
          ? this.notifications.filter(n => !n.is_read)
          : this.notifications
      }
    },
    methods: {
      formatTimestamp(timestamp) {
        const createdAt = new Date(timestamp);
        if (isNaN(createdAt.getTime())) {
          console.error("Invalid timestamp:", timestamp);
          return "Invalid date";
        }
  
        const now = new Date();
        const diffInMinutes = Math.floor((now - createdAt) / (1000 * 60));
  
        if (diffInMinutes < 1) return "Just now";
        if (diffInMinutes === 1) return "1 minute ago";
        if (diffInMinutes < 60) return `${diffInMinutes} minutes ago`;
  
        const diffInHours = Math.floor(diffInMinutes / 60);
        if (diffInHours === 1) return "1 hour ago";
        if (diffInHours < 24) return `${diffInHours} hours ago`;
  
        const diffInDays = Math.floor(diffInHours / 24);
        if (diffInDays === 1) return "1 day ago";
        if (diffInDays < 7) {
          return `${createdAt.toLocaleDateString(undefined, { weekday: "long" })}, ${createdAt.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' })}`;
        }
  
        return createdAt.toLocaleDateString(undefined, { month: "long", day: "numeric" });
      },
      getIcon(type) {
        switch (type) {
          case "message":
            return this.$options.components.MailIcon
          case "appointment":
            return this.$options.components.CalendarIcon
          case "session_end":
            return this.$options.components.AlertCircleIcon
          case "consultation":
            return this.$options.components.UserPlusIcon
          default:
            return this.$options.components.BellIcon
        }
      },
      async markAllAsRead() {
        try{
            const response = await axios.post('read_all/')
            this.notificationStore.markAllNotificationsAsRead()



        }catch(error){

        }
      },
     
      async markAsRead(id) {
        console.log(id)

        try{
            const response = await axios.post('read/',{id:id})
            this.notificationStore.markNotificationAsRead(id)


        }catch(error){

        }


      }
    }
  }
  </script>