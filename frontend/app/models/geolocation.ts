import { z } from "zod";

export const GeoLocationSchema = z.object({
  latitude: z.number(),
  longitude: z.number(),
});

export type GeoLocation = z.infer<typeof GeoLocationSchema>;
