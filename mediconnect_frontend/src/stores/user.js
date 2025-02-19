import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore("user", {
  state: () => ({
    user: {
      isAuthenticated: false,
      first_name: null,
      last_name: null,
      email: null,
      gender:null,
      role:null,
      phone:null,
      dob:null,
      display_age: null,
      weight:null,
      height:null,
      allergies: null,
      emergency_contact_number : null,
      emergency_contact_name: null,
      blood_type: null,
      speciality:null,
      access: null,
      refresh: null,
    },
    activeSession: {},
  }),
        

  actions: {

    initStore() {
      const storedUser = localStorage.getItem("user");
      if (storedUser) {
        const parsedUser = JSON.parse(storedUser);
        this.user = { ...this.user, ...parsedUser, isAuthenticated: true };
      }
    },

    setToken(data) {
      this.user.access = data.access;
      this.user.refresh = data.refresh;
      this.user.isAuthenticated = true;
      this.saveUserToLocalStorage();
    },

    setUserInfo(user) {
      this.user = { ...this.user, ...user };
      this.saveUserToLocalStorage();
    },

    removeToken() {
      this.user = {
        isAuthenticated: false,
        first_name: null,
        last_name: null,
        email: null,
        role: null,
        gender:null,
        phone:null,
        dob:null,
        display_age: null,
        weight:null,
        height:null,
        allergies: null,
        emergency_contact_number : null,
        emergency_contact_name: null,
        blood_type: null,
        speciality:null,
        access: null,
        refresh: null,
      };
      this.activeSession = {};
      localStorage.removeItem("user");
    },

    async refreshToken() {
      if (!this.user.refresh) {
        this.removeToken();
        throw new Error("No refresh token available");
      }
      
      try {
        const response = await axios.post("auth/token/refresh/", {
          refresh: this.user.refresh,
        }, {
          // Important: don't use the interceptors for this request to avoid loops
          _skipAuthRefresh: true
        });
        
        if (response.data && response.data.access) {
          this.user.access = response.data.access;
          this.saveUserToLocalStorage();
          return response.data.access;
        } else {
          throw new Error("Invalid refresh token response");
        }
      } catch (error) {
        console.log("Refresh token expired or invalid. Logging out.");
        this.removeToken();
        throw error;
      }
    },
    
    async getActiveSession() {

      try{
            const response = await axios.get('session/active/')
            this.activeSession = response.data
            console.log('active id',response.data.id)
            this.activeSessionStatus = response.data.status
            
            
      }catch(error){
        if (error){
          this.activeSession = {}
          this.activeSessionStatus = null
        }

      }


  },
  clearActiveSession(){
    this.activeSession = {}

  },

    saveUserToLocalStorage() {
      localStorage.setItem("user", JSON.stringify(this.user));
    },
    
  },
});


