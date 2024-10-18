import z from "zod";

export default z
  .object({
    BACKEND_API_URL: z.string(),
  })
  .parse(process.env);
