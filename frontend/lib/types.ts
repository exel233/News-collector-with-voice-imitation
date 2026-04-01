export type Topic = {
  id: number;
  slug: string;
  label: string;
  description: string;
};

export type TopicSelection = {
  slug: string;
  priority_weight: number;
};

export type Preferences = {
  timezone: string;
  briefing_length_minutes: number;
  daily_schedule_time: string;
  include_weekends: boolean;
  selected_topics: TopicSelection[];
};

export type BriefingItem = {
  id: number;
  event_title: string;
  section: string;
  rank: number;
  summary: string;
  why_it_matters: string;
  topic_slug: string;
  score: number;
  article_urls: string[];
};

export type Briefing = {
  id: string;
  title: string;
  script: string;
  audio_path: string | null;
  status: string;
  generation_mode: string;
  generated_at: string;
  metadata_json: Record<string, unknown>;
  items: BriefingItem[];
};

export type VoiceProfile = {
  id: number;
  provider_status: string;
  sample_path: string | null;
  provider_voice_id: string | null;
  notes: string;
  created_at: string;
};

export type AudioPayload = {
  briefing_id: string;
  audio_url: string | null;
  fallback_mode: string;
  script: string;
};
