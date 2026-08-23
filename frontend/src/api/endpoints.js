export const ENDPOINTS = {
  AUTH: {
    LOGIN: "/auth/login",
    SIGNUP: "/auth/signup",
  },

  USERS: {
    SEARCH: "/users/search",
    GET_BY_ID: (userId) => `/users/${userId}`,
    CREATE_INTERNAL: "/users/register/internal",
    APPROVE: (userId) => `/users/${userId}/approve`,
    REJECT: (userId) => `/users/${userId}/reject`,
    ACTIVATE: (userId) => `/users/${userId}/activate`,
    DEACTIVATE: (userId) => `/users/${userId}/deactivate`,
    CHANGE_ROLE: (userId) => `/users/${userId}/change-role`,
    PROFILE: "/users/profile",
    CHANGE_PASSWORD: "/users/change-password",
  },

  PRODUCTS: "/products",
  INVENTORY: "/inventories",
  SUPPLIERS: "/suppliers",
  PURCHASE_ORDERS: "/purchase-orders",
  SALES_ORDERS: "/sales-orders",
  FORECASTING: "/forecasting",
};