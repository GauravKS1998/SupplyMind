import client from "../client";
import { ENDPOINTS } from "../endpoints";

export const getProducts = async () => {
  return await client.get(
    ENDPOINTS.PRODUCTS
  );
};