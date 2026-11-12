import { readFileSync, existsSync } from "node:fs";
import path from "node:path";
import { marked } from "marked";

export type RecordFile = { file: string; href: string; desc: string; tag: string; html: string };

const ENTRIES = [
  { file: "MANDATE.md", rel: "MANDATE.md", desc: "The mission, its terms, and what is still proposed", tag: "3.0" },
  { file: "RULES.md", rel: "RULES.md", desc: "Hard limits: universe, sizing, drawdown ladder, kill switches", tag: "3.0" },
  { file: "DECISIONS.md", rel: "DECISIONS.md", desc: "Append-only log of every proposal and ruling, by model", tag: "Day 1 · live" },
  { file: "2026-11-09-c1", rel: "cycles/2026-11-09-c1/DECISIONS.md", desc: "Cycle 1 decisions with content hashes, fills and rejects", tag: "Cycle · Nov 9" },
  { file: "brief.md", rel: "cycles/2026-11-09-c1/brief.md", desc: "Identical brief sent to every model for cycle 1", tag: "Cycle · Nov 9" },
  { file: "rejects.log", rel: "cycles/2026-11-09-c1/rejects.log", desc: "Risk-gate rejects for cycle 1", tag: "Cycle · Nov 9" },
  { file: "2026-11-09-c2", rel: "cycles/2026-11-09-c2/DECISIONS.md", desc: "Cycle 2 catch-up: Kimi and Qwen join at 14:56 ET prices", tag: "Cycle · Nov 9" },
  { file: "brief-c2.md", rel: "cycles/2026-11-09-c2/brief.md", desc: "Identical brief sent for cycle 2 catch-up", tag: "Cycle · Nov 9" },
  { file: "rejects-c2.log", rel: "cycles/2026-11-09-c2/rejects.log", desc: "Risk-gate rejects for cycle 2", tag: "Cycle · Nov 9" },
  { file: "2026-11-09-c3", rel: "cycles/2026-11-09-c3/DECISIONS.md", desc: "Cycle 3 catch-up: Grok, Claude, Mistral and GLM join at 15:15 ET prices", tag: "Cycle · Nov 9" },
  { file: "brief-c3.md", rel: "cycles/2026-11-09-c3/brief.md", desc: "Identical brief sent for cycle 3 catch-up", tag: "Cycle · Nov 9" },
  { file: "rejects-c3.log", rel: "cycles/2026-11-09-c3/rejects.log", desc: "Risk-gate rejects for cycle 3", tag: "Cycle · Nov 9" },
  { file: "2026-11-11-c1", rel: "cycles/2026-11-11-c1/DECISIONS.md", desc: "Cycle 2026-11-11-c1: first v2 rebalance; Grok and Mistral GLD stops hit", tag: "Cycle · Nov 11" },
  { file: "brief-2026-11-11-c1.md", rel: "cycles/2026-11-11-c1/brief.md", desc: "Shared brief for the Nov 11 10:30 ET cycle (per-model briefs also in the record)", tag: "Cycle · Nov 11" },
  { file: "rejects-2026-11-11-c1.log", rel: "cycles/2026-11-11-c1/rejects.log", desc: "Risk-gate rejects for the Nov 11 10:30 ET cycle", tag: "Cycle · Nov 11" },
  { file: "2026-11-11-c2", rel: "cycles/2026-11-11-c2/DECISIONS.md", desc: "Cycle 2026-11-11-c2: midday v2 rebalance; no stop hits or rejects", tag: "Cycle · Nov 11" },
  { file: "brief-2026-11-11-c2.md", rel: "cycles/2026-11-11-c2/brief.md", desc: "Shared brief for the Nov 11 12:30 ET cycle (per-model briefs also in the record)", tag: "Cycle · Nov 11" },
  { file: "rejects-2026-11-11-c2.log", rel: "cycles/2026-11-11-c2/rejects.log", desc: "Risk-gate rejects for the Nov 11 12:30 ET cycle", tag: "Cycle · Nov 11" },
  { file: "2026-11-11-c3", rel: "cycles/2026-11-11-c3/DECISIONS.md", desc: "Cycle 2026-11-11-c3: afternoon v2 rebalance; no stop hits or rejects", tag: "Cycle · Nov 11" },
  { file: "brief-2026-11-11-c3.md", rel: "cycles/2026-11-11-c3/brief.md", desc: "Shared brief for the Nov 11 2:30 ET cycle (per-model briefs also in the record)", tag: "Cycle · Nov 11" },
  { file: "rejects-2026-11-11-c3.log", rel: "cycles/2026-11-11-c3/rejects.log", desc: "Risk-gate rejects for the Nov 11 2:30 ET cycle", tag: "Cycle · Nov 11" },
  { file: "SOUL.md", rel: "canonical/SOUL.md", desc: "Constitution: identity, edge, risk, prime directive", tag: "Carried over" },
  { file: "AGENT.md", rel: "canonical/AGENT.md", desc: "Operating manual: the six specialists and the cycle", tag: "Carried over" },
  { file: "BENCHMARK.md", rel: "canonical/BENCHMARK.md", desc: "Evaluation standard: gates, scorecard, MinTRL", tag: "Carried over" },
  { file: "HERMES.md", rel: "canonical/HERMES.md", desc: "Orchestrator: gates, halt authority, escalation", tag: "Carried over" },
  { file: "MEMORY.md", rel: "canonical/MEMORY.md", desc: "State, journal, calibration and learning layers", tag: "Carried over" },
];

export function loadRecord(): RecordFile[] {
  return ENTRIES.flatMap((e) => {
    const full = path.join(process.cwd(), "public", "record", e.rel);
    if (!existsSync(full)) return [];
    const md = readFileSync(full, "utf8");
    return [{ file: e.file, href: `/record/${e.rel}`, desc: e.desc, tag: e.tag, html: marked.parse(md, { async: false }) as string }];
  });
}
