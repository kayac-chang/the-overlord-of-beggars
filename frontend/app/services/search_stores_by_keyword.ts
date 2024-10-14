import { z } from "zod";
import { GeoLocationSchema } from "~/models/geolocation";
import { StoreWithNearExpiredFood } from "~/models/store_with_near_expired_foods";

const InputSchema = z.object({
  // 關鍵字 (店名，地址，品名)
  keyword: z.string(),
  // 用戶的當前位置 (optional)
  location: GeoLocationSchema.optional(),
});

type Input = z.infer<typeof InputSchema>;

function searchStoresByKeyword(
  input: Input
): Promise<StoreWithNearExpiredFood[]> {
  throw new Error("Not implemented");
}

export default searchStoresByKeyword;
