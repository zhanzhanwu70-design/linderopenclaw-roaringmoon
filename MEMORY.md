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
- **路徑：** `/home/node/.openclaw/workspace/llm-wiki/raw/code/elle_ws/`
- **Ouroboros 結構：** raw/ repos/ graphify/ wiki/ spec/
- **現況：**
  - ✅ raw/ 完成
  - ⚠️ repos/ 5 個 repo 框架已建（但只在 bringup 有實質內容）
  - ⚠️ wiki/ 部分完成
  - ❌ spec/ 完全空白

## Key Decisions

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
- **Source：** `/home/node/.openclaw/workspace/llm-wiki/raw/code/nemoclaw-nvidia/`
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

## Promoted From Short-Term Memory (2026-06-30)

<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1206.md:31:32 -->
- Conversation Summary: **Sensor Fusion 每日研究 (`task_20260609_001`) 卡住** — `run_count=0` 顯示從未被執行，需確認 rowlet 是否收到任務; **`task_20260527_005` 狀態不一致** — 已完成但 ongoing flag 未清除，可能影響 mrmime 的後續排程 [score=0.901 recalls=0 avg=0.620 source=memory/2026-06-23-1206.md:31-32]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1206.md:34:34 -->
- Conversation Summary: **無需關注的已完成任務（建議 archive）** [score=0.901 recalls=0 avg=0.620 source=memory/2026-06-23-1206.md:34-34]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1654.md:25:27 -->
- Conversation Summary: 查詢 `openclaw plugins list` 確認 plugin 狀態; 查詢 `openclaw tasks flow list` 確認 TaskFlow 是否正常; 主動告訴 Linder 已確認重啟完成 [score=0.872 recalls=0 avg=0.620 source=memory/2026-06-23-1654.md:25-27]
<!-- openclaw-memory-promotion:memory:memory/2026-06-24-0352.md:27:28 -->
- 客戶交付流程: docker save 成 .tar.gz; 客戶 docker load + docker run [score=0.862 recalls=0 avg=0.620 source=memory/2026-06-24-0352.md:27-28]
<!-- openclaw-memory-promotion:memory:memory/2026-06-24-0352.md:32:34 -->
- smolagents 討論: Hugging Face 輕量 Agent 框架; 可考慮 smolagents + NemoClaw 組合; 但 NemoClaw 已內建 Agent（OpenClaw/Hermes） [score=0.862 recalls=0 avg=0.620 source=memory/2026-06-24-0352.md:32-34]
<!-- openclaw-memory-promotion:memory:memory/2026-06-24-0352.md:37:39 -->
- 待確認: 設備到位後開始實作; 模型大小（影響是否一起包進 Image）; 客戶主機規格（決定 GPU 分配方式） [score=0.862 recalls=0 avg=0.620 source=memory/2026-06-24-0352.md:37-39]
<!-- openclaw-memory-promotion:memory:memory/2026-06-24-0352.md:6:7 -->
- NemoClaw 研究: **下載並整理：** Source → `llm-wiki/raw/code/nemoclaw-nvidia/`; **Wiki 條目：** `wiki/entities/nemoclaw.md`, `wiki/concepts/distributed-gpu-agent-with-nemoclaw.md` [score=0.862 recalls=0 avg=0.620 source=memory/2026-06-24-0352.md:6-7]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1654.md:29:32 -->
- Conversation Summary: 這次你告訴我已重啟，我才去查。以後我應該在懷疑 gateway 可能重啟時，主動查詢確認。 assistant: 已通知 gengar：這是 Linder 15:33 UTC 指示的清理行動，不是異常。任務佇列已完全移除。 assistant: HEARTBEAT_OK assistant: HEARTBEAT_OK [score=0.840 recalls=0 avg=0.620 source=memory/2026-06-23-1654.md:29-32]
<!-- openclaw-memory-promotion:memory:memory/2026-06-21.md:17:20 -->
- Top 10 Overall (Open LLM Leaderboard): | 7 | MaziyarPanahi/calme-2.1-qwen2.5-72b | 47.86 | 86.62 | 61.66 | 59.14 | 15.10 | 13.30 | 51.32 | 73B | | 8 | newsbang/Homer-v1.0-Qwen2.5-72B | 47.46 | 76.28 | 62.27 | 49.02 | 22.15 | 17.90 | 57.17 | 73B | | 9 | ehristoforu/qwen2.5-test-32b-it | 47.37 | 78.89 | 58.28 | 59.74 | 15.21 | 19.13 | 52.95 | 33B | | 10 | Saxo/Linkbricks-Horizon-AI-Avengers-V1-32B | 47.34 | 79.72 | 57.63 | 60.27 | 14.99 | 18.16 | 53.25 | 33B | [score=0.824 recalls=0 avg=0.620 source=memory/2026-06-21.md:17-20]
<!-- openclaw-memory-promotion:memory:memory/2026-06-21.md:25:27 -->
- Reasoning (BBH): qingy2024/Benchmaxx-Llama-3.2-1B-Instruct: 76.70; JungZoona/T3Q-Qwen2.5-14B-Instruct-1M-e3: 65.47; JungZoona/T3Q-qwen2.5-14b-v1.0-e3: 65.47 [score=0.824 recalls=0 avg=0.620 source=memory/2026-06-21.md:25-27]

## Promoted From Short-Term Memory (2026-07-01)

