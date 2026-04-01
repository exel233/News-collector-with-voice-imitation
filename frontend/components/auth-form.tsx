"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { login, register, setToken } from "@/lib/api";


export function AuthForm({ mode }: { mode: "signin" | "signup" }) {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [timezone, setTimezone] = useState("Europe/Stockholm");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const result =
        mode === "signup"
          ? await register({ email, password, full_name: fullName, timezone })
          : await login({ email, password });
      setToken(result.access_token);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Authentication failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={onSubmit} className="card mx-auto max-w-xl space-y-4">
      <h1 className="font-display text-3xl">{mode === "signup" ? "Create your briefing account" : "Welcome back"}</h1>
      {mode === "signup" && (
        <label className="block">
          <span className="mb-2 block text-sm font-semibold">Full name</span>
          <input className="input" value={fullName} onChange={(e) => setFullName(e.target.value)} required />
        </label>
      )}
      <label className="block">
        <span className="mb-2 block text-sm font-semibold">Email</span>
        <input className="input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      </label>
      <label className="block">
        <span className="mb-2 block text-sm font-semibold">Password</span>
        <input className="input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
      </label>
      {mode === "signup" && (
        <label className="block">
          <span className="mb-2 block text-sm font-semibold">Timezone</span>
          <input className="input" value={timezone} onChange={(e) => setTimezone(e.target.value)} required />
        </label>
      )}
      {error ? <p className="text-sm text-rose">{error}</p> : null}
      <button className="button-primary" disabled={loading}>
        {loading ? "Working..." : mode === "signup" ? "Create account" : "Sign in"}
      </button>
    </form>
  );
}
