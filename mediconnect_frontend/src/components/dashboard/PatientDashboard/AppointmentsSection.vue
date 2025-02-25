<template>
  <section aria-labelledby="appointments-title">
       <div class="rounded-lg bg-white overflow-hidden shadow mb-8">
         <div class="p-6">
           <h2 class="text-lg font-medium text-gray-900" id="appointments-title">Appointments</h2>
           <div class="mt-6 flow-root">
             <ul class="-my-5 divide-y divide-gray-200">
               <li
                 v-for="appointment in appointments"
                 :key="appointment.id"
                 class="py-5"
               >
                 <div class="flex items-center space-x-4">
                   <div class="flex-shrink-0">
                     <Calendar class="h-8 w-8 text-indigo-600" />
                   </div>
                   <div class="flex-1 min-w-0">
                     <p 
                     v-if="appointment.created_for"
                     class="text-sm font-medium text-gray-900 truncate">
                       Dr {{ appointment.created_for.first_name }} {{ appointment.created_for.last_name }} - {{ appointment.created_for.speciality }}
                     </p>
                     <p v-else class="text-sm text-red-500 font-semibold">Doctor not yet allocated</p>
                     <p class="text-sm text-gray-500 truncate">
                       {{ formatDate(appointment.created_at) }}
                     </p>
                   </div>
                   <div>
                     <span
                       :class="[
                         'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                         appointment.status === 'processed' ? 'bg-yellow-100 text-yellow-800' :
                         appointment.status === 'sent' ? 'bg-blue-100 text-blue-800' :
                         appointment.status === 'in_session' ? 'bg-orange-100 text-orange-800' :

                         appointment.status === 'done' ? 'bg-green-100 text-green-800' :
                         'bg-red-100 text-red-800'
                       ]"
                     >
                       {{ appointment.status }}
                     </span>
                   </div>
                 </div>
               </li>
             </ul>
           </div>
         </div>
       </div>
     </section>
</template>


<script>
import { Calendar } from 'lucide-vue-next';

export default {
  name: 'AppointmentsSection',
  components:{
       Calendar
   },
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

