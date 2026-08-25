import axios from "axios";
import { store } from "../store/store";
import { clearAuth } from "../store/slices/authSlice";

const client = axios.create({
  baseURL: import.meta.env.VITE_API_GATEWAY_URL,
});

client.interceptors.request.use(
  (config) => {
    const token =
      localStorage.getItem("accessToken") ||
      sessionStorage.getItem("accessToken");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error),
);

// Response Interceptor to Handle Expired Tokens
client.interceptors.response.use(
  (response) => response,
  (error) => {
    // Check if error response status is 401 Unauthorized
    if (error.response && error.response.status === 401) {
      // Dispatch clearAuth to reset Redux state and wipe storage
      store.dispatch(clearAuth());

      // Hard redirect to login page (if not already there)
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }

    return Promise.reject(error);
  }
);

export default client;