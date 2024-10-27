import { z } from "zod";
import { zfd } from "zod-form-data";
import { P, match } from "ts-pattern";
import { replace } from "@remix-run/react";
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
        if (bookmarks.some((bookmark) => bookmark.storeid === subscribe)) {
          return bookmarks;
        }
        return [...bookmarks, { storeid: subscribe, brand }];
      }
    )
    .with({ unsubscribe: P.string }, ({ unsubscribe }) => {
      return bookmarks.filter((bookmark) => bookmark.storeid !== unsubscribe);
    })
    .otherwise(() => bookmarks);

  return replace(args.request.url, {
    headers: {
      "Set-Cookie": await BookmarkCookie.serialize(_bookmarks),
    },
  });
}
