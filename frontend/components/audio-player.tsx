"use client";

import { useState } from "react";


export function AudioPlayer({ audioUrl, script }: { audioUrl: string | null; script: string }) {
  const [speaking, setSpeaking] = useState(false);

  function speakWithBrowser() {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(script);
    utterance.onstart = () => setSpeaking(true);
    utterance.onend = () => setSpeaking(false);
    utterance.onerror = () => setSpeaking(false);
    window.speechSynthesis.speak(utterance);
  }

  return (
    <div className="card space-y-4">
      <h2 className="font-display text-2xl">Playback</h2>
      {audioUrl ? (
        <audio controls className="w-full">
          <source src={audioUrl} type="audio/wav" />
        </audio>
      ) : (
        <div className="space-y-3">
          <p className="text-sm text-slate-600">No server-generated audio found, so the browser fallback will read the script aloud.</p>
          <button onClick={speakWithBrowser} className="button-secondary">
            {speaking ? "Speaking..." : "Play with browser voice"}
          </button>
        </div>
      )}
    </div>
  );
}
