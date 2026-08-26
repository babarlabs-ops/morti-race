#!/bin/bash
# Morti Race — daily autonomous cycle.
# Silent on success (verbose → data/cycle.log). Prints a 🚨 alert to stdout ONLY on failure,
# so the cron can deliver failures to the operator's channel without daily spam.
set -uo pipefail
REPO="/Users/minimi/Claude Working files/morti-race"
LOG="$REPO/data/cycle.log"
cd "$REPO" || { echo "🚨 Morti cycle FATAL: repo not found"; exit 1; }
log(){ echo "[$(date '+%F %T')] $*" >> "$LOG"; }

# 0/6 OpenRouter credit preflight — halt before burning a partial cycle
CRED=$(python3 scripts/check_credits.py 2>/dev/null); RC=$?
if [ "$RC" -eq 1 ]; then
  echo "🚨 Morti HALTED: OpenRouter credits low (${CRED} remaining). Refill before next cycle."
  exit 1
fi
if [ "$RC" -eq 2 ]; then log "credit check failed: ${CRED} (continuing)"; fi
log "credits remaining: ${CRED}"

log "=== cycle start ==="
python3 scripts/fetch_snapshot.py       >>"$LOG" 2>&1 || { echo "🚨 Morti FAILED: fetch_snapshot (see data/cycle.log)"; exit 1; }
python3 scripts/fetch_macro.py          >>"$LOG" 2>&1 || log "(macro fetch failed — continuing)"
# NEW research sources (free-first, X paid via xAI)
python3 scripts/fetch_news.py           >>"$LOG" 2>&1 || log "(news fetch failed — continuing)"
python3 scripts/fetch_reddit.py         >>"$LOG" 2>&1 || log "(reddit fetch failed — continuing)"
python3 scripts/fetch_edgar.py          >>"$LOG" 2>&1 || log "(edgar fetch failed — continuing)"
python3 scripts/fetch_calendar.py       >>"$LOG" 2>&1 || log "(calendar fetch failed — continuing)"
python3 scripts/fetch_sentiment.py      >>"$LOG" 2>&1 || log "(sentiment fetch failed — continuing)"
python3 scripts/run_picks.py            >>"$LOG" 2>&1 || { echo "🚨 Morti FAILED: run_picks (see data/cycle.log)"; exit 1; }
python3 scripts/build_ledger.py         >>"$LOG" 2>&1 || { echo "🚨 Morti FAILED: build_ledger (see data/cycle.log)"; exit 1; }
python3 scripts/resolve_calibration.py  >>"$LOG" 2>&1 || { echo "🚨 Morti FAILED: resolve_calibration (see data/cycle.log)"; exit 1; }

git add -A
git -c user.name="Morti" -c user.email="morti@morti.capital" commit -m "Daily cycle $(date '+%Y-%m-%d')" >>"$LOG" 2>&1 || log "(no changes to commit)"
TOKEN=$(grep '^GITHUB_TOKEN=' /Users/minimi/.hermes/profiles/morti/.env | head -1 | cut -d= -f2- | tr -d '"' | tr -d "'" | tr -d '[:space:]')
if [ -n "$TOKEN" ]; then
  git push "https://x-access-token:${TOKEN}@github.com/babarlabs-ops/morti-race.git" main >>"$LOG" 2>&1 || { echo "🚨 Morti FAILED: git push (conflict or auth — see data/cycle.log)"; exit 1; }
else
  echo "🚨 Morti FAILED: no GITHUB_TOKEN"; exit 1
fi

log "=== cycle complete ==="