<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:18:18 -->
- Native Ollama Provider 支援 (`be8112f`): **架構關鍵點**： [score=0.825 recalls=0 avg=0.620 source=memory/2026-06-27.md:18-18]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:20:23 -->
- Native Ollama Provider 支援 (`be8112f`): // openai_compat.rs 新增 pub const OLLAMA_CONFIG: OpenAiCompatConfig = OpenAiCompatConfig { provider_name: "Ollama", api_key_env: "OLLAMA_HOST", [score=0.825 recalls=0 avg=0.620 source=memory/2026-06-27.md:20-23]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:24:26 -->
- Native Ollama Provider 支援 (`be8112f`): base_url_env: "OLLAMA_HOST", default_base_url: "http://127.0.0.1:11434/v1", max_request_body_bytes: 104_857_600, [score=0.825 recalls=0 avg=0.620 source=memory/2026-06-27.md:24-26]
<!-- openclaw-memory-promotion:memory:memory/2026-06-21.md:30:32 -->
- Math (MATH Lvl 5): nvidia/AceMath-72B-Instruct: 71.45; nvidia/AceMath-7B-Instruct: 63.37; nvidia/AceInstruct-72B: 62.61 [score=0.816 recalls=0 avg=0.620 source=memory/2026-06-21.md:30-32]
<!-- openclaw-memory-promotion:memory:memory/2026-06-21.md:9:12 -->
- Top 10 Overall (Open LLM Leaderboard): | Rank | Model | Average | IFEval | BBH | MATH | GPQA | MUSR | MMLU-PRO | Params | |------|-------|---------|--------|-----|------|------|------|----------|--------| | 1 | MaziyarPanahi/calme-3.2-instruct-78b | 52.08 | 80.63 | 62.61 | 40.33 | 20.36 | 38.53 | 70.03 | 78B | | 2 | MaziyarPanahi/calme-3.1-instruct-78b | 51.29 | 81.36 | 62.41 | 39.27 | 19.46 | 36.50 | 68.72 | 78B | [score=0.816 recalls=0 avg=0.620 source=memory/2026-06-21.md:9-12]

## Promoted From Short-Term Memory (2026-07-02)

<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:13:16 -->
- Native Ollama Provider 支援 (`be8112f`): 透過 `OLLAMA_HOST` 環境變數直接支援本地 Ollama; 最高優先級 provider 檢測（早於 OPENAI_BASE_URL）; 無需 API key（使用 placeholder token）; 模型名稱如 `qwen3:8b` 可繞過嚴格 provider/model 語法驗證 [score=0.861 recalls=0 avg=0.620 source=memory/2026-06-27.md:13-16]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:29:29 -->
- Native Ollama Provider 支援 (`be8112f`): pub fn from_ollama_env() -> Option<Self> { ... } [score=0.861 recalls=0 avg=0.620 source=memory/2026-06-27.md:29-29]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:33:36 -->
- Setup Wizard 入口點 (`3845040`): 新增 `/setup` slash command; 新增 `claw setup` CLI subcommand; 新增 `RuntimeProviderConfig` struct（kind, apiKey, baseUrl, model）; 三層 provider 配置解析：環境變數 > .env > settings.json [score=0.861 recalls=0 avg=0.620 source=memory/2026-06-27.md:33-36]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:39:41 -->
- 路徑驗證安全改進 (`eb21179`): Python `path_scope.py` 新增 redirection operator 剝離; 防止 `>file.txt` 或 `2>&1` 等 redirection 被誤認為路徑; 正則：`^(?:\d*)?(?:<>|>>?|<)(.+)$|^&>>?(.+)$` [score=0.861 recalls=0 avg=0.620 source=memory/2026-06-27.md:39-41]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:44:45 -->
- 命令查詢正規化 (`5babda1`): 改善 command lookup normalization; 修復 `src/commands.py` 和 `test_porting_workspace.py` [score=0.861 recalls=0 avg=0.620 source=memory/2026-06-27.md:44-45]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:48:48 -->
- 眾多 ROADMAP 項目關閉: 大量 ROADMAP 項目被標記為 DONE，包括： [score=0.856 recalls=0 avg=0.620 source=memory/2026-06-27.md:48-48]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:5:6 -->
- upstream/main 新 commits 概覽: 共 **1549 個新 commits**（上次研究後的累積）; 涵蓋時間：從 2026-06-05 到 2026-06-27 [score=0.856 recalls=0 avg=0.620 source=memory/2026-06-27.md:5-6]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:61:64 -->
- Commands 模組 (Rust): `SlashCommandSpec` 靜態定義所有 slash commands; `SlashCommand` enum 完整列舉所有命令變體; 統一解析入口 `SlashCommand::parse(input: &str)`; 每個命令有 `resume_supported` 標記 [score=0.825 recalls=0 avg=0.620 source=memory/2026-06-27.md:61-64]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:77:79 -->
- Config 層級: RuntimeConfig (Rust) → RuntimeFeatureConfig → RuntimeProviderConfig (新增) [score=0.825 recalls=0 avg=0.620 source=memory/2026-06-27.md:77-79]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:80:83 -->
- Config 層級: kind: Option<String>; api_key: Option<String>; base_url: Option<String>; model: Option<String> [score=0.825 recalls=0 avg=0.620 source=memory/2026-06-27.md:80-83]
