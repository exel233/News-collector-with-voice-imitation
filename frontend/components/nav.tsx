"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

import { fetchCurrentUser } from "@/lib/api";

const links = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/preferences", label: "Preferences" },
  { href: "/voice", label: "Voice" },
  { href: "/history", label: "History" }
];

export function Nav() {
  const pathname = usePathname();
  const router = useRouter();
  const [role, setRole] = useState<string | null>(null);

  useEffect(() => {
    if (!window.localStorage.getItem("token")) return;
    fetchCurrentUser()
      .then((user) => setRole(user.role))
      .catch(() => setRole(null));
  }, []);

  const allLinks = role === "admin" ? [...links, { href: "/admin", label: "Admin" }] : links;

  return (
    <nav className="mb-10 flex flex-wrap items-center gap-3">
      {allLinks.map((link) => (
        <Link
          key={link.href}
          href={link.href}
          className={`rounded-full px-4 py-2 text-sm font-semibold transition ${
            pathname.startsWith(link.href) ? "bg-ink text-paper" : "bg-white/70 text-ink"
          }`}
        >
          {link.label}
        </Link>
      ))}
      <button
        className="rounded-full border border-ink/20 px-4 py-2 text-sm"
        onClick={() => {
          window.localStorage.removeItem("token");
          router.push("/auth/signin");
        }}
      >
        Sign out
      </button>
    </nav>
  );
}
