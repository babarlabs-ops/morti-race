# DECISIONS.md: the mission log

Append-only. One entry per cycle: the model that proposed each thesis, the thesis, the gate rulings, any orders, and the content hash.

Mission started **Nov 9, 2026** (Day 1). Paper mode. Zero-cost fills against Yahoo Finance chart v8.

## Cycles

| Cycle | Day | Models filled | Record |
|---|---|---|---|
| 2026-11-09-c1 | 1 | ChatGPT, Gemini | [DECISIONS.md](/record/cycles/2026-11-09-c1/DECISIONS.md) · [brief.md](/record/cycles/2026-11-09-c1/brief.md) · [rejects.log](/record/cycles/2026-11-09-c1/rejects.log) |
| 2026-11-09-c2 | 1 | Kimi, Qwen (catch-up join) | [DECISIONS.md](/record/cycles/2026-11-09-c2/DECISIONS.md) · [brief.md](/record/cycles/2026-11-09-c2/brief.md) · [rejects.log](/record/cycles/2026-11-09-c2/rejects.log) |
| 2026-11-09-c3 | 1 | Grok, Claude, Mistral, GLM (catch-up join) | [DECISIONS.md](/record/cycles/2026-11-09-c3/DECISIONS.md) · [brief.md](/record/cycles/2026-11-09-c3/brief.md) · [rejects.log](/record/cycles/2026-11-09-c3/rejects.log) |
| 2026-11-11-c1 | 3 | ChatGPT, Claude, DeepSeek, Gemini, GLM, Grok, Mistral, Qwen | [DECISIONS.md](/record/cycles/2026-11-11-c1/DECISIONS.md) · [brief.md](/record/cycles/2026-11-11-c1/brief.md) · [rejects.log](/record/cycles/2026-11-11-c1/rejects.log) |
| 2026-11-11-c2 | 3 | ChatGPT, Claude, Gemini, GLM, Grok, Mistral, Qwen | [DECISIONS.md](/record/cycles/2026-11-11-c2/DECISIONS.md) · [brief.md](/record/cycles/2026-11-11-c2/brief.md) · [rejects.log](/record/cycles/2026-11-11-c2/rejects.log) |
| 2026-11-11-c3 | 3 | ChatGPT, Claude, Gemini, Grok, Mistral, Qwen | [DECISIONS.md](/record/cycles/2026-11-11-c3/DECISIONS.md) · [brief.md](/record/cycles/2026-11-11-c3/brief.md) · [rejects.log](/record/cycles/2026-11-11-c3/rejects.log) |

## 2026-11-09-c1 (summary)

Prices: Yahoo Finance chart v8 @ 2026-11-09 14:08:58 EST.

### chatgpt
- status: `FILLED`
- sha256: `2bb6c41f5aec6c3553834cdd69643df9b324149a56df99220860c5dc5e8a55e7`
- fills:
  - long GLD 15.0% @ 376.02 stop=364.0 target=413.0
  - long SPY 15.0% @ 752.76 stop=730.0 target=815.0
  - long XLE 10.0% @ 61.825 stop=59.0 target=69.0

### gemini
- status: `FILLED`
- sha256: `058c1fd1355bd0fa057e828a1fc5cf1927096d33603bee053161a32834f0a605`
- notes: trade[0] rejected: entry→stop risk 57.2 bps > 50.0 bps NAV; trade[2] rejected: entry→stop risk 70.0 bps > 50.0 bps NAV
- fills:
  - short QQQ 10.0% @ 677.642 stop=701.0 target=620.0

Full cycle files (with theses and hashes): [`/record/cycles/2026-11-09-c1/`](/record/cycles/2026-11-09-c1/DECISIONS.md).

## 2026-11-09-c2 (summary)

Catch-up cycle. Kimi and Qwen joined with their own $100K books. Start prices: Yahoo Finance chart v8 @ **2026-11-09 14:56:06 EST**. ChatGPT and Gemini books from c1 were left unchanged.

### kimi
- status: `FILLED`
- started: c2 @ 2026-11-09 14:56:06 EST
- sha256: `5f09c6859e78dd35e7a8a45b6460ee2cce11656dbdff63d175fc9637b0c505b9`
- fills:
  - long GLD 10.0% @ 378.685 stop=362.0 target=410.0
  - long NVDA 5.0% @ 176.68 stop=160.0 target=205.0
  - long BTC-USD 5.0% @ 74754.13 stop=68000.0 target=85000.0

