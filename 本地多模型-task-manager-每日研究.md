## 每日研究更新

### 日期: 2026-05-31

### 今日新發現
- **ZeroShield AI Mesh Firewall**: 具備多模型路由控制功能，專注於 AI 安全和合規可觀測性，適合大型企業應用。
- **Langchain**: 新增多項語言代理功能，進一步提升任務分揀和代理可靠性。
- **Bytedance Deer Flow**: 提供長期自動代理管理，適合需要逐步執行的長時間任務。

### 對既有結論的修正
- 調整：**LangGraph** 現在能夠更好地與多種框架整合，建議在現有架構中實驗。

### 目前最推薦的開源方向
- 繼續監測 **ZeroShield AI Mesh Firewall** 和 **Bytedance Deer Flow**，他們在安全和任務長期管理上提供卓越的解決方案。

### 改善建議
- 可將 **ZeroShield** 嵌入現有多模型環境中，強化安全防護和路由可控性。

### 值得追蹤的項目
- 持續關注 **OpenHands** 和 **Langchain** 的發展，以及如何有效整合至您的工作流中。
---

### 日期: 2026-06-01

### 今日新發現
- **Ollama ↔ OpenCode 整合已變成一條非常直接的路徑**：Ollama 官方文件已有 `ollama launch opencode`，可把 Ollama 設定透過 `OPENCODE_CONFIG_CONTENT` inline 傳給 OpenCode；同頁也提醒 OpenCode 建議至少 64k context。這表示「opencode + ollama」不必先自建完整 router，就能快速跑 local coding agent baseline。
- **OpenCode 本身支援 75+ providers、local models、baseURL override**：OpenCode 透過 AI SDK / models.dev 管理 provider，可對 provider 設 `baseURL`，因此可以接 Ollama、LiteLLM proxy、OpenRouter、LM Studio/vLLM 類 OpenAI-compatible 端點。內建 `build` / `plan` agent，以及可用 `@general` 呼叫複雜搜尋/多步任務 subagent。這比較像「coding shell + agent profile」，不是完整 workflow engine。
- **LiteLLM 仍是最成熟的模型路由層**：官方 routing 支援 weighted pick、rate-limit aware、latency based、least-busy、lowest-cost、自訂 routing、fallback/retry/cooldown、Redis-based usage/cooldown；同時支援 Ollama provider，建議用 `ollama_chat/*` 走 Ollama `/api/chat`。LiteLLM repo 今日仍活躍，GitHub API 觀察：`BerriAI/litellm` 約 48.9k stars，2026-06-01 有 push。
- **LiteLLM 新增/強調 Agent A2A Gateway 方向**：README 提到 AI Gateway 不只代理 LLM，也可 invoke A2A Agents，列出 LangGraph、Vertex AI Agent Engine、Azure AI Foundry、Bedrock AgentCore、Pydantic AI。這讓 LiteLLM 從「模型 gateway」往「agent gateway」延伸，值得追蹤。
- **OpenHands 的 local LLM 指引更新明確**：OpenHands local LLM 文件在 2026-05-21 建議先試 **Qwen3.6-35B-A3B**，理由是 agentic coding、large context，並可透過 LM Studio、Ollama、vLLM、SGLang 供應；但也明說 local LLM 可能功能受限，建議 GPU。這修正了「任何本地小模型都適合 coding agent」的過度樂觀。
- **Vibestrate 是今日最貼近本研究題目的新候選**：`guyshonshon/vibestrate` 自稱 local-first supervisor/orchestrator，會把任務切成 planner → architect → executor → reviewer → fixer/verifier，在 git worktree 中執行，跑測試/驗證，保留 prompt/diff/decision/token 紀錄，且可混用 Claude Code、Codex、Aider、Ollama、OpenCode。GitHub 搜尋顯示 stars 很低、仍屬早期，但概念非常貼近「task manager 分派不同任務到不同模型」。
- **Mastra / CrewAI / AutoGen / LangGraph 的定位更清楚**：
  - Mastra workflows：TypeScript workflow engine，明確 step schema、資料流、suspend/resume/streaming，可把 agent/tool 放進 step；適合產品化的可控流程。
  - CrewAI Flows：event-driven workflow + state management + branch/loop，並可搭配 LiteLLM completion；適合快速 Python orchestration。
  - AutoGen：v0.x 後分成 Studio / AgentChat / Core / Extensions，Core 強調 event-driven scalable multi-agent systems、distributed runtime、Docker executor/MCP extension。
  - LangGraph：仍是最強「可控 state graph / multi-agent workflow」候選，但今天未取得新版 multi-agent doc 內容，需下輪補查最新 doc URL。
- **小型新 repo 訊號多但可信度參差**：GitHub search 出現多個 `Ollama + routing + coding agent` 題材 repo（如 megingjord-harness、dxa-deimos、Autodidact 等），多數 stars 低、README 宣稱多，暫不應納入主架構，只適合追蹤設計概念。

