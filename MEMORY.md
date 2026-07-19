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

## Promoted From Short-Term Memory (2026-07-13)

<!-- openclaw-memory-promotion:memory:memory/2026-07-08.md:50:53 -->
- 狀態: [ ] Phase 1: 止血; [ ] Phase 2: 強制力; [ ] Phase 3: 召回; [ ] Phase 4: QA [score=0.839 recalls=0 avg=0.620 source=memory/2026-07-08.md:50-53]
<!-- openclaw-memory-promotion:memory:memory/2026-07-08.md:54:55 -->
- 狀態: [ ] Phase 5: 設計; [ ] Phase 6: 範圍 [score=0.829 recalls=0 avg=0.620 source=memory/2026-07-08.md:54-55]
<!-- openclaw-memory-promotion:memory:memory/2026-07-08.md:15:16 -->
- Phase 2：強制力（重要）: 程式化 Hooks（pre-commit, pre-merge, post-merge）; Schema 驗證 [score=0.827 recalls=0 avg=0.620 source=memory/2026-07-08.md:15-16]
<!-- openclaw-memory-promotion:memory:memory/2026-07-08.md:19:19 -->
- Phase 3：召回機制（核心）: 填補語義搜尋（整合 codebase-memory-mcp） [score=0.827 recalls=0 avg=0.620 source=memory/2026-07-08.md:19-19]
<!-- openclaw-memory-promotion:memory:memory/2026-07-08.md:38:41 -->
- 任務分配: | 任務 | 負責人 | 緊急度 | |------|--------|--------| | Phase 1a: 熵管理機制 | 木木鴞 | 緊急 | | Phase 1b: 去重偵測 | 木木鴞 | 緊急 | [score=0.827 recalls=0 avg=0.620 source=memory/2026-07-08.md:38-41]
<!-- openclaw-memory-promotion:memory:memory/2026-07-08.md:4:4 -->
- 來源: Linder 轉發 Ouroboros 批判分析（外部評價） [score=0.827 recalls=0 avg=0.620 source=memory/2026-07-08.md:4-4]
<!-- openclaw-memory-promotion:memory:memory/2026-07-08.md:42:45 -->
- 任務分配: | Phase 2: 強制力 Hooks | 噴火龍 | 重要 | | Phase 3: 召回機制 | 噴火龍 | 核心 | | Phase 4: QA 自動化 | 木木鴞 | 重要 | | Phase 5: 設計調整 | 魔牆人偶 | 中等 | [score=0.827 recalls=0 avg=0.620 source=memory/2026-07-08.md:42-45]
<!-- openclaw-memory-promotion:memory:memory/2026-07-08.md:32:32 -->
- Phase 6：範圍擴展: Agent Working Memory 整合 [score=0.817 recalls=0 avg=0.620 source=memory/2026-07-08.md:32-32]
<!-- openclaw-memory-promotion:memory:memory/2026-07-08.md:23:23 -->
- Phase 4：QA 自動化: Lint 工具鏈 [score=0.807 recalls=0 avg=0.620 source=memory/2026-07-08.md:23-23]

## Promoted From Short-Term Memory (2026-07-14)

<!-- openclaw-memory-promotion:memory:memory/2026-07-10-0735.md:12:12 -->
- Conversation Summary: assistant: 那是**不同的目錄**。 [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-10-0735.md:12-12]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10-0735.md:14:14 -->
- Conversation Summary: 我跑的 graphify 在**伺服器**上，不是你本機。 [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-10-0735.md:14-14]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10-0735.md:9:9 -->
- Conversation Summary: user: "D:\llm-wiki\raw\code\elle_ws\graphify\elle_ws_functions-ast\graphify-out\cache\semantic" [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-10-0735.md:9-9]

## Promoted From Short-Term Memory (2026-07-15)

