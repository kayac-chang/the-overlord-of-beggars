import { z } from "zod";
import { GeoLocationSchema } from "~/models/geolocation";
import { StoreWithNearExpiredFood } from "~/models/store_with_near_expired_foods";

const InputSchema = z.object({
  /** @description 品項 */
  category: z.string(),
  /** @description 用戶的當前位置 */
  location: GeoLocationSchema.optional(),
});

type Input = z.infer<typeof InputSchema>;

function searchStoresByItemCategory(
  input: Input
): Promise<StoreWithNearExpiredFood[]> {
  throw new Error("Not implemented");
}

export default searchStoresByItemCategory;
