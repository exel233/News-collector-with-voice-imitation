import { AudioPayload, Briefing, Preferences, Topic, VoiceProfile } from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";
const BACKEND_ORIGIN = process.env.NEXT_PUBLIC_BACKEND_ORIGIN ?? "http://localhost:8000";

export function getToken() {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem("token");
}

export function setToken(token: string) {
  if (typeof window === "undefined") return;
  window.localStorage.setItem("token", token);
}

async function request<T>(path: string, options: RequestInit = {}, auth = false): Promise<T> {
  const headers = new Headers(options.headers);
  headers.set("Content-Type", headers.get("Content-Type") ?? "application/json");
  if (auth) {
    const token = getToken();
    if (token) headers.set("Authorization", `Bearer ${token}`);
  }
  const response = await fetch(`${API_URL}${path}`, { ...options, headers, cache: "no-store" });
  if (!response.ok) {
    const payload = await response.text();
    throw new Error(payload || "Request failed");
  }
  return response.json();
}

export async function register(payload: { email: string; password: string; full_name: string; timezone: string }) {
  return request<{ access_token: string }>("/auth/register", { method: "POST", body: JSON.stringify(payload) });
}

export async function login(payload: { email: string; password: string }) {
  return request<{ access_token: string }>("/auth/login", { method: "POST", body: JSON.stringify(payload) });
}

export async function fetchPreferences() {
  return request<Preferences>("/preferences", {}, true);
}

export async function updatePreferences(payload: { timezone: string; briefing_length_minutes: number }) {
  return request<Preferences>("/preferences", { method: "PUT", body: JSON.stringify(payload) }, true);
}

export async function fetchTopics() {
  return request<Topic[]>("/preferences/topics");
}

export async function updateTopics(payload: { topics: { slug: string; priority_weight: number }[] }) {
  return request<Preferences>("/preferences/topics", { method: "PUT", body: JSON.stringify(payload) }, true);
}

export async function updateSchedule(payload: { daily_schedule_time: string; briefing_length_minutes: number; include_weekends: boolean }) {
  return request("/preferences/schedule", { method: "PUT", body: JSON.stringify(payload) }, true);
}

export async function generateBriefing() {
  return request<Briefing>("/briefings/generate", { method: "POST", body: JSON.stringify({ mode: "on_demand" }) }, true);
}

export async function fetchBriefings() {
  return request<{ items: Briefing[] }>("/briefings", {}, true);
}

export async function fetchBriefing(id: string) {
  return request<Briefing>(`/briefings/${id}`, {}, true);
}

export async function fetchBriefingAudio(id: string) {
  return request<AudioPayload>(`/briefings/${id}/audio`, {}, true);
}

export async function fetchVoiceProfile() {
  return request<VoiceProfile>("/voice", {}, true);
}

export async function uploadVoiceSample(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  const token = getToken();
  const response = await fetch(`${API_URL}/voice/sample`, {
    method: "POST",
    headers: token ? { Authorization: `Bearer ${token}` } : undefined,
    body: formData,
  });
  if (!response.ok) throw new Error(await response.text());
  return (await response.json()) as VoiceProfile;
}

export function resolveAudioUrl(audioPath: string | null) {
  return audioPath ? `${BACKEND_ORIGIN}${audioPath}` : null;
}
