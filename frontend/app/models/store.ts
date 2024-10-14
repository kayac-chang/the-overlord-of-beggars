import { z } from "zod";

export const StoreSchema = z.object({
  /** @description 店號 */
  id: z.string(),
  /** @description 店名 */
  name: z.string(),
  /** @description 地址 */
  address: z.string(),
  /** @description 與用戶的直線距離 (nullable, default: --) */
  distance: z.number().nullish(),
});

export type Store = z.infer<typeof StoreSchema>;
