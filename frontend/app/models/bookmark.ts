import { z } from "zod";
import { SUPPORT_BRANDS } from "./brand";

export const BookmarkSchema = z.object({
  storeid: z.string(),
  brand: z.enum(SUPPORT_BRANDS),
});

export type Bookmark = z.infer<typeof BookmarkSchema>;
