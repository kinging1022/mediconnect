<template>
    <section class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
      <div class="p-6">
        <h3 class="text-xl font-semibold text-gray-900 mb-4">Recent Patients</h3>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Age</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Last Visit</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="patient in patients" :key="patient.name">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900">{{ patient.name }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-500">{{ patient.age }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-500">{{ patient.lastVisit }}</div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    name: 'PatientsSection',
    props: {
      patients: {
        type: Array,
        required: true,
      },
    },
  };
  </script>
  
  