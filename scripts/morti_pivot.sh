#!/bin/bash
# Morti Race — mid-day pivot: re-run the decision cycle so models can reverse a wrong thesis.
# Silent on success (verbose → data/cycle.log). Prints 🚨 on failure.
set -uo pipefail
REPO="/Users/minimi/Claude Working files/morti-race"
LOG="$REPO/data/cycle.log"
cd "$REPO" || { echo "🚨 Morti pivot FATAL: repo not found"; exit 1; }
log(){ echo "[$(date '+%F %T')] $*" >> "$LOG"; }

# credit preflight
CRED=$(python3 scripts/check_credits.py 2>/dev/null); RC=$?
if [ "$RC" -eq 1 ]; then echo "🚨 Morti pivot HALTED: OpenRouter credits low (${CRED}). Refill."; exit 1; fi
if [ "$RC" -eq 2 ]; then log "credit check failed: ${CRED} (continuing)"; fi
log "pivot credits: ${CRED}"

# archive the prior cycle's picks before overwriting (audit trail, distinct per pivot)
DAY=$(date '+%Y-%m-%d')
HHMM=$(date '+%H%M')
PICKS="data/picks/${DAY}.json"
if [ -f "$PICKS" ]; then
  mkdir -p data/picks/archive
  cp "$PICKS" "data/picks/archive/${DAY}-${HHMM}.json" 2>/dev/null && log "archived prior picks → ${DAY}-${HHMM}.json"
fi

log "=== pivot start ==="
python3 scripts/fetch_snapshot.py       >>"$LOG" 2>&1 || { echo "🚨 Morti pivot FAILED: fetch_snapshot"; exit 1; }
python3 scripts/fetch_macro.py          >>"$LOG" 2>&1 || log "(macro fetch failed — continuing)"
# NEW research sources (free-first, X paid via xAI)
python3 scripts/fetch_news.py           >>"$LOG" 2>&1 || log "(news fetch failed — continuing)"
python3 scripts/fetch_reddit.py         >>"$LOG" 2>&1 || log "(reddit fetch failed — continuing)"
python3 scripts/fetch_edgar.py          >>"$LOG" 2>&1 || log "(edgar fetch failed — continuing)"
python3 scripts/fetch_calendar.py       >>"$LOG" 2>&1 || log "(calendar fetch failed — continuing)"
python3 scripts/fetch_sentiment.py      >>"$LOG" 2>&1 || log "(sentiment fetch failed — continuing)"
python3 scripts/run_picks.py            >>"$LOG" 2>&1 || { echo "🚨 Morti pivot FAILED: run_picks"; exit 1; }
python3 scripts/build_ledger.py         >>"$LOG" 2>&1 || { echo "🚨 Morti pivot FAILED: build_ledger"; exit 1; }
python3 scripts/resolve_calibration.py  >>"$LOG" 2>&1 || { echo "🚨 Morti pivot FAILED: resolve_calibration"; exit 1; }
git add -A
git -c user.name="Morti" -c user.email="morti@morti.capital" commit -m "Pivot $(date '+%F %T')" >>"$LOG" 2>&1 || log "(no changes)"
TOKEN=$(grep '^GITHUB_TOKEN=' /Users/minimi/.hermes/profiles/morti/.env | head -1 | cut -d= -f2- | tr -d '"' | tr -d "'" | tr -d '[:space:]')
if [ -n "$TOKEN" ]; then
  git push "https://x-access-token:${TOKEN}@github.com/babarlabs-ops/morti-race.git" main >>"$LOG" 2>&1 || { echo "🚨 Morti pivot FAILED: git push"; exit 1; }
else
  echo "🚨 Morti pivot FAILED: no GITHUB_TOKEN"; exit 1
fi
log "=== pivot complete ==="
