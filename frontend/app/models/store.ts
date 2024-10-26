import { z } from "zod";
import { SUPPORT_BRANDS } from "./brand";

export const StoreSchema = z.object({
  /** @description 店號 */
  id: z.string(),
  /** @description 店名 */
  name: z.string(),
  /** @description 地址 */
  address: z.string(),
  /** @description 與用戶的直線距離 (nullable, default: --) */
  distance: z.number().nullish(),
  /** @description 品牌 */
  brand: z.enum(SUPPORT_BRANDS),
});

export type Store = z.infer<typeof StoreSchema>;