### 對既有結論的修正
- **修正 1：ZeroShield 不應是目前主推薦方向**。前次把 ZeroShield 放在推薦位置，但本研究主軸是 local coding agent / opencode + ollama；今天證據顯示更直接、可落地的是「OpenCode/Ollama + LiteLLM + workflow orchestrator」。ZeroShield 若是安全/合規層可另案追蹤，不應主導本地 coding workflow。
- **修正 2：OpenCode 不等於 task manager**。OpenCode 很適合作為 coding executor / plan shell，但 task 切分、跨模型分派、審核 gate、重試/回滾仍需要外部 orchestrator 或 wrapper。
- **修正 3：本地模型路由不該只看 provider 切換**。真正有用的策略應包含：任務分類、能力分級、context window、工具調用能力、成本/延遲、失敗 fallback、測試驗證 gate、worktree 隔離。
- **修正 4：OpenHands 比想像更適合當「重型 agent runtime」候選**。它有 SDK / CLI / local GUI / REST API，且可跑 local LLM；但資源需求與 agentic coding model 品質門檻高，未必適合當第一版輕量 task manager。

### 目前最推薦的開源方向
1. **第一階段 MVP：OpenCode + Ollama 作 coding executor，LiteLLM 作模型 router / gateway。**
   - OpenCode 負責互動式 coding、plan/build 模式與本地模型接入。
   - Ollama 提供 local model serving，先以長上下文 coding model 為主。
   - LiteLLM 統一 local/cloud model endpoint，處理 fallback、routing、usage、latency/cost 策略。
2. **第二階段加上輕量 Task Manager wrapper。**
   - 先不要直接上完整 LangGraph/Temporal。
   - 用簡單 YAML/JSON task spec：`task_type -> role -> preferred_model -> fallback_model -> executor_cli -> validation_command -> approval_gate`。
   - 每個任務開 git worktree，記錄 prompt/diff/test/log，避免模型互相污染。
3. **第三階段再評估 workflow engine。**
   - 若偏 Python/research：LangGraph 或 CrewAI Flow。
   - 若偏 TypeScript/product：Mastra Workflows。
   - 若需要長時間 durable execution / retry / human-in-loop：Temporal，但目前不是第一優先。
   - 若需要完整 coding runtime / GUI / REST API：OpenHands。
4. **把 Vibestrate 作為設計參考或候選實驗**，但暫不作為主依賴；它的 planner→architect→executor→reviewer→verifier、worktree、token/diff audit 方向很符合需求。

### 是否建議修改工作流 / 模型路由策略
- **建議修改：是。** 將工作流從「單 agent 換模型」改成「角色化路由 + 驗證 gate」。
- 建議初版路由：
  - `triage / summarize / repo scan`：本地便宜長上下文模型（Ollama，例如 Qwen/DeepSeek-Coder 類）。
  - `planning / architecture`：較強 reasoning/coding model，可 local 優先，不足時 fallback cloud。
  - `implementation`：OpenCode build 或 aider executor；用 coding 能力最穩的模型。
  - `review / security / tests interpretation`：不同於 executor 的模型，避免同模型盲點。
  - `final verify`：固定跑 typecheck/test/build，不讓 LLM 自評取代驗證。
- LiteLLM routing 層建議先做三種 alias：
  - `local-fast`：便宜快速任務。
  - `local-code`：主要本地 coding 模型。
  - `strong-code`：高難度/失敗 fallback，可接 cloud 或更大本地模型。
- OpenCode 端建議先保留 `plan` / `build` 二分；不要把所有任務都交給 build mode。

### 值得持續追蹤的項目
- OpenCode 的 agent/profile/subagent 能力是否新增更正式的 multi-agent/task dispatch API。
- Ollama 對 OpenCode、OpenClaw、Codex、Claude Code 等 integration 的成熟度與 config 可控性。
- LiteLLM A2A Gateway 是否成熟到能接 LangGraph/OpenHands 類 agent，而不只是 model proxy。
- OpenHands local LLM model recommendation 是否持續更新，尤其 Qwen/DeepSeek/Kimi/GLM coding MoE 模型的 agentic coding 表現。
- Vibestrate 是否快速成長、是否真的能穩定驅動 OpenCode/Ollama/aider。
- Mastra Workflows / CrewAI Flows 是否更適合做「可觀測、可暫停、可恢復」的本地 coding task manager。

### 今日摘要
今天有實質新進展：主軸應從前次的安全閘道/泛 agent 框架，收斂到 **OpenCode + Ollama + LiteLLM + 輕量 orchestrator**。Ollama 已有官方 OpenCode integration，OpenCode 支援 local/provider baseURL，LiteLLM 是最成熟 router；真正缺的是 task manager wrapper。建議下一步做一個小型 proof-of-concept：用 YAML 定義任務角色與模型 alias，OpenCode/aider 執行，LiteLLM/Ollama 提供模型，git worktree + test/build 作驗證 gate。

### 來源/查核記錄
- OpenCode repo/docs/providers：open source coding agent、plan/build agents、75+ provider、local model/baseURL support。
- Ollama docs：OpenAI compatibility、OpenCode integration `ollama launch opencode`、Ollama repo README integrations。
- LiteLLM docs/repo：router/load balancing/fallback/retry/cooldown、Ollama provider、AI Gateway/A2A mention。
- OpenHands docs/repo：SDK/CLI/local GUI/REST API、local LLM recommendation Qwen3.6-35B-A3B。
- CrewAI Flows、Mastra Workflows、AutoGen docs：workflow/state/event-driven/multi-agent runtime 定位。
- GitHub API metadata snapshot 2026-06-01：opencode、ollama、LiteLLM、LangGraph、AutoGen、CrewAI、Mastra、OpenHands、aider、Temporal 均仍活躍或具高社群關注。
