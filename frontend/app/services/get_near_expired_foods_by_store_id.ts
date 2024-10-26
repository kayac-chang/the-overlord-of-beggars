import { z } from "zod";
import { ResponseSchema, api } from "./shared";
import {
  NearExpiredFood,
  NearExpiredFoodSchema,
} from "~/models/near_expired_food";
import { SUPPORT_BRANDS } from "~/models/brand";

const InputSchema = z.object({
  storeid: z.string(),
  brand: z.enum(SUPPORT_BRANDS),
});
type Input = z.infer<typeof InputSchema>;

async function getNearExpiredFoodsByStoreId(
  input: Input
): Promise<NearExpiredFood[]> {
  return InputSchema.parseAsync(input)
    .then(({ brand, storeid }) =>
      api.get(`stores/${brand}/${storeid}/stock`).json()
    )
    .then(ResponseSchema(z.array(NearExpiredFoodSchema)).parseAsync)
    .then(({ data }) => data);
}

export default getNearExpiredFoodsByStoreId;
