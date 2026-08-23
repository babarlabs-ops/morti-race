import fs from 'fs';
import path from 'path';

const CRYPTO = new Set(["BTC","ETH","SOL","DOGE","XRP","ADA","LTC","AVAX","LINK","DOT","BCH","UNI","SHIB","PEPE","TRX","XLM","NEAR","APT","SUI","ARB","OP","TON","INJ","MATIC","WIF","BONK"]);

// Options pricing — mirrors scripts/build_ledger.py (Black-Scholes)
const VOL = 0.35;
const RATE = 0.04;
const MULT = 100;

function normCdf(x) {
  const t = 1 / (1 + 0.2316419 * Math.abs(x));
  const d = 0.3989422804014327 * Math.exp(-x * x / 2);
  const p = d * t * (0.319381530 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + t * 1.330274429))));
  return x > 0 ? 1 - p : p;
}

function bsPrice(spot, strike, tYears, isCall) {
  if (!(spot > 0) || !(strike > 0)) return 0;
  if (tYears <= 0) return isCall ? Math.max(0, spot - strike) : Math.max(0, strike - spot);
  const d1 = (Math.log(spot / strike) + (RATE + 0.5 * VOL * VOL) * tYears) / (VOL * Math.sqrt(tYears));
  const d2 = d1 - VOL * Math.sqrt(tYears);
  if (isCall) return spot * normCdf(d1) - strike * Math.exp(-RATE * tYears) * normCdf(d2);
  return strike * Math.exp(-RATE * tYears) * normCdf(-d2) - spot * normCdf(-d1);
}

function optionValue(opt, spot, now) {
  const expiry = new Date(opt.expiry);
  const tYears = Math.max(0, (expiry.getTime() - now.getTime()) / (365 * 86400 * 1000));
  return bsPrice(spot, opt.strike, tYears, opt.is_call);
}

async function alpaca(url) {
  const r = await fetch(url, {
    headers: {
      "APCA-API-KEY-ID": process.env.ALPACA_KEY,
      "APCA-API-SECRET-KEY": process.env.ALPACA_SECRET,
    },
  });
  if (!r.ok) throw new Error(`Alpaca HTTP ${r.status}`);
  return r.json();
}

async function livePrices(tickers) {
  const eq = tickers.filter(t => !CRYPTO.has(t));
  const cr = tickers.filter(t => CRYPTO.has(t));
  const out = {};
  if (eq.length) {
    const d = await alpaca(`https://data.alpaca.markets/v2/stocks/snapshots?symbols=${eq.join(',')}&feed=iex`);
    for (const [s, v] of Object.entries(d)) {
      const t = v.latestTrade || {};
      const db = v.dailyBar || {};
      out[s] = t.p || db.c;
    }
  }
  if (cr.length) {
    const pairs = cr.map(s => encodeURIComponent(`${s}/USD`)).join(',');
    const d = await alpaca(`https://data.alpaca.markets/v1beta3/crypto/us/latest/bars?symbols=${pairs}`);
    for (const [pair, bar] of Object.entries(d.bars || {})) {
      out[pair.split('/')[0]] = bar.c;
    }
  }
  return out;
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 'no-store');
  try {
    const ledger = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'data', 'ledger.json'), 'utf8'));
    const tickers = new Set();
    for (const m of Object.values(ledger.models)) {
      for (const p of (m.positions || [])) tickers.add(p.ticker);
    }
    const live = await livePrices([...tickers]);
    const now = new Date();
    for (const m of Object.values(ledger.models)) {
      let u = 0;
      for (const p of (m.positions || [])) {
        let pnl;
        if (p.kind === 'option') {
          const spot = live[p.ticker] ?? p.underlying_spot ?? p.entry;
          pnl = (optionValue(p, spot, now) - (p.premium || 0)) * (p.contracts || 0) * MULT;
          p.last = spot;
        } else {
          const last = live[p.ticker] ?? p.last;
          if (p.shares == null) { p.unrealized_pnl = 0; p.unrealized_pnl_pct = 0; continue; }
          pnl = p.side === 'long' ? (last - p.entry) * p.shares : (p.entry - last) * p.shares;
          p.last = last;
        }
        if (!Number.isFinite(pnl)) pnl = 0;
        p.unrealized_pnl = +pnl.toFixed(2);
        p.unrealized_pnl_pct = p.dollar ? +(pnl / p.dollar * 100).toFixed(2) : 0;
        u += pnl;
      }
      m.unrealized_pnl = +u.toFixed(2);
      const base = Number.isFinite(m.equity) ? m.equity : ledger.start_capital;
      m.equity = +(base + u).toFixed(2);
      m.return_pct = +((m.equity / ledger.start_capital - 1) * 100).toFixed(3);
      m.return_24h = Number.isFinite(m.prev_equity) && m.prev_equity > 0 ? +((m.equity / m.prev_equity - 1) * 100).toFixed(2) : null;
    }
    ledger.as_of = new Date().toISOString();
    res.status(200).json(ledger);
  } catch (e) {
    res.status(500).json({ error: String((e && e.message) || e) });
  }
}
