"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { Nav } from "@/components/nav";
import { fetchBriefings, fetchPreferences, generateBriefing, resolveAudioUrl } from "@/lib/api";
import { Briefing, Preferences } from "@/lib/types";


export default function DashboardPage() {
  const router = useRouter();
  const [preferences, setPreferences] = useState<Preferences | null>(null);
  const [briefings, setBriefings] = useState<Briefing[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = window.localStorage.getItem("token");
    if (!token) {
      router.push("/auth/signin");
      return;
    }
    Promise.all([fetchPreferences(), fetchBriefings()])
      .then(([pref, briefingResult]) => {
        setPreferences(pref);
        setBriefings(briefingResult.items);
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load dashboard"))
      .finally(() => setLoading(false));
  }, [router]);

  async function onGenerate() {
    setGenerating(true);
    try {
      const briefing = await generateBriefing();
      setBriefings((current) => [briefing, ...current]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate briefing");
    } finally {
      setGenerating(false);
    }
  }

  const latest = briefings[0];
  const focusItems = latest?.items.filter((item) => item.section === "focus_topics") ?? [];
  const generalItems = latest?.items.filter((item) => item.section === "major_headlines") ?? [];
  const latestAudioUrl = latest?.audio_path ? resolveAudioUrl(latest.audio_path) : null;

  return (
    <div>
      <Nav />
      <div className="grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
        <section className="card space-y-5">
          <p className="text-sm uppercase tracking-[0.25em] text-ocean">Today&apos;s briefing</p>
          <h1 className="font-display text-4xl">Your news, with room for what the world makes impossible to ignore.</h1>
          <p className="text-slate-700">
            The app allocates about 70% of your briefing to selected topics when enough relevant stories exist, while still reserving room for major events elsewhere.
          </p>
          <div className="flex flex-wrap gap-3">
            <button className="button-primary" onClick={onGenerate} disabled={generating}>
              {generating ? "Generating..." : "Generate briefing now"}
            </button>
            {latest ? (
              <button className="button-secondary" onClick={() => router.push(`/briefings/${latest.id}`)}>
                Open latest briefing
              </button>
            ) : null}
          </div>
          {error ? <p className="text-sm text-rose">{error}</p> : null}
          {latestAudioUrl ? (
            <audio controls className="w-full">
              <source src={latestAudioUrl} type="audio/wav" />
            </audio>
          ) : null}
        </section>
        <aside className="space-y-6">
          <div className="card">
            <h2 className="mb-3 font-display text-2xl">Briefing setup</h2>
            {loading || !preferences ? (
              <p className="text-sm text-slate-600">Loading preferences...</p>
            ) : (
              <div className="space-y-3 text-sm text-slate-700">
                <p><strong>Topics:</strong> {preferences.selected_topics.map((topic) => topic.slug).join(", ") || "None selected yet"}</p>
                <p><strong>Schedule:</strong> {preferences.daily_schedule_time}</p>
                <p><strong>Length:</strong> {preferences.briefing_length_minutes} minutes</p>
                <p><strong>Timezone:</strong> {preferences.timezone}</p>
              </div>
            )}
          </div>
          <div className="card">
            <h2 className="mb-3 font-display text-2xl">Your prioritized topics</h2>
            <ul className="space-y-3 text-sm text-slate-700">
              {focusItems.length ? focusItems.map((item) => <li key={item.id}>{item.event_title}</li>) : <li>Generate a briefing to populate your focus feed.</li>}
            </ul>
          </div>
          <div className="card">
            <h2 className="mb-3 font-display text-2xl">Important general headlines</h2>
            <ul className="space-y-3 text-sm text-slate-700">
              {generalItems.length ? generalItems.map((item) => <li key={item.id}>{item.event_title}</li>) : <li>Major non-selected stories will appear here.</li>}
            </ul>
          </div>
        </aside>
      </div>
    </div>
  );
}