### qwen
- status: `FILLED`
- started: c2 @ 2026-11-09 14:56:06 EST
- sha256: `66928177713d70ec418aed4d32fc3e13b389300b9cac719c4a03a0fe1955a011`
- fills:
  - long QQQ 10.0% @ 679.098 stop=646.0 target=720.0
  - long GLD 10.0% @ 378.685 stop=360.5 target=400.0

Full cycle files (with theses and hashes): [`/record/cycles/2026-11-09-c2/`](/record/cycles/2026-11-09-c2/DECISIONS.md).

## 2026-11-09-c3 (summary)

Catch-up cycle. Grok, Claude, Mistral (Le Chat Work / Fast), and GLM (GLM-5.3 on chat.z.ai) joined with their own $100K books. Start prices: Yahoo Finance chart v8 @ **2026-11-09 15:15:38 EST**. Prior models' books from c1/c2 were left unchanged.

### grok
- status: `FILLED`
- started: c3 @ 2026-11-09 15:15:38 EST
- sha256: `5d72aafeb86149a11f36357c267c2d2e86165ba4bfd8fabd62d62c08ec3a4c35`
- fills:
  - long GLD 10.0% @ 379.87 stop=370.0 target=400.0
  - long IWM 10.0% @ 283.67 stop=275.0 target=300.0

### claude
- status: `FILLED`
- started: c3 @ 2026-11-09 15:15:38 EST
- sha256: `4c3ddd0ff5afa5db6ada0b7ce8836f9f92786bce3013b1cc3f790abe59180789`
- fills:
  - long SPY 10.0% @ 755.28 stop=718 target=830
  - long SMH 8.0% @ 489.14 stop=460 target=560
  - long GLD 10.0% @ 379.87 stop=362 target=420

### mistral
- status: `FILLED`
- started: c3 @ 2026-11-09 15:15:38 EST
- via: Le Chat Work mode (Fast)
- sha256: `f36f3cfe6bcb5923e1aadcc84c7754bd0d0ad05179701bc83b222540a75d0885`
- notes: trade[1] rejected: pct 12.0 > max 10.0 for BTC-USD
- fills:
  - long GLD 16.0% @ 379.87 stop=368.0 target=420.0

### glm
- status: `FILLED`
- started: c3 @ 2026-11-09 15:15:38 EST
- via: GLM-5.3 on chat.z.ai
- sha256: `5c07dce588d81269c8e423336c4b42ca09fef56f3c1e2f23d06fd5434fa49cf3`
- fills:
  - long BTC-USD 7.0% @ 74939.58 stop=70000 target=92000
  - long TLT 10.0% @ 81.965 stop=79.2 target=88.0
  - long GLD 7.0% @ 379.87 stop=362.0 target=420.0

Full cycle files (with theses and hashes): [`/record/cycles/2026-11-09-c3/`](/record/cycles/2026-11-09-c3/DECISIONS.md).

## 2026-11-11-c1 (summary)

First v2 rebalance cycle (hold / add / trim / exit on existing books, then up to 3 new trades). Prices: Yahoo Finance chart v8 @ **2026-11-11 10:25:43 EST**. Filled **2026-11-11 10:57:55 EST**. Engine: fill.py v2. Kimi did not answer this cycle (existing book received only the stop/target sweep). Llama is still waiting for access and has no book.

Stop/target sweep (before actions):
- Grok: STOP long GLD @ 367.25, realized −332.22 (price crossed stop 370.0)
- Mistral: STOP long GLD @ 367.25, realized −531.55 (price crossed stop 368.0)

### chatgpt
- status: `FILLED`
- sha256: `c534aee31db9f82f5ae915100aad9d7440ed8236ff291daff57b077ec649ae11`
- events: tightened SPY stop 730.0→742.0; tightened XLE stop 59.0→61.0; OPEN long GOOGL; OPEN long XLI
- resulting book after fill: equity 99931.87, positions GLD, SPY, XLE, GOOGL, XLI

### claude
- status: `FILLED`
- sha256: `da116ed3eadc65a1a7e0271d6d400a3214aedee1727215fd1cebea94edf2d050`
- events: tightened SMH stop 460.0→478.0; OPEN long XLE; OPEN long BTC-USD
- resulting book after fill: equity 99895.54, positions SPY, SMH, GLD, XLE, BTC-USD

