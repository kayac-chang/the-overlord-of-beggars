import ky from "ky";
import { z } from "zod";
import env from "~/config";

export const ResponseSchema = <T extends z.ZodTypeAny>(schema: T) =>
  z.object({
    data: schema,
  });

export const api = ky.extend({
  prefixUrl: env.BACKEND_API_URL,
  timeout: false,
});
