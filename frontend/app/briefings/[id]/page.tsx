"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";

import { AudioPlayer } from "@/components/audio-player";
import { Nav } from "@/components/nav";
import { fetchBriefing, fetchBriefingAudio } from "@/lib/api";
import { AudioPayload, Briefing } from "@/lib/types";


export default function BriefingDetailPage() {
  const router = useRouter();
  const params = useParams<{ id: string }>();
  const [briefing, setBriefing] = useState<Briefing | null>(null);
  const [audio, setAudio] = useState<AudioPayload | null>(null);

  useEffect(() => {
    if (!window.localStorage.getItem("token")) {
      router.push("/auth/signin");
      return;
    }
    if (!params.id) return;
    Promise.all([fetchBriefing(params.id), fetchBriefingAudio(params.id)]).then(([briefingData, audioData]) => {
      setBriefing(briefingData);
      setAudio(audioData);
    });
  }, [params.id, router]);

  return (
    <div>
      <Nav />
      {!briefing || !audio ? (
        <div className="card">Loading briefing...</div>
      ) : (
        <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
          <section className="card space-y-5">
            <Link href="/history" className="text-sm text-ocean">Back to history</Link>
            <h1 className="font-display text-4xl">{briefing.title}</h1>
            <p className="text-sm text-slate-600">{new Date(briefing.generated_at).toLocaleString()} · {briefing.generation_mode}</p>
            <div className="space-y-4">
              <div>
                <h2 className="mb-2 font-display text-2xl">Your Focus Topics</h2>
                <ul className="space-y-3 text-sm text-slate-700">
                  {briefing.items.filter((item) => item.section === "focus_topics").map((item) => (
                    <li key={item.id}>
                      <strong>{item.event_title}</strong> {item.summary} {item.why_it_matters}
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <h2 className="mb-2 font-display text-2xl">Major Headlines You Should Still Know</h2>
                <ul className="space-y-3 text-sm text-slate-700">
                  {briefing.items.filter((item) => item.section === "major_headlines").map((item) => (
                    <li key={item.id}>
                      <strong>{item.event_title}</strong> {item.summary} {item.why_it_matters}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </section>
          <div className="space-y-6">
            <AudioPlayer audioUrl={audio.audio_url} script={audio.script} />
            <section className="card">
              <h2 className="mb-3 font-display text-2xl">Script</h2>
              <pre className="whitespace-pre-wrap text-sm text-slate-700">{briefing.script}</pre>
            </section>
          </div>
        </div>
      )}
    </div>
  );
}
