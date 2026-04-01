import Link from "next/link";

export default function HomePage() {
  return (
    <div className="grid gap-8 lg:grid-cols-[1.3fr_0.7fr]">
      <section className="card space-y-6">
        <p className="text-sm uppercase tracking-[0.3em] text-ocean">Daily intelligence</p>
        <h1 className="font-display text-5xl leading-tight">A personalized news briefing that still catches what really matters.</h1>
        <p className="max-w-2xl text-lg text-slate-700">
          Prioritize the topics you care about, keep a safety net for major global headlines, and turn each briefing into audio on demand.
        </p>
        <div className="flex gap-3">
          <Link href="/auth/signup" className="button-primary">Create account</Link>
          <Link href="/auth/signin" className="button-secondary">Sign in</Link>
        </div>
      </section>
      <section className="card">
        <h2 className="mb-4 font-display text-2xl">MVP highlights</h2>
        <ul className="space-y-3 text-sm text-slate-700">
          <li>Weighted ranking across topic relevance, global importance, recency, source diversity, and novelty.</li>
          <li>Daily scheduled briefing plus on-demand generation.</li>
          <li>Offline-friendly standard TTS path with a safe voice-cloning abstraction.</li>
          <li>Mock-first ingestion so local development works before real APIs are connected.</li>
        </ul>
      </section>
    </div>
  );
}
