# 本地多模型 Task Manager 每日研究

更新日期：2026-04-02
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

## 文件位置

`/home/node/.openclaw/workspace-roaringmoon/本地多模型-task-manager-每日研究.md`
