import { Form, Link, useLoaderData } from "@remix-run/react";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "~/components/ui/tooltip";
import { Toggle } from "~/components/ui/toggle";
import { Store } from "~/models/store";
import { clientLoader } from "./route";
import { Bookmark, BookmarkCheck } from "lucide-react";
import { Button } from "~/components/ui/button";
import { createContext, useContext, useEffect, useState } from "react";
import { cn } from "~/lib/utils";

type Bookmark = {
  storeid: string;
  brand: "7-11" | "FamilyMart";
};

type State = {
  bookmarks: Bookmark[];
  subscribe: (storeid: string, brand: "7-11" | "FamilyMart") => void;
  unsubscribe: (storeid: string, brand: "7-11" | "FamilyMart") => void;
};

const BOOKMARKS_LIMIT = 10;

const Context = createContext<State | null>(null);

const hasBookmarked = (
  bookmarks: Bookmark[],
  storeid: string,
  brand: "7-11" | "FamilyMart"
) =>
  bookmarks.some(
    (bookmark) => bookmark.storeid === storeid && bookmark.brand === brand
  );

type BookmarkProviderProps = {
  children: React.ReactNode;
};
export function BookmarkProvider(props: BookmarkProviderProps) {
  const data = useLoaderData<typeof clientLoader>();

  const [bookmarks, setBookmarks] = useState<Bookmark[]>(
    data?.query.bookmarks ?? []
  );

  useEffect(() => {
    if (!data?.query.bookmarks) return;

    setBookmarks((bookmarks) => {
      const diff = data.query.bookmarks.filter(
        (bookmark) =>
          !hasBookmarked(bookmarks, bookmark.storeid, bookmark.brand)
      );

      if (!diff.length) return data.query.bookmarks;
      return bookmarks;
    });
  }, [data?.query.bookmarks]);

  function subscribe(storeid: string, brand: "7-11" | "FamilyMart") {
    setBookmarks((bookmarks) => {
      if (bookmarks.length > BOOKMARKS_LIMIT) return bookmarks;

      // if storeid is already bookmarked, return bookmarks
      if (hasBookmarked(bookmarks, storeid, brand)) {
        return bookmarks;
      }

      return [...bookmarks, { storeid, brand }];
    });
  }

  function unsubscribe(storeid: string, brand: "7-11" | "FamilyMart") {
    setBookmarks((bookmarks) => {
      return bookmarks.filter(
        (bookmark) => bookmark.storeid !== storeid || bookmark.brand !== brand
      );
    });
  }

  return (
    <Context.Provider value={{ bookmarks, subscribe, unsubscribe }}>
      {props.children}
    </Context.Provider>
  );
}

export function BookmarkButton(props: Store) {
  const ctx = useContext(Context);
  if (!ctx) throw new Error("BookmarkProvider is missing");

  const hasBooked = hasBookmarked(ctx.bookmarks, props.id, props.brand);

  if (!hasBooked && ctx.bookmarks.length >= BOOKMARKS_LIMIT) {
    return (
      <Tooltip delayDuration={300}>
        <Button
          variant="outline"
          size="icon"
          disabled
          className="!pointer-events-auto"
          asChild
        >
          <TooltipTrigger>
            <Bookmark />
          </TooltipTrigger>
        </Button>
        <TooltipContent>
          <p>關注上限 10 家</p>
        </TooltipContent>
      </Tooltip>
    );
  }

  return (
    <Form method="post" preventScrollReset>
      <Toggle
        type="submit"
        className="group"
        pressed={hasBooked}
        onPressedChange={() =>
          hasBooked
            ? ctx.unsubscribe(props.id, props.brand)
            : ctx.subscribe(props.id, props.brand)
        }
        name={hasBooked ? "subscribe" : "unsubscribe"}
        value={props.id}
      >
        <span className="group-data-[state=on]:hidden">
          <Bookmark className="size-4" />
        </span>
        <span className="group-data-[state=off]:hidden">
          <BookmarkCheck className="size-4" />
        </span>
      </Toggle>

      <input type="hidden" name="brand" value={props.brand} />
    </Form>
  );
}

export function HasBookmarkedButton() {
  const ctx = useContext(Context);
  if (!ctx) throw new Error("BookmarkProvider is missing");

  return (
    <Button
      className={cn(
        "w-12 h-12 rounded-full gap-1 md:w-auto md:h-auto md:rounded-md md:gap-2",
        "!bg-amber-500 !text-primary-foreground"
        //
      )}
      asChild
    >
      <Link to="/">
        <Bookmark />
        <span className="hidden md:inline">已收藏</span>
        <span>{ctx.bookmarks.length}</span>
      </Link>
    </Button>
  );
}