<!-- openclaw-memory-promotion:memory:memory/2026-07-10-0735.md:3:5 -->
- Session: 2026-07-10 07:35:50 UTC: **Session Key**: agent:roaringmoon:discord:channel:1482561255955763293; **Session ID**: 7816db42-7f96-40b9-9b40-07cef119660b; **Source**: discord [score=0.893 recalls=0 avg=0.620 source=memory/2026-07-10-0735.md:3-5]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10-0735.md:30:31 -->
- 原因: elle_ws_functions-ast → 之前失敗的 run（只有 AST，沒有 semantic） elle_ws_functions → 剛剛成功的 run（有 semantic + graph.json） [score=0.893 recalls=0 avg=0.620 source=memory/2026-07-10-0735.md:30-31]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10-0735.md:40:40 -->
- 在伺服器上: find /home/node/.openclaw/workspace/llm-wiki/raw/code/elle_ws/graphify/elle_ws_functions -name "*.json" | wc -l [score=0.893 recalls=0 avg=0.620 source=memory/2026-07-10-0735.md:40-40]
<!-- openclaw-memory-promotion:memory:memory/2026-07-08.md:60:63 -->
- 已完成: [x] staleness_rules.yaml — 定義各類型的過時閾值; [x] auto_archive_hook.py — 自動歸檔過時頁面; [x] deduplication_hook.py — 偵測近義重複頁面; [x] wikilinks_integrity_hook.py — 檢查 wikilinks 完整性 [score=0.869 recalls=0 avg=0.620 source=memory/2026-07-08.md:60-63]
<!-- openclaw-memory-promotion:memory:memory/2026-07-08.md:64:65 -->
- 已完成: [x] frontmatter_schema.json — frontmatter 驗證 schema; [x] SKILL.md 更新 — v2.6 加入熵管理與強制力章節 [score=0.869 recalls=0 avg=0.620 source=memory/2026-07-08.md:64-65]
<!-- openclaw-memory-promotion:memory:memory/2026-07-08.md:69:72 -->
- 新增檔案: ouroboros/ ├── references/ │ ├── staleness_rules.yaml # 過時閾值設定 │ └── frontmatter_schema.json # frontmatter 驗證 [score=0.869 recalls=0 avg=0.620 source=memory/2026-07-08.md:69-72]
<!-- openclaw-memory-promotion:memory:memory/2026-07-08.md:73:76 -->
- 新增檔案: ├── scripts/ │ ├── auto_archive_hook.py # 自動歸檔腳本 │ ├── deduplication_hook.py # 去重偵測腳本 │ └── wikilinks_integrity_hook.py # 斷鏈檢查 [score=0.869 recalls=0 avg=0.620 source=memory/2026-07-08.md:73-76]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10-0735.md:20:23 -->
- 實際路徑對照: | 你的本機（Windows） | 伺服器（Linux） | |--------------------|----------------| | `D:\llm-wiki\...\` | `/home/node/.openclaw/workspace/llm-wiki/raw/code/elle_ws/` | | `elle_ws_functions-ast\` | `elle_ws_functions/`（有 semantic）| [score=0.861 recalls=0 avg=0.620 source=memory/2026-07-10-0735.md:20-23]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10-0735.md:44:46 -->
- 結果: 1368 + graph.json = 1369 個檔案: **Semantic extraction 成功了，資料在 `graphify/elle_ws_functions/graphify-out/`** user: elle_ws_functions-ast 部分應該可以刪掉 assistant: ✅ 已刪除 `elle_ws_functions-ast` [score=0.861 recalls=0 avg=0.620 source=memory/2026-07-10-0735.md:44-46]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10-0735.md:53:56 -->
- 目前結構: graphify/ └── elle_ws_functions/ └── graphify-out/ ├── graph.json (21,393 nodes, 27,710 edges) [score=0.861 recalls=0 avg=0.620 source=memory/2026-07-10-0735.md:53-56]

## Promoted From Short-Term Memory (2026-07-16)

<!-- openclaw-memory-promotion:memory:memory/2026-07-10-0735.md:57:59 -->
- 目前結構: └── cache/ ├── ast/ (1,368 files) └── semantic/ (chunk results) [score=0.888 recalls=0 avg=0.620 source=memory/2026-07-10-0735.md:57-59]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10-0735.md:62:64 -->
- 目前結構: **有用的資料都保留了。** user: 為何只有function 其他部分也要做啊 assistant: 對，其他 repos 也要做。目前進度： [score=0.888 recalls=0 avg=0.620 source=memory/2026-07-10-0735.md:62-64]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10-0735.md:66:69 -->
- 目前結構: | Repo | 檔案數 | Graphify | |------|--------|---------| | elle_ws_functions | 1370 | ✅ 完成 | | elle_ws_bringup | 71 | ❌ 未做 | [score=0.888 recalls=0 avg=0.620 source=memory/2026-07-10-0735.md:66-69]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10-0735.md:70:73 -->
- 目前結構: | elle_ws_hardware | - | ❌ 未做 | | elle_ws_simulations | - | ❌ 未做 | | elle_ws_tools | - | ❌ 未做 | | elle_web_backend | - | ❌ 未做 | [score=0.888 recalls=0 avg=0.620 source=memory/2026-07-10-0735.md:70-73]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10-0735.md:79:82 -->
- 繼續執行: user: hey assistant: NO_REPLY user: 做的如何了 assistant: elle_ws_bringup 被中斷了，繼續跑完： [score=0.888 recalls=0 avg=0.620 source=memory/2026-07-10-0735.md:79-82]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10-0735.md:84:87 -->
- 繼續執行: user: hi assistant: [assistant turn failed before producing content] user: 繼續把 bringup hardware 的graphify部分完成 user: 有繼續做嗎 [score=0.812 recalls=0 avg=0.620 source=memory/2026-07-10-0735.md:84-87]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10-0735.md:88:88 -->
- 繼續執行: user: 設定一個cron 每五分鐘檢測一次是否完成 完成後把cron刪除 [score=0.812 recalls=0 avg=0.620 source=memory/2026-07-10-0735.md:88-88]
