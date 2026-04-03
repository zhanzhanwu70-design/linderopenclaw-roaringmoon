# 本地多模型 Task Manager 每日研究

更新日期：2026-04-02（晚間）
主題：
- 本地 AI coding / agent 工作流中，如何用 task manager / orchestration 方式，把不同任務切分到不同模型執行
- 以 `opencode` + `ollama` 為主軸
- 持續追蹤可用的開源軟體、工作流框架、router / orchestrator / multi-agent 套件

---

## 研究問題定義

目標不是單純「切模型」，而是建立一個能把任務自動切分給不同模型執行的系統，例如：

- 閱讀 / 摘要 → 快模型
- coding / debug → 主力 code 模型
- 架構分析 / 研究 → 強推理模型
- 背景 indexing / embedding / rerank → 輕量模型或專用服務

關鍵研究問題：
1. 哪些開源軟體適合當 task manager / router / orchestrator？
2. 哪些方案適合和 `opencode` + `ollama` 組合？
3. 哪些框架是真的適合 coding-agent workflow，而不只是通用 agent demo？
4. 哪些方案支援多模型分工、子任務拆分、可觀測性、失敗恢復？
5. 是否要用多 agent，還是單 agent + router 更實用？

---

## 初步判斷

目前這類需求通常落在幾種路線：

### 路線 A：多 agent orchestration 框架
代表思路：
- 一個 coordinator / manager
- 多個 specialist agents
- 每個 agent 綁定不同模型

優點：
- 概念直觀
- 易於把任務切給不同模型

缺點：
- 容易過度工程化
- 常見 demo 多、真正適合 coding workflow 的少

### 路線 B：單 agent + task router
代表思路：
- 一個主 agent 收任務
- 先做分類
- 再把不同子任務送到不同 model endpoint

優點：
- 比較容易控制
- 比較像實際產品化 workflow

缺點：
- 需要自己設計路由規則

### 路線 C：工具層 task manager
代表思路：
- CLI / editor agent 當前台
- 背後接一層 workflow engine / queue / task executor
- executor 依任務類型選模型

優點：
- 最接近真正工程系統
- 容易做觀測、重試、排程

缺點：
- 實作成本較高

---

## 現階段優先關注的開源方向

以下是值得持續追蹤的類型，不代表最終結論：

### 1. 通用 agent orchestration
- LangGraph
- AutoGen 類框架
- CrewAI 類框架

### 2. 偏 workflow / graph / state machine
- LangGraph
- Mastra 類 workflow 系統
- 可表達 task graph / retries / branching 的框架

### 3. 偏 coding agent / harness / CLI
- OpenCode / Claude Code 類社群衍生工具
- OpenHands / aider / 類 coding agent 生態
- 具備 tool use + task decomposition 的本地 agent 專案

### 4. 偏模型 router / gateway
- LiteLLM 類 router
- Ollama 上層 router / policy layer
- OpenRouter 風格的本地替代層

### 5. 偏任務佇列 / executor
- Temporal 類工作流引擎
- Celery / Redis Queue 類傳統 task queue
- 用於把 agent 任務工程化的執行層

---

## 當前暫時建議

如果目標是：
**讓 `opencode` + `ollama` 能把 task 細分給不同模型執行**

目前我最看好的研究方向是：

### 短期實用派
- **LiteLLM / 類 router** 做模型路由
- **LangGraph / 類 state graph** 做任務分解
- `opencode` 當前台 CLI
- Ollama 當本地模型 serving

### 工程化長期派
- `opencode` 當入口
- 自建 task router / policy layer
- 背後用 workflow engine（LangGraph / Temporal 類）
- Ollama / 雲端模型共同作為執行端

目前還不建議過早鎖死單一框架；這個主題每天都在快速變動。

---

## 每日研究方式

每日研究應聚焦：
1. 新的開源 orchestration / multi-agent / router 專案
2. 既有專案重大更新
3. 是否有更適合 coding agent 的本地工作流設計
4. 是否有更適合 Ollama 的多模型 task routing 實例
5. 是否出現比當前候選更輕、更穩、更工程化的方案

每次更新時，應補：
- 新發現
- 對舊結論的修正
- 候選方案排行變化
- 實作可行性判斷

---

## 2026-04-02 晚間研究新發現

### 🔴 重大新發現