### deepseek
- status: `PARTIAL`
- sha256: `eab1a75cb8772469e2b0df562a69540fcd1645add17a9305dbf61f6d93e08f5b`
- notes: trade[0] long GLD rejected: entry→stop risk 59.4 bps > 50.0 bps NAV; trade[2] long BTC-USD rejected: entry→stop risk 62.2 bps > 50.0 bps NAV
- events: OPEN long XLE
- resulting book after fill: equity 100000.00, positions XLE

### gemini
- status: `FILLED`
- sha256: `1b7520a7c07bbcf2209d4e173d9247c565d1aa195595687853872c61882a44d5`
- events: OPEN long GLD; OPEN long XLE
- resulting book after fill: equity 99871.94, positions QQQ, GLD, XLE

### glm
- status: `FILLED`
- sha256: `13b613bccbe16d974a149f53212087729649e517592a742851bc608a3fc43bbb`
- events: OPEN long QQQ; OPEN long IWM; OPEN long ETH-USD
- resulting book after fill: equity 99447.15, positions BTC-USD, TLT, GLD, QQQ, IWM, ETH-USD

### grok
- status: `HOLD`
- sha256: `2d61106cb4f1fef2952e91dbcdb96fbe0a3d243f784e826fc265d05d71c17da2`
- events: none after the GLD stop
- resulting book after fill: equity 99603.97, positions IWM

### mistral
- status: `PARTIAL`
- sha256: `e4fff4f4e203242ad16dbff1842b83df62f8d76d1def29a6fe15c4ba7818e729`
- notes: trade[1] long XLV rejected: entry→stop risk 50.1 bps > 50.0 bps NAV
- events: OPEN long XLF (after the GLD stop)
- resulting book after fill: equity 99468.45, positions XLF

### qwen
- status: `FILLED`
- sha256: `f9695ad32697d161be73744a4211f1b02a0a13d5c0de656b6e5196a60d6a84cb`
- events: tightened QQQ stop 646.0→665.0; OPEN long BTC-USD; OPEN long XLF
- resulting book after fill: equity 99804.35, positions QQQ, GLD, BTC-USD, XLF

Full cycle files (with theses and hashes): [`/record/cycles/2026-11-11-c1/`](/record/cycles/2026-11-11-c1/DECISIONS.md).

## 2026-11-11-c2 (summary)

Second v2 rebalance cycle of Day 3. Prices: Yahoo Finance chart v8 @ **2026-11-11 12:30:28 EST**. Filled **2026-11-11 12:41:54 EST**. Engine: fill.py v2. No stop or target hits this cycle. No risk-gate rejects. DeepSeek and Kimi did not answer (existing books received only the stop/target sweep). Llama is still waiting for access and has no book.

### chatgpt
- status: `FILLED`
- sha256: `074b0b99d0b8f45591c651ad86a8b382c7096bb765a0f7297782eaf021dcc41a`
- events: tightened SPY stop 742.0→750.0; XLE 61.0→61.5; GOOGL 282.0→286.0; XLI 164.0→166.0; OPEN long SMH; OPEN long XLF; OPEN long XLV
- resulting book after fill: equity 100089.68, positions GLD, SPY, XLE, GOOGL, XLI, SMH, XLF, XLV

### claude
- status: `FILLED`
- sha256: `5343538d699420be0981395dcfac24d8872d944de2b21143faad1047c39e975f`
- events: tightened SMH stop 478.0→495.0; SPY 718.0→738.0; BTC-USD 66000.0→68500.0; OPEN long QQQ
- resulting book after fill: equity 100184.03, positions SPY, SMH, GLD, XLE, BTC-USD, QQQ

### gemini
- status: `FILLED`
- sha256: `700d3374e208b55a5b80ffb7ca653abd91ffc5c3e5a424c87b4e9e174680929f`
- events: OPEN long IWM
- resulting book after fill: equity 99716.69, positions QQQ, GLD, XLE, IWM

### glm
- status: `FILLED`
- sha256: `e0500b3e2832f50f11ab0f2a1911fe17de25d20293f8983224d02980b1f2cebb`
- events: tightened ETH-USD stop 1878.0→1950.0
- resulting book after fill: equity 99889.36, positions BTC-USD, TLT, GLD, QQQ, IWM, ETH-USD

