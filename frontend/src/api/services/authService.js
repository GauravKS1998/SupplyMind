import client from "../client";
import { ENDPOINTS } from "../endpoints";

export const login = async (payload) => {
  const response = await client.post(
    ENDPOINTS.AUTH.LOGIN,
    payload,
  );

  return response.data;
};

export const signup = async (payload) => {
  const response = await client.post(
    ENDPOINTS.AUTH.SIGNUP,
    payload,
  );

  return response.data;
};