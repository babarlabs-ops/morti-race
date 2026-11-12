# DECISIONS — 2026-11-11-c2

Generated: 2026-11-11 12:41:54 EST
Prices: Yahoo Finance chart v8 (query1.finance.yahoo.com) @ 2026-11-11 12:30:28 EST
Engine: fill.py v2 (rebalance against existing books; stops/targets checked first)

## chatgpt
- status: `FILLED`
- sha256: `074b0b99d0b8f45591c651ad86a8b382c7096bb765a0f7297782eaf021dcc41a`
- source_file: `answers/chatgpt.md`
- events:
  - EDIT long SPY 0.0 sh @ 760.69 (stop 742.0->750.0)
  - EDIT long XLE 0.0 sh @ 62.915 (stop 61.0->61.5)
  - EDIT long GOOGL 0.0 sh @ 293.36 (stop 282.0->286.0)
  - EDIT long XLI 0.0 sh @ 171.109 (stop 164.0->166.0)
  - OPEN long SMH 13.605744 sh @ 514.95 stop=490.0 target=580.0
  - OPEN long XLF 137.214883 sh @ 58.355 stop=56.0 target=65.0
  - OPEN long XLV 42.693546 sh @ 187.55 stop=182.0 target=205.0
- resulting book: equity 100089.68, cash 21989.59, gross 78.03%, net 78.03%, positions ['GLD', 'SPY', 'XLE', 'GOOGL', 'XLI', 'SMH', 'XLF', 'XLV']

## claude
- status: `FILLED`
- sha256: `5343538d699420be0981395dcfac24d8872d944de2b21143faad1047c39e975f`
- source_file: `answers/claude.md`
- events:
  - EDIT long SMH 0.0 sh @ 514.95 (stop 478.0->495.0)
  - EDIT long SPY 0.0 sh @ 760.69 (stop 718.0->738.0)
  - EDIT long BTC-USD 0.0 sh @ 74406.41 (stop 66000.0->68500.0)
  - OPEN long QQQ 5.77388 sh @ 694.05 stop=660.0 target=760.0
- resulting book: equity 100184.03, cash 59002.04, gross 41.11%, net 41.11%, positions ['SPY', 'SMH', 'GLD', 'XLE', 'BTC-USD', 'QQQ']

## gemini
- status: `FILLED`
- sha256: `700d3374e208b55a5b80ffb7ca653abd91ffc5c3e5a424c87b4e9e174680929f`
- source_file: `answers/gemini.md`
- events:
  - OPEN long IWM 72.777174 sh @ 283.35 stop=276.5 target=305.0
- resulting book: equity 99716.69, cash 73399.08, gross 46.93%, net 26.39%, positions ['QQQ', 'GLD', 'XLE', 'IWM']

## glm
- status: `FILLED`
- sha256: `e0500b3e2832f50f11ab0f2a1911fe17de25d20293f8983224d02980b1f2cebb`
- source_file: `answers/glm.md`
- events:
  - EDIT long ETH-USD 0.0 sh @ 2090.87 (stop 1878.0->1950.0)
- resulting book: equity 99889.36, cash 46663.06, gross 53.29%, net 53.29%, positions ['BTC-USD', 'TLT', 'GLD', 'QQQ', 'IWM', 'ETH-USD']

## grok
- status: `FILLED`
- sha256: `aa8db5f4e6afff4e6b8889147513e99ffbe1d2184a8dbb0871184b88599527e6`
- source_file: `answers/grok.md`
- events:
  - EDIT long IWM 0.0 sh @ 283.35 (stop 275.0->278.0)
  - OPEN long SPY 13.100803 sh @ 760.69 stop=745.0 target=810.0
  - OPEN long QQQ 11.486953 sh @ 694.05 stop=670.0 target=740.0
- resulting book: equity 99656.50, cash 71729.61, gross 28.02%, net 28.02%, positions ['IWM', 'SPY', 'QQQ']

## mistral
- status: `FILLED`
- sha256: `62be031365c8712c501f64fb07be037da67d454b639c73918a5c89554b9fdb26`
- source_file: `answers/mistral.md`
- events:
  - EDIT long XLF 0.0 sh @ 58.355 (stop 55.3->57.0)
  - OPEN long TLT 123.053535 sh @ 80.855 stop=79.3 target=84.0
- resulting book: equity 99494.94, cash 79572.11, gross 20.02%, net 20.02%, positions ['XLF', 'TLT']

## qwen
- status: `FILLED`
- sha256: `5a7e6464064840792dffb1b0c5e008bc4d9a527d7f6925710ac2eb3ee047e892`
- source_file: `answers/qwen.md`
- events:
  - EDIT long QQQ 0.0 sh @ 694.05 (stop 665.0->680.0)
  - OPEN long IWM 17.643799 sh @ 283.35 stop=270.0 target=300.0
- resulting book: equity 99987.41, cash 65020.19, gross 34.97%, net 34.97%, positions ['QQQ', 'GLD', 'BTC-USD', 'XLF', 'IWM']

