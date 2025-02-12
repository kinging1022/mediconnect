<template>
  <section class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
    <div class="p-6">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Upcoming Appointments</h3>
      <div class="space-y-4">
        <div v-for="(appointment, index) in appointments" :key="index" class="flex justify-between items-center border-b border-gray-200 pb-4 last:border-b-0">
          <div>
            <p class="font-semibold">{{ appointment.doctor }}</p>
            <p class="text-sm text-gray-500">{{ appointment.date }} at {{ appointment.time }}</p>
            <p class="text-sm text-gray-500">{{ appointment.type }}</p>
          </div>
          <span :class="[
            'px-2 py-1 rounded-full text-xs font-semibold',
            appointment.status === 'confirmed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
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
    appointments: {
      type: Array,
      required: true,
    },
  },
};
</script>

