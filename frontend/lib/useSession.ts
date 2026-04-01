"use client";

import { useEffect, useState } from "react";

import { getToken } from "@/lib/api";

export function useSession() {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    setToken(getToken());
  }, []);

  return { token, authenticated: Boolean(token) };
}
