import client from "../client";
import { ENDPOINTS } from "../endpoints";

export const getProducts = async () => {
  const response = await client.get(ENDPOINTS.PRODUCTS);

  return response.data;
};