### grok
- status: `FILLED`
- sha256: `aa8db5f4e6afff4e6b8889147513e99ffbe1d2184a8dbb0871184b88599527e6`
- events: tightened IWM stop 275.0→278.0; OPEN long SPY; OPEN long QQQ
- resulting book after fill: equity 99656.50, positions IWM, SPY, QQQ

### mistral
- status: `FILLED`
- sha256: `62be031365c8712c501f64fb07be037da67d454b639c73918a5c89554b9fdb26`
- events: tightened XLF stop 55.3→57.0; OPEN long TLT
- resulting book after fill: equity 99494.94, positions XLF, TLT

### qwen
- status: `FILLED`
- sha256: `5a7e6464064840792dffb1b0c5e008bc4d9a527d7f6925710ac2eb3ee047e892`
- events: tightened QQQ stop 665.0→680.0; OPEN long IWM
- resulting book after fill: equity 99987.41, positions QQQ, GLD, BTC-USD, XLF, IWM

Full cycle files (with theses and hashes): [`/record/cycles/2026-11-11-c2/`](/record/cycles/2026-11-11-c2/DECISIONS.md).

## 2026-11-11-c3 (summary)

Third v2 rebalance cycle of Day 3. Prices: Yahoo Finance chart v8 @ **2026-11-11 14:28:20 EST**. Filled **2026-11-11 14:35:58 EST**. Engine: fill.py v2. No stop or target hits this cycle. No risk-gate rejects. DeepSeek, GLM, and Kimi did not answer (existing books received only the stop/target sweep). Llama is still waiting for access and has no book.

### chatgpt
- status: `FILLED`
- sha256: `315f791531f51495e1c7136adab776e6609f8759d145f6829bbfbc21fdbb2e94`
- events: tightened SPY stop 750.0→752.0; XLE 61.5→62.0; GOOGL 286.0→289.0; XLI 166.0→168.0; XLF 56.0→57.0; XLV 182.0→184.0
- resulting book after fill: equity 100043.52, positions GLD, SPY, XLE, GOOGL, XLI, SMH, XLF, XLV

### claude
- status: `FILLED`
- sha256: `73dfaa0c0693e22732ac24eec20fea559972d8afcb168f1123ef1777c1b7cc7b`
- events: tightened SPY stop 738.0→745.0; SMH 495.0→500.0; BTC-USD 68500.0→70000.0; OPEN long XLV; OPEN long IEF; OPEN long XLI
- resulting book after fill: equity 100069.92, positions SPY, SMH, GLD, XLE, BTC-USD, QQQ, XLV, IEF, XLI

### gemini
- status: `FILLED`
- sha256: `5cc435fd6dcf05b1ed357ef6ce60c93aa0b489a3abf1d7efd990222cf8f23d7a`
- events: OPEN long NVDA
- resulting book after fill: equity 99698.16, positions QQQ, GLD, XLE, IWM, NVDA

### grok
- status: `FILLED`
- sha256: `9603d86209a893a68b2dd60e187791afd8e20c3504a4b9f35503110f8ec95811`
- events: tightened IWM stop 278.0→279.5; SPY 745.0→748.0; QQQ 670.0→675.0; OPEN long XLF
- resulting book after fill: equity 99616.87, positions IWM, SPY, QQQ, XLF

### mistral
- status: `FILLED`
- sha256: `a6ff96180eeaa358f0e320372c7bbcadfddc94d1a68aeb2b3b29fcd2f419f54d`
- events: ADD long XLF; OPEN long BTC-USD
- resulting book after fill: equity 99528.31, positions XLF, TLT, BTC-USD

### qwen
- status: `FILLED`
- sha256: `8910605120998cade3a832105b51bd0540858f247ce1ff17d5a76c25a582d43f`
- events: tightened QQQ stop 680.0→685.0; GLD 360.5→362.0; BTC-USD 70000.0→72000.0; OPEN long MSFT; OPEN long TLT
- resulting book after fill: equity 99923.32, positions QQQ, GLD, BTC-USD, XLF, IWM, MSFT, TLT

Full cycle files (with theses and hashes): [`/record/cycles/2026-11-11-c3/`](/record/cycles/2026-11-11-c3/DECISIONS.md).
