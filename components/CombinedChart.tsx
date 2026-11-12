import { START, type SeriesPoint } from "../lib/mission";

type Props = { w: number; h: number; compact?: boolean; points: SeriesPoint[] };

function niceStep(range: number, target: number) {
  const raw = range / target;
  const mag = Math.pow(10, Math.floor(Math.log10(raw)));
  const n = raw / mag;
  return (n < 1.5 ? 1 : n < 3 ? 2 : n < 7 ? 5 : 10) * mag;
}

function timeLabel(p: SeriesPoint) {
  if (p.kind === "day0") return "Start";
  const t = p.ts_et.slice(11, 16);
  const [hh, mm] = t.split(":").map(Number);
  const h12 = ((hh + 11) % 12) + 1;
  return `D${p.day} ${h12}:${String(mm).padStart(2, "0")}${hh < 12 ? "a" : "p"}`;
}

/** One combined line: mission equity (mean of active $100K books) at every mark (state.json series, written by mark.py from history.json). */
export function CombinedChart({ w, h, compact = false, points }: Props) {
  const pad = compact ? { l: 70, r: 16, t: 22, b: 30 } : { l: 84, r: 30, t: 26, b: 36 };
  const vals = points.map((p) => p.equity);
  let lo = Math.min(START, ...vals);
  let hi = Math.max(START, ...vals);
  const span = Math.max(hi - lo, 20);
  lo -= span * 0.25;
  hi += span * 0.25;
  const step = niceStep(hi - lo, compact ? 3 : 4);
  const ticks: number[] = [];
  for (let v = Math.ceil(lo / step) * step; v <= hi; v += step) ticks.push(Math.round(v * 100) / 100);

  const n = points.length;
  const x = (i: number) => pad.l + (n <= 1 ? 0 : (i / (n - 1)) * (w - pad.l - pad.r));
  const y = (v: number) => pad.t + (1 - (v - lo) / (hi - lo)) * (h - pad.t - pad.b);
  const fs = compact ? 10 : 11.5;
  const d = points.map((p, i) => `${i === 0 ? "M" : "L"} ${x(i).toFixed(1)} ${y(p.equity).toFixed(1)}`).join(" ");
  const area = `${d} L ${x(n - 1).toFixed(1)} ${y(lo).toFixed(1)} L ${x(0).toFixed(1)} ${y(lo).toFixed(1)} Z`;
  const last = points[n - 1];
  const lastV = last.equity;
  const showEvery = Math.max(1, Math.ceil(n / (compact ? 3 : 7)));
  const fmt = (v: number) => "$" + v.toLocaleString("en-US", { minimumFractionDigits: step < 1 ? 2 : 0, maximumFractionDigits: step < 1 ? 2 : 0 });

  return (
    <svg viewBox={`0 0 ${w} ${h}`} className="chart-svg" role="img"
      aria-label={`Combined mission equity at each of ${n} marks. Latest: ${fmt(lastV)}.`}>
      <defs>
        <linearGradient id={compact ? "cfill-m" : "cfill"} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#5bd69b" stopOpacity="0.16" />
          <stop offset="1" stopColor="#5bd69b" stopOpacity="0" />
        </linearGradient>
      </defs>
      {ticks.map((v) => (
        <g key={v}>
          <line x1={pad.l} x2={w - pad.r} y1={y(v)} y2={y(v)} className="c-grid" />
          <text x={pad.l - 10} y={y(v) + 4} textAnchor="end" className="c-axis" fontSize={fs}>{fmt(v)}</text>
        </g>
      ))}
      <line x1={pad.l} x2={w - pad.r} y1={y(START)} y2={y(START)} className="c-base" />
      <text x={w - pad.r} y={y(START) - 7} textAnchor="end" className="c-base-label" fontSize={fs}>$100,000 start</text>
      {points.map((p, i) =>
        i % showEvery === 0 || i === n - 1 ? (
          <text key={`x-${i}`} x={x(i)} y={h - 10} textAnchor={i === 0 ? "start" : i === n - 1 ? "end" : "middle"} className="c-axis" fontSize={fs}>
            {timeLabel(p)}
          </text>
        ) : null,
      )}
      <path d={area} fill={`url(#${compact ? "cfill-m" : "cfill"})`} />
      <path d={d} className="c-track" fill="none" />
      {points.map((p, i) => (
        <circle key={`${p.ts_et}-${i}`} cx={x(i)} cy={y(p.equity)} r={i === n - 1 ? 5 : 3} className={i === n - 1 ? "c-day0" : "c-pt"} />
      ))}
      <text x={x(n - 1) - 10} y={y(lastV) - 12} textAnchor="end" className="c-day0-label" fontSize={fs + 1}>${lastV.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</text>
    </svg>
  );
}
