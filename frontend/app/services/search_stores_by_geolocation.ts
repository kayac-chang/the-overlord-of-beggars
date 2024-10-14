import { z } from "zod";
import { GeoLocationSchema } from "~/models/geolocation";
import { StoreWithNearExpiredFood } from "~/models/store_with_near_expired_foods";

const InputSchema = z.object({
  // 位置
  location: GeoLocationSchema.optional(),
  // 搜尋範圍 (單位: 公尺) (optional)
  distance: z.number().optional(),
});

type Input = z.infer<typeof InputSchema>;

function searchStoresByGeoLocation(
  input: Input
): Promise<StoreWithNearExpiredFood[]> {
  throw new Error("Not implemented");
}

export default searchStoresByGeoLocation;
