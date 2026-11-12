import { readFileSync } from "node:fs";
import path from "node:path";

export const START = 100_000;
export const TARGET = 1_000_000;
export const WINDOW_DAYS = 365;

export type Position = {
  ticker: string;
  side: "long" | "short" | string;
  shares: number;
  entry: number;
  price: number;
  pct_nav: number;
  notional: number;
  pnl: number;
  stop?: number;
  target?: number;
  thesis?: string;
};

export type ModelState = {
  id: string;
  lab: string;
  mark: string;
  name: string;
  status: "active" | "waiting" | string;
  note?: string;
  equity?: number;
  return?: number;
  cash?: number;
  positions?: Position[];
};

export type SeriesPoint = {
  ts_et: string;
  day: number;
  equity: number;
  return: number;
  kind?: string;
};

export type MissionState = {
  day: number;
  window_days: number;
  status: string;
  started: string;
  started_iso: string;
  as_of_et: string;
  data_as_of: string;
  nav_base: number;
  mission_equity: number;
  mission_return: number;
  mission_aggregate: string;
  active_models: string[];
  cycle?: string;
  price_source: string;
  models: ModelState[];
  series: SeriesPoint[];
  prices: Record<string, number>;
};

let cached: MissionState | null = null;

export function loadState(): MissionState {
  if (cached) return cached;
  const raw = readFileSync(path.join(process.cwd(), "public", "data", "state.json"), "utf8");
  cached = JSON.parse(raw) as MissionState;
  return cached;
}

export function usd(v: number): string {
  return "$" + Math.round(v).toLocaleString("en-US");
}

export function pct(v: number): string {
  const sign = v > 0 ? "+" : "";
  return sign + (v * 100).toFixed(2) + "%";
}

/* ---------- One shared mission (preview) ---------- */

/** Return of one $100K book, always derived from equity: (equity − $100,000) ÷ $100,000. */
export function bookReturn(equity: number): number {
  return (equity - START) / START;
}

/**
 * Combined mission figures, recomputed from the active books (never read from a stored % field).
 * Mission equity = mean of active books = $100K + Σ(book P&L) ÷ N.
 * This is identical to (Σ book equity ÷ (N × $100K)) × $100K, so "mean of books" and
 * "sum vs N × $100K" give the same return.
 */
export function missionFromBooks(models: ModelState[]) {
  const active = models.filter((m) => m.status === "active" && typeof m.equity === "number");
  const n = active.length;
  const total = active.reduce((s, m) => s + (m.equity as number), 0);
  const pnl = total - n * START;
  const equity = n ? total / n : START;
  return {
    n,
    total,
    capital: n * START,
    pnl,
    equity,
    ret: n ? pnl / (n * START) : 0,
    goalProgress: (equity - START) / (TARGET - START),
  };
}

export function usd2(v: number): string {
  return "$" + v.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

export function signedUsd2(v: number): string {
  const s = v > 0 ? "+" : v < 0 ? "−" : "";
  return s + usd2(Math.abs(v));
}

export function pct3(v: number): string {
  const s = v > 0 ? "+" : v < 0 ? "−" : "";
  return s + Math.abs(v * 100).toFixed(3) + "%";
}
