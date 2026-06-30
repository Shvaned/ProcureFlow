"use client";

import { ThemeSwitch } from "@/components/ui/theme-switch";
import { Search, Bell, ChevronDown } from "lucide-react";

export function Navbar() {
  return (
    <header className="sticky top-0 z-30 flex h-14 items-center gap-4 border-b bg-card px-6">
      <div className="flex flex-1 items-center gap-4">
        <nav className="flex items-center gap-2 text-sm text-muted-foreground">
          <span className="text-foreground">Dashboard</span>
        </nav>
      </div>
      <div className="flex items-center gap-3">
        <button
          className="flex items-center gap-2 rounded-md border px-3 py-1.5 text-sm text-muted-foreground hover:text-foreground"
          onClick={() => {}}>
          <Search className="h-4 w-4" />
          <span className="hidden md:inline">Search...</span>
          <kbd className="ml-8 hidden rounded border px-1.5 py-0.5 text-xs md:inline">
            ⌘K
          </kbd>
        </button>
        <button className="relative rounded-md p-2 text-muted-foreground hover:bg-muted hover:text-foreground">
          <Bell className="h-4 w-4" />
          <span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-primary" />
        </button>
        <ThemeSwitch />
        <button className="flex items-center gap-2 rounded-md p-1.5 hover:bg-muted">
          <div className="flex h-7 w-7 items-center justify-center rounded-full bg-primary text-xs font-medium text-primary-foreground">
            A
          </div>
          <ChevronDown className="h-3 w-3 text-muted-foreground" />
        </button>
      </div>
    </header>
  );
}