#### 1. `clawcal`（jlacerte/clawcal）— 今天剛發布！
**鏈接：** https://github.com/jlacerte/clawcal
**描述：** Local coding agent MCP server powered by Ollama. 結合本地 LLM（Qwen 3 14B, Llama 等）與 7 個 coding tools + agentic loop，全部透過 Model Context Protocol（MCP）暴露。
**為何重要：**
- 今天（2026-04-02）才建立，極新鮮！
- 直接把 Ollama 封裝成 MCP server，可被 Claude Desktop、VS Code 等使用
- 7 個工具：read_file, write_file, edit_file, bash, glob_tool, grep_tool, list_directory
- 複合 tool `code_agent`：讓本地 LLM 調用這些工具完成任務
- 支援 hybrid tool calling（原生 function calling + XML fallback，給小型模型用）
- 全本地，零雲端依賴
- MIT license

**評估：** 這是 opencode + ollama 組合的直接競爭對手或補充方案。它的 MCP server 架構意味著可以當作 opencode 的工具層或替代方案。重點關注。

#### 2. `orchestra`（ruska-ai/orchestra）— LangGraph + MCP + A2A 融合
**鏈接：** https://github.com/ruska-ai/orchestra
**描述：** 開源 AI agent orchestration 平台，基於 LangGraph，支援 MCP 和 A2A（Google 的 Agent-to-Agent）協議。可 self-host 或用 managed cloud。
**為何重要：**
- 同時支援 MCP（Model Context Protocol）和 A2A（Google A2A）—— 這是 protocol-level 的標準化
- 基於 LangGraph，代表 state graph 工作流
- 有社區免費版（可 docker pull）
- 支援社區部署 self-host
- 有前端介面 + backend + TaskIQ worker
- Python 3.11+

**評估：** Orchestra 是目前看到最完整的「工程化 + 協議支援」的 orchestration 平台。對於想用 LangGraph 做 workflow、同時又想標準化 agent 間通訊的團隊，這是首選。

#### 3. `Hybrid-ai-stack-intent-solutions`（jeremylongshore/）— 生產級本地+雲端路由
**鏈接：** https://github.com/jeremylongshore/Hybrid-ai-stack-intent-solutions
**描述：** 生產級 AI orchestration 系統，路由請求到本地模型（Ollama）或雲端 API（Claude/OpenAI），號稱降低 60-80% 成本。
**為何重要：**
- 複雜度估算路由：根據 prompt 特徵（長度、關鍵字、程式碼存在與否）估算複雜度
- 三層路由：TinyLlama / Phi-2 / Claude Sonnet，複雜度 < 0.3 → TinyLlama，0.3-0.6 → Phi-2，> 0.6 → Claude
- 完整 Docker stack：n8n、Ollama、API Gateway、Prometheus、Grafana、Redis、Qdrant、PostgreSQL
- 有 API Gateway（port 8080）統一入口
- 可觀測性完整：Prometheus + Grafana dashboards
- 有 Taskwarrior 整合追蹤 routing decision

**評估：** 這是目前看到最接近「工程化產品」的 routing 實作。複雜度估算的策略很值得參考，但 n8n 那層對 pure coding agent workflow 可能有點過重。更適合有 DevOps 需求的團隊。

### 🟡 中度重要發現

#### 4. `sprintloop-orchestration`（q-j0k/sprintloop-orchestration）— 新型 orchestration 引擎
**鏈接：** https://github.com/q-j0k/sprintloop-orchestration
**描述：** 高性能 orchestration engine，跨 LLM、SLM 和自定義 agent 路由任務。
**Topics：** agentic-ai, ai-orchestration, llm-orchestration, multi-model-router, workflow-engine, ai-sdlc, agentic-agile-sdlc
**為何重要：** 
- 今天（2026-04-02）才更新
- 覆蓋 topics 完整（agent orchestration、workflow engine、multi-model router、AI SDLC）
- MIT license
- 但目前看起來是預發布階段（zip download + README 安裝說明），成熟度待確認

**評估：** 概念完整，但需要實際測試才能判斷穩定性。先列為觀察名單。

#### 5. `devops-genai`（GauJosh/devops-genai）— CI/CD 分析 + 多模型路由
**鏈接：** https://github.com/GauJosh/devops-genai
**描述：** 生產風格的 GenAI 平台，用於 CI/CD failure analysis，含 RAG、多模型 inference routing、retry/fallback、K8s 可觀測性。
**架構元件：**
- `inference-router`：內部 generation gateway，支援 openai/ollama/mock provider abstraction，retry 邏輯，JSON logs，Prometheus metrics
- `rag-service`：文件攝取、chunking、embedding、ChromaDB 儲存
- K8s 部署（含 HPA autoscaling）
- Grafana dashboards

**評估：** `inference-router` 的設計（provider abstraction + retry/fallback）對 opencode + ollama 工作流很有參考價值。RAG 那層對 coding agent 場景則不一定需要。

#### 6. `shmastra`（just-ai/shmastra）— Mastra Studio vibe-code 插件
**鏈接：** https://github.com/just-ai/shmastra
**描述：** Vibe-code AI agents and workflows，運行在 Mastra Studio 內。
**為何重要：** 今天（2026-04-02）更新，Mastra 生態系的新成員。vibe-code 走向代表低程式碼 agent workflow 趨勢。

