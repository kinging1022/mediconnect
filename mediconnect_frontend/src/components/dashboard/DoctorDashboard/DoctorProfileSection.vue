<template>
    <section class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
      <div class="p-6">
        <div class="flex justify-between items-center">
          <div>
            <h2 class="text-2xl font-semibold text-gray-900">{{ doctor.name }}</h2>
            <p class="text-md text-gray-600">{{ doctor.speciality }}</p>
            <p class="text-sm text-gray-500 mt-2">License: {{ doctor.license }}</p>
          </div>
          <div class="flex flex-col items-end">
            <p class="text-sm text-gray-500">{{ doctor.email }}</p>
            <p class="text-sm text-gray-500">{{ doctor.phone }}</p>
            <button @click="$emit('logout')" class="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors">Logout</button>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    name: 'DoctorProfileSection',
    props: {
      doctor: {
        type: Object,
        required: true,
      },
    },
  };
  </script>
  
  