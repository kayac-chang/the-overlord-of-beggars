import { Outlet } from "@remix-run/react";
import Header from "./header";

export default function Layout() {
  return (
    <>
      <Header />
      <Outlet />
    </>
  );
}
