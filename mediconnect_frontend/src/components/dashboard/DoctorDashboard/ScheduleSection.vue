<template>
    <section class="bg-white rounded-xl shadow-sm border border-gray-200">
      <div class="p-6">
        <h3 class="text-xl font-semibold text-gray-900 mb-4">Weekly Schedule</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          <div v-for="day in schedule" :key="day.day" class="bg-gray-50 p-4 rounded-lg">
            <h4 class="font-semibold text-gray-700">{{ day.day }}</h4>
            <p class="text-sm text-gray-600">{{ day.hours }}</p>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    name: 'ScheduleSection',
    props: {
      schedule: {
        type: Array,
        required: true,
      },
    },
  };
  </script>
  
  