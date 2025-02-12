<template>
    <section class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
      <div class="p-6">
        <h3 class="text-xl font-semibold text-gray-900 mb-4">Vitals Information</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div v-for="(value, key) in vitals" :key="key" class="bg-gray-100 p-4 rounded-lg">
            <p class="text-sm text-gray-500">{{ key }}</p>
            <p class="text-lg font-semibold">{{ value }}</p>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    name: 'VitalsSection',
    props: {
      vitals: {
        type: Object,
        required: true,
      },
    },
  };
  </script>
  
  