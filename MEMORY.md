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

## Promoted From Short-Term Memory (2026-07-25)

<!-- openclaw-memory-promotion:memory:memory/2026-07-18.md:12:15 -->
- AI Model Rankings — 2026-07-17（from cron agent）: 🥇 Claude Mythos 5 — 64.5%; 🥈 Claude Opus 4.8 — 57.9%; 🥉 Claude Sonnet 5 — 57.4%; 4. GLM 5.2 — 54.7% [score=0.850 recalls=0 avg=0.620 source=memory/2026-07-18.md:12-15]
<!-- openclaw-memory-promotion:memory:memory/2026-07-18.md:16:16 -->
- AI Model Rankings — 2026-07-17（from cron agent）: 5. Kimi K2.6 — 54.0% [score=0.850 recalls=0 avg=0.620 source=memory/2026-07-18.md:16-16]
<!-- openclaw-memory-promotion:memory:memory/2026-07-18.md:19:22 -->
- AI Model Rankings — 2026-07-17（from cron agent）: **Agent coding (SWE-Bench)**: Claude Mythos 5 — 95.5%; **Computer operation (OSWorld)**: Claude Fable 5 — 85%; **Web browsing (BrowseComp)**: Claude Fable 5 — 88%; **Terminal (Terminal-Bench 2.1)**: Claude Mythos 5 — 88% [score=0.850 recalls=0 avg=0.620 source=memory/2026-07-18.md:19-22]

## Promoted From Short-Term Memory (2026-07-26)

<!-- openclaw-memory-promotion:memory:memory/2026-07-18.md:18:18 -->
- AI Model Rankings — 2026-07-17（from cron agent）: Notable per-domain: [score=0.831 recalls=0 avg=0.620 source=memory/2026-07-18.md:18-18]
<!-- openclaw-memory-promotion:memory:memory/2026-07-18.md:24:25 -->
- AI Model Rankings — 2026-07-17（from cron agent）: Speed king: Llama 4 Scout — 2600 t/s Best value: Nova Micro — $0.04/$0.14 per 1M tokens [score=0.831 recalls=0 avg=0.620 source=memory/2026-07-18.md:24-25]
<!-- openclaw-memory-promotion:memory:memory/2026-07-18.md:9:9 -->
- AI Model Rankings — 2026-07-17（from cron agent）: Source: Vellum LLM Leaderboard + Artificial Analysis [score=0.831 recalls=0 avg=0.620 source=memory/2026-07-18.md:9-9]

## Promoted From Short-Term Memory (2026-07-27)

<!-- openclaw-memory-promotion:memory:memory/2026-07-21.md:23:23 -->
- AI Model Rankings — 2026-07-21（from cron agent）: **開源 Top 5（Open Weights）:** [score=0.894 recalls=0 avg=0.620 source=memory/2026-07-21.md:23-23]
<!-- openclaw-memory-promotion:memory:memory/2026-07-21.md:6:6 -->
- AI Model Rankings — 2026-07-21（from cron agent）: **🏆 Top 10 Overall (Intelligence Index)** [score=0.894 recalls=0 avg=0.620 source=memory/2026-07-21.md:6-6]
<!-- openclaw-memory-promotion:memory:memory/2026-07-21.md:11:14 -->
- AI Model Rankings — 2026-07-21（from cron agent）: GPT-5.6 Terra — 55.0 (II), 76.7 (CI), 47.4 (AI) ▲2; GPT-5.5 — 54.8 (II), 74.9 (CI), 44.9 (AI) ▼1; Grok 4.5 — 53.8 (II), 72.4 (CI), 45.7 (AI) ▲1; Claude Opus 4.7 — 53.5 (II), 73.6 (CI), 44.4 (AI) ▼2 [score=0.868 recalls=0 avg=0.620 source=memory/2026-07-21.md:11-14]
<!-- openclaw-memory-promotion:memory:memory/2026-07-21.md:15:16 -->
- AI Model Rankings — 2026-07-21（from cron agent）: Claude Sonnet 5 — 53.4 (II), 71.5 (CI), 46.7 (AI) ▲1; GPT-5.4 — 51.4 (II), 71.1 (CI), 41.1 (AI) ▼1 [score=0.868 recalls=0 avg=0.620 source=memory/2026-07-21.md:15-16]
<!-- openclaw-memory-promotion:memory:memory/2026-07-21.md:19:21 -->
- AI Model Rankings — 2026-07-21（from cron agent）: 💻 Coding (CI): GPT-5.6 Sol — 77.4; 🤖 Agent (AI): GPT-5.6 Sol — 54.0; 🎨 Design Arena: Kimi K3（3D/UI/網站）, Claude Fable 5（網頁 Apps/Godot） [score=0.868 recalls=0 avg=0.620 source=memory/2026-07-21.md:19-21]
<!-- openclaw-memory-promotion:memory:memory/2026-07-21.md:24:27 -->
- AI Model Rankings — 2026-07-21（from cron agent）: GLM 5.2 — 51.1 (II), 68.8 (CI), 43.1 (AI); DeepSeek V4 Pro — 44.3 (II), 59.4 (CI), 36.4 (AI); MiniMax M3 — 44.4 (II), 58.6 (CI), 35.4 (AI); Kimi K2.6 — 44.2 (II), 61.8 (CI), 30.3 (AI) [score=0.862 recalls=0 avg=0.620 source=memory/2026-07-21.md:24-27]
<!-- openclaw-memory-promotion:memory:memory/2026-07-21.md:28:28 -->
- AI Model Rankings — 2026-07-21（from cron agent）: Tencent Hy3 preview — 41.2 (II), 58.8 (CI), 30.7 (AI) [score=0.862 recalls=0 avg=0.620 source=memory/2026-07-21.md:28-28]
<!-- openclaw-memory-promotion:memory:memory/2026-07-21.md:31:34 -->
- AI Model Rankings — 2026-07-21（from cron agent）: Meituan LongCat 2.0 — 1.6T MoE（480億激活）, 1M 上下文, 極低價; Thinking Machines Inkling — 9750億 MoE, 多模態代理; GPT-5.6 Sol — 新旗艦推理模型，CI/AI 雙冠; Claude Fable 5 — 總排名第一，Design Arena 大滿貫 [score=0.862 recalls=0 avg=0.620 source=memory/2026-07-21.md:31-34]
<!-- openclaw-memory-promotion:memory:memory/2026-07-21.md:37:40 -->
- Inter-session Messages: 04:31 UTC: Harness smoke test (roaringmoon 4) — OPENCLAW_ROARINGMOON_OK_4; 04:35 UTC: Harness retry test (roaringmoon retry) — OPENCLAW_ROARINGMOON_OK_RETRY_1; 04:26 UTC: Harness smoke test (roaringmoon 2) — OPENCLAW_ROARINGMOON_OK_2; 21:27 UTC: Harness full-token-test — OPENCLAW_BRIDGE_OK [score=0.862 recalls=0 avg=0.620 source=memory/2026-07-21.md:37-40]
<!-- openclaw-memory-promotion:memory:memory/2026-07-21.md:4:4 -->
- AI Model Rankings — 2026-07-21（from cron agent）: Source: OpenRouter × Artificial Analysis Intelligence Index v4.1 [score=0.862 recalls=0 avg=0.620 source=memory/2026-07-21.md:4-4]

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
