import { z } from "zod";
import { ResponseSchema, api } from "./shared";
import {
  NearExpiredFood,
  NearExpiredFoodSchema,
} from "~/models/near_expired_food";

async function getNearExpiredFoodsByStoreId(
  storeid: string
): Promise<NearExpiredFood[]> {
  return z
    .string()
    .parseAsync(storeid)
    .then((storeid) => api.get(`stores/${storeid}/stock`).json())
    .then(ResponseSchema(z.array(NearExpiredFoodSchema)).parseAsync)
    .then(({ data }) => data);
}

export default getNearExpiredFoodsByStoreId;
