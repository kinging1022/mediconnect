<template>
  <section aria-labelledby="medications-title">
        <div class="rounded-lg bg-white overflow-hidden shadow mb-8">
          <div class="p-6">
            <h2 class="text-lg font-medium text-gray-900" id="medications-title">Medications</h2>
            <div class="mt-6 flow-root">
              <ul class="-my-5 divide-y divide-gray-200">
                <li
                  v-for="medication in medications"
                  :key="medication.id"
                  class="py-5"
                >
                  <div class="flex items-center space-x-4">
                    <div class="flex-shrink-0">
                      <Pill class="h-8 w-8 text-indigo-600" />
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-gray-900 truncate">
                        {{ medication.name }}
                      </p>
                      <p class="text-sm text-gray-500 truncate">
                        {{ `${medication.weight}mg - ${medication.dosage}` }}
                      </p>
                    </div>
                    <div>
                      <button v-if="medication.has_reminder"
                          @click="DeleteReminder(medication.id)"
                          class="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                          >
                          Delete Reminder
                      </button>
                      <button v-else
                          @click="openReminderModal(medication.id)"
                          class="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                          >
                          Set Reminder
                      </button>

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
import axios from 'axios';
import {Pill} from 'lucide-vue-next';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';
export default{
  name:'Medication',
  components:{
      Pill
      

  },
  props:{
      medications:{
          type:Array,
          Required:true
      }
      

  },
  data(){
      return{
          userStore: useUserStore(),
          toastStore: useToastStore()

      }
  },
  mounted(){


  },
  methods:{
      openReminderModal(medicationId) {
          this.$emit('medics', medicationId)

      },
      async DeleteReminder(medicationId){
          try{
          const response = await axios.post(`reminder/${medicationId}/delete/`)
          this.toastStore.showToast(5000, 'Reminder deleted succesfully', "bg-red-500");

          const updatedMedication = this.medications.find(medication => medication.id === medicationId)
          if(updatedMedication){
              updatedMedication.has_reminder = false;
          }
          
          
          }catch(error){
              console.log(error);
              this.toastStore.showToast(5000, "Error deleting reminder", "bg-red-500");
          }
      }
      

  }
}



</script>
