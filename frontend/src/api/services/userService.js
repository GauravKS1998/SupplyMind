import client from "../client";
import { ENDPOINTS } from "../endpoints";

// --------------------------------------------------
// Get current user's profile
// --------------------------------------------------

export const getMyProfile = async () => {
  const response = await client.get(
    ENDPOINTS.USERS.PROFILE,
  );

  return response.data;
};

// --------------------------------------------------
// Update current user's profile
// --------------------------------------------------

export const updateMyProfile = async (payload) => {
  const response = await client.put(
    ENDPOINTS.USERS.PROFILE,
    payload,
  );

  return response.data;
};

// --------------------------------------------------
// Change current user's password
// --------------------------------------------------

export const changePassword = async (payload) => {
  const response = await client.patch(
    ENDPOINTS.USERS.CHANGE_PASSWORD,
    payload,
  );

  return response.data;
};

// --------------------------------------------------
// Search users
// --------------------------------------------------

export const searchUsers = async (payload) => {
  const response = await client.post(
    ENDPOINTS.USERS.SEARCH,
    payload,
  );

  return response.data;
};

// --------------------------------------------------
// Get user by ID
// --------------------------------------------------

export const getUserById = async (userId) => {
  const response = await client.get(
    ENDPOINTS.USERS.GET_BY_ID(userId),
  );

  return response.data;
};

// --------------------------------------------------
// Create internal employee
// --------------------------------------------------

export const createInternalUser = async (payload) => {
  const response = await client.post(
    ENDPOINTS.USERS.CREATE_INTERNAL,
    payload,
  );

  return response.data;
};

// --------------------------------------------------
// Approve user
// --------------------------------------------------

export const approveUser = async (userId) => {
  const response = await client.patch(
    ENDPOINTS.USERS.APPROVE(userId),
  );

  return response.data;
};

// --------------------------------------------------
// Reject user
// --------------------------------------------------

export const rejectUser = async (userId, payload) => {
  const response = await client.patch(
    ENDPOINTS.USERS.REJECT(userId),
    payload,
  );

  return response.data;
};

// --------------------------------------------------
// Activate user
// --------------------------------------------------

export const activateUser = async (userId) => {
  const response = await client.patch(
    ENDPOINTS.USERS.ACTIVATE(userId),
  );

  return response.data;
};

// --------------------------------------------------
// Deactivate user
// --------------------------------------------------

export const deactivateUser = async (userId) => {
  const response = await client.patch(
    ENDPOINTS.USERS.DEACTIVATE(userId),
  );

  return response.data;
};

// --------------------------------------------------
// Change user role
// --------------------------------------------------

export const changeUserRole = async (userId, payload) => {
  const response = await client.patch(
    ENDPOINTS.USERS.CHANGE_ROLE(userId),
    payload,
  );

  return response.data;
};