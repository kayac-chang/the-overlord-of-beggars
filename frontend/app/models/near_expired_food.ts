import { z } from "zod";

export const NearExpiredFoodSchema = z.object({
  /** @description 品名 */
  name: z.string(),
  /** @description 品項 */
  category_name: z.string(),
  /** @description 數量 */
  quantity: z.number(),
});
export type NearExpiredFood = z.infer<typeof NearExpiredFoodSchema>;
