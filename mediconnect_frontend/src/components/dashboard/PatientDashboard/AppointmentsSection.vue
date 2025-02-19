<template>
  <section class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
    <div class="p-6">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Appointments</h3>
      <div class="space-y-4">
        <div 
          v-for="appointment in appointments" 
          :key="appointment.id" 
          class="flex justify-between items-center border-b border-gray-200 pb-4 last:border-b-0"
        >
          <div>
            <p v-if="appointment.created_for">
              <span class="font-semibold">Dr {{ appointment.created_for.first_name }} {{ appointment.created_for.last_name }}</span>
              <p class="text-sm text-gray-500">{{ appointment.created_for.speciality }}</p>
            </p>
            <p v-else class="text-sm text-red-500 font-semibold">Doctor not yet allocated</p>

            <p class="text-sm text-gray-500">{{ formatDate(appointment.created_at) }}</p>
          </div>
          <span :class="[
            'px-2 py-1 rounded-full text-xs font-semibold',
            appointment.status === 'processed' ? 'bg-yellow-100 text-yellow-800' :
            appointment.status === 'sent' ? 'bg-blue-100 text-blue-800' :
            appointment.status === 'done' ? 'bg-green-100 text-green-800' :  
            appointment.status === 'in_session' ? 'bg-orange-100 text-orange-800' : ''  
          ]">
            {{ appointment.status }}
          </span>
        </div>
      </div>
    </div>
  </section>
</template>


<script>
export default {
  name: 'AppointmentsSection',
  props: {
    formatDate: {
       type: Function,
       required: true,
     },
    appointments: {
      type: Array,
      required: true,
    },
  },
  
};
</script>

