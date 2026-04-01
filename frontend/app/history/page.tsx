"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { BriefingList } from "@/components/briefing-list";
import { Nav } from "@/components/nav";
import { fetchBriefings } from "@/lib/api";
import { Briefing } from "@/lib/types";


export default function HistoryPage() {
  const router = useRouter();
  const [briefings, setBriefings] = useState<Briefing[]>([]);

  useEffect(() => {
    if (!window.localStorage.getItem("token")) {
      router.push("/auth/signin");
      return;
    }
    fetchBriefings().then((result) => setBriefings(result.items));
  }, [router]);

  return (
    <div>
      <Nav />
      <section className="space-y-6">
        <div className="card">
          <h1 className="font-display text-4xl">Briefing history</h1>
          <p className="mt-2 text-sm text-slate-600">Revisit daily runs, replay audio, or inspect how the ranking output changed over time.</p>
        </div>
        <BriefingList briefings={briefings} />
      </section>
    </div>
  );
}
