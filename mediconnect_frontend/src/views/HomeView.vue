<template>
 <section class="w-full px-4 pt-32 pb-20 bg-gradient-to-br from-blue-50 via-white to-blue-50">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between">
        <div class="md:w-1/2 mb-10 md:mb-0">
          <div class="inline-flex items-center px-4 py-2 bg-blue-100 rounded-full text-blue-600 font-medium text-sm mb-6">
            <Star class="w-4 h-4 mr-2" /> Trusted by 10,000+ Healthcare Providers
          </div>
          <h1 class="text-4xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            Connect with Your Doctor
            <span class="text-blue-600"> Anytime, Anywhere</span>
          </h1>
          <p class="text-xl text-gray-600 mb-8 leading-relaxed">
            Experience healthcare reimagined with secure, instant communication. Get the personalized care you need, right when you need it.
          </p>
          <div class="flex flex-col sm:flex-row gap-4">
            <button class="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg hover:bg-blue-700 transition-colors duration-300 flex items-center justify-center">
              Start Free Trial
              <ChevronRight class="ml-2" :size="20" />
            </button>
            <button class="border-2 border-gray-200 text-gray-700 px-8 py-3 rounded-lg text-lg hover:border-blue-600 hover:text-blue-600 transition-colors duration-300">
              Watch Demo
            </button>
          </div>
          <div class="mt-8 flex items-center space-x-4">
            <div class="flex -space-x-2">
              <img
                v-for="i in 4"
                :key="i"
                :src="`https://i.pravatar.cc/40?img=${i}`"
                alt="User"
                class="w-8 h-8 rounded-full border-2 border-white"
              />
            </div>
            <div class="text-sm text-gray-600">
              <span class="font-semibold text-gray-900">4.9/5</span> from over 1,000+ reviews
            </div>
          </div>
        </div>
        <div class="md:w-1/2 relative">
          <div class="absolute inset-0 bg-gradient-to-r from-blue-500 to-blue-600 transform rotate-3 rounded-2xl opacity-10"></div>
          <img
            src="https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80"
            alt="Doctor using digital tablet"
            class="rounded-2xl shadow-2xl relative z-10"
          />
        </div>
      </div>
    </section>

    <section class="w-full px-4 py-12 bg-white border-y border-gray-100">
      <div class="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8">
        <div v-for="stat in stats" :key="stat.number" class="text-center">
          <div class="text-3xl md:text-4xl font-bold text-blue-600 mb-2">
            {{ stat.number }}
          </div>
          <div class="text-gray-600">{{ stat.label }}</div>
        </div>
      </div>
    </section>

    <section id="features" class="w-full px-4 py-20 bg-white">
      <div class="max-w-7xl mx-auto">
        <div class="text-center max-w-3xl mx-auto mb-16">
          <h2 class="text-3xl md:text-4xl font-bold mb-6">
            Why Healthcare Providers Choose MediConnect
          </h2>
          <p class="text-xl text-gray-600">
            Powerful features that transform the way you deliver and receive healthcare
          </p>
        </div>
        <div class="grid md:grid-cols-3 gap-8">
          <div v-for="feature in features" :key="feature.title" class="p-6 bg-white rounded-xl border hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1">
            <div class="w-12 h-12 bg-blue-50 rounded-lg flex items-center justify-center mb-4">
              <component :is="feature.icon" class="text-blue-600" :size="32" />
            </div>
            <h3 class="text-xl font-semibold mb-2">{{ feature.title }}</h3>
            <p class="text-gray-600 leading-relaxed">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <section id="how-it-works" class="w-full px-4 py-20 bg-gray-50">
      <div class="max-w-7xl mx-auto">
        <div class="text-center max-w-3xl mx-auto mb-16">
          <h2 class="text-3xl md:text-4xl font-bold mb-6">
            Simple Steps to Better Healthcare
          </h2>
          <p class="text-xl text-gray-600">
            Get started with MediConnect in three easy steps
          </p>
        </div>
        <div class="grid md:grid-cols-3 gap-8 relative">
          <div class="hidden md:block absolute top-1/2 left-1/4 right-1/4 h-0.5 bg-blue-100"></div>
          <div v-for="step in steps" :key="step.number" class="p-6 bg-white rounded-xl shadow-lg relative z-10">
            <div class="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold mb-4 text-lg">
              {{ step.number }}
            </div>
            <h3 class="text-xl font-semibold mb-2">{{ step.title }}</h3>
            <p class="text-gray-600 leading-relaxed">{{ step.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <section id="testimonials" class="w-full px-4 py-20 bg-white">
      <div class="max-w-7xl mx-auto">
        <div class="text-center max-w-3xl mx-auto mb-16">
          <h2 class="text-3xl md:text-4xl font-bold mb-6">
            Trusted by Healthcare Professionals
          </h2>
          <p class="text-xl text-gray-600">
            See what our users have to say about MediConnect
          </p>
        </div>
        <div class="grid md:grid-cols-3 gap-8">
          <div v-for="testimonial in testimonials" :key="testimonial.author" class="p-6 bg-white rounded-xl border hover:shadow-lg transition-all duration-300">
            <div class="flex items-center mb-4">
              <img :src="testimonial.image" :alt="testimonial.author" class="w-12 h-12 rounded-full mr-4" />
              <div>
                <div class="font-semibold">{{ testimonial.author }}</div>
                <div class="text-gray-600 text-sm">{{ testimonial.role }}</div>
              </div>
            </div>
            <p class="text-gray-600 italic">"{{ testimonial.quote }}"</p>
          </div>
        </div>
      </div>
    </section>

    <section class="w-full px-4 py-20 bg-gradient-to-br from-blue-600 to-blue-700">
      <div class="max-w-4xl mx-auto text-center">
        <h2 class="text-3xl md:text-4xl font-bold text-white mb-6">
          Ready to Transform Your Healthcare Experience?
        </h2>
        <p class="text-xl text-blue-100 mb-8">
          Join thousands of healthcare providers and patients who have already simplified their healthcare journey.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <button class="bg-white text-blue-600 px-8 py-3 rounded-lg text-lg hover:bg-blue-50 transition-colors duration-300">
            Get Started Free
          </button>
          <button class="border-2 border-white text-white px-8 py-3 rounded-lg text-lg hover:bg-blue-500 transition-colors duration-300">
            Contact Sales
          </button>
        </div>
      </div>
    </section>
</template>

<script>
import {
  MessageSquare,
  Clock,
  Shield,
  ChevronRight,
  Star,
  Users,
  Check,
} from 'lucide-vue-next'

export default {
  name: 'App',
  components: {
    MessageSquare,
    Clock,
    Shield,
    ChevronRight,
    Star,
    Users,
    Check,
  },
  data() {
    return {
      stats: [
        { number: '10k+', label: 'Active Users' },
        { number: '95%', label: 'Satisfaction Rate' },
        { number: '24/7', label: 'Support Available' },
        { number: '50+', label: 'Healthcare Partners' },
      ],
      features: [
        {
          icon: MessageSquare,
          title: 'Instant Messaging',
          description: 'Direct communication with your healthcare provider through secure messaging.',
        },
        {
          icon: Shield,
          title: 'Secure & Private',
          description: 'Your data is protected with enterprise-grade security and encryption.',
        },
        {
          icon: Clock,
          title: '24/7 Access',
          description: 'Get medical attention whenever you need it, day or night.',
        },
      ],
      steps: [
        {
          number: '1',
          title: 'Create Account',
          description: 'Sign up and fill in your medical profile in minutes.',
        },
        {
          number: '2',
          title: 'Connect with Doctor',
          description: 'Choose your healthcare provider or connect with your existing one.',
        },
        {
          number: '3',
          title: 'Start Conversation',
          description: 'Begin secure conversations and receive care guidance.',
        },
      ],
      testimonials: [
        {
          quote: 'MediConnect has transformed how I communicate with my patients. It\'s efficient and secure.',
          author: 'Dr. Sarah Johnson',
          role: 'Cardiologist',
          image: 'https://i.pravatar.cc/100?img=1',
        },
        {
          quote: 'The platform is intuitive and has greatly improved our patient engagement rates.',
          author: 'Dr. Michael Chen',
          role: 'Family Physician',
          image: 'https://i.pravatar.cc/100?img=2',
        },
        {
          quote: 'As a patient, I love how easy it is to reach my doctor when I need to.',
          author: 'Emily Rodriguez',
          role: 'Patient',
          image: 'https://i.pravatar.cc/100?img=3',
        },
      ],
    }
  },
  methods: {
    
  },
 
}
</script>

<style scoped>
/* Add any component-specific styles here */
</style>
