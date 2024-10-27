import { z } from "zod";

export const GeoLocationSchema = z.object({
  latitude: z.number(),
  longitude: z.number(),
});

export type GeoLocation = z.infer<typeof GeoLocationSchema>;

export function toString(location: GeoLocation): string {
  return `${location.latitude},${location.longitude}`;
}

export function deserialize(location: string): GeoLocation {
  const [latitude, longitude] = location.split(",").map(Number);
  return GeoLocationSchema.parse({ latitude, longitude });
}

export default {
  schema: GeoLocationSchema,
  serialize: toString,
  deserialize,
};
