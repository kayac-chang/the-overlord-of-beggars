import { z } from "zod";
import { zfd } from "zod-form-data";
import { P, match } from "ts-pattern";
import { json } from "@remix-run/react";
import BookmarkCookie from "./cookie";
import { ActionFunctionArgs } from "@remix-run/node";

const ActionSchema = zfd.formData(
  z.object({
    subscribe: z.string().nullish(),
    unsubscribe: z.string().nullish(),
    brand: z.string().nullish(),
  })
);

export async function action(args: ActionFunctionArgs) {
  const formdata = await args.request
    .clone()
    .formData()
    .then(ActionSchema.parseAsync);

  const bookmarks = await BookmarkCookie.deserialize(args.request);

  const _bookmarks = match(formdata)
    .with(
      { subscribe: P.string, brand: P.union("7-11", "FamilyMart") },
      ({ subscribe, brand }) => {
        const hasBookmarked = bookmarks.some(
          (bookmark) =>
            bookmark.brand === brand && bookmark.storeid === subscribe
        );

        if (hasBookmarked) {
          return bookmarks;
        }

        return [...bookmarks, { storeid: subscribe, brand }];
      }
    )
    .with(
      { unsubscribe: P.string, brand: P.union("7-11", "FamilyMart") },
      ({ unsubscribe, brand }) =>
        bookmarks.filter(
          (bookmark) =>
            bookmark.storeid !== unsubscribe || bookmark.brand !== brand
        )
    )
    .otherwise(() => bookmarks);

  return json(null, {
    headers: {
      "Set-Cookie": await BookmarkCookie.serialize(_bookmarks),
    },
  });
}
