import { z } from "zod";
import { StoreSchema } from "./store";
import { NearExpiredFoodSchema } from "./near_expired_food";

export const StoreWithNearExpiredFoodSchema = StoreSchema.merge(
  z.object({
    nearExpiredFoods: z.array(NearExpiredFoodSchema),
  })
);
export type StoreWithNearExpiredFood = z.infer<
  typeof StoreWithNearExpiredFoodSchema
>;
