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

## Promoted From Short-Term Memory (2026-06-27)

<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1206.md:21:21 -->
- Conversation Summary: **Demand 佇列（需裁決）** [score=0.857 recalls=0 avg=0.620 source=memory/2026-06-23-1206.md:21-21]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1206.md:13:13 -->
- Conversation Summary: **任務狀態（需要關注）** [score=0.844 recalls=0 avg=0.620 source=memory/2026-06-23-1206.md:13-13]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1206.md:19:19 -->
- Conversation Summary: | `task_20260531_001/002` problem-solver-workflow skill 審查 | ✅ `accepted`+`completed` | 已完成，狀態需归档为 `done` 而非持续 `accepted` | [score=0.824 recalls=0 avg=0.620 source=memory/2026-06-23-1206.md:19-19]

## Promoted From Short-Term Memory (2026-06-28)

<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1654.md:22:22 -->
- Conversation Summary: **原因：** Gateway 重啟是基礎設施層級的事件，我的 session 不會自動收到通知。Session 繼續從上次的地方運作，只有在我主動去查（如 `openclaw plugins list`）或某個操作失敗時才會察覺。 [score=0.857 recalls=0 avg=0.620 source=memory/2026-06-23-1654.md:22-22]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1206.md:15:18 -->
- Conversation Summary: | Task | 狀態 | 說明 | |---|---|---| | `task_20260527_005` 台北租屋搜尋 | ⚠️ `accepted` 但 `run_count=3` + `completed_at` 已設定 | **需確認是否真正持續運行** — mrmime 已執行 3 次，但任務標記為 ongoing，無新的 `last_check_at` 更新 | | `task_20260609_001` Sensor Fusion 每日研究 | 🔴 `pending` | 創建後從未執行（`run_count=0`），已 ongoing 超過 2 週，**rowlet 可能未接手** | [score=0.853 recalls=0 avg=0.620 source=memory/2026-06-23-1206.md:15-18]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1206.md:23:25 -->
- Conversation Summary: | Demand | 狀態 | 說明 | |---|---|---| | `DEM_20260623_012646_charizard_upstream_tracker_path_audit` | 🟡 `pending` | **需要 CEO（我）審核** — 關於 upstream tracker 路徑 audit，指派給 `ceo`，今天建立 | [score=0.853 recalls=0 avg=0.620 source=memory/2026-06-23-1206.md:23-25]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1206.md:3:5 -->
- Session: 2026-06-23 12:06:46 UTC: **Session Key**: agent:roaringmoon:discord:channel:1482561255955763293; **Session ID**: 45104436-0c0e-49b2-b26d-a56c77d631e4; **Source**: discord [score=0.853 recalls=0 avg=0.620 source=memory/2026-06-23-1206.md:3-5]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1206.md:9:9 -->
- Conversation Summary: assistant: **🪝 TaskFlow / 佇列回報（2026-06-23）** [score=0.853 recalls=0 avg=0.620 source=memory/2026-06-23-1206.md:9-9]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1654.md:12:12 -->
- Conversation Summary: Gateway 已重啟，TaskFlow 功能正常運作。 [score=0.847 recalls=0 avg=0.620 source=memory/2026-06-23-1654.md:12-12]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1654.md:3:5 -->
- Session: 2026-06-23 16:54:06 UTC: **Session Key**: agent:roaringmoon:discord:channel:1482561255955763293; **Session ID**: d0ce91c9-0b5f-47fa-8b84-0d6a0cae1079; **Source**: discord [score=0.847 recalls=0 avg=0.620 source=memory/2026-06-23-1654.md:3-5]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1654.md:9:10 -->
- Conversation Summary: user: 我已經重啟 assistant: **taskflow-tools 已成功載入 ✅** [score=0.847 recalls=0 avg=0.620 source=memory/2026-06-23-1654.md:9-10]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1206.md:29:29 -->
- Conversation Summary: **主要阻塞點** [score=0.843 recalls=0 avg=0.620 source=memory/2026-06-23-1206.md:29-29]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23-1654.md:14:14 -->
- Conversation Summary: 目前有 4 個 TaskFlow： [score=0.837 recalls=0 avg=0.620 source=memory/2026-06-23-1654.md:14-14]
