<template>
    <section class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
      <div class="p-6">
        <h3 class="text-xl font-semibold text-gray-900 mb-4">Current Medications</h3>
        <div class="space-y-4">
          <div v-for="(medication, index) in medications" :key="index" class="flex justify-between items-center border-b border-gray-200 pb-4 last:border-b-0">
            <div>
              <p class="font-semibold">{{ medication.name }}</p>
              <p class="text-sm text-gray-500">{{ medication.dosage }}</p>
              <p class="text-sm text-gray-500">{{ medication.frequency }}</p>
            </div>
            <button class="px-3 py-1 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors">Set Reminder</button>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    name: 'MedicationsSection',
    props: {
      medications: {
        type: Array,
        required: true,
      },
    },
  };
  </script>
  
  