<template>
    <section class="bg-white rounded-xl shadow-sm border border-gray-200">
      <div class="p-6">
        <h3 class="text-xl font-semibold text-gray-900 mb-4">Consultation History</h3>
        <div class="space-y-4">
          <div v-for="(consultation, index) in consultations" :key="index" class="border-b border-gray-200 pb-4 last:border-b-0">
            <p class="font-semibold">{{ consultation.doctor }}</p>
            <p class="text-sm text-gray-500">{{ consultation.date }}</p>
            <p class="text-sm">{{ consultation.summary }}</p>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    name: 'ConsultationsSection',
    props: {
      consultations: {
        type: Array,
        required: true,
      },
    },
  };
  </script>
  
  