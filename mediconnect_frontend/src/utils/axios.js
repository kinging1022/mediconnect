import axios from "axios";

// Create Axios instance
const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
  withCredentials: true, // Allows Django to send CSRF cookie
});

// Function to read CSRF token from cookies
function getCsrfTokenFromCookie() {
  const name = "csrftoken=";
  const cookies = document.cookie.split(";");
  for (let cookie of cookies) {
    while (cookie.charAt(0) === " ") {
      cookie = cookie.substring(1);
    }
    if (cookie.indexOf(name) === 0) {
      return cookie.substring(name.length, cookie.length);
    }
  }
  return null;
}

// Axios interceptor to attach CSRF token
api.interceptors.request.use((config) => {
  if (config.method !== "get") {
    const csrfToken = getCsrfTokenFromCookie(); // Get CSRF token from cookies
    if (csrfToken) {
      config.headers["X-CSRFToken"] = csrfToken;
    }
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export default api;
