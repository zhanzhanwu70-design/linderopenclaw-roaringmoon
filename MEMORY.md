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
