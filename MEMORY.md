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

## Promoted From Short-Term Memory (2026-06-29)

<!-- openclaw-memory-promotion:memory:memory/2026-06-21.md:35:37 -->
- Knowledge (MMLU-PRO): MaziyarPanahi/calme-3.2-instruct-78b: 70.03; MaziyarPanahi/calme-3.1-instruct-78b: 68.72; dfurman/CalmeRys-78B-Orpo-v0.1: 66.80 [score=0.865 recalls=0 avg=0.620 source=memory/2026-06-21.md:35-37]
<!-- openclaw-memory-promotion:memory:memory/2026-06-21.md:4:5 -->
- Data Sources: Open LLM Leaderboard (HuggingFace) - 4576 models; Artificial Analysis - AA-Omniscience & AA-Briefcase [score=0.865 recalls=0 avg=0.620 source=memory/2026-06-21.md:4-5]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1654.md:15:18 -->
- Conversation Summary: `ptcgp-meta-retry-0517` — succeeded; `learning-notes-corpus-synthesis` — succeeded; `graphify-claw-code` — succeeded; `Reply with exactly: OK...` — failed [score=0.847 recalls=0 avg=0.620 source=memory/2026-06-23-1654.md:15-18]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1654.md:19:20 -->
- Conversation Summary: user: 為何你認知不到自己被重啟這件是 assistant: 抱歉，這是我的認知盲點。 [score=0.847 recalls=0 avg=0.620 source=memory/2026-06-23-1654.md:19-20]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1654.md:24:24 -->
- Conversation Summary: ** Gateway 重啟後，我應該：** [score=0.837 recalls=0 avg=0.620 source=memory/2026-06-23-1654.md:24-24]
<!-- openclaw-memory-promotion:memory:memory/2026-06-24-0352.md:10:12 -->
- 商業模式評估: Linder 目前把 OpenCode 包成 Docker image 給客戶; 想轉移到 NemoClaw + K3s 包裝; **結論：** NemoClaw 原生就是 Docker，商業模式完全吻合 [score=0.837 recalls=0 avg=0.620 source=memory/2026-06-24-0352.md:10-12]
<!-- openclaw-memory-promotion:memory:memory/2026-06-24-0352.md:15:18 -->
- 技術關鍵點: **Landlock 安全機制** — NemoClaw 的核心價值; **鎖死本地模型** — 修改 `network_policies` 移除外部 API; **GPU 分配** — NemoClaw 不做，靠 Docker `--gpus` 或外部排程; **Task 分派** — 由 Coordinator Agent 自己用 `sessions_spawn`/`sessions_send` 做 [score=0.837 recalls=0 avg=0.620 source=memory/2026-06-24-0352.md:15-18]
<!-- openclaw-memory-promotion:memory:memory/2026-06-24-0352.md:19:19 -->
- 技術關鍵點: **K3s 包裝** — 官方不支援，但可用 Docker commit 方式 [score=0.837 recalls=0 avg=0.620 source=memory/2026-06-24-0352.md:19-19]
<!-- openclaw-memory-promotion:memory:memory/2026-06-24-0352.md:23:26 -->
- 客戶交付流程: 架好 NemoClaw Sandbox; 設定 Policy（只有本地模型）; shields up 鎖死 config; docker commit 成新 image [score=0.837 recalls=0 avg=0.620 source=memory/2026-06-24-0352.md:23-26]
<!-- openclaw-memory-promotion:memory:memory/2026-06-21.md:13:16 -->
- Top 10 Overall (Open LLM Leaderboard): | 3 | dfurman/CalmeRys-78B-Orpo-v0.1 | 51.23 | 81.63 | 61.92 | 40.63 | 20.02 | 36.37 | 66.80 | 78B | | 4 | MaziyarPanahi/calme-2.4-rys-78b | 50.77 | 80.11 | 62.16 | 40.71 | 20.36 | 34.57 | 66.69 | 78B | | 5 | huihui-ai/Qwen2.5-72B-Instruct-abliterated | 48.11 | 85.93 | 60.49 | 60.12 | 19.35 | 12.34 | 50.41 | 73B | | 6 | Qwen/Qwen2.5-72B-Instruct | 47.98 | 86.38 | 61.87 | 59.82 | 16.67 | 11.74 | 51.40 | 73B | [score=0.833 recalls=0 avg=0.620 source=memory/2026-06-21.md:13-16]

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
