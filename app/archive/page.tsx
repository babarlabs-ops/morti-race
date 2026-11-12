import race from "../../data/race-2.0.json";
import { SiteFooter } from "../../components/SiteFooter";
import { SiteHeader } from "../../components/SiteHeader";
import { usd } from "../../lib/mission";

export const dynamic = "force-static";
export const metadata = { title: "Morti 2.0 archive" };

function pct(r: number) {
  if (Math.abs(r) < 0.0005) return "0.0%";
  return (r > 0 ? "+" : "−") + Math.abs(r * 100).toFixed(1) + "%";
}

export default function Archive() {
  return (
    <>
      <SiteHeader current="archive" />
      <main id="content" className="wrap archive">
        <p className="eyebrow">Archive</p>
        <h1 className="archive-h">Morti 2.0 archive</h1>
        <p className="sub">13 models, each with its own $100K paper account under identical rules. 2.0 was paused and archived on Sep 22, 2026 at 9:30 AM ET. It is not part of the 3.0 mission.</p>
        <table>
          <thead><tr><th>Model</th><th className="lab-h">Lab</th><th className="r">Equity</th><th className="r">Return</th></tr></thead>
          <tbody>
            {[...race.models].sort((a, b) => a.name.localeCompare(b.name)).map((m) => {
              const r = m.equity / 100000 - 1;
              return (
                <tr key={m.name}>
                  <td className="name">{m.name}{m.cohort !== "season1" && <span className="since">since Sep 9</span>}</td>
                  <td className="lab">{m.lab}</td>
                  <td className="r num">{usd(m.equity)}</td>
                  <td className={`r num ${r > 0.0005 ? "up" : r < -0.0005 ? "dn" : "flat"}`}>{pct(r)}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
        <p className="archive-note">Return = (equity − $100K) ÷ $100K. Listed A–Z. Source: the public 2.0 ledger (github.com/babarlabs-ops/morti-race), data as of Sep 22, 2026, 9:30 AM ET.</p>
      </main>
      <SiteFooter disclaimer="Paper trading only. Nothing here is investment advice." />
    </>
  );
}
