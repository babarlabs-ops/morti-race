import { readFileSync } from "node:fs";
import path from "node:path";

export const MOODS = ["risk-on", "neutral", "risk-off"] as const;
export type MoodValue = (typeof MOODS)[number];

export type MoodSeat = {
  id: string;
  name: string;
  lab: string;
  mark: string;
  mood: MoodValue | null;
  mood_label: string;
  hypothesis: string | null;
  round_time_et: string | null;
  answered: boolean;
};

export type MoodState = {
  cycle: string;
  round_time_et: string | null;
  updated_et: string;
  stance: "risk-on" | "neutral" | "risk-off" | "mixed" | null;
  stance_label: string | null;
  counts: { "risk-on": number; neutral: number; "risk-off": number; "not-given": number };
  team_hypothesis: string | null;
  seats: MoodSeat[];
};

export function loadMood(): MoodState | null {
  const file = path.join(process.cwd(), "public", "data", "mood.json");
  try {
    const raw = readFileSync(file, "utf8");
    const data = JSON.parse(raw) as MoodState;
    if (!data || !Array.isArray(data.seats)) return null;
    return data;
  } catch {
    return null;
  }
}

export function hasAnyMood(mood: MoodState | null): boolean {
  if (!mood) return false;
  const c = mood.counts;
  return c["risk-on"] + c.neutral + c["risk-off"] > 0 || Boolean(mood.team_hypothesis);
}

export function formatRoundTime(et: string | null): string | null {
  if (!et) return null;
  // "2026-11-11 14:28:20 EST" → "Nov 11, 2026, 2:28 PM ET"
  const m = et.match(/^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})(?::\d{2})? (EST|EDT|ET)?/);
  if (!m) return et;
  const months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  const hour = Number(m[4]);
  const h12 = ((hour + 11) % 12) + 1;
  const ampm = hour < 12 ? "AM" : "PM";
  const zone = "ET";
  return `${months[Number(m[2]) - 1]} ${Number(m[3])}, ${m[1]}, ${h12}:${m[5]} ${ampm} ${zone}`;
}
