import {
  Links,
  Meta,
  MetaFunction,
  Outlet,
  Scripts,
  ScrollRestoration,
} from "@remix-run/react";
import type { LinksFunction } from "@remix-run/node";

import "./tailwind.css";

export const links: LinksFunction = () => [
  { rel: "preconnect", href: "https://fonts.googleapis.com" },
  {
    rel: "preconnect",
    href: "https://fonts.gstatic.com",
    crossOrigin: "anonymous",
  },
  {
    rel: "stylesheet",
    href: "https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap",
  },
];

export const meta: MetaFunction = () => {
  return [
    { title: "The Overload Of Beggars 乞丐超人" },
    {
      property: "description",
      content:
        "提供在台灣生活的小資族整合過的各種省錢資訊， 像是：7-11 i珍食 + 全家友善時光。",
    },
    {
      property: "og:title",
      content: "The Overload Of Beggars 乞丐超人",
    },
    {
      property: "og:description",
      content:
        "提供在台灣生活的小資族整合過的各種省錢資訊， 像是：7-11 i珍食 + 全家友善時光。",
    },
    {
      property: "og:url",
      content: "https://the-overload-of-beggars.fly.dev/",
    },
    {
      property: "og:type",
      content: "website",
    },
    {
      property: "twitter:title",
      content: "The Overload Of Beggars 乞丐超人",
    },
    {
      property: "twitter:description",
      content:
        "提供在台灣生活的小資族整合過的各種省錢資訊， 像是：7-11 i珍食 + 全家友善時光。",
    },
    {
      property: "twitter:url",
      content: "https://the-overload-of-beggars.fly.dev/",
    },
    //
  ];
};

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="zh-TW"
      dir="ltr"
      className="dark bg-background text-foreground font-mono"
    >
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta />
        <Links />
      </head>
      <body className="min-h-screen">
        {children}
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  );
}

export default function App() {
  return <Outlet />;
}
