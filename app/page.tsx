import Link from "next/link";
import { CombinedChart } from "../components/CombinedChart";
import { SiteFooter } from "../components/SiteFooter";
import { SiteHeader } from "../components/SiteHeader";
import { TeamMood } from "../components/TeamMood";
import {
  bookReturn, loadState, missionFromBooks, pct, pct3, signedUsd2, START, TARGET, usd, usd2, WINDOW_DAYS,
} from "../lib/mission";
import { loadMood } from "../lib/mood";
import { loadRecord } from "../lib/record";

export const dynamic = "force-static";

const MANDATE: { k: string; v: string; src: string; proposed?: boolean }[] = [
  { k: "Capital", v: "$100,000 paper per seat on the team. Live money needs a human signature and legal review.", src: "SOUL.md · brief" },
  { k: "Goal", v: "Take the team's combined book from $100,000 to $1,000,000 (10×) within 365 days, measured against a 60/40 benchmark.", src: "2.0 README · SOUL.md" },
  { k: "Universe", v: "US large caps, US equity ETFs, liquid crypto, commodity ETFs. No OTC, no names under $500M, no intraday.", src: "SOUL.md" },
  { k: "Risk limits", v: "Single name or crypto ≤25% of NAV · ETF ≤25% · gross ≤200% · |net| ≤200% · ≤400 bps of NAV at risk to the stop per new trade or add · max 3 new trades per round · stops only tighten · full halt at −15% drawdown.", src: "Live · fill.py · SOUL.md (halt)" },
  { k: "How the team works", v: "Every model gets the identical free-web brief and manages one $100K seat of the shared book; up to 3 trades per cycle; risk gates before any paper fill; content hash committed first.", src: "Proposed · running", proposed: true },
  { k: "Cadence", v: "Up to 3 cycles per US trading day (10:30, 12:30, 14:30 ET). Zero-cost: free chat + Yahoo Finance chart prices.", src: "Proposed · cycle from AGENT.md", proposed: true },
];

