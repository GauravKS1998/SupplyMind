import { createSlice } from "@reduxjs/toolkit";

const storedToken =
  localStorage.getItem("accessToken") ||
  sessionStorage.getItem("accessToken");

const storedUser =
  localStorage.getItem("user") ||
  sessionStorage.getItem("user");

const initialState = {
  token: storedToken || null,
  user: storedUser ? JSON.parse(storedUser) : null,
  isAuthenticated: !!storedToken,
};

const authSlice = createSlice({
  name: "auth",

  initialState,

  reducers: {
    loginSuccess: (state, action) => {
      const { token, user, rememberMe = false } = action.payload;

      state.token = token;
      state.user = user;
      state.isAuthenticated = true;

      // Clear any previous session first.
      localStorage.removeItem("accessToken");
      localStorage.removeItem("user");

      sessionStorage.removeItem("accessToken");
      sessionStorage.removeItem("user");

      const storage = rememberMe ? localStorage : sessionStorage;

      storage.setItem("accessToken", token);
      storage.setItem("user", JSON.stringify(user));
    },

    updateUser: (state, action) => {
      state.user = {
        ...state.user,
        ...action.payload,
      };

      const userStorage =
        localStorage.getItem("user") !== null
          ? localStorage
          : sessionStorage;

      userStorage.setItem(
        "user",
        JSON.stringify(state.user),
      );
    },

    logout: (state) => {
      state.token = null;
      state.user = null;
      state.isAuthenticated = false;

      localStorage.removeItem("accessToken");
      localStorage.removeItem("user");

      sessionStorage.removeItem("accessToken");
      sessionStorage.removeItem("user");
    },

    clearAuth: (state) => {
      state.token = null;
      state.user = null;
      state.isAuthenticated = false;

      localStorage.removeItem("accessToken");
      localStorage.removeItem("user");

      sessionStorage.removeItem("accessToken");
      sessionStorage.removeItem("user");
    },
  },
});

export const {
  loginSuccess,
  updateUser,
  logout,
  clearAuth,
} = authSlice.actions;

export default authSlice.reducer;