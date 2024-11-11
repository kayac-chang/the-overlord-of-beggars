export default function Header() {
  return (
    <header className="sticky top-0 z-20 w-full border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="mx-auto container flex h-14 max-w-screen-2xl items-center px-8">
        <a href="/" className="mr-4 flex items-center space-x-2 lg:mr-6">
          The Overload Of Beggars 乞丐超人
        </a>
        <nav className="flex items-center gap-4 text-sm lg:gap-6"></nav>
      </div>
    </header>
  );
}
