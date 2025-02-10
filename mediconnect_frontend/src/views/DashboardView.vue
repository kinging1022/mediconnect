<template>
    <div>
        <component :is="dashboardComponent"/>
    </div>
</template>




<script>
import { useUserStore } from '@/stores/user';
import Patient from '@/components/dashboard/Patient.vue';
import Doctor from '@/components/dashboard/Doctor.vue';
import Admin from '@/components/dashboard/Admin.vue';
export default {
    setup(){
        const userStore = useUserStore()

        return{
            userStore
        }
    },
    data(){
        return {
            role : '',
        };
    },
    computed:{
        dashboardComponent(){
            switch(this.role){
                case "patient":
                    return Patient
                case "doctor":
                    return Doctor
                case "admin":
                    return Admin
            }
        }
    },
    created(){
        this.role = this.userStore.user.role
    }

}

</script>

