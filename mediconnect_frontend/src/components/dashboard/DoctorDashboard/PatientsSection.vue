<template>
  <section class="bg-white rounded-xl shadow-sm border border-gray-200">
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
            <tr v-for="appointment in recentAppointments" :key="appointment.id">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">{{ appointment.created_by.first_name }} {{ appointment.created_by.last_name }}</div>
              </td>
              <td
                v-if="appointment.created_by.display_age"
                class="px-6 py-4 whitespace-nowrap"
              >
                <div class="text-sm text-gray-500">{{ appointment.created_by.display_age }}</div>
              </td>
              <td
                v-else
                class="px-6 py-4 whitespace-nowrap"
              >
                <div class="text-sm text-gray-500">No dob set</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-500">{{ formatDate(appointment.created_at) }}</div>
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
      recentAppointments: {
        type: Array,
        required: true,
      },
      formatDate: {
       type: Function,
       required: true,
     },
    },
  };
  </script>
  
  