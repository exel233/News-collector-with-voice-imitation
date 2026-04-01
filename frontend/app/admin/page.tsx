"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { Nav } from "@/components/nav";
import { fetchAdminStatus, fetchCurrentUser } from "@/lib/api";
import { AdminStatus, CurrentUser } from "@/lib/types";


export default function AdminPage() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [status, setStatus] = useState<AdminStatus | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!window.localStorage.getItem("token")) {
      router.push("/auth/signin");
      return;
    }
    fetchCurrentUser()
      .then((currentUser) => {
        setUser(currentUser);
        if (currentUser.role !== "admin") {
          setError("This page is only available to admin users.");
          return;
        }
        return fetchAdminStatus().then(setStatus);
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load admin page"));
  }, [router]);

  return (
    <div>
      <Nav />
      <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <section className="card space-y-4">
          <p className="text-sm uppercase tracking-[0.25em] text-ocean">Admin access</p>
          <h1 className="font-display text-4xl">Environment overview</h1>
          {user ? (
            <div className="text-sm text-slate-700">
              <p><strong>Signed in as:</strong> {user.full_name}</p>
              <p><strong>Email:</strong> {user.email}</p>
              <p><strong>Role:</strong> {user.role}</p>
            </div>
          ) : null}
          {error ? <p className="text-sm text-rose">{error}</p> : null}
        </section>
        <section className="card">
          <h2 className="mb-4 font-display text-3xl">System status</h2>
          {status ? (
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="rounded-[24px] bg-white p-5">
                <p className="text-sm text-slate-500">Users</p>
                <p className="font-display text-4xl">{status.users}</p>
              </div>
              <div className="rounded-[24px] bg-white p-5">
                <p className="text-sm text-slate-500">Articles</p>
                <p className="font-display text-4xl">{status.articles}</p>
              </div>
              <div className="rounded-[24px] bg-white p-5">
                <p className="text-sm text-slate-500">Events</p>
                <p className="font-display text-4xl">{status.events}</p>
              </div>
              <div className="rounded-[24px] bg-white p-5">
                <p className="text-sm text-slate-500">Briefings</p>
                <p className="font-display text-4xl">{status.briefings}</p>
              </div>
            </div>
          ) : (
            <p className="text-sm text-slate-600">Loading admin status...</p>
          )}
        </section>
      </div>
    </div>
  );
}