**評估：** 對 Mastra 用戶是個新工具；對 opencode + ollama 組合的直接影響有限。

#### 7. `ProjectLodestar`（estrify/ProjectLodestar）— 本地+雲端路由節省 90%
**鏈接：** https://github.com/estrify/ProjectLodestar
**描述：** Smart routing between free local and premium LLM models，聲稱節省 90% 以上成本。
**評估：** 概念同 Hybrid-ai-stack，但更輕量（細節待確認）。值得持續追蹤。

---

## 對既有結論的修正

### 修正 1：MCP 協議的重要性大幅上升
之前的假設是 LangGraph / orchestration 框架會是核心。**今日發現改變：** Model Context Protocol（MCP）正在成為本地 coding agent 的事實標準——`clawcal` 和 `orchestra` 都強調 MCP 支援。**建議：** 選擇工具時，優先考慮支援 MCP 的專案。

### 修正 2：LangGraph + MCP + A2A 三層組合值得重視
`orchestra`（ruska-ai/orchestra）同時支援 LangGraph workflow + MCP tools + A2A protocol，這是截至目前最有整合力的方案。**對原本「路線 A/B/C」的修正：** 
- Orchestra 代表一種新的「路線 D」：不只是 framework，而是整合了 protocol 標準的 full-stack orchestration platform

### 修正 3：「複雜度估算」路由策略驗證
`Hybrid-ai-stack-intent-solutions` 提供了可行的複雜度估算實作（prompt 長度、關鍵字、程式碼存在與否）。這印證了「單 agent + task router」路線的可行性。

---

## 目前最推薦的開源方向（更新版）

### 🥇 首選：`orchestra`（ruska-ai/orchestra）+ `clawcal` 組合
- `orchestra` 負責 workflow orchestration（LangGraph based，支援 MCP + A2A）
- `clawcal` 當本地 coding agent engine（MCP server + Ollama）
- 兩者都以 MCP 為核心，天然整合

### 🥈 次選：LiteLLM + LangGraph + opencode
- LiteLLM 做 router（统一调用的多模型接口）
- LangGraph 做 task decomposition
- opencode 當 CLI coding agent
- 適合想自建 policy layer 的團隊

### 🥉 第三：Hybrid-ai-stack-intent-solutions 借鑒架構
- 複雜度估算路由器設計值得參考
- n8n 那層可選擇性引入（取決於 workflow 複雜度）

---

## 本地模型候選補記：Gemma 4

已確認 `gemma4` 值得列入本地模型候選，尤其在 `opencode + LangGraph + Ollama` 工作流中可作為快模 / 規劃模 / review 模型的候選家族。

### 可用型號
- `gemma4:e2b`
- `gemma4:e4b`
- `gemma4:26b`（MoE，active 約 3.8B）
- `gemma4:31b`（dense）

### 目前判斷
- `e2b` / `e4b`：很適合本地快模、Reader、Summarizer、輕量 Reviewer
- `26b`：很值得當本地中高能力主力候選，可用於 Planner / Reviewer / 中高強度分析
- `31b`：可作為重推理 / 架構分析 / 高品質 review 候選，但更適合 VRAM 餘裕較大的配置

### 對既有硬體的粗判
- **2× Pro 6000 48G**：最適合完整嘗試 `e2b/e4b/26b/31b`
- **2× 5090 32G**：`e2b/e4b/26b` 很值得優先試，`31b` 可試但更吃量化與上下文配置
- **RTX4000 SFF 40G**：適合 `e2b/e4b`，`26b` 可視量化與實際延遲再評估，暫不建議把 `31b` 當主戰模型

### 在工作流中的角色建議
- `gemma4:e2b` / `gemma4:e4b` → 快模型層
- `gemma4:26b` → Planner / Reviewer / 中高階 reasoning
- `gemma4:31b` → 重推理 / 長上下文 / 高品質架構分析

### 備註
Benchmark 漂亮不等於 coding agent 手感一定最好，但 Gemma 4 已值得納入本地部署候選池，後續應持續比較它與 Qwen / Llama / DeepSeek 系在 coding agent 場景中的實戰表現。

### 🚀 明日重點觀察
- `clawcal` 的實際表現（今天才發布）
- `orchestra` 的社群成長（600+ stars，生態仍在建立）
- `sprintloop-orchestration` 的成熟度
- `gemma4:26b` / `gemma4:31b` 在本地 coding agent 場景的實戰手感

---

## 文件位置

`/home/node/.openclaw/workspace-roaringmoon/本地多模型-task-manager-每日研究.md`
