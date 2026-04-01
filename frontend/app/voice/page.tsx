"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { Nav } from "@/components/nav";
import { fetchVoiceProfile, uploadVoiceSample } from "@/lib/api";
import { VoiceProfile } from "@/lib/types";


export default function VoicePage() {
  const router = useRouter();
  const [profile, setProfile] = useState<VoiceProfile | null>(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (!window.localStorage.getItem("token")) {
      router.push("/auth/signin");
      return;
    }
    fetchVoiceProfile().then(setProfile);
  }, [router]);

  async function onUpload(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;
    const updated = await uploadVoiceSample(file);
    setProfile(updated);
    setMessage("Voice sample uploaded.");
  }

  return (
    <div>
      <Nav />
      <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <section className="card space-y-4">
          <h1 className="font-display text-3xl">Voice settings</h1>
          <p className="text-sm text-slate-700">
            Standard TTS is always available for the MVP. Voice sample uploads are stored only for the authenticated user and routed through a guarded provider abstraction.
          </p>
          <input type="file" accept="audio/*" onChange={onUpload} />
          {message ? <p className="text-sm text-ocean">{message}</p> : null}
        </section>
        <section className="card">
          <h2 className="mb-4 font-display text-3xl">Current status</h2>
          {profile ? (
            <div className="space-y-3 text-sm text-slate-700">
              <p><strong>Provider status:</strong> {profile.provider_status}</p>
              <p><strong>Voice id:</strong> {profile.provider_voice_id ?? "Not assigned yet"}</p>
              <p><strong>Sample path:</strong> {profile.sample_path ?? "No sample uploaded"}</p>
              <p>{profile.notes}</p>
            </div>
          ) : (
            <p className="text-sm text-slate-600">Loading voice profile...</p>
          )}
        </section>
      </div>
    </div>
  );
}
