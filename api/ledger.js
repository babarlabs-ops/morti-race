import fs from 'fs';
import path from 'path';

const CRYPTO = new Set(["BTC","ETH","SOL","DOGE","XRP","ADA","LTC","AVAX","LINK","DOT","BCH","UNI","SHIB","PEPE","TRX","XLM","NEAR","APT","SUI","ARB","OP","TON","INJ","MATIC","WIF","BONK"]);

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
    for (const m of Object.values(ledger.models)) {
      let u = 0;
      for (const p of (m.positions || [])) {
        const last = live[p.ticker] ?? p.last;
        const pnl = p.side === 'long' ? (last - p.entry) * p.shares : (p.entry - last) * p.shares;
        p.last = last;
        p.unrealized_pnl = +pnl.toFixed(2);
        p.unrealized_pnl_pct = +(pnl / p.dollar * 100).toFixed(2);
        u += pnl;
      }
      m.unrealized_pnl = +u.toFixed(2);
      m.equity = +(ledger.start_capital + u).toFixed(2);
      m.return_pct = +((m.equity / ledger.start_capital - 1) * 100).toFixed(3);
    }
    ledger.as_of = new Date().toISOString();
    res.status(200).json(ledger);
  } catch (e) {
    res.status(500).json({ error: String((e && e.message) || e) });
  }
}
