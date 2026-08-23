import axios from "axios";

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

export default client;