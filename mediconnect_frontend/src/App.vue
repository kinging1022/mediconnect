<template>
  <div class="w-full min-h-screen bg-white mt-7">
    <header
    v-if="!$route.meta.hideHeaderFooter"
      :class="[
        'w-full px-4 fixed top-0 z-50 transition-all duration-300',
        scrolled ? 'py-2 bg-white/90 backdrop-blur-sm shadow-sm' : 'py-4 bg-transparent'
      ]"
    >
      <div class="max-w-7xl mx-auto flex justify-between items-center">
        <RouterLink to="/" class="text-2xl font-bold text-blue-600 flex items-center">
          <div class="w-8 h-8 bg-blue-600 rounded-lg mr-2"></div>
          MediConnect
        </RouterLink>
        <nav class="hidden md:flex space-x-8">
          <RouterLink  
            v-for="link in filteredNavLinks" 
            :key="link.href" 
            :to="link.href" 
            class="text-gray-600 hover:text-blue-600 transition-colors duration-300 font-medium">
            {{ link.text }}
          </RouterLink>
        </nav>

        <div class="flex items-center space-x-4">
          <RouterLink to="/notifications">
          <div class="relative">
            <Bell :size="24" class="text-gray-600 hover:text-blue-600 cursor-pointer" />
            <div v-if="hasNotifications" class="absolute top-0 right-0 w-2 h-2 bg-blue-500 rounded-full"></div>
          </div>
          </RouterLink>
          
          <RouterLink 
              v-if="sessionId"
              :to="{ name: 'session', params: { id: sessionId } }"
            >
              <div class="relative">
                <User :size="24" class="text-gray-600 hover:text-blue-600 cursor-pointer" />
                <div v-if="sessionId" class="absolute top-0 right-0 w-2 h-2 bg-blue-500 rounded-full"></div>
              </div>
        </RouterLink>

          
          <template v-if="!userStore.user.isAuthenticated">
            <RouterLink to="/login" class="hidden md:inline-block text-gray-600 hover:text-blue-600 font-medium">
              Sign in
            </RouterLink>
            <RouterLink to="/signup" class="hidden md:flex bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-300 items-center">
              Get Started
              <ChevronRight class="ml-2 w-4 h-4" />
            </RouterLink>
          </template>
        </div>
        <button
          class="md:hidden text-gray-600 hover:text-blue-600"
          @click="isOpen = true"
        >
          <Menu :size="24" />
        </button>
      </div>
    </header>

    <div v-if="isOpen" class="fixed inset-0 bg-white z-50 md:hidden">
      <div class="p-4">
        <div class="flex justify-between items-center mb-8">
          <div class="text-2xl font-bold text-blue-600">
            MediConnect
          </div>
          <button
            class="text-gray-600"
            @click="isOpen = false"
          >
            <X :size="24" />
          </button>
        </div>
        <nav class="space-y-6">
          <RouterLink
            v-for="link in filteredNavLinks" 
            :key="link.href" 
            :to="link.href" 
            class="block text-xl font-medium text-gray-800 hover:text-blue-600"
            @click="isOpen = false"
          >
            {{ link.text }}
          </RouterLink>
          <template v-if="!userStore.user.isAuthenticated">
            <div class="pt-6 space-y-4">
              <RouterLink to="/login" class="block w-full text-gray-600 py-2 font-medium">
                Sign in
              </RouterLink>
              <RouterLink to="/signup" class="block w-full bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700">
                Get Started
              </RouterLink>
            </div>
          </template>
        </nav>
      </div>
    </div>
    
    <section class="pt-10">
      <RouterView/>
    </section>
    <Toast />

    <footer 
    v-if="!$route.meta.hideHeaderFooter"
    class="w-full px-4 py-12 bg-gray-900 text-gray-300">
      <div class="max-w-7xl mx-auto">
        <div class="grid md:grid-cols-4 gap-8 mb-12">
          <div>
            <div class="text-2xl font-bold text-white mb-4 flex items-center">
              <div class="w-8 h-8 bg-blue-600 rounded-lg mr-2"></div>
              MediConnect
            </div>
            <p class="text-gray-400">
              Transforming healthcare communication for better patient outcomes.
            </p>
          </div>
          <div v-for="(links, title) in footerLinks" :key="title">
            <h3 class="text-lg font-semibold mb-4">{{ title }}</h3>
            <ul class="space-y-2">
              <li v-for="link in links" :key="link.href">
                <a
                  :href="link.href"
                  class="hover:text-white transition-colors duration-300"
                >
                  {{ link.text }}
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div class="pt-8 border-t border-gray-800 text-center text-gray-400">
          <p>© 2024 MediConnect. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from "./stores/user";
import Toast from "@/components/Toast.vue";
import { useNotificationStore } from './stores/notification';

import {  
  Menu,
  X,
  ChevronRight,
  Bell,
  User
} from 'lucide-vue-next'

export default {
  name: 'App',
  components: {
    Menu,
    X,
    ChevronRight,
    Bell,
    User,
    Toast,
  },
  setup(){
    const userStore = useUserStore()
    const notificationStore = useNotificationStore()

    return {
      userStore,
      notificationStore
    }

  },
  computed:{
    filteredNavLinks() {
      if (this.userStore.user.isAuthenticated) {
        return this.navLinks;
      } else {
        return this.navLinks.filter(link => link.href !== '/dashboard');
      }
    },
    hasNotifications() {
    return this.notificationStore.hasUnreadNotifications
    },
    sessionId() {
      return this.userStore.activeSession.id || null;
    },

  },
  data() {
    return {
      isOpen: false,
      scrolled: false,
      navLinks: [
        {href: '/dashboard', text:'Dashboard'},
        { href: '#features', text: 'Features' },
        { href: '#how-it-works', text: 'How it works' },
        { href: '#testimonials', text: 'Testimonials' },
      ],
      footerLinks: {
        Product: [
          { href: '#features', text: 'Features' },
          { href: '#how-it-works', text: 'How it works' },
          { href: '#pricing', text: 'Pricing' },
        ],
        Company: [
          { href: '#about', text: 'About' },
          { href: '#careers', text: 'Careers' },
          { href: '#contact', text: 'Contact' },
        ],
        Legal: [
          { href: '#privacy', text: 'Privacy Policy' },
          { href: '#terms', text: 'Terms of Service' },
          { href: '#compliance', text: 'Compliance' },
        ],
      },
    }
  },
  methods: {
    handleScroll() {
      this.scrolled = window.scrollY > 20
    },
    logout(){
      this.userStore.removeToken()
      this.$router.push('/login')
    },
    
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll)
    this.userStore.initStore();
    this.userStore.getActiveSession();
    if(this.userStore.user.access){
      this.notificationStore.initWebSocket()
    }

   
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll)
  },
}
</script>

<style scoped>
/* Add any component-specific styles here */
</style>