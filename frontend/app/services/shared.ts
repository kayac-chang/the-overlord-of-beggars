import ky from "ky";
import { z } from "zod";

export const ResponseSchema = <T extends z.ZodTypeAny>(schema: T) =>
  z.object({
    data: schema,
  });

export const api = ky.extend({
  prefixUrl: "http://localhost:8000",
});
