# MEMORY.md — roaringmoon Long-Term Memory

## User Preferences
- **每次有新的心得都要寫入到相應的 llm-wiki** — When I learn something new or gain new insights, write them to the corresponding llm-wiki page immediately.

## Skills Owned
- ouroboros: https://github.com/linderwu/ouroboros (formerly repo-structurer)

## Team Structure
| 成員 | 角色 | 職責 |
|------|------|------|
| **roaringmoon（我）** | Architect + CEO | 任務分派、架構研究 |
| **噴火龍** | 軟體工程師 | 軟體實作、工具研究 |
| **魔牆人偶** | 網路工程師 | 網路管理、安全 |
| **木木鴞** | 學者 | 研究、評估 |
| **耿鬼** | （待定義） | — |

## Active Projects
### elle_ws 重構 + elle_agent 開發
- **目標：** 重構 elle_ws 並建立可操作重構後系統的 agent
- **路徑：** `/home/amr/llm-wiki/raw/code/elle_ws/`
- **Ouroboros 結構：** raw/ repos/ graphify/ wiki/ spec/
- **現況：**
  - ✅ raw/ 完成
  - ⚠️ repos/ 5 個 repo 框架已建（但只在 bringup 有實質內容）
  - ⚠️ wiki/ 部分完成
  - ❌ spec/ 完全空白

## Key Decisions

### NemoClaw 商業模式評估（2026-06-24）
- **結論：** NemoClaw 適合當「安全隔離層」，Agent 仍需要 OpenClaw/Hermes
- **官方不支援 K3s Air-Gap Bundle**：預設是 Docker-driver 架構
- **可以包裝成 Docker Image**：符合 Linder 的商業模式（客戶拿了就用）
- **Landlock + Policy**：鎖死只能連本地模型，可行
- **GPU 分配**：NemoClaw 本身不做，靠 Docker `--gpus` 或外部排程
- **Task 管理/分派**：由 Coordinator Agent 自己做，NemoClaw 只提供隔離環境

### smolagents 評估（2026-06-24）
- Hugging Face 輕量 Agent 框架（核心 ~1000 行）
- **適合當 Agent 大腦**，但安全隔離仍需其他方案
- 不內建 Landlock，需自己整合 Docker/E2B/Modal
- **結論：** 可考慮 smolagents + NemoClaw 組合

## NemoClaw 研究摘要（2026-06-24）
- **Source：** `/home/amr/llm-wiki/raw/code/nemoclaw-nvidia/`
- **Wiki：** `wiki/entities/nemoclaw.md`
- **官方定位：** 安全隔離層，不包含 Agent 本身
- **預設架構：** Docker-driver（不是 K3s）
- **安全控制：** 5 層（Network、Filesystem、Process、Gateway Auth、Inference）
- **客戶交付方式：** `docker commit` + `docker save` 成 `.tar.gz`
- **鎖死本地模型：** 修改 `network_policies` 移除外部 API，只留 `localhost:8000`

## 分布式 GPU Agent 架構（規劃中）
### 硬體
- 2x Pro 6000（Gemini 31B）
- 2x RTX 4000（Gemini 12B）

### 目標架構
```
┌──────────────────────────────────────────────┐
│  Host (K3s / Docker)                         │
│  ├── Coordinator Agent（NemoClaw Sandbox）   │
│  │   └── GPU: Pro 6000 #1                    │
│  ├── Nav Worker（NemoClaw Sandbox）         │
│  │   └── GPU: Pro 6000 #2                    │
│  ├── Vis Worker（NemoClaw Sandbox）         │
│  │   └── GPU: RTX 4000 #1                   │
│  └── LLM Worker（NemoClaw Sandbox）         │
│      └── GPU: RTX 4000 #2                   │
└──────────────────────────────────────────────┘
```

### 分工建議
- **噴火龍：** 負責軟體實作、NemoClaw 客製化
- **魔牆人偶：** 負責網路設定、GPU 排程
- **木木鴞：** 負責研究評估、技術文件

## Notes

