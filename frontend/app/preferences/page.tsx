"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { Nav } from "@/components/nav";
import { fetchPreferences, fetchTopics, updatePreferences, updateSchedule, updateTopics } from "@/lib/api";
import { Preferences, Topic } from "@/lib/types";


export default function PreferencesPage() {
  const router = useRouter();
  const [preferences, setPreferences] = useState<Preferences | null>(null);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (!window.localStorage.getItem("token")) {
      router.push("/auth/signin");
      return;
    }
    Promise.all([fetchPreferences(), fetchTopics()]).then(([prefs, allTopics]) => {
      setPreferences(prefs);
      setTopics(allTopics);
    });
  }, [router]);

  async function toggleTopic(slug: string) {
    if (!preferences) return;
    const existing = preferences.selected_topics.find((item) => item.slug === slug);
    const next = existing
      ? preferences.selected_topics.filter((item) => item.slug !== slug)
      : [...preferences.selected_topics, { slug, priority_weight: 1 }];
    const updated = await updateTopics({ topics: next });
    setPreferences(updated);
    setMessage("Topics updated.");
  }

  async function saveProfile(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!preferences) return;
    const form = new FormData(event.currentTarget);
    const timezone = String(form.get("timezone"));
    const briefingLength = Number(form.get("briefing_length_minutes"));
    const scheduleTime = String(form.get("daily_schedule_time"));
    const includeWeekends = form.get("include_weekends") === "on";
    const updatedPrefs = await updatePreferences({ timezone, briefing_length_minutes: briefingLength });
    await updateSchedule({
      daily_schedule_time: scheduleTime,
      briefing_length_minutes: briefingLength,
      include_weekends: includeWeekends
    });
    setPreferences({
      ...updatedPrefs,
      daily_schedule_time: scheduleTime,
      include_weekends: includeWeekends
    });
    setMessage("Preferences saved.");
  }

  return (
    <div>
      <Nav />
      <div className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
        <form className="card space-y-4" onSubmit={saveProfile}>
          <h1 className="font-display text-3xl">Preferences</h1>
          <label className="block">
            <span className="mb-2 block text-sm font-semibold">Timezone</span>
            <input name="timezone" className="input" defaultValue={preferences?.timezone} />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm font-semibold">Daily schedule time</span>
            <input name="daily_schedule_time" type="time" className="input" defaultValue={preferences?.daily_schedule_time.slice(0, 5)} />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm font-semibold">Briefing length in minutes</span>
            <input name="briefing_length_minutes" type="number" min={3} max={15} className="input" defaultValue={preferences?.briefing_length_minutes ?? 6} />
          </label>
          <label className="flex items-center gap-3 text-sm">
            <input type="checkbox" name="include_weekends" defaultChecked={preferences?.include_weekends ?? true} />
            Include weekend briefings
          </label>
          <button className="button-primary">Save settings</button>
          {message ? <p className="text-sm text-ocean">{message}</p> : null}
        </form>
        <section className="card">
          <h2 className="mb-4 font-display text-3xl">Topic selection</h2>
          <p className="mb-6 text-sm text-slate-600">
            Pick what you care about most. The system still monitors other domains for major events, but selected topics receive higher ranking weight and more briefing time.
          </p>
          <div className="grid gap-4 sm:grid-cols-2">
            {topics.map((topic) => {
              const selected = Boolean(preferences?.selected_topics.find((item) => item.slug === topic.slug));
              return (
                <button
                  key={topic.slug}
                  type="button"
                  className={`rounded-[24px] border p-5 text-left transition ${selected ? "border-ink bg-ink text-paper" : "border-slate-200 bg-white"}`}
                  onClick={() => toggleTopic(topic.slug)}
                >
                  <h3 className="mb-2 font-display text-2xl">{topic.label}</h3>
                  <p className={`text-sm ${selected ? "text-paper/80" : "text-slate-600"}`}>{topic.description}</p>
                </button>
              );
            })}
          </div>
        </section>
      </div>
    </div>
  );
}
