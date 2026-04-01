import Link from "next/link";

import { Briefing } from "@/lib/types";


export function BriefingList({ briefings }: { briefings: Briefing[] }) {
  return (
    <div className="space-y-4">
      {briefings.map((briefing) => (
        <div key={briefing.id} className="card flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-slate-500">{new Date(briefing.generated_at).toLocaleString()}</p>
            <h3 className="font-display text-2xl">{briefing.title}</h3>
            <p className="text-sm text-slate-600">{briefing.generation_mode} · {briefing.status}</p>
          </div>
          <Link href={`/briefings/${briefing.id}`} className="button-secondary">
            Open briefing
          </Link>
        </div>
      ))}
    </div>
  );
}
