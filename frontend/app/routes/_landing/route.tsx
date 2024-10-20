import { Outlet } from "@remix-run/react";
import Header from "./header";
import Progressbar from "./progressbar";

export default function Layout() {
  return (
    <>
      <Progressbar />
      <Header />
      <Outlet />
    </>
  );
}
