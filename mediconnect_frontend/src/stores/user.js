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
      access: null,
      refresh: null,
    },
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
        access: null,
        refresh: null,
        role: null,
        gender:null
      };
      localStorage.removeItem("user");
    },

    async refreshToken() {
      try {
        const response = await axios.post("auth/token/refresh/", {
          refresh: this.user.refresh,
        });
        this.user.access = response.data.access;
        this.saveUserToLocalStorage();
      } catch (error) {
        if (error.response && error.response.status === 400) {
          console.log("Refresh token expired or invalid. Logging out.");
          this.removeToken();
        } else {
          throw new Error("Token refresh failed");
        }
      }
    },

    saveUserToLocalStorage() {
      localStorage.setItem("user", JSON.stringify(this.user));
    },
  },
});