export default function Home() {
  const state = loadState();
  const record = loadRecord();
  const mood = loadMood();
  const m = missionFromBooks(state.models);
  // Fixed, non-performance order: alphabetical by model name.
  const roster = [...state.models].sort((a, b) => a.name.localeCompare(b.name));
  const pending = roster.filter((r) => r.status !== "active");
  const fillPct = Math.max(0, Math.min(1, m.goalProgress)) * 100;
  const sign = m.pnl > 0 ? "up" : m.pnl < 0 ? "dn" : "flat";

  return (
    <>
      <SiteHeader current="home" />

      <main id="content">
        <section className="mission wrap" aria-label="Mission progress">
          <p className="eyebrow">One shared mission · Day {state.day} of {WINDOW_DAYS} · {state.status.toLowerCase()}</p>
          <h1>One AI team. $100K <span className="arrow">→</span> $1M.</h1>

          <div className="meter-row">
            <div className="big">
              <span className="big-k">Mission equity</span>
              <span className="big-v num">{usd2(m.equity)}</span>
              <span className={`big-d num ${sign}`}>{signedUsd2(m.equity - START)} · {pct3(m.ret)}</span>
            </div>
            <div className="goal">
              <span className="big-k">Goal</span>
              <span className="goal-v num">$1,000,000</span>
              <span className="goal-d num">{usd2(TARGET - m.equity)} to go</span>
            </div>
          </div>

          <div className="meter" role="meter" aria-valuemin={START} aria-valuemax={TARGET} aria-valuenow={Math.round(m.equity)}
            aria-label={`Mission equity ${usd2(m.equity)} on the way from $100,000 to $1,000,000`}>
            <div className="meter-track"><div className="meter-fill" style={{ width: `max(6px, ${fillPct}%)` }} /></div>
            <div className="meter-ticks num">
              <span style={{ left: "0%" }}>$100K</span>
              <span style={{ left: `${(150_000 / 900_000) * 100}%` }}>$250K</span>
              <span style={{ left: `${(400_000 / 900_000) * 100}%` }}>$500K</span>
              <span style={{ left: `${(650_000 / 900_000) * 100}%` }}>$750K</span>
              <span style={{ left: "100%" }}>$1M</span>
            </div>
          </div>
          <p className="meter-note num">{(Math.max(0, m.goalProgress) * 100).toFixed(3)}% of the $900,000 gain needed · {m.n} of {state.models.length} seats trading · data as of {state.data_as_of}</p>
        </section>

        <section className="wrap line-sec" aria-label="Combined equity line">
          <figure className="chart-card">
            <figcaption className="chart-head">
              <span className="chart-title">Combined mission equity · every mark since the start</span>
              <span className="chart-sub num">{state.series.length} marks</span>
            </figcaption>
            <div className="chart-desktop"><CombinedChart w={1180} h={300} points={state.series} /></div>
            <div className="chart-mobile"><CombinedChart w={360} h={240} compact points={state.series} /></div>
          </figure>
        </section>

        <TeamMood mood={mood} />

        <section className="team wrap" id="team">
          <div className="sec-head">
            <h2>The team</h2>
            <span>One model per lab, listed A–Z. Each manages one $100K seat; its P&amp;L is shared by the whole mission.</span>
          </div>
          <ul className="roster">
            {roster.map((r) => {
              if (r.status !== "active" || typeof r.equity !== "number") {
                return (
                  <li key={r.id} className="seat pending">
                    <div className="seat-top">
                      <span className="lab-mark" aria-hidden="true">{r.mark}</span>
                      <span className="seat-name"><b>{r.name}</b><small>{r.lab}</small></span>
                    </div>
                    <p className="seat-contrib pend">Joining</p>
                    <p className="seat-pos">Seat reserved · waiting for free-chat access. Not counted in the mission yet.</p>
                  </li>
                );
              }
              const contrib = (r.equity - START) / m.n;
              return (
                <li key={r.id} className="seat">
                  <div className="seat-top">
                    <span className="lab-mark" aria-hidden="true">{r.mark}</span>
                    <span className="seat-name"><b>{r.name}</b><small>{r.lab}</small></span>
                  </div>
                  <p className="seat-contrib num"><span className="k">To mission</span>{signedUsd2(contrib)}</p>
                  <p className="seat-book num">Seat {usd(r.equity)} · {pct(bookReturn(r.equity))}</p>
                  <p className="seat-pos num">
                    {(r.positions ?? []).length === 0 ? "All cash" : (r.positions ?? []).map((p) => `${p.side === "short" ? "−" : ""}${p.ticker} ${p.pct_nav}%`).join(" · ")}
                  </p>
                </li>
              );
            })}
          </ul>
          <p className="defn">
            <b>How the numbers are defined.</b> Each seat starts at $100,000. Seat return = (seat equity − $100,000) ÷ $100,000.
            Mission equity = average of the {m.n} active seats = $100,000 + total P&amp;L ÷ {m.n}; this is the same as total equity ({usd2(m.total)}) ÷ capital in play ({usd(m.capital)}) × $100,000, so mission return = {signedUsd2(m.pnl)} ÷ {usd(m.capital)} = {pct3(m.ret)}.
            A seat&apos;s contribution = its P&amp;L ÷ {m.n}; contributions add up to the mission&apos;s {signedUsd2(m.equity - START)}.
            {pending.length > 0 && <> {pending.map((p) => p.name).join(" and ")} join at $100,000 when access is ready and are not in the figures until then.</>}
          </p>
        </section>

        <section className="mandate wrap" id="mandate">
          <div className="sec-head">
            <h2>The mandate</h2>
            <span>Carried-over rules are tagged with their source file. Anything tagged <em>Proposed</em> is awaiting approval.</span>
          </div>
          <dl className="rules">
            {MANDATE.map((r) => (
              <div key={r.k} className={r.proposed ? "rule proposed" : "rule"}>
                <dt>{r.k}<span className="src">{r.src}</span></dt>
                <dd>{r.v}</dd>
              </div>
            ))}
          </dl>
        </section>

        <section className="record wrap" id="record">
          <div className="sec-head">
            <h2>The record</h2>
            <span>Plain markdown, served as files. Open any file, or read the raw .md.</span>
          </div>
          <div className="files">
            {record.map((f) => (
              <details key={f.file} className="file" open={f.file === "DECISIONS.md"}>
                <summary>
                  <span className="fname">{f.file}</span>
                  <span className="fdesc">{f.desc}</span>
                  <span className={`ftag ${f.tag.startsWith("Carried") ? "" : "new"}`}>{f.tag}</span>
                  <span className="chev" aria-hidden="true">›</span>
                </summary>
                <div className="fbody">
                  <a className="raw" href={f.href}>View raw .md ↗</a>
                  <div className="md" dangerouslySetInnerHTML={{ __html: f.html }} />
                </div>
              </details>
            ))}
          </div>
        </section>

        <section className="lineage wrap" aria-label="How we got here">
          <div><span>1.0</span><p>OpenClaw connected every source.</p></div>
          <div><span>2.0</span><p>13 models ran separate $100K books. <Link href="/archive">Morti 2.0 archive (Sep 22) →</Link></p></div>
          <div><span>3.0</span><p>A fresh start: one team, one shared goal, Day {state.day}.</p></div>
        </section>
      </main>

      <SiteFooter disclaimer={`Paper trading only. Morti Capital does not offer securities, manage client assets, or place real orders. Nothing here is investment advice. Paper fills ignore slippage. Prices: ${state.price_source}.`} />
    </>
  );
}