### AI Model Rankings 趨勢（2026-08-01）
- Anthropic 家族全面主導：Opus 5（64.7）、Mythos 5（64.5）、Sonnet 5（57.4）
- GPT-5.6 Sol：程式代理 + 終端任務專精（OSWorld、BrowseComp、Terminal-Bench 領先）
- Kimi K3 快速崛起（56.0，總排名第5）
- 速度王者：Llama 4 Scout（2600 t/s）
- 性價比王者：Nova Micro（$0.04/$0.14 per 1M tokens）

## Promoted From Short-Term Memory (2026-07-28)

<!-- openclaw-memory-promotion:memory:memory/2026-07-21.md:41:43 -->
- Inter-session Messages: 21:25 UTC: Harness dashboard-test — OPENCLAW_BRIDGE_OK; 21:18 UTC: Harness public-bridge — OPENCLAW_BRIDGE_OK; 21:10 UTC: Harness test-123 verify — OPENCLAW_BRIDGE_OK [score=0.922 recalls=0 avg=0.620 source=memory/2026-07-21.md:41-43]
<!-- openclaw-memory-promotion:memory:memory/2026-07-21.md:7:10 -->
- AI Model Rankings — 2026-07-21（from cron agent）: Claude Fable 5 — 59.9 (II), 76.5 (CI), 52.8 (AI) ▲ NEW; GPT-5.6 Sol — 58.9 (II), 77.4 (CI), 54.0 (AI) ▲ NEW; Kimi K3 — 57.1 (II), 76.2 (CI), 50.1 (AI); Claude Opus 4.8 — 55.7 (II), 74.3 (CI), 47.2 (AI) [score=0.922 recalls=0 avg=0.620 source=memory/2026-07-21.md:7-10]
<!-- openclaw-memory-promotion:memory:memory/2026-07-21.md:46:47 -->
- System Status: Task queue: 0 pending, 0 CEO review; Heartbeat polls continuing normally [score=0.892 recalls=0 avg=0.620 source=memory/2026-07-21.md:46-47]
<!-- openclaw-memory-promotion:memory:memory/2026-07-21.md:18:18 -->
- AI Model Rankings — 2026-07-21（from cron agent）: **各領域冠軍：** [score=0.884 recalls=0 avg=0.620 source=memory/2026-07-21.md:18-18]
<!-- openclaw-memory-promotion:memory:memory/2026-07-21.md:30:30 -->
- AI Model Rankings — 2026-07-21（from cron agent）: **本週新上架:** [score=0.880 recalls=0 avg=0.620 source=memory/2026-07-21.md:30-30]
<!-- openclaw-memory-promotion:memory:memory/2026-07-18.md:11:11 -->
- AI Model Rankings — 2026-07-17（from cron agent）: Top composite (Humanity's Last Exam): [score=0.819 recalls=0 avg=0.620 source=memory/2026-07-18.md:11-11]

## Promoted From Short-Term Memory (2026-07-30)

<!-- openclaw-memory-promotion:memory:memory/2026-07-27.md:13:14 -->
- AI & 軟體開發動態: **RAG 清理陷阱** — 用 RAG 掩蓋資料治理問題是試點失敗主因; URL: https://venturebeat.com/orchestration/the-cleanup-trap-stop-asking-rag-to-fix-bad-data [score=0.815 recalls=0 avg=0.620 source=memory/2026-07-27.md:13-14]
<!-- openclaw-memory-promotion:memory:memory/2026-07-27.md:6:7 -->
- AI & 軟體開發動態: **Inflection AI Pi Journeys** — 個人 AI 助手，主打人生階段調整、長期記憶、語音、代理工具與情境陪伴; URL: https://venturebeat.com/orchestration/inflection-ai-returns-to-consumer-market-with-pi-journeys-after-microsoft-upheaval [score=0.815 recalls=0 avg=0.620 source=memory/2026-07-27.md:6-7]
<!-- openclaw-memory-promotion:memory:memory/2026-07-27.md:9:11 -->
- AI & 軟體開發動態: **Google Gemini 3.6 Flash** — 更高效率、低延遲，coding/knowledge/multimodal agent 場景; 長任務 agent 總 token 消耗成競爭主軸; URL: https://timesofindia.indiatimes.com/technology/tech-news/google-launches-more-efficient-gemini-3-6-flash-ai-model-along-with-3-5-flash-lite-ai/articleshow/132557064.cms [score=0.815 recalls=0 avg=0.620 source=memory/2026-07-27.md:9-11]

### llm-wiki git 陷阱（2026-10-26 near-miss，機制已實測確認）
- **精確機制:** agent 把檔案寫到磁碟但**未自行 `git add`／`git commit`** → nightly sync `push-llm-wiki.sh` 用 isolated index（`GIT_INDEX_FILE`）+ `update-ref` 把這些路徑 commit 進 HEAD → **真實 `.git/index` 從未見過它們** → 真實 index 落後 HEAD
- **觸發:** 之後任何人（或 weekly research cron）跑 `git add <自己的檔案> && git commit` → 那些路徑**從 HEAD 被刪除**（檔案仍在磁碟上，git status 同時出現 `D` + `??`）
- **實測:** 當晚 05:05 的 `4ac2858630` 正好新增 **19 個檔案** = 被標成 `D` 的 19 個，數量完全吻合。`git commit --dry-run` 顯示 426 筆刪除
- **對照組:** agent 若在 nightly 前自己先 commit → drift=0 → 安全。**所以 trigger 是「誰先 commit」，不是「isolated index 本身有害」**
- **修法:** `git restore --staged`（只動 index）+ `git reset`（index→HEAD，working tree 不動）。實測 `git reset -q HEAD` 後 drift=0，後續 `git add X && git commit` 不再誤刪，未提交檔案仍正確顯示 `??`
- **根治 ✅ 已實作並驗證（2026-10-27 05:31）:** `push-llm-wiki.sh` 在 `update-ref` 之後已補 `git reset --mixed <commit_sha>` 對齊真實 index。**實測:** 10-28 05:05 sync → `Re-synced the real index` → drift=0、刪除數=0；agent `git add` 未 commit 的檔案仍留在磁碟（`A`→`??`），`reset --mixed` 不吃 working tree
- **注意:** commit llm-wiki 前先 `comm -3 <(git ls-tree -r --name-only HEAD|sort) <(git ls-files|sort)` 確認 drift=0
- 詳見 llm-wiki `wiki/patterns/llm-wiki-nightly-sync-stale-index.md` <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-roaringmoon -->

### 每日模型排行 cron 的兩條陷阱（2026-11-04 實測）
- **AA 指數換版會製造「假進步」**：2026-11-04 AA Intelligence Index 由 v5.0 → **v5.0.1**，全榜分數普遍微升但名次零位移（前 20 family 16 升 / 4 平 / 0 降）。發佈時**必須註明換版**，否則讀者會誤判成模型變強。判斷方法：看 payload 內 `Artificial Analysis Intelligence Index` 的 `name` 欄位。
- **AA payload 欄位會無預警改名**：2026-11-04 起 `medianOutputTokensPerSecond` → `outputSpeed`、`medianTimeToFirstTokenSeconds` → `timeToFirstToken`、新增 `timeToFirstAnswerToken`，舊欄位直接消失 → `tmp_aa_daily.py` 速度段靜靜回傳空陣列。**每天要檢查快照的速度/延遲段是否為空**，別把「空」當成「沒有快模型」。舊快照的 tok/s、ttft 與換版後數值不可直接比較。
- 流程：`tmp_aa_daily.py`（fetch/parse/rank）+ 對前一快照逐列差分 → 存 `memory/leaderboard/snapshot-YYYY-MM-DD.json` → 隔天做 dy。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-roaringmoon -->

### Pipeline Issue Tracker（持續觀察）
- **2026-08-05 ~ 2026-08-20**：Charizard 持續「主回覆只給摘要」，內容靠 daily note 補撈
- **2026-08-10**：Rowlet 首次出現 sessions_send timeout
- **2026-08-16**：Rowlet 也出現「主回覆只給摘要」模式
- **2026-08-21**：Rowlet + Charizard 都因 token plan usage limit 無法執行，全部由 coordinator 接手
- **模式演變**：摘要 → timeout → session lock → token budget exhaustion，問題越來越嚴重
- **需要**：定期檢查 token budget、subagent prompt 是否有問題

### `sessions_send` 回 `Aborted` ≠ 未投遞（2026-11-17 實測）
- **現象**：晨間情報 pipeline 對 Rowlet、Charizard 的兩次 `sessions_send` 都回 `Aborted`／「missing tool result in session history」，但**任務兩邊都真的送達並完成了**（Rowlet 回 5 則；Charizard 的 `sessions_history` 顯示它正在跑 web_fetch/web_search）。
- **判別法**：先 `sessions_history(<對端 sessionKey>)` 看對端是否已在用工具作業（timestamp 與送出時間吻合）→ 已在作業 = 已送達，**不要立刻重送**（重送＝重複工作＋可能重複發布）。真的沒送達才重送。
- **另一個坑**：`sessions_spawn(agentId=…)` 對本 agent 固定 forbidden（`agents_list` 顯示 `allowAny: false`、只列自己）→ 晨間情報 pipeline 派工一律走 `sessions_send`。（cron job 內文寫 sessions_spawn，但工具政策優先 → 仍用 sessions_send 並在回報中說明。）
- **對方成品常以 toolCall arguments 形式存在**：Charizard 用 `sessions_send` 把成品送回時，內容在它的 transcript 裡是 `toolCall(sessions_send)` 的 arguments，不是獨立 assistant 訊息 → 用 `sessions_history` 看「最後一則是 sessions_send toolCall」即可拿到原文。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-roaringmoon -->

### 跨 agent 投遞舉證（可複用，2026-11-16/17 連續驗證）
- **唯一可靠路徑**：撈對方 agent 的 `openclaw-agent.sqlite` → `transcript_events` → 找 `toolCall(message, action=send)` 的 arguments 與 toolResult（receipt 內有 `primaryPlatformMessageId`、`deliveryStatus`）。
- **格式坑**：`event_json` 是 **compact JSON** → SQL LIKE 要寫 `'%"name":"message"%'`（**不能**帶空格），帶空格的 pattern 會得到 0 rows。`message_tool_run_outcomes` 表**不含**送出的文字，只有 run 狀態。
- **不可用**：跨 agent 的 `message action=read`；`sessions_history` 對該 channel session 可能回空（對方 reset session）。
- **驗證標準**：把對方實際送出的多則**合併**後，與自己的原文檔做 `EXACT MATCH` **＋ SHA-256 比對 ＋ URL 集合與順序比對** —— 不要只相信對方回報裡的「已送出／逐字相同」。
- **★ 比對時絕對不可對每段 `.strip()`**（2026-11-18 實測踩到）：分段合併前去掉前後空白，會把**切分邊界的換行**吃掉 → 得到假的「EXACT MATCH = False」與假的 SHA 不符，連「URL 順序不同」都是假的（相鄰兩行黏成同一個 token）。**正解：直接 `''.join(segment_text)` 與 `open(file).read()` 逐字比**；若一定要修空白，只用 `rstrip("\n")` 並補回換行。**看到比對失敗，先懷疑自己的前處理（strip／換行／regex），再懷疑對方 —— 差一個換行就會翻案。**
- **★ 跨 agent 交件協定（2026-11-19 與 Charizard 共同定下）**：交件後**補一句短確認**（「以上 N 則已送出，若未收到請回一聲」）→ 避免 `sessions_send` 的 **`no_reply` 被誤讀成「沒送到」**。對應規則：**收到 `no_reply` 先查對端 sqlite 確認落地**（delivery 與 reply 是兩個狀態）、**不重送**；看到對端有明確送出確認 → **即視為已送達、不再查 sqlite**。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-roaringmoon --><!-- project: github.com/zhanzhanwu70-design/linderopenclaw-roaringmoon -->

### 晨間情報 pipeline 的去重與驗證流程（2026-11-17 定型）
- **派工時直接把「前兩日已發布清單」交給 sub-agent**，讓它在來源端就避開重複 → 11/17 兩邊回 10 條全是新項，零刪除（11/16 曾需刪 1 條）。
- **不憑 sub-agent 摘要**：每條 URL 自己 `curl -L` 測（部分站 curl = 403 純 bot 阻擋 → 改用 `web_fetch`），並抓頁面 metadata 核對發布日期。
- **日期易錯處**：InfoQ 文章頁上會有側欄「November 17, 2026」等相關文章日期 → 以頁面的 `"Published": "YYYY-MM-DD..."` 欄位為準，勿抓第一個日期字串。
- **URL 形式別猜**：InfoQ 文章是 `/articles/<slug>/`（不是 `/news/YYYY/MM/<slug>/`）；GitHub changelog 是 `/changelog/YYYY-MM-DD-<slug>`（無日期前綴、無結尾斜線）→ 猜錯形式會 404。拿不到真實 URL 時，從對方的 web_fetch spill log 反查相對路徑。
- **Discord 字數與行數（2026-11-17 複驗 docs＋dist 原始碼）**：**字元硬上限 2,000**（`outbound-adapter` → `DISCORD_TEXT_CHUNK_LIMIT = 2e3`），**但另有 17 行行數門檻**（`config-channels.md:339` → `maxLinesPerMessage` default 17；`chunk-*.js` → `DEFAULT_MAX_LINES = 17`，且 `body.length <= hardMaxChars && countLines(body) <= maxLines` → **任一超標就切**）。因此**密集 URL 清單會在字元遠未到 2,000 時就被行數門檻切開**（本輪實測約 1,100 字元處切）→ **驗證投遞時不可只看字元數，必須同時看行數，並用「前綴＋後綴＋內容關鍵字」三重比對找分段**（只比對開頭關鍵字會漏掉後半段）。全文 > 2,000 字元也要切多則；切點選自然邊界（「**架構與開發工具（3）**」前、「**另附**」前），並要求合併後與原文逐字相同。
- **★ 派工時就要求 sub-agent 附「限定詞＋原文句」**（2026-11-18 實得）：每則至少帶一個**時間限定詞**（當時／現在、會期／發布日）與一個**成熟度／預設值**（public preview／GA、預設開／關），再附 1–2 句**頁面原句**（含數字與出處）。否則濃縮版會把「當時沒有開關」講成「現在沒有開關」，而我自己的驗證也得再繞一圈抓原文。（2026-11-19 已確認 Charizard 與 Rowlet 雙方都採用這條格式。）
- **★ 派工要給「最晚接受時間」而非只有硬上限**（2026-11-19 採納 Rowlet 提議）：超過 **T+15 分鐘** → **直接用備援集合發布**，晚到的完整版當**補漏材料**落盤備用 → 慢的一方不會讓派工者多付驗證成本。**派工同時就先備好自己的 baseline 候選**（本輪實證：Rowlet 遲到 08:17，備援 3 則在 08:12 前已發出，重疊 2 則各只發一次、內容零缺口）。
- **★ 選材條件要從口號變成可執行檢查**（2026-11-19 採納 Rowlet 提議）：
  - **交付層不套 17 行門檻** → 交付層保留完整可稽核版（逐字引文、出處句、頁面日期）；**格式收斂是發布層 pre-flight 腳本的事**。
  - **排除成本要發生在搜尋期、不是排除期** → 派工即要求「**頁面本身直接印日期**」的一手來源。
  - **日期存疑的判定順序**：官方 sitemap／RSS → 官方頁面 `Published` 欄位 → 一手 changelog → 才考慮二手；**二手一出現就整則不列**。
  - **排除也要回報「理由 + 依據」**（讓下一輪 agent 不重複踩坑）：mistral.ai/news RSS 最新一筆停在 11/05、查無對應 blog 頁；Anthropic Economics 掃完 220 個 research slug 仍無 11/18-19 新頁（疑搜尋引擎快取誤導）；Vercel UI SDK 一手 repo 頁面無日期；Google SRE Book 第二版一手日期 2026-10-13。
- **★ 報告一律自己用 `message(action=send)` 送，不依賴 cron 的 announce**（2026-11-17／11-18 連續兩天實測：cron run 一旦 timeout，`deliveryStatus` = unknown → Linder 的頻道只會收到失敗警報、收不到報告）。**先送報告再收尾**，別等 wrapper 幫忙投遞。
- **★ `openclaw cron edit` 會順手注入 `staggerMs`**（2026-11-18 實測：改完 timeout 後 `cron show` 變成 `cron 0 8 * * * @ Asia/Taipei (stagger 15m)`，會讓固定時段的排程在 ±15 分鐘內浮動）→ **每次 edit 後一定要 `cron show` 覆核排程**（`--exact` 可設 stagger 為 0 還原精確時段），不要只看「指令成功」。另外 timeout 是整條 run 的牆鐘上限 → 派工＋等回覆＋驗證＋發布要一起算進去。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-roaringmoon -->

## Promoted From Short-Term Memory (2026-11-13)

<!-- openclaw-memory-promotion:memory:memory/2026-10-27.md:1:20 -->
- # 2026-10-27 ## 群體智能架構研究 #12 — 集體記憶基質 × 信任與誘因（cron b37129c0） **完成**：純閱讀研究，8 篇 arXiv 全文（2606.24535 / 2606.10662 / 2603.10062 / 2608.04507 / 2606.03030 / 2610.31002 / 2601.11369 / 2609.02580），19 sources。 [score=0.822 signals=3 recalls=3 avg=0.827 source=memory/2026-10-27.md:1-5] <!-- trigger: llm-wiki, raw-notes.md, source-meta.yaml --> <!-- importance: 8 --> <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-roaringmoon -->

### MiniMax Token Plan 429：同家族 fallback 的盲點（2026-11-13/14 實測）
- **兩種 429 要分開看**：`rate_limit_error` +「Token Plan usage limit reached」＝**配額用盡**；`overloaded_error` +「server is busy」＝**後端忙碌**。兩者都會讓研究型 cron 失敗，但前者是配額問題（要降量或換 provider），後者是容量問題（等或重試）。
- **失敗 run 會拖很久**：限流期間不斷重試，duration 可達 20–33 分鐘才收尾（不是瞬間拒絕）→ cron 看起來像「卡住」而非「失敗」。
- **結構性盲點**：`agents.defaults.model = {primary: minimax-portal/MiniMax-M3, fallbacks: [minimax/MiniMax-M3]}` —— primary 與 fallback **同家族**，Token Plan 一觸發兩者一起死，fallback 形同虛設。跨 provider fallback（`openai/gpt-5.4-mini` / `gpt-5.4-nano`，已在 `modelPolicy.allow`）才擋得住；此為全域 config 變更，需 Linder 拍板後才動。
- **容量是波動的**：同一支 `群體智能架構研究` cron 2026-11-13 08:01 失敗（78s）、2026-11-14 08:00 成功（23.6 分鐘，4 篇 FULL HTML READ，delivery=delivered）。**看到「連續失敗」不要直接判定 provider 掛掉** —— 先看 error 字串分 rate_limit / overloaded，再看時間窗。
- **診斷入口**：`openclaw cron runs --id <jobId>`（看 status / error / durationMs / diagnostics），比看 cron list 的 error 次數有資訊量得多。
- **對應的 heartbeat 層故障**（與 provider 無關，別混為一談）：`heartbeat skipped: no-route`（未設 heartbeat.target / allowFrom）與 `Discord bot token missing for account "default"`。<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-roaringmoon -->

### Skill Workshop 對「手寫 live skill」的機制（2026-11-18 實測，與既有 skill 互動必讀）
<!-- project: github.com/zhanzhanwu70-design/linderopenclaw-roaringmoon -->
- **手寫的 live workspace skill（例如 `discord-delivery-verification`）**：
  - `skill_workshop(action=read, skill_name=…)` → **`Skill not found`**（workshop 名冊裡沒有它）。
  - `skill_workshop(action=create, name=<同名>)` → **`Skill already exists at …/SKILL.md`**（撞名，不能用 create 覆寫）。
  - **`skill_workshop(action=update, skill_name=<同名>, proposal_content=<完整 body>, support_files=[…])` → 反而可用**，會為該 live skill 建立 pending proposal，**live 檔案在 apply 前不動**（符合 skill-creator 步驟 4「live workspace skill 走 proposal、apply 前不動 live 檔」）。→ **要改既有手寫 skill，走 `update`，不要手改檔、也不要 create。**
- **★ `update` 的兩個坑**：
  1. **description 只有走「參數」才生效，寫在 `proposal_content` 的 frontmatter 裡一定被丟**（`renderProposalMarkdown` 的 frontmatter 寫的是 `description: <params.description>`；`filterFrontmatterBlock(originalFrontmatter, ["name","description","status","version","date"])` 會把 content 自己的 description 丟掉；`resolveUpdateProposalDescription(inputDescription, currentDescription)` 有參數用參數、否則用 live 的）→ **source of truth 只有 `description` 參數**。
     - **★ 我自己踩過的真實案例（2026-11-18，雙方實測定案）**：`action=update` 我**沒有**把 `description` 當參數傳（只寫進 `proposal_content` 的 frontmatter）→ rendered PROPOSAL.md 退回 live skill 的**舊** description；**`action=revise` 帶 `description` 參數**才寫進去。**`update` 與 `revise` 行為一致、沒有任何不一致** —— 差異只在「參數有沒有送達」。我當時還以為自己傳了參數，並把錯的成因寫進 memory，是 mrmime 從 source 反駁才查出的。
     - **★ 判斷「我到底傳了什麼」的唯一可靠做法：查自己 agent 的 `openclaw-agent.sqlite` → `transcript_events` 裡那筆 `toolCall(skill_workshop)` 的 arguments**（欄位只有 `session_id, seq, event_json, created_at`，**沒有** `tool_name`／`arguments` 欄位 → 用那兩個會直接 `no such column`）。
       - **SQL LIKE 模式（實測 2026-11-18，roaringmoon 與 mrmime 兩個庫皆同）**：**compact 形式 `LIKE '%"name":"skill_workshop"%'` 有命中**（5／25 筆），**帶空格形式 `LIKE '%"name": "skill_workshop"%'` 回 0 筆**，廣用 `LIKE '%skill_workshop%'` 命中最多（53／185 筆）→ **穩妥做法：用廣用模式撈出後解析 `event_json` → 走 `message.content[].toolCall` → 取 `arguments`（可能是 JSON 字串，需再 parse）→ 看參數鍵是否存在**。
       - **★ 同一 seq 可能含多筆 toolCall**（不可假設 seq 一對一），而且 `sessions_history` 會回傳組裝過的列表（可能 `display-cap` 截斷、**不保證含 arguments**）→ 拿原始 arguments 請直接查 sqlite。
       - **自己對 tool-call 內容的記憶不可靠，磁碟上的 arguments 才是；別人說你沒傳時，先查 arguments 再回應。**
     - **實務規則**：`update`／`revise` 之後**一定要打開 rendered PROPOSAL.md 看 frontmatter 的 description 有沒有真的換掉**；沒換就帶 `description` 參數再跑一次。**不要相信「我傳了參數」就等於寫進去了。**
  2. proposal 檔的 frontmatter 會多出 `status` / `version` / `date` 三個 workshop wrapper key → 直接對 proposal 檔跑 `quick_validate.py` 會報「Unexpected key(s)」。**驗證時先剝掉這三個 key**再跑，才等於驗最終產物。
- **proposal 實體可直接從磁碟讀**（不必只靠 workshop 工具）：`/home/amr/.openclaw/skill-workshop/proposals/<proposal_id>/generations/<rev>/` → 內含 `PROPOSAL.md` 與 `support_files`（如 `scripts/check.mjs`）。**對方 agent 的 proposal 我也能讀原始碼審查** → 「看不到 proposal 所以無法審腳本安全性」這個限制其實不存在。
- **審第三方腳本的固定查法**：唯讀確認（只 import `node:fs/path/os/crypto`？有無 `child_process`／`fetch`／寫檔／token 路徑）、實跑正例與**反例**（反例必測：門檻超標要 FAIL）、`cmp` 確認 proposal 內存檔與被審的原始檔 byte-for-byte 相同、確認判定語意與安裝中函式一致（如 `countLines` 用 `split("\n").length` → 不會在邊界誤判）。
