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

## Promoted From Short-Term Memory (2026-07-03)

<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:49:50 -->
- 眾多 ROADMAP 項目關閉: #325, #330, #338, #339, #341, #342, #343, #344; 涵蓋 JSON contract stabilization、session resume、help system [score=0.853 recalls=0 avg=0.620 source=memory/2026-06-27.md:49-50]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:57:58 -->
- 雙語言架構: **Rust**: 核心 CLI、commands、runtime、API client; **Python**: 輔助工具、porting workspace infrastructure [score=0.853 recalls=0 avg=0.620 source=memory/2026-06-27.md:57-58]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:68:71 -->
- Provider 路由: detect_provider_kind() → OLLAMA_HOST (最高優先) → ANTHROPIC_API_KEY → OPENAI_API_KEY / OPENAI_BASE_URL [score=0.853 recalls=0 avg=0.620 source=memory/2026-06-27.md:68-71]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:90:93 -->
- 對 OpenClaw 整合的影響: **Ollama 支援增強**：可更自然地使用本地模型; **Provider 配置簡化**：三層解析減少環境設定複雜度; **安全改進**：redirection 路徑驗證防止 sandbox escape; **JSON contract 穩定化**：有利於程式化整合 [score=0.853 recalls=0 avg=0.620 source=memory/2026-06-27.md:90-93]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:98:100 -->
- 繼續研究重點: 深入 `runtime/src/config.rs` 的 provider 解析邏輯; 理解 `tools` crate 的 tool dispatch 機制; MCP server lifecycle 管理實作 [score=0.853 recalls=0 avg=0.620 source=memory/2026-06-27.md:98-100]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:72:72 -->
- Provider 路由: → 其他 provider... [score=0.813 recalls=0 avg=0.620 source=memory/2026-06-27.md:72-72]

## Promoted From Short-Term Memory (2026-07-07)

<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:13:13 -->
- OpenClaw Source Code 架構研究: **目錄結構重點：** [score=0.832 recalls=0 avg=0.620 source=memory/2026-07-03.md:13-13]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:18:18 -->
- OpenClaw Source Code 架構研究: `context-engine/` — System Prompt 組裝（SOUL/IDENTITY/USER/AGENTS 拼接） [score=0.832 recalls=0 avg=0.620 source=memory/2026-07-03.md:18-18]

## Promoted From Short-Term Memory (2026-07-08)

<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:14:17 -->
- OpenClaw Source Code 架構研究: `gateway/` — WebSocket 伺服器; `agents/` — Agent 執行引擎; `sessions/` — 對話狀態管理; `channels/` — Discord/Telegram/WhatsApp 接入 [score=0.900 recalls=0 avg=0.620 source=memory/2026-07-03.md:14-17]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:7:7 -->
- OpenClaw Source Code 架構研究: **建議閱讀順序：** [score=0.894 recalls=0 avg=0.620 source=memory/2026-07-03.md:7-7]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:8:11 -->
- OpenClaw Source Code 架構研究: `docs/concepts/agent-loop.md` — 核心工作流; `docs/concepts/architecture.md` — 整體架構; `docs/concepts/multi-agent.md` — 多 Agent 路由; Source: `gateway/server/` → `routing/` → `sessions/` → `agents/runtime/` → `context-engine/` [score=0.887 recalls=0 avg=0.620 source=memory/2026-07-03.md:8-11]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:25:25 -->
- OpenClaw 為何用 TypeScript: Node.js 生態完整（messaging SDK 全是 JS/TS） [score=0.868 recalls=0 avg=0.620 source=memory/2026-07-03.md:25-25]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:27:28 -->
- OpenClaw 為何用 TypeScript: Cross-platform（macOS/Linux/Windows）; Skill 生態（npm package） [score=0.868 recalls=0 avg=0.620 source=memory/2026-07-03.md:27-28]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:30:30 -->
- OpenClaw 為何用 TypeScript: **Rust 不適合的原因：** [score=0.868 recalls=0 avg=0.620 source=memory/2026-07-03.md:30-30]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:31:33 -->
- OpenClaw 為何用 TypeScript: Messaging SDK 幾乎全是 JS/TS; 重寫等於放棄生態; 效能瓶頸可在局部用 Rust（沙盒），其餘不需要 [score=0.868 recalls=0 avg=0.620 source=memory/2026-07-03.md:31-33]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:35:35 -->
- OpenClaw 為何用 TypeScript: **Python clone (kitpaw)：** [score=0.868 recalls=0 avg=0.620 source=memory/2026-07-03.md:35-35]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:36:39 -->
- OpenClaw 為何用 TypeScript: Repo: `reyoung/kitpaw`; 只 clone 了 `pi-agent`（Agent runtime），不是完整 OpenClaw; 落後半年（2026-03-30），WIP 狀態; **價值低** — 沒有 channel 接入，不是完整 clone [score=0.868 recalls=0 avg=0.620 source=memory/2026-07-03.md:36-39]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:45:48 -->
- OpenClaw 優勢分析: | 維度 | OpenClaw | 其他框架（LangGraph/CrewAI/smolagents） | |------|----------|---------| | Time-to-Production | ✅ 極低（npm install） | ❌ 需從零建構 | | Channel 接入 | ✅ 原生 20+ | ❌ 需自己刻 | [score=0.868 recalls=0 avg=0.620 source=memory/2026-07-03.md:45-48]

## Promoted From Short-Term Memory (2026-07-09)

<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:49:50 -->
- OpenClaw 優勢分析: | 本地部署 | ✅ 優先 | ⚠️ 通常是選項 | | Python 生態 | ❌ | ✅ 主流 | [score=0.858 recalls=0 avg=0.620 source=memory/2026-07-03.md:49-50]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:52:52 -->
- OpenClaw 優勢分析: **核心定位：「給你一個完整的 AI Agent 系統，不需要知道怎麼做」** [score=0.858 recalls=0 avg=0.620 source=memory/2026-07-03.md:52-52]
