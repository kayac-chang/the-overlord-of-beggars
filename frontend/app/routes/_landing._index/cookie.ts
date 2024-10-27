import { z } from "zod";
import { createCookie } from "@remix-run/node";
import { Bookmark, BookmarkSchema } from "~/models/bookmark";

const Cookie = createCookie("bookmarks", {
  maxAge: 60 * 60 * 24 * 30, // 30 days
  httpOnly: true,
  secure: process.env.NODE_ENV === "production",
});

async function deserialize(request: Request): Promise<Bookmark[]> {
  return Cookie.parse(request.headers.get("Cookie"))
    .then(z.array(BookmarkSchema).parseAsync)
    .catch(() => []);
}

async function serialize(data: Bookmark[]): Promise<string> {
  return Cookie.serialize(data);
}

export default {
  deserialize,
  serialize,
};
