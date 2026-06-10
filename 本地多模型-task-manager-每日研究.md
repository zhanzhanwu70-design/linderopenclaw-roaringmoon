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

---

### 日期: 2026-06-03

### 今日新發現
- **OpenCode repo 名稱/歸屬需修正：目前 GitHub API 回傳為 `anomalyco/opencode`，不是前次記錄的 `sst/opencode`。** 2026-06-03 仍高度活躍，約 169k stars，當日有 push。這不改變「OpenCode 作 coding executor」的結論，但來源標註要更新。
- **OpenCode agents 文件確認它已具備「輕量 agent profile/subagent」能力**：內建 primary agents `Build` / `Plan`，以及 subagents `General` / `Explore` / `Scout`。其中 `Plan` 預設把 file edits 與 bash 設為 ask，`Explore`/`Scout` 偏 read-only，`General` 可跑複雜多步任務。這表示 OpenCode 可承擔部分「任務角色切換」，但仍不是完整 task manager：缺 queue、跨 worktree orchestration、可觀測 retry、全域模型選擇策略。
- **OpenCode provider/config 文件確認 local/router 接法很順**：支援 75+ providers、local models、任意 provider `baseURL` override，且 config precedence 支援 project config、`.opencode`、`OPENCODE_CONFIG_CONTENT`。這讓「OpenCode → LiteLLM proxy → Ollama/cloud fallback」很容易產品化。
- **LiteLLM routing / Ollama provider 仍是最成熟的 routing layer**：docs 再次確認支援 load-balance、queueing、cooldown、fallback、timeout、retry、Redis usage/cooldown；Ollama provider 支援 `ollama/*`，且官方建議使用 `ollama_chat/*` 以取得較好回應，也支援 JSON mode / tool calling（模型能力仍要個別確認）。
- **Mastra Workflows 的定位更清楚**：官方文件明確說 workflows 是用結構化 steps 控制多步任務，不依賴單一 agent 推理；支援 step input/output schema、data flow、suspend/resume、streaming，並可呼叫 agents/tools。若未來要做 TypeScript 版 task manager，Mastra 比 CrewAI/LangGraph 更貼近 OpenCode/Node 生態。
- **CrewAI Flows 文件確認它和 LiteLLM 相容**：Flow example 直接用 `litellm.completion`；它提供 state management、event-driven workflow、branch/loop。對 Python 快速實驗仍可用，但跟 OpenCode/Node CLI 生態的整合成本略高於 Mastra。
- **OpenHands local LLM 指引仍維持高門檻**：2026-05-21 docs 建議 Qwen3.6-35B-A3B，並明說 local LLM 可能功能受限、建議 GPU；硬體至少偏 24GB VRAM / Apple Silicon 64GB unified memory 等級。這支持「OpenHands 暫列重型 runtime，不作 MVP 第一層」的判斷。
- **新增候選：`ucav/mozart-router`（約 6 stars，2026-05-25 push）**。README 自稱 local conductor for AI agents，會 auto-detect Ollama/OpenClaw/OpenCode/LiteLLM/OpenRouter/LM Studio/vLLM/NIM，做 task classification、secret scan、cost estimate、quality/cost/latency/privacy/context/reliability scoring、fallback/circuit breaker、route explanation。可信度仍低（新、小），但概念非常貼近我們想做的「routing policy layer」。
- **新增候選：`pockanoodles/Mahoraga`（約 9 stars，2026-05-20 push）**。以 LinUCB contextual bandit 做 heterogeneous agent routing，支援 Ollama、Codex CLI、Aider、Gemini CLI、Goose、OpenCode；會用 capability bucket、context vector、品質評估、episodic memory、retry/escalation。這是今天最值得追蹤的「自學式路由」設計參考，但不宜直接依賴。
- **新增候選：`aiagentflow/aiagentflow`（約 41 stars，2026-05-24 push）**。local-first CLI，多 agent pipeline：Architect → Coder → Reviewer → Security → Tester → Fixer → Judge → Ship；支援 provider/model per role、Ollama、worktree isolation、plan review gate、parallel batch、project memory。比 Vibestrate 更像可試跑的本地 coding task manager 候選。
- **Vibestrate 仍符合方向但成熟度未變**：`guyshonshon/vibestrate` 今日仍有 push，但 stars 仍很低。它的 plan → build → review → verify、isolated worktree、驅動既有 coding-agent CLIs 的設計值得借鑑，不建議當核心依賴。

### 對既有結論的修正
- **修正 1：OpenCode 不是只有 `plan/build` 二分，而是已有 agents/subagents 結構。** 這讓 MVP 可以先利用 OpenCode 原生 `Plan` / `Build` / `Explore` / `Scout` 作角色分工；外部 task manager 主要補「排程、路由、隔離、驗證、紀錄」。
- **修正 2：路由策略可拆成兩層，而不是全交給 LiteLLM。** LiteLLM 很適合 provider/model gateway 與 fallback；但「任務分類、隱私掃描、角色選擇、agent CLI 選擇、驗證 gate」更像 Mozart/Mahoraga/aiagentflow 這種 orchestration policy layer。
- **修正 3：Mastra 的優先級上升。** 若主軸是 opencode + ollama，TypeScript/Node 的 Mastra Workflows 比 Python 框架更容易整合 CLI、JSON config、`.opencode` 目錄與 npm 發佈；LangGraph 仍強但不是最短路徑。
- **修正 4：小 repo 不宜忽視但要分級。** Mozart、Mahoraga、aiagentflow、Vibestrate 不一定成熟，但它們集中反映同一個新趨勢：本地 coding agent 不只需要 model proxy，而需要「可解釋的 task/router supervisor」。

### 目前最推薦的開源方向
1. **MVP 主線：OpenCode + Ollama + LiteLLM + 自製薄 task manager。**
   - OpenCode：coding executor / Plan-Build-Explore-Scout agent shell。
   - Ollama：local model serving。
   - LiteLLM：OpenAI-compatible gateway、fallback、routing、usage/cooldown。
   - 自製薄層：task spec、role selection、privacy gate、worktree isolation、validation command、audit log。
2. **設計參考：Mozart Router + Mahoraga + aiagentflow + Vibestrate。**
   - Mozart：policy/routing explanation、secret scan、cost/privacy/context scoring。
   - Mahoraga：bandit-based adaptive routing、quality feedback loop。
   - aiagentflow：role pipeline、provider/model per role、plan review、worktree isolation。
   - Vibestrate：plan/build/review/verify supervisor loop。
3. **第二階段 workflow engine：Mastra Workflows 優先，LangGraph/CrewAI 次之。**
   - 若要 npm/TypeScript 原生：Mastra。
   - 若要 Python research / graph state：LangGraph。
   - 若要快速 Python flows + role-playing crews：CrewAI。
   - 若要 durable execution / long-running retry / human wait：Temporal，但暫不作 MVP 核心。
4. **重型 coding runtime：OpenHands 保持候選。** 適合完整 GUI/REST/SDK 與重型 coding agent，但 local LLM 硬體與模型品質門檻高。

### 是否建議修改工作流 / 模型路由策略
- **建議修改：是，但保持小步。** 不要直接導入大型 workflow engine；先加一層「policy router + task spec」。
- 建議把 routing 從三個 alias 擴成「任務類型 + 角色 + 資安等級」：
  - `scan/explore`：OpenCode `Explore` 或 `Scout` + `local-fast`，read-only。
  - `plan/architecture`：OpenCode `Plan` + `strong-code` 或 `local-code` fallback。
  - `implementation`：OpenCode `Build` 或 aider + `local-code` / `strong-code`。
  - `review/security`：不同模型、不同 agent，優先 read-only，必要時 cloud fallback 但需 privacy gate。
  - `verify`：非 LLM；固定跑 tests/typecheck/build/lint，結果回寫 audit log。
- 新增 policy 欄位建議：`privacy_level`、`requires_write`、`context_size`、`expected_runtime`、`validation_command`、`fallback_chain`、`human_approval_gate`、`worktree_mode`。
- 若任務涉及 secrets、`.env`、private keys、客戶資料：router 必須禁止 cloud fallback，或要求明確 human approval。

### 值得持續追蹤的項目
- OpenCode 是否把 agents/subagents 暴露成更穩定的 non-interactive dispatch API。
- LiteLLM A2A Gateway 是否能成熟到統一 agent invocation，而不只是 model proxy。
- Mozart Router 是否持續更新，尤其 OpenClaw/OpenCode auto-detect 與 secret scan 是否可靠。
- Mahoraga 的 bandit routing 是否有實際 benchmark / regression tests，而非 README 概念。
- aiagentflow 是否能穩定驅動真實 repo，尤其 worktree isolation、plan review gate、model-per-role config。
- Qwen/DeepSeek/Kimi/GLM/MiniMax 類 local coding MoE 模型在 OpenCode/OpenHands/aider 上的實測表現。

### 今日摘要
今天有實質新進展：OpenCode 自身的 agents/subagents 能力比前次理解更完整，因此 MVP 不必先做複雜 multi-agent engine；可以先用 OpenCode 的 `Plan` / `Build` / `Explore` / `Scout`，外面加一層薄 task manager。最值得新增追蹤的是 Mozart Router、Mahoraga、aiagentflow：它們都指向同一個趨勢——本地 coding workflow 的缺口不是「再多一個模型 proxy」，而是「可解釋、可審核、帶隱私 gate 的 task/router supervisor」。目前仍推薦 **OpenCode + Ollama + LiteLLM + 自製薄 orchestration layer**，並把 Mastra Workflows 作為第二階段 TypeScript workflow engine 候選。

### 來源/查核記錄
- GitHub API snapshot 2026-06-03：`anomalyco/opencode`、`ollama/ollama`、`BerriAI/litellm`、`langchain-ai/langgraph`、`microsoft/autogen`、`crewAIInc/crewAI`、`mastra-ai/mastra`、`temporalio/temporal`、`OpenHands/OpenHands`、`Aider-AI/aider`、`guyshonshon/vibestrate`。
- OpenCode docs：agents/subagents、config precedence、provider `baseURL`、75+ providers/local models。
- LiteLLM docs：routing/load balancing、fallback/retry/cooldown/Redis、Ollama provider / `ollama_chat` 建議。
- Mastra docs：workflows overview、step schema、suspend/resume、streaming、agent/tool steps。
- CrewAI docs：Flows、state management、event-driven workflow、branch/loop、LiteLLM example。
- OpenHands docs：local LLM recommendation Qwen3.6-35B-A3B、local limitations/hardware guidance。
- GitHub search / README review：`ucav/mozart-router`、`pockanoodles/Mahoraga`、`aiagentflow/aiagentflow`、`guyshonshon/vibestrate`。

---

### 日期: 2026-06-04

### 今日新發現
- **OpenCode repo 歸屬/活躍度再確認**：GitHub API 今日顯示 `opencode-ai/opencode` 已 archived，活躍主 repo 仍是 `anomalyco/opencode`，約 169.9k stars，2026-06-04 21:30 UTC 有 push。這修正了可能從舊 namespace 取資料的風險；後續查核應優先看 `anomalyco/opencode` 與官方 docs。
- **OpenCode Agents docs 今日仍確認 agent/subagent 是可用的內建分工單位**：primary agents 有 `Build` / `Plan`，subagents 有 `General` / `Explore` / `Scout`，另有 context compaction / title / summary 等 hidden agents。`Explore` / `Scout` read-only、`Plan` 預設 writes/bash ask、`Build` 全工具，這很適合被外部 task manager 當作角色映射層，而不是從零自建所有 agent 行為。
- **LiteLLM routing 仍是模型 gateway 首選**：routing docs 今日仍明確列出 load balancing、queueing、cooldown、fallback、timeout、retry、Redis usage/cooldown，以及 weighted / rate-limit aware / latency / least-busy / lowest-cost / custom routing。結論不變：LiteLLM 負責「模型部署與 fallback」，不要讓它背負整個「任務語意分類與驗證 gate」。
- **新增候選：`berkayturanci/ai-jury`**（約 1 star，2026-06-04 push）。它不是完整 coding task manager，而是「cross-vendor multi-agent review jury」：驅動 Claude Code、Codex CLI、Google Antigravity，加上 Ollama/OpenAI-compatible local model，對同一 PR/diff/issue 做平行 review、互相 rebuttal，再由 chair synthesize verdict；主打 sandboxed/read-only、CI gating、large-diff chunking。對我們最有價值的是「異質模型審查/仲裁」模式，可作為 review/security/final verdict 階段設計參考。
- **新增候選：`kcsinclair/kaos-control`**（約 4 stars，2026-06-03 push）。它是自架 Claude Code orchestrator，重點是 markdown-on-disk lifecycle、YAML frontmatter、role-gated SDLC、per-agent sandbox、PreToolUse hook audit、per-role model assignment（含 local Ollama）、token spend log、Web UI/DevOps pipeline。雖然核心偏 Claude Code 不是 OpenCode，但「artefact-as-task + lifecycle state machine + audited tool gate」非常貼近我們 task manager 應補的那一層。
- **新增候選：`VikingOwl91/gnoma`**（約 1 star，2026-06-04 push）。Go 寫的 provider-agnostic coding assistant，支援 Anthropic/OpenAI/Gemini/Mistral/Ollama/llama.cpp 與 subprocess CLIs；有 multi-armed bandit router、`prefer=local|cloud|auto`、Tier-0 小模型分類、secret scanner、content boundary、no phone-home、MCP/skills/hooks/plugins。它和 Mahoraga 一樣屬於「自學/可解釋路由」設計參考，但成熟度仍低。
- **新增候選：`XAIHT/Tlamatini`**（約 5 stars，2026-06-04 push / README v1.14.0）。local-first developer assistant，Ollama、本地 RAG（FAISS+BM25）、多工具 multi-turn operator、視覺 workflow designer、ACPX 可委派 Claude Code/Cursor/Codex/Gemini CLI/Qwen。它太龐雜、不適合當 MVP 依賴，但證明「local-first + workflow canvas + external coding CLI delegation」這條路正在出現。
- **小 repo 訊號更集中**：GitHub search 今日還看到 `dxa-deimos`、`Nexora-agent`、`claude-agent-team`、`Overseer`、`loom`、`electrictown` 等多個低 star 專案，都在談 multi-model routing、local-first coding agent、SDLC supervisor、MCP/hook/sandbox。多數不宜直接採用，但共同趨勢非常明確：大家都在補「coding-agent CLI 之外的 supervisor / policy / audit layer」。
- **主流框架活躍度無重大反轉**：`BerriAI/litellm`、`ollama/ollama`、`langchain-ai/langgraph`、`crewAIInc/crewAI`、`mastra-ai/mastra`、`temporalio/temporal`、`OpenHands/OpenHands` 今日仍有更新；`Aider-AI/aider` 最近 push 為 2026-05-22，仍活躍但今日沒有新訊號改變定位。

### 對既有結論的修正
- **修正 1：OpenCode namespace 必須明確標準化。** 之前已修正為 `anomalyco/opencode`，今天再補充：`opencode-ai/opencode` 是 archived 舊/非主 repo，不應作為活躍度判斷來源。
- **修正 2：review 階段應升級為「異質模型 jury」，不只是單一 reviewer。** ai-jury 的設計提醒我們：review/security/test interpretation 最容易受單模型盲點影響，建議至少用不同模型或不同 CLI agent 交叉審查，最後由 chair/strong model 合併 verdict。
- **修正 3：task manager 的資料模型應從單純 YAML routing table 升級為 artefact lifecycle。** kaos-control 顯示 markdown/YAML frontmatter 作任務來源，加 lineage、stage、approval gate、acceptance criteria，比單次 CLI wrapper 更容易長期維護與審計。
- **修正 4：bandit/adaptive routing 值得保留在中期路線，但不該進 MVP。** Mahoraga/gnoma 都主打 multi-armed bandit；這對長期成本/品質最佳化有價值，但第一版應先做 deterministic policy + audit log，等有足夠 run history 再學習。
- **修正 5：視覺 workflow / full IDE 類方案不應影響第一階段選型。** Tlamatini 類工具功能多，但範圍太大；目前只拿其 ACPX / workflow canvas / local-first delegation 概念當參考。

### 目前最推薦的開源方向
1. **MVP 主線維持：OpenCode + Ollama + LiteLLM + 自製薄 task manager。**
   - OpenCode：負責 Plan / Build / Explore / Scout 角色化 coding shell。
   - Ollama：本地模型 serving 與 privacy-preserving baseline。
   - LiteLLM：模型 alias、fallback、timeout、retry、usage/cooldown、router observability。
   - 自製薄層：task artefact、role/model/executor mapping、privacy gate、worktree isolation、validation command、audit log。
2. **把 task spec 升級成 markdown/YAML artefact lifecycle。**
   - 建議資料夾：`tasks/inbox`、`tasks/planning`、`tasks/ready`、`tasks/running`、`tasks/review`、`tasks/done`、`tasks/blocked`。
   - 每個 task frontmatter 至少包含：`id`、`stage`、`privacy_level`、`requires_write`、`role`、`executor`、`model_alias`、`fallback_chain`、`worktree`、`validation_command`、`approval_gate`、`lineage`、`created_by`、`audit_log`。
3. **第二階段候選排序微調：Mastra Workflows 仍優先；Temporal 只在 durable execution 需求明確時加入。**
   - Mastra：Node/TypeScript 生態，較容易接 OpenCode CLI、`.opencode` config、LiteLLM HTTP。
   - LangGraph/CrewAI：適合 Python research / graph/crew experiments。
   - Temporal：適合長時間、可恢復、可重試、人類等待很多的 production workflow；MVP 暫不需要。
4. **review/security 階段新增設計參考：ai-jury。**
   - 可以設計成 `review_panel`: `local-code` + `strong-code` + `security-model`，read-only parallel review，最後 chair 合併。
5. **中期 tracking：Mahoraga + gnoma 的 bandit routing。**
   - 等本地 task manager 有 run history（成功率、test pass、review defect、latency、token/cost）後，再用 bandit/score routing 自動調整模型選擇。

### 是否建議修改工作流 / 模型路由策略
- **建議修改：是，小幅但重要。** 今日不建議換主棧；建議把路由策略從「角色 -> model alias」擴成「task artefact lifecycle + deterministic policy + review jury」。
- 新版路由建議：
  - `intake/triage`：local-fast；輸出 task frontmatter，不寫 repo。
  - `scan/explore`：OpenCode `Explore` / `Scout` + local-fast/local-code；read-only；禁止 cloud fallback，除非只查公開 docs。
  - `plan/architecture`：OpenCode `Plan` + local-code 或 strong-code；writes/bash 維持 ask。
  - `implementation`：OpenCode `Build` 或 aider + local-code/strong-code；必須 worktree isolation。
  - `review/security`：異質模型 panel；至少一個非 executor 模型；read-only；高隱私任務禁止 cloud。
  - `verify`：非 LLM；固定跑 test/typecheck/build/lint；結果寫回 audit log。
  - `ship/merge`：human approval gate；不要讓 agent 自動 merge/push。
- LiteLLM aliases 建議保留 `local-fast` / `local-code` / `strong-code`，新增邏輯 alias：`review-local`、`review-strong`、`private-only`。其中 `private-only` 的 fallback chain 只能含 Ollama/本機 OpenAI-compatible 端點。

### 值得持續追蹤的項目
- OpenCode 是否提供穩定 non-interactive agent/subagent dispatch API 或更完整 session control。
- LiteLLM A2A Gateway / agent invocation 是否成熟到能統一 OpenCode/OpenHands/LangGraph 類 agent，而非只管 LLM calls。
- kaos-control 的 lifecycle artefact / sandbox hook 是否能抽象到 OpenCode 或通用 CLI agent。
- ai-jury 是否能穩定用於 PR/diff review，尤其 false-positive filtering 與 CI gate。
- gnoma / Mahoraga 的 bandit router 是否有真實 benchmark、可重現評估、長期品質回饋資料結構。
- aiagentflow / Vibestrate 是否出現可穩定試跑的 release 或實戰案例。
- Qwen / DeepSeek / Kimi / GLM / MiniMax 等本地 coding 模型在 OpenCode + Ollama 上的長上下文、tool-use、patch reliability 表現。

### 今日摘要
今天有實質新進展，但不是推翻主結論，而是把設計補強：活躍 OpenCode repo 應固定看 `anomalyco/opencode`，`opencode-ai/opencode` 已 archived；OpenCode agent/subagent + LiteLLM routing 的主線仍成立。新增最有價值的觀察是 **ai-jury 的異質模型審查模式**、**kaos-control 的 artefact lifecycle + sandbox/audit gate**、以及 **gnoma/Mahoraga 的 bandit routing 思路**。目前仍推薦 **OpenCode + Ollama + LiteLLM + 自製薄 orchestration layer**，但建議把第一版 task manager 從簡單 routing table 升級成 markdown/YAML task lifecycle，並把 review/security 做成不同模型的 read-only jury。

### 來源/查核記錄
- GitHub API snapshot 2026-06-04：`opencode-ai/opencode` archived；`anomalyco/opencode`、`BerriAI/litellm`、`ollama/ollama`、`langchain-ai/langgraph`、`microsoft/autogen`、`crewAIInc/crewAI`、`mastra-ai/mastra`、`temporalio/temporal`、`OpenHands/OpenHands`、`Aider-AI/aider`、`guyshonshon/vibestrate`、`ucav/mozart-router`、`pockanoodles/Mahoraga`、`aiagentflow/aiagentflow`。
- OpenCode docs：Agents / built-in Build, Plan, General, Explore, Scout / permissions / hidden agents。
- LiteLLM docs：Router load balancing、queueing、cooldown、fallback、timeout、retry、Redis、routing strategies。
- README review 2026-06-04：`berkayturanci/ai-jury`、`kcsinclair/kaos-control`、`VikingOwl91/gnoma`、`XAIHT/Tlamatini`。
- GitHub search 2026-06-04：local coding agent / Ollama orchestration / multi-model routing 類低 star 新專案訊號。

---

### 日期: 2026-06-05

### 今日新發現
- **主流主線今日仍高度活躍，沒有被新框架取代。** GitHub API 快照 2026-06-05 22:00 UTC：`anomalyco/opencode` 約 170.5k stars、今日 push；`BerriAI/litellm` 約 49.4k stars、今日 push；`ollama/ollama` 約 173.3k stars、今日 push；`OpenHands/OpenHands`、`mastra-ai/mastra`、`crewAIInc/crewAI`、`langchain-ai/langgraph`、`temporalio/temporal` 也都有今日更新。`opencode-ai/opencode` 仍 archived，不應作為活躍 OpenCode 來源。
- **OpenCode Agents docs 再確認：它已可當「角色化 coding shell」，但不是 task manager。** 文件列出 primary agents `Build` / `Plan` 與 subagents `General` / `Explore` / `Scout`；`Explore` / `Scout` read-only，`Plan` 預設 edits/bash ask，`Build` 全工具。新增/確認重點是：OpenCode agent 可透過 JSON 或 `.opencode/agents/` markdown 配置自訂 prompt、model、permission，因此外部 task manager 可以把角色映射到 OpenCode agent，而不是每次硬塞 prompt。
- **OpenCode config precedence 對 runtime routing 很友善。** 文件確認 config merge/precedence 包含 remote、global、custom path、project、`.opencode`、`OPENCODE_CONFIG_CONTENT` inline runtime override。這支持「task manager 每次根據任務生成臨時 OpenCode config / agent model mapping」的設計。
- **LiteLLM routing 結論不變：可靠模型 gateway，不是語意 orchestrator。** 官方 routing docs 今日仍列 load balancing、queueing、cooldown、fallback、timeout、retry、Redis tpm/rpm usage/cooldown、weighted/rate-limit/latency/least-busy/cost/custom routing。適合負責 provider/model alias 與 resilience，但 task lifecycle、privacy gate、worktree、review jury 還是應在上層。
- **新增候選：`scottgl9/skelm`（約 23 stars，2026-06-05 push）。** README 定位是 typed TypeScript pipelines、default-deny permissions、gateway-owned privileged actions，可支援短任務、agent loop、cron、webhook、多日 human approval workflow。它不是 OpenCode 專用，但很貼近「安全、可測、可審計的 workflow engine」；值得作為 Mastra 之外的 TypeScript workflow candidate，尤其是 default-deny gateway/permission 思路。
- **新增候選：`Suraj1235/open-dynamic-workflows`（0 stars，2026-06-05 push）。** README 核心句是「script is the orchestrator, not the model」，面向 OpenCode、Codex、Antigravity、VS Code，local daemon、BYO model、QuickJS/WASM sandbox、無 telemetry。成熟度目前很低，但概念非常準：讓本地 script 執行模型規劃出的 swarm/workflow，避免把 orchestration 權限交給單一 LLM。
- **新增候選：`aegntic/compound-engineering`（0 stars，2026-06-05 push）。** 提供跨 Claude Code / Copilot / OpenCode 的 portable skills/commands/workflows，強調 `/constitution → /ideate → /plan → /deepen-plan → work → review → ship`、specialized reviewers、docs/solutions 知識沉澱。它偏「workflow/skill pack」而非 router，但提醒我們：task manager 不只要執行，還要把解法與 reviewer knowledge 留在 repo。
- **新增候選：`tusharmewara/loom` ecosystem（homebrew formula 2026-06-01 push）。** 目標是在 Claude Code、jcode、Cursor、Goose、OpenCode、crush 間共享 skills、MCP servers、sessions，並可選擇每個 task 用哪個 agent。它不是直接多模型 router，但指向「跨 coding-agent CLI 共享上下文/工具/技能」這個後續需求。
- **其他低 star 訊號仍集中在同一趨勢。** `yash249114/loom` 主打 local-first multi-model coding agent、auto routing、3-tier fallback、verification loop；`meganerd/electrictown` 主打 provider-agnostic role routing/fallback/cost tracking；`skgandikota/coracle` 主打 drop-in OpenAI-compatible scheduler 給 OpenCode/Claude Code/Codex/Cursor 使用。這些目前不宜當核心依賴，但共同證明「本地個人機器上的 router/scheduler/supervisor」正在變成一類工具。
- **既有小候選今天仍有更新：** `vibestrate`、`ai-jury`、`kaos-control`、`Tlamatini` 今日都有 push；`mozart-router`、`Mahoraga`、`aiagentflow` 暫無新 push。`ai-jury` 描述更明確：stdlib-only Python CLI，驅動 native coding-agent CLIs + local model 做 diff/PR/issue review jury、debate、verify、synthesize verdict，local-first secure by default。

### 對既有結論的修正
- **修正 1：第一版 task manager 應更偏「script/state-machine orchestrator」，不要讓 LLM 自己當 workflow engine。** open-dynamic-workflows 與 skelm 都支持這點：模型可以產生 plan，但真正的排程、權限、sandbox、狀態遷移、驗證應由本地 deterministic script/engine 管。
- **修正 2：Mastra 仍是 TypeScript workflow 首選之一，但不是唯一候選。** skelm 的 default-deny permissions / gateway pattern 對本地 coding agent 更安全；若 MVP 只需 typed pipeline + permission gate，可與 Mastra 並列評估。Mastra 優勢是成熟 AI app/agent 生態與 step schema/suspend/resume/streaming；skelm 優勢是安全 gateway 與長任務權限模型。
- **修正 3：OpenCode agent config 應納入路由輸出，而不是只輸出 model alias。** task manager 應能為每個 task 生成/選擇 OpenCode agent：`explore` / `plan` / `build` / `reviewer`，並指定 permission、model、prompt；再由 LiteLLM alias 提供實際模型。
- **修正 4：knowledge compounding 應進入 task lifecycle。** compound-engineering 顯示每次任務的 plan、review、solution 都應變成 repo 內可搜尋 artifact；這比只留 token log 更有長期價值。
- **修正 5：跨 agent CLI ecosystem 可列為後續需求。** Loom 類 shared layer 提醒我們，長期可能不只 OpenCode/Ollama，也會同時用 aider、Codex CLI、Claude Code、Goose、Cursor；但 MVP 仍應先鎖 OpenCode + aider/verify commands，避免範圍爆炸。

### 目前最推薦的開源方向
1. **MVP 主線維持：OpenCode + Ollama + LiteLLM + 自製薄 task manager。**
   - OpenCode：角色化 coding executor（Build / Plan / Explore / Scout + 自訂 reviewer agents）。
   - Ollama：local/private serving baseline。
   - LiteLLM：統一 provider/model alias、fallback、timeout、retry、routing observability。
   - 自製薄層：deterministic task lifecycle、OpenCode config/agent selection、worktree isolation、validation command、privacy gate、audit/solution artifact。
2. **第一版不要上 full autonomous multi-agent swarm；先做「script orchestrates, model proposes」。**
   - LLM 產生 plan/task breakdown。
   - 本地 script 檢查 frontmatter、privacy、permissions、worktree、validation。
   - script 決定哪些 OpenCode agent / model alias / CLI executor 可用。
   - verify/review/ship 都有明確 gate。
3. **第二階段 workflow engine 候選排序微調：Mastra + skelm 並列 TypeScript 候選。**
   - Mastra：step schema、data flow、suspend/resume、streaming，AI app 生態成熟。
   - skelm：typed pipeline、default-deny permissions、gateway-controlled privileged actions，安全/長任務觀念更貼近本地 coding agent。
   - LangGraph/CrewAI：Python research 或 graph/crew 實驗仍可用。
   - Temporal：等 durable execution、人類等待、跨日 retry 需求明確才導入。
4. **review/security 仍建議採異質模型 jury。** ai-jury 持續更新，適合當 read-only panel / chair verdict 設計參考，不建議目前把它當唯一核心依賴。
5. **中期才評估 adaptive/bandit routing。** Mahoraga/gnoma 方向有價值，但先累積 run history（成功率、測試通過、review defect、latency、token/cost）再讓 routing 學習。

### 是否建議修改工作流 / 模型路由策略
- **建議修改：是，小幅升級。** 主棧不換，但把 router 輸出從 `model_alias` 擴成 `executor + opencode_agent + permission_profile + model_alias + validation + artifact_policy`。
- 建議新版 task frontmatter 增加：
  - `opencode_agent`: `explore | scout | plan | build | reviewer | custom`
  - `permission_profile`: `read_only | ask_writes | worktree_write | no_shell | allow_tests_only`
  - `orchestrator_policy`: `script_driven | human_approval_required | jury_required`
  - `artifact_policy`: `save_plan | save_diff | save_review | save_solution_note`
  - `privacy_fallback`: `local_only | cloud_allowed_after_redaction | cloud_allowed_with_approval`
- 建議路由策略：
  - `intake/triage`：local-fast，script 只產 task artifact。
  - `repo_scan`：OpenCode `Explore`/`Scout` + read_only + local-fast/local-code。
  - `plan`：OpenCode `Plan` + ask_writes/no_shell + local-code/strong-code。
  - `implementation`：OpenCode `Build` 或 aider + worktree_write + local-code，失敗再 strong-code。
  - `review/security`：read-only jury；至少一個非 executor 模型；private 任務 local-only。
  - `verify`：非 LLM command；test/typecheck/build/lint 結果寫 artifact。
  - `ship`：human approval，不自動 merge/push。

### 值得持續追蹤的項目
- OpenCode 是否提供穩定 non-interactive dispatch/session API，讓外部 task manager 更容易啟動指定 agent/subagent。
- LiteLLM A2A Gateway 是否真正成熟到可統一 agent invocation，而非只統一 LLM calls。
- skelm 是否出現 OpenCode / CLI agent integration example，尤其 permission gateway 是否能包住 shell/file/network/MCP。
- open-dynamic-workflows 是否有可跑範例、OpenCode adapter、sandbox 實作與 tests。
- compound-engineering 是否能跨 OpenCode 穩定安裝/使用，尤其 review/solution artifact 是否可抽出成通用模板。
- ai-jury 的 PR/diff review false-positive 控制、CI gate 實測。
- vibestrate / aiagentflow / kaos-control 是否出現真實專案實戰報告。
- 本地 coding 模型（Qwen/DeepSeek/Kimi/GLM/MiniMax）在 OpenCode + Ollama 的 tool-use、patch reliability、長上下文表現。

### 今日摘要
今天有實質新進展，但不是推翻主結論，而是讓 MVP 設計更具體：仍推薦 **OpenCode + Ollama + LiteLLM + 自製薄 task manager**。新增重點是 `skelm` 的 default-deny typed workflow、`open-dynamic-workflows` 的「script is the orchestrator, not the model」、`compound-engineering` 的 artifact/knowledge compounding。建議工作流小幅修改：task manager 不只選模型，還要選 OpenCode agent、permission profile、validation gate、artifact policy；模型負責提出 plan，真正 orchestration 由本地 script/state machine 控制。

### 來源/查核記錄
- GitHub API snapshot 2026-06-05 22:00 UTC：`anomalyco/opencode`、`opencode-ai/opencode`、`BerriAI/litellm`、`ollama/ollama`、`langchain-ai/langgraph`、`microsoft/autogen`、`crewAIInc/crewAI`、`mastra-ai/mastra`、`temporalio/temporal`、`OpenHands/OpenHands`、`Aider-AI/aider`、`guyshonshon/vibestrate`、`ucav/mozart-router`、`pockanoodles/Mahoraga`、`aiagentflow/aiagentflow`、`berkayturanci/ai-jury`、`kcsinclair/kaos-control`、`VikingOwl91/gnoma`、`XAIHT/Tlamatini`。
- OpenCode docs 2026-06-05：Agents / primary agents / subagents / JSON + markdown agent config / permissions；Config precedence / `.opencode` / `OPENCODE_CONFIG_CONTENT`。
- LiteLLM routing docs 2026-06-05：load balancing、queueing、cooldown、fallback、timeout、retry、Redis usage/cooldown、routing strategies。
- Mastra workflows docs 2026-06-05：step schema、data flow、suspend/resume、streaming、agent/tool execution in step。
- CrewAI Flows docs 2026-06-05：event-driven workflow、state management、branch/loop、LiteLLM completion example。
- GitHub search / README review 2026-06-05：`scottgl9/skelm`、`Suraj1235/open-dynamic-workflows`、`aegntic/compound-engineering`、`tusharmewara/homebrew-loom`、`mx-Liu123/AgentCommander`、`yash249114/loom`、`meganerd/electrictown`、`skgandikota/coracle`。

---

### 日期: 2026-06-06

### 今日新發現
- **主流主線今天仍活躍，沒有出現足以取代 MVP 主棧的新框架。** GitHub API 快照 2026-06-06 22:00 UTC：`anomalyco/opencode` 約 170.8k stars、今日 push；`BerriAI/litellm` 約 49.5k stars、今日 push；`ollama/ollama` 約 173.4k stars、今日 push；`mastra-ai/mastra`、`temporalio/temporal`、`OpenHands/OpenHands`、`crewAIInc/crewAI`、`XAIHT/Tlamatini`、`scottgl9/skelm`、`Suraj1235/open-dynamic-workflows` 也都有今日更新。`Aider-AI/aider` 最近 push 仍停在 2026-05-22，但社群關注仍高。
- **OpenCode Agents / Config 文件再次確認：OpenCode 很適合被外部 task manager 當作「可配置 executor shell」。** Agents 文件明確說 agent 可自訂 prompt、model、tool access；內建 `Build` / `Plan` / `General` / `Explore` / `Scout`。Config precedence 確認 `OPENCODE_CONFIG_CONTENT` inline runtime override 在標準 config 之上，這讓 task manager 可依任務動態生成 agent/model/permission 配置，而不必污染 repo 長期設定。
- **skelm 的優先級上升：它不是只是一個候選 workflow engine，而是明確列出 `opencode` backend。** README 範例用 `agent({ backend: 'opencode', permissions: ... })`，並強調 typed TypeScript pipelines、default-deny permissions、gateway-owned privileged actions、durable wait/resume、persistent workflows、SQLite/file system local-first。這與我們要的「script/state-machine 管 orchestration，OpenCode 管 coding executor」高度吻合。
- **open-dynamic-workflows 今天仍更新，且把「script-as-orchestrator」模式具體化。** README 描述：模型只負責寫一次 `execute(context)` plan，local daemon 在 QuickJS/WASM sandbox 中執行 `agent` / `parallel` / `pipeline` / `verify` / `loop` / `checkpoint`；SQLite WAL 保存狀態，可 resume；critic/quorum 用來降低 false positives；支援 Ollama 與任意 OpenAI-compatible endpoint。成熟度仍低，但它是目前最貼近「模型不要 babysit swarm，由本地 runtime 執行」的設計參考。
- **LiteLLM routing 文件結論維持：它是可靠模型 gateway，不是完整 task semantics orchestrator。** 今日文件仍列出 load balancing、queueing、cooldown、fallback、timeout、retry、Redis tpm/rpm usage/cooldown，以及 weighted / rate-limit aware / latency / least-busy / lowest-cost / custom routing。上層仍需要 policy/task lifecycle 來決定何時用哪個 executor/agent/permission profile。
- **Mastra Workflows 仍是成熟 TypeScript workflow 候選。** 文件強調用 structured steps 而非單 agent reasoning 控制多步任務，支援 input/output schema、data flow、suspend/resume、streaming，step 可呼叫 agents/tools。相較 skelm，Mastra 生態與 AI app integration 較成熟；skelm 的安全 gateway / default-deny 更貼近本地 coding-agent 風險模型。
- **CrewAI Flows / LangGraph / AutoGen / Temporal 定位沒有重大變化。** CrewAI Flows 仍適合 Python event-driven/state/branch/loop 快速實驗；LangGraph 仍是 graph/state/control 強者；AutoGen 今日 repo push 訊號不強但框架定位仍是 event-driven multi-agent；Temporal 仍適合 durable long-running production workflow，但 MVP 導入成本偏高。
- **OpenHands local LLM 文件未改變核心警訊：本地 agentic coding 模型仍有硬體與品質門檻。** 2026-05-21 文件仍建議 Qwen3.6-35B-A3B 作為第一個 local model，並明說 local LLM 功能可能受限、建議 GPU，24GB VRAM / Apple Silicon 64GB unified memory 等級更合理。這支持「OpenHands 是重型 runtime 候選，不是第一版薄 task manager」的判斷。
- **Tlamatini 今天仍更新，但更像 full local assistant / workflow canvas，不適合 MVP 主依賴。** v1.17.x README 強調 Windows 本地安裝、Ollama、FAISS+BM25、ACPX 委派 Claude Code/Cursor/Codex/Gemini/Qwen、視覺 workflow designer、multi-turn operator。可借鑑「外部 coding-agent CLIs as tools」與「local-first toolbelt」理念，但範圍與授權/平台假設不適合作為 opencode+ollama MVP 核心。
- **既有小候選今天沒有全面突破。** `vibestrate`、`ai-jury`、`kaos-control` 最近仍停在 2026-06-05；`mozart-router`、`Mahoraga`、`aiagentflow` 暫無新 push。它們仍是設計參考：review jury、artefact lifecycle、bandit routing、role pipeline，但目前不宜作核心依賴。

### 對既有結論的修正
- **修正 1：skelm 從「一般 TypeScript 候選」升級為「最值得做 adapter/prototype 的候選」。** 原因是它已在 README 以 `backend: 'opencode'` 示範 agent step，並把 permissions/network/fs/MCP/exec 都放在 gateway 控制下；這比單純 workflow library 更像本研究需要的安全 task manager 層。
- **修正 2：第一版 task manager 可分兩條 implementation path。** 若要最快落地：自製薄 script + markdown/YAML task lifecycle；若要直接站在現成 runtime 上：優先試 skelm，再試 Mastra。兩者不互斥：自製 task artifact 可先定義資料模型，之後由 skelm/Mastra runner 執行。
- **修正 3：OpenCode runtime config 應被視為 task manager 的輸出物。** 不是只呼叫 `opencode`，而是為每個 task 產生/選擇 `OPENCODE_CONFIG_CONTENT` 或 `.opencode/agents/*.md`，把 agent、model、permission、prompt 都作為可審計 artifact。
- **修正 4：review/verify primitive 應內建在 orchestrator，而不是靠 LLM prompt 自覺。** open-dynamic-workflows 的 `verify` / critic quorum 概念與 ai-jury 的 panel 都指向同一件事：review 要是 workflow step，不是「請同一個模型再檢查一次」。
- **修正 5：不要被 full-workshop 工具牽走 MVP 範圍。** Tlamatini 類工具展示了 local-first + many tools + workflow canvas 的可能性，但 MVP 仍應保持 CLI/script/task-file 可 diff、可測、可審計。

### 目前最推薦的開源方向
1. **MVP 主線不變：OpenCode + Ollama + LiteLLM + 薄 task manager。**
   - OpenCode：coding executor / agent shell（Build / Plan / Explore / Scout + 自訂 reviewer）。
   - Ollama：local/private model serving baseline。
   - LiteLLM：model alias、fallback、retry、timeout、usage/cooldown、observability。
   - 薄 task manager：task lifecycle、policy routing、OpenCode config generation、permission profile、worktree isolation、validation/review artifact。
2. **第一個現成 runtime prototype 建議試 skelm。**
   - 理由：TypeScript、typed pipeline、opencode backend、default-deny gateway、durable wait/resume、local-first storage，和本研究目標高度貼合。
   - 風險：新專案、stars 少、需要實測 opencode backend 成熟度與 permission enforcement 是否真的包住 shell/file/network/MCP。
3. **Mastra 作為成熟 TypeScript workflow 方案並列第二。**
   - 若重點是 AI app 生態、structured steps、schema、stream/suspend/resume，Mastra 仍很強。
   - 若重點是本地 coding-agent 安全邊界、default-deny permissions、gateway-owned privileged actions，skelm 更貼切。
4. **open-dynamic-workflows 作為架構靈感，不作第一依賴。**
   - 借鑑：model writes plan once、script runs swarm、sandboxed JS、checkpoint/resume、verify quorum。
   - 暫不依賴：成熟度低、stars 少、需更多實戰案例。
5. **OpenHands 保持重型 runtime 候選。** 適合 GUI/REST/SDK/完整 agent runtime，但 local LLM 硬體門檻高，不適合第一版輕量 opencode+ollama task manager。

### 是否建議修改工作流 / 模型路由策略
- **建議修改：是，小幅升級但不換主棧。** 今日建議把「runner 選型」加入策略：`runner = shell_script | skelm | mastra | temporal`，而不是只選 `executor/model`。
- 建議新版 task frontmatter / routing output：
  - `runner`: `thin-script | skelm | mastra | manual`
  - `executor`: `opencode | aider | verify-command | jury-panel`
  - `opencode_agent`: `explore | scout | plan | build | reviewer | custom`
  - `permission_profile`: `read_only | ask_writes | worktree_write | no_shell | tests_only | network_limited`
  - `model_alias`: `local-fast | local-code | strong-code | review-local | review-strong | private-only`
  - `privacy_fallback`: `local_only | cloud_allowed_after_redaction | cloud_allowed_with_approval`
  - `validation_command`: concrete deterministic command, not LLM self-rating
  - `review_policy`: `none | single_non_executor | jury_quorum`
  - `artifact_policy`: `save_plan | save_config | save_prompt | save_diff | save_review | save_solution_note | save_run_log`
- 建議路由分層：
  1. **Policy layer**：讀 task artifact，判斷 privacy/write/network/context/risk。
  2. **Runner layer**：簡單任務用 thin-script；需要 durable/persistent/default-deny gateway 時試 skelm；產品化 AI app workflow 再試 Mastra。
  3. **Executor layer**：OpenCode agent / aider / verify command / review jury。
  4. **Model gateway layer**：LiteLLM alias -> Ollama/local/cloud fallback。
  5. **Validation layer**：test/typecheck/build/lint + review jury + human approval gate。

### 值得持續追蹤的項目
- OpenCode 是否推出更穩定的 non-interactive agent/subagent dispatch API、session API、或 machine-readable run output。
- skelm 的 opencode backend 是否有更多 examples/tests，尤其 gateway permission 是否能真正限制 exec/filesystem/network/MCP。
- open-dynamic-workflows 是否出現可重現 demo、adapter、test suite、以及 OpenCode/Ollama 真實 repo 案例。
- Mastra workflows 是否更容易接 OpenCode CLI / LiteLLM / local artifact store。
- LiteLLM A2A Gateway 是否從 model gateway 成熟到 agent invocation gateway。
- ai-jury / kaos-control 是否能提供可抽出的 review jury / markdown lifecycle 實戰模板。
- 本地 coding 模型（Qwen3.x/3.6、DeepSeek、Kimi、GLM、MiniMax）在 OpenCode + Ollama 的 tool-use、patch reliability、長上下文與 review precision 實測。

### 今日摘要
今天有實質新進展，但不是推翻主線：仍推薦 **OpenCode + Ollama + LiteLLM + 薄 task manager**。最大更新是 **skelm 優先級上升**：它已明確支援 `opencode` backend，並提供 typed pipeline、default-deny permissions、gateway 控制 privileged actions、durable wait/resume，值得作為第一個現成 runtime prototype。另一個重點是 **open-dynamic-workflows** 持續更新，強化「model plans once, local script orchestrates」這個方向。建議工作流小幅升級：router 不只輸出模型與 executor，也輸出 `runner`、OpenCode runtime config、permission profile、review policy、artifact policy；verification 必須是獨立 workflow step，而不是模型自評。

### 來源/查核記錄
- GitHub API snapshot 2026-06-06 22:00 UTC：`anomalyco/opencode`、`BerriAI/litellm`、`ollama/ollama`、`langchain-ai/langgraph`、`microsoft/autogen`、`crewAIInc/crewAI`、`mastra-ai/mastra`、`temporalio/temporal`、`OpenHands/OpenHands`、`Aider-AI/aider`、`guyshonshon/vibestrate`、`ucav/mozart-router`、`pockanoodles/Mahoraga`、`aiagentflow/aiagentflow`、`berkayturanci/ai-jury`、`kcsinclair/kaos-control`、`VikingOwl91/gnoma`、`XAIHT/Tlamatini`、`scottgl9/skelm`、`Suraj1235/open-dynamic-workflows`、`aegntic/compound-engineering`、`skgandikota/coracle`、`meganerd/electrictown`、`yash249114/loom`。
- OpenCode docs 2026-06-06：Agents / built-in Build, Plan, General, Explore, Scout / JSON + markdown agent config / permissions；Config precedence / `OPENCODE_CONFIG_CONTENT` runtime override。
- LiteLLM routing docs 2026-06-06：load balancing、queueing、cooldown、fallback、timeout、retry、Redis usage/cooldown、routing strategies。
- Mastra workflows docs 2026-06-06：structured steps、schema、data flow、suspend/resume、streaming、agent/tool execution。
- CrewAI Flows docs 2026-06-06：event-driven workflow、state management、branch/loop、LiteLLM completion example。
- OpenHands local LLM docs 2026-06-06：Qwen3.6-35B-A3B recommendation、local LLM limitations、GPU/hardware guidance。
- README review 2026-06-06：`scottgl9/skelm`、`Suraj1235/open-dynamic-workflows`、`XAIHT/Tlamatini`。

---

### 日期: 2026-06-07

### 今日新發現
- **主線活躍度仍強，沒有出現足以取代 MVP 主棧的新框架。** GitHub API 快照 2026-06-07 22:00 UTC：`anomalyco/opencode` 約 171.2k stars、今日 push；`ollama/ollama` 約 173.5k stars、今日 push；`BerriAI/litellm` 約 49.6k stars、今日 push；`langchain-ai/langgraph`、`mastra-ai/mastra`、`temporalio/temporal`、`OpenHands/OpenHands` 也都有今日更新。`opencode-ai/opencode` 仍 archived，不應用來判斷 OpenCode 活躍度。
- **OpenCode Agents / Config 結論再確認，且更適合被 task manager 動態配置。** Agents 文件確認 primary agents `Build` / `Plan`、subagents `General` / `Explore` / `Scout`；agent 可自訂 prompt、model、tool access、temperature、permission。Config precedence 仍包含 `.opencode` 與 `OPENCODE_CONFIG_CONTENT` runtime override，這支持「每個 task 產生可審計 OpenCode config / agent mapping」的設計。
- **skelm 繼續升級為最值得 prototype 的現成 runtime 候選。** README 明確列出 `backend: 'opencode'`、`@skelm/opencode` backend、default-deny permissions、gateway-owned exec/network/filesystem/MCP、typed TypeScript pipelines、durable wait/resume、persistent chat workflow、SQLite/filesystem local-first、hash-chained audit journal。這和「OpenCode 負責 coding executor，script/runtime 負責 orchestration 與權限」高度吻合。
- **open-dynamic-workflows 今天最重要的新訊號：OpenCode plugin / keyless native mode。** README 描述 OpenCode adapter 可作為 drop-in plugin，在 OpenCode 內透過 plugin SDK / `session.prompt` 使用既有 OpenCode model，不需 daemon、不需第二組 API key；並聲稱已在 OpenCode 1.2.27 live validated，93 round-trips 完成 multi-agent run。這若屬實，對 opencode + ollama 主軸非常關鍵：可把「dynamic workflow engine」內嵌到 OpenCode，而不是外掛一個需要另行配 key 的 daemon。仍需實測，因 repo stars 很低。
- **LiteLLM routing 文件新增/確認 routing groups 與 traffic mirroring 對模型策略有用。** 除了既有 load balance、queueing、cooldown、fallback、timeout、retry、Redis tpm/rpm usage/cooldown，今日查到 routing groups 可針對不同 model group 套用不同 routing strategy；traffic mirroring 可做 silent experiments。這支持下一版 router 把 `local-fast` / `local-code` / `strong-code` / `review-*` 分成不同策略，並用 mirror 收集候選本地模型品質資料。
- **ai-jury 今天仍活躍，review jury 方向更具體。** README 顯示它是 stdlib-only Python CLI，驅動 Claude Code / Codex / Antigravity native CLIs + Ollama/OpenAI-compatible local model，做 diff/PR/issue review、debate、verify、chair synthesis 或 panel vote；支援 sandbox/read-only、CI gating、large-diff chunking、incremental review、suggested patches，並有 coverage/CodeQL/PyPI badges與方向性 benchmark。仍不宜當核心 orchestrator，但可作 `review_policy: jury_quorum` 參考實作。
- **新增候選：`RBraga01/a-team`（約 4 stars，2026-06-07 push）。** 它是「一個資料夾式工程團隊」：25 specialist agents、18 workflow skills、lead orchestrator、hard quality gates、pipeline auditor、`.opencode/` integration。價值是 agent roster / hooks / quality gate / pipeline auditor 模板；缺點是偏 agent/skill pack，不是模型 router 或 durable runtime。
- **新增候選：`izhiwen/AiPlus`（約 1 star，2026-06-07 push）。** 面向 Codex / Claude Code / OpenCode 的 local CLI meta-layer，重點是 project memory、role-based dispatch、handoff/compact reminder、status、self-correct、tamper-evident dispatch log、key injection。可作「本地 project memory + routing audit」設計參考，但目前不替代 LiteLLM / OpenCode / skelm。
- **新增候選：`halbritt/striatum`（約 3 stars，2026-06-07 push）。** README 描述 local workflow runner for terminal AI coding agents，支援 implement → review → repair → synthesize loops、leases、verdicts、audit chains、daemon-owned Postgres、repo durable artifacts、terminal-command provider wrappers。它偏重型、需要 Postgres/daemon，但「verdicts + leases + audit-chain + terminal wrapper」是中期 production runner 的好參考。
- **新增候選：`earlvanze/sage-router`（約 2 stars，2026-06-06 push）。** Local-first model gateway，支援 OpenAI/Anthropic/Gemini-compatible endpoints、Ollama auto-discovery、intent/complexity/requirements/thinking-level scoring、fallback chain、debug headers。它與 LiteLLM 角色重疊；價值是「semantic intent router」設計，但成熟度與安全性需審查，暫不替代 LiteLLM。
- **可疑/低信任訊號：`RandallRO/axon`。** GitHub 搜尋描述看似 local zero-trust orchestration，但 README 指向 raw zip download、內容像一般 Windows installer 宣傳，與本研究關聯弱且供應鏈風險高；不納入候選。

### 對既有結論的修正
- **修正 1：open-dynamic-workflows 的優先級小幅上升，但仍是「需實測的高潛力設計參考」。** 昨天只把它視為 script-as-orchestrator 靈感；今天它聲稱已有 OpenCode plugin keyless native mode，若實測成立，會比外部 daemon 更貼合 opencode + ollama。但因 repo 很新、stars 少，不能直接升為主依賴。
- **修正 2：LiteLLM 不只做 fallback，也可作「實驗收集層」。** routing groups + traffic mirroring 讓我們可以在不影響主流程的情況下鏡像到新本地模型，累積 review/verify 結果後再調整路由。
- **修正 3：task manager 候選可以分成三層，不應混在一起比較。** (a) runtime/gateway：skelm、Mastra、Temporal、Striatum；(b) dynamic workflow pattern：open-dynamic-workflows；(c) agent/team/process packs：A Team、AiPlus、compound-engineering。MVP 應選 runtime + pattern，process pack 只抽模板。
- **修正 4：review jury 已從「加分項」變成第一版應保留的 routing policy 欄位。** 不一定導入 ai-jury，但 task schema 應先有 `review_policy: none | single_non_executor | jury_quorum | panel_vote`，避免未來重改資料模型。
- **修正 5：安全/供應鏈審查要納入小 repo 評估流程。** 今天的 axon 類結果提醒：低 star 新 repo 很容易包裝成 orchestration/router，但 README 若要求下載 raw binary/zip、與描述不一致，應直接降級或排除。

### 目前最推薦的開源方向
1. **MVP 主線維持：OpenCode + Ollama + LiteLLM + 薄 task manager。**
   - OpenCode：coding executor / role shell（Build / Plan / Explore / Scout + custom reviewer）。
   - Ollama：local/private model serving baseline。
   - LiteLLM：model alias、fallback、retry、timeout、routing groups、traffic mirroring、usage/cooldown。
   - 薄 task manager：task lifecycle、policy routing、OpenCode runtime config generation、permission profile、worktree isolation、validation/review artifact。
2. **第一個現成 runtime prototype：skelm。**
   - 理由：TypeScript、opencode backend、default-deny gateway、durable/persistent workflow、local-first storage、audit journal。
   - 驗證重點：`@skelm/opencode` 是否可穩定指定 OpenCode agent/model/permission；gateway 是否真的限制 shell/filesystem/network/MCP；run log 是否足夠做審計。
3. **第一個 OpenCode-native dynamic workflow 實驗：open-dynamic-workflows plugin。**
   - 理由：若 OpenCode plugin 可直接用 host model / Ollama config，會大幅降低整合摩擦。
   - 驗證重點：plugin 安裝、OpenCode 版本相容、Ollama/local model 支援、sandbox/permission、large fan-out crash-resume 是否需要 daemon。
4. **review/security 設計參考：ai-jury。**
   - 不必直接綁定，但把 jury quorum / panel vote / chair synthesis / CI gate / large-diff chunking 納入 schema。
5. **中期 production runner 參考：Striatum。**
   - 若未來需要 daemon-owned state、leases、verdicts、Postgres、audit-chain，Striatum 的架構值得研究；MVP 暫時太重。

### 是否建議修改工作流 / 模型路由策略
- **建議修改：是，策略小幅升級，不換主棧。**
- 建議新增兩個 routing 維度：
  - `integration_mode`: `external_runner | opencode_plugin | cli_wrapper`。用來區分 skelm/Mastra、open-dynamic-workflows plugin、純 shell wrapper。
  - `experiment_policy`: `none | litellm_mirror | shadow_review | benchmark_only`。用 LiteLLM traffic mirroring 或 shadow review 收集新模型品質，不直接影響 production result。
- 建議新版 routing output 保留昨天欄位並補強：
  - `runner`: `thin-script | skelm | mastra | striatum | manual`
  - `integration_mode`: `external_runner | opencode_plugin | cli_wrapper`
  - `executor`: `opencode | aider | verify-command | jury-panel`
  - `opencode_agent`: `explore | scout | plan | build | reviewer | custom`
  - `permission_profile`: `read_only | ask_writes | worktree_write | no_shell | tests_only | network_limited`
  - `model_alias`: `local-fast | local-code | strong-code | review-local | review-strong | private-only`
  - `litellm_strategy_group`: `fast | code | review | fallback | experimental-mirror`
  - `privacy_fallback`: `local_only | cloud_allowed_after_redaction | cloud_allowed_with_approval`
  - `validation_command`: deterministic command
  - `review_policy`: `none | single_non_executor | jury_quorum | panel_vote`
  - `experiment_policy`: `none | litellm_mirror | shadow_review | benchmark_only`
  - `artifact_policy`: `save_plan | save_config | save_prompt | save_diff | save_review | save_solution_note | save_run_log | save_route_decision`
- 建議下輪實作順序：
  1. 先做 thin-script + task markdown schema，不綁 runtime。
  2. 對同一個 task 跑 skelm prototype 與 open-dynamic-workflows OpenCode plugin smoke test。
  3. LiteLLM 設定 routing groups，並對一個非關鍵 review 任務開 traffic mirroring。
  4. review 階段先做 single non-executor reviewer，再擴成 jury quorum。

### 值得持續追蹤的項目
- OpenCode 是否提供更穩定 non-interactive dispatch/session API、machine-readable run output、plugin model API 文件。
- skelm `@skelm/opencode` backend 實測成熟度與 permission gateway 是否能覆蓋 OpenCode agent 的 shell/file/network/MCP 行為。
- open-dynamic-workflows OpenCode plugin 的 keyless native mode 是否可重現，尤其在 Ollama/local model 下是否可靠。
- LiteLLM routing groups / traffic mirroring 在 coding-agent 場景下的 observability 與評估資料如何落地。
- ai-jury 的 benchmark 是否擴大到更多 fixtures、是否能穩定降低 false positives。
- Striatum 是否持續更新，尤其 terminal-agent wrapper、leases/verdicts/audit-chain 是否有可跑 demo。
- Sage Router / Mozart / Mahoraga / gnoma 類 semantic/adaptive routers 是否出現可重現 benchmark，而不只是 README 宣稱。
- 本地 coding 模型（Qwen、DeepSeek、Kimi、GLM、MiniMax）在 OpenCode + Ollama 的 patch reliability、tool-use、長上下文、review precision 實測。

### 今日摘要
今天有實質新進展，但主線不變：仍推薦 **OpenCode + Ollama + LiteLLM + 薄 task manager**。最大新增是 **open-dynamic-workflows 聲稱已有 OpenCode plugin / keyless native mode**，可直接透過 OpenCode 既有模型跑 dynamic workflow；若實測成立，會是 opencode+ollama 路線的重要加速器。**skelm 仍是第一個現成 runtime prototype 候選**，因為它明確支援 opencode backend、typed pipeline、default-deny gateway、durable/persistent workflow。另補強 LiteLLM 的定位：除了 fallback，也應用 routing groups + traffic mirroring 做本地模型 shadow experiment。建議工作流新增 `integration_mode` 與 `experiment_policy`，但暫時不要換主棧或導入重型 Striatum/Temporal。

### 來源/查核記錄
- GitHub API snapshot 2026-06-07 22:00 UTC：`anomalyco/opencode`、`opencode-ai/opencode`、`BerriAI/litellm`、`ollama/ollama`、`langchain-ai/langgraph`、`microsoft/autogen`、`crewAIInc/crewAI`、`mastra-ai/mastra`、`temporalio/temporal`、`OpenHands/OpenHands`、`Aider-AI/aider`、`scottgl9/skelm`、`Suraj1235/open-dynamic-workflows`、`berkayturanci/ai-jury`、`RBraga01/a-team`、`izhiwen/AiPlus`、`halbritt/striatum`、`earlvanze/sage-router` 等。
- OpenCode docs 2026-06-07：Agents / Build, Plan, General, Explore, Scout / JSON + markdown agent config / permissions；Config precedence / `.opencode` / `OPENCODE_CONFIG_CONTENT`。
- LiteLLM routing docs 2026-06-07：load balancing、queueing、cooldown、fallback、timeout、retry、Redis usage/cooldown、routing strategies、routing groups、traffic mirroring。
- README review 2026-06-07：`scottgl9/skelm`、`Suraj1235/open-dynamic-workflows`、`berkayturanci/ai-jury`、`RBraga01/a-team`、`izhiwen/AiPlus`、`halbritt/striatum`、`earlvanze/sage-router`、`RandallRO/axon`。

---

### 日期: 2026-06-08

### 今日新發現
- **主線活躍度仍強，沒有出現足以推翻 MVP 主棧的新框架。** GitHub API 快照 2026-06-08 22:00 UTC：`anomalyco/opencode` 約 171.7k stars、今日 push；`BerriAI/litellm` 約 49.7k stars、今日 push；`ollama/ollama` 約 173.6k stars、今日 push；`crewAIInc/crewAI`、`mastra-ai/mastra`、`temporalio/temporal`、`OpenHands/OpenHands` 今日也都有更新。`opencode-ai/opencode` 仍 archived，後續仍應排除為活躍主 repo。
- **OpenCode Agents / Config 文件今日確認更細的 permission surface。** Agents 文件除了再確認 `Build` / `Plan` / `General` / `Explore` / `Scout`，也明確列出 agent 可設定 `model`、`temperature`、`steps`、`prompt`、`permission`；permissions 可管 `read`、`edit`、`bash`、`task`、`external_directory`、`webfetch`、`websearch`、`skill`、`doom_loop` 等，且支援 per-agent override 與 Markdown agent frontmatter。這讓 task manager 可以把 `permission_profile` 更精準地編譯成 OpenCode 原生 config，而不是只靠外部 wrapper。
- **OpenCode config precedence 今天補強了 runtime override 設計。** 官方 config 文件列出 precedence：remote → global → `OPENCODE_CONFIG` custom path → project → `.opencode` directories → `OPENCODE_CONFIG_CONTENT` inline runtime override → managed config / MDM。這意味著 task manager 可用 inline config 做每次任務的臨時 agent/model/permission 佈署，同時保留 managed config 作組織級安全底線。
- **skelm 仍是第一個現成 runtime prototype 候選，且 README 更完整地支持此定位。** `scottgl9/skelm` 今日 push，約 24 stars；README 明確列出 `@skelm/opencode` backend、typed TypeScript pipelines、default-deny permissions、gateway-owned exec/network/filesystem/MCP、durable wait/resume、persistent workflows、SQLite/filesystem local-first、hash-chained tamper-evident audit journal。它最貼近「OpenCode 管 coding executor，runtime/gateway 管 orchestration 與權限」。
- **Striatum 今日活躍，從 tracking candidate 升級為中期 production runner 參考。** `halbritt/striatum` 今日 push，約 3 stars；README 描述 local workflow runner for terminal AI coding agents，核心是 daemon-owned Postgres、leases、verdicts、audit chains、repo durable artifacts、MCP/RPC control plane、parallel implement→review→repair→synthesize loops。它比 MVP 所需重，但「verdicts / leases / hash-chain / evidence-backed artifact / multi-review synthesis」值得抽到 schema 與 audit model。
- **新增候選：`JuReyms/Palabre`。** GitHub search 今日找到，約 1 star、今日 push；README 定位是讓本機多個 agent 互相辯論的 CLI orchestrator，支援 Claude Code、Codex CLI、Gemini CLI、Antigravity CLI、OpenCode via `opencode run`、Ollama local HTTP，輸出 Markdown，且提供 JSON/NDJSON event stream 作 integration API。它不是 coding implementation runner，而是「debate / architecture review / plan critique」工具，適合放入 `review_policy` 或 `decision_review` 階段設計參考。
- **新增候選：`keakon/chord`。** 約 10 stars、今日 push；它是 Go 寫的 lightweight local-first terminal coding agent，不是 OpenCode wrapper，但 README 強調 long-session context trimming、typed summaries、runtime model pool hot-swap、ordered fallback、headless JSONL control plane、subagents、git worktree parallelism，並給出 Chord v0.6.3 vs Codex CLI 的方向性 benchmark。價值在「coding shell 自身也在內建 model orchestration / long-session efficiency」，但它若作候選會與 OpenCode executor 角色重疊，暫不進 MVP 主棧。
- **新增候選：`tiny-intelligence/localcoding`。** 0 stars、今日 push；README 描述 supervised agentic coding system，重點是 stronger model/human reviewer 設邊界、審 evidence、驗 outcome，local 或低成本 worker 做 bounded implementation，含 worker packet、review/evidence example、Ollama/OpenAI-compatible worker config。這與「review-led supervision + bounded worker packets」高度一致，可作任務封包格式參考；但目前是研究樣本，不是可依賴 runtime。
- **新增/重新評估：`skgandikota/coracle`。** 今日 push但 0 stars；README 定位為 personal-machine AI gateway / RAM-aware scheduler，面向 16GB Mac M1，將 big/free-tier planning 與 local Ollama coder 分工，外部提供 OpenAI-compatible endpoint；但 opencode integration 仍標為 placeholder，授權為 CC BY-NC-SA 4.0（非典型軟體商用授權）。因此只能作「低資源 single-LLM-slot scheduler」設計參考，不宜成為主依賴。
- **AiPlus 與 Vibestrate 今日仍有更新，定位更清楚。** AiPlus 約 1 star、今日 push：project memory、role-based dispatch、handoff/compact、self-correct、tamper-evident dispatch log、token cost，適合做 process/memory/audit pack 參考。Vibestrate 約 1 star、今日 push：plan → architecture → implement → validate → review → fix → verify、worktree、CLI detection、OpenCode/Ollama 支援，仍是 supervised coding loop 的直接參考，但 stars 與成熟度仍低。
- **LiteLLM routing 結論維持但細節更可用。** docs 今日確認 routing groups 可對不同 model group 套不同 strategy 並可 runtime update；traffic mirroring 可把 production traffic 靜默鏡像到 secondary model；basic reliability 補充 deployment ordering / weighted failover。這支持把 LiteLLM 用作 model gateway + shadow experiment layer，而不是語意 task orchestrator。
- **Sage Router 仍與 LiteLLM 角色重疊但有語意 router 參考價值。** README 描述 intent / complexity / requirements / thinking-level scoring、Ollama auto-discovery、debug headers、多 API 格式、OpenClaw/Codex OAuth discovery。它很貼近 semantic model router，但成熟度與安全性仍需審查，不建議替代 LiteLLM；可借鑑 debug headers / route explanation / local-first hard filters。
- **theFactory 類 full software factory 不適合 MVP。** 今日 search 找到 `kherrera6219/theFactory`，描述完整 production lifecycle、41-agent runtime、LangGraph、Redis Streams、observability、mission control UI；這類架構證明「agentic SDLC factory」方向存在，但對 opencode + ollama 薄 task manager 來說過重。

### 對既有結論的修正
- **修正 1：OpenCode permission profile 可以比昨天建議更細。** 建議不只用 `read_only | ask_writes | worktree_write | tests_only` 這種粗分類，而是讓 task manager 產生 OpenCode 原生 permission map：`edit`、`bash`、`external_directory`、`webfetch`、`websearch`、`task`、`skill`、`doom_loop` 等都應可配置。
- **修正 2：中期 runner 候選應分為「安全 gateway runtime」與「production state daemon」。** skelm 偏 TypeScript code-first gateway/runtime，適合先 prototype；Striatum 偏 daemon-owned state、leases/verdicts/audit-chain，適合中期 production/多 lane evidence runner，不宜跟 skelm 直接一對一比較。
- **修正 3：review policy 應拆成兩種模式：jury 與 debate。** ai-jury 偏 diff/PR verdict jury；Palabre 偏多 agent debate / plan critique / architecture review。schema 可保留 `review_policy` 給 verdict，並新增 `debate_policy` 或 `decision_review_policy` 給設計決策討論。
- **修正 4：低資源本地 routing 應納入策略但不改主棧。** coracle / Chord 都提醒：在 16GB~低 VRAM 機器上，single-slot scheduling、context trimming、background compaction、model pool fallback 很重要。這應影響「local model runner policy」，但目前仍由 Ollama + LiteLLM + task manager 承擔，不另引入 coracle/chord 為核心。
- **修正 5：process/memory packs 與 runtime 不應混用。** AiPlus、A Team、compound-engineering 類工具可抽取 memory、handoff、role roster、quality gates、audit log 模板；但它們不是 model router，也不是 durable runtime，不應替代 skelm/Mastra/Striatum/LiteLLM。

### 目前最推薦的開源方向
1. **MVP 主線維持：OpenCode + Ollama + LiteLLM + 薄 task manager。**
   - OpenCode：coding executor / role shell / agent permission surface。
   - Ollama：local/private model serving baseline。
   - LiteLLM：model alias、routing groups、fallback、retry、timeout、traffic mirroring、usage/cooldown。
   - 薄 task manager：task lifecycle、policy routing、OpenCode runtime config generation、permission map、worktree isolation、validation/review/debate artifact。
2. **第一個現成 runtime prototype：skelm。**
   - 優先驗證 `@skelm/opencode` backend、default-deny gateway、per-step permissions、hash-chained audit journal、durable wait/resume。
   - 若成功，可把自製 markdown task schema 交給 skelm runner 執行。
3. **第二個 OpenCode-native experiment：open-dynamic-workflows plugin。**
   - 優先 smoke test 其 OpenCode plugin keyless native mode 與 Ollama/local model 相容性。
   - 若成立，可作「大 fan-out / dynamic workflow」補充，不替代 skelm/thin-script 的 deterministic lifecycle。
4. **中期 production runner 參考：Striatum。**
   - 借鑑 leases、verdicts、audit chains、evidence-backed artifacts、multi-review synthesis。
   - 暫不導入 daemon/Postgres 作 MVP，避免部署成本過高。
5. **review/debate 工具參考：ai-jury + Palabre。**
   - ai-jury：diff/PR/issue review jury、chair synthesis、panel vote、CI gate。
   - Palabre：plan/architecture debate、NDJSON event stream、Markdown export。
6. **低資源策略參考：Chord + coracle。**
   - Chord：context trimming、model pools、fallback、headless JSONL、worktree parallelism。
   - coracle：single-LLM-slot scheduler、status without LLM、RAM-aware local/cloud split。

### 是否建議修改工作流 / 模型路由策略
- **建議修改：是，小幅但具體；不換主棧。** 今日建議把 OpenCode 原生 permission map、debate policy、resource policy 納入 routing output。
- 建議新版 routing/task schema 補強欄位：
  - `opencode_permission_map`: `{ read, edit, bash, external_directory, webfetch, websearch, task, skill, doom_loop }`
  - `runner`: `thin-script | skelm | mastra | striatum | manual`
  - `integration_mode`: `external_runner | opencode_plugin | cli_wrapper | debate_cli`
  - `executor`: `opencode | aider | verify-command | jury-panel | debate-panel`
  - `review_policy`: `none | single_non_executor | jury_quorum | panel_vote`
  - `debate_policy`: `none | two_agent_debate | multi_agent_debate | chair_synthesis`
  - `resource_policy`: `normal | low_ram_single_slot | no_parallel_llm | allow_parallel_review`
  - `litellm_strategy_group`: `fast | code | review | fallback | experimental-mirror`
  - `artifact_policy`: `save_plan | save_config | save_prompt | save_diff | save_review | save_debate | save_solution_note | save_run_log | save_route_decision`
- 建議下輪實作 / 實測順序：
  1. 先把 task schema 的 permission 欄位對齊 OpenCode 原生 permission keys。
  2. 對一個低風險 repo task 產生 `OPENCODE_CONFIG_CONTENT`，測 `plan/read-only/reviewer` agent 是否按 permission 工作。
  3. skelm 跑同一個 task 的 minimal `agent({ backend: 'opencode' })` prototype。
  4. open-dynamic-workflows plugin 做 keyless native smoke test。
  5. Palabre / ai-jury 只做 review/debate sidecar，不讓它們寫 repo。
  6. LiteLLM 開一個非關鍵 `review-local` traffic mirror，收集本地模型 shadow output，不影響主結果。

### 值得持續追蹤的項目
- OpenCode permission / plugin / non-interactive run API 是否更穩定，尤其 machine-readable output、agent/subagent dispatch、plugin model API。
- skelm `@skelm/opencode` backend 的真實 permission enforcement：是否能限制 OpenCode agent 的 shell、filesystem、network、MCP、external directory。
- open-dynamic-workflows OpenCode plugin keyless native mode 是否可重現，尤其 Ollama/local model、large fan-out、crash-resume、sandbox 權限。
- Striatum 是否有可輕量試跑 demo；leases/verdicts/audit-chain 是否可抽成不需 Postgres 的簡版。
- Palabre 的 NDJSON event stream 是否適合接進 task artifact；多 agent debate 對架構決策是否真的提升品質。
- Chord 的 headless JSONL / model pools / context trimming 是否能被 OpenCode 生態借鑑，或未來作 executor 替代候選。
- coracle 是否補上 opencode integration、授權是否調整、pre-alpha 是否變成可測 runtime。
- LiteLLM routing groups / traffic mirroring 如何與 deterministic validation result 關聯成模型品質資料集。
- 本地 coding 模型（Qwen、DeepSeek、Kimi、GLM、MiniMax）在 OpenCode + Ollama 的 patch reliability、tool-use、長上下文、review precision 實測。

### 今日摘要
今天有實質新進展，但主線不變：仍推薦 **OpenCode + Ollama + LiteLLM + 薄 task manager**。最大更新是 OpenCode permission/config surface 更明確，task manager 可以直接產生 per-task `OPENCODE_CONFIG_CONTENT` 與原生 permission map；**skelm 仍是第一個現成 runtime prototype**，**Striatum 升級為中期 production runner 參考**。新增值得追蹤的是 **Palabre**（多 agent debate / NDJSON / Markdown export）、**Chord**（local-first coding shell、model pools、context trimming、headless JSONL）與 **LocalCoding**（review-led supervision / bounded worker packets）。建議工作流小幅修改：在 routing output 補上 `opencode_permission_map`、`debate_policy`、`resource_policy`，並把 Palabre/ai-jury 放在 read-only review/debate sidecar，而不是讓它們寫 repo。

### 來源/查核記錄
- GitHub API snapshot 2026-06-08 22:00 UTC：`anomalyco/opencode`、`opencode-ai/opencode`、`BerriAI/litellm`、`ollama/ollama`、`langchain-ai/langgraph`、`microsoft/autogen`、`crewAIInc/crewAI`、`mastra-ai/mastra`、`temporalio/temporal`、`OpenHands/OpenHands`、`Aider-AI/aider`、`scottgl9/skelm`、`Suraj1235/open-dynamic-workflows`、`berkayturanci/ai-jury`、`halbritt/striatum`、`earlvanze/sage-router`、`RBraga01/a-team`、`izhiwen/AiPlus`、`guyshonshon/vibestrate`、`skgandikota/coracle`、`keakon/chord`、`JuReyms/Palabre` 等。
- OpenCode docs 2026-06-08：Agents / Build, Plan, General, Explore, Scout / agent JSON + Markdown config / model、temperature、steps、permissions；Config precedence / `OPENCODE_CONFIG_CONTENT` / managed config。
- LiteLLM routing docs 2026-06-08：routing strategies、routing groups、traffic mirroring、deployment ordering、weighted failover、fallback/retry/cooldown/Redis usage。
- README review 2026-06-08：`scottgl9/skelm`、`halbritt/striatum`、`Suraj1235/open-dynamic-workflows`、`berkayturanci/ai-jury`、`JuReyms/Palabre`、`keakon/chord`、`tiny-intelligence/localcoding`、`skgandikota/coracle`、`izhiwen/AiPlus`、`guyshonshon/vibestrate`、`earlvanze/sage-router`、`kherrera6219/theFactory`。

---

### 日期: 2026-06-09

### 今日新發現
- **主線活躍度仍強，沒有出現足以取代 MVP 主棧的新框架。** GitHub API 快照 2026-06-09 22:00 UTC：`anomalyco/opencode` 約 172.1k stars、今日 push；`BerriAI/litellm` 約 49.8k stars、今日 push；`ollama/ollama` 約 173.7k stars、今日 push；`langchain-ai/langgraph`、`crewAIInc/crewAI`、`mastra-ai/mastra`、`temporalio/temporal`、`OpenHands/OpenHands` 今日也都有更新。`Aider-AI/aider` 最近 push 仍停在 2026-05-22，但社群關注與 terminal coding agent 角色仍穩。
- **OpenCode Agents / Config 結論維持，且足以支撐 per-task runtime config。** 官方 docs 今日確認 primary agents `Build` / `Plan`、subagents `General` / `Explore` / `Scout`；agent 可用自訂 prompt、model、tool access；`Plan` 預設 edits/bash ask，`Explore`/`Scout` read-only。Config precedence 仍包含 `.opencode` 與 `OPENCODE_CONFIG_CONTENT` inline runtime override，表示 task manager 可以把任務策略編譯成一次性的 OpenCode agent/model/permission config。
- **LiteLLM 仍是模型 gateway 首選，但今日更應強調「硬限流/可觀測 routing」。** Load balancing docs 明確列出 `simple-shuffle`、`least-busy`、`usage-based-routing`、`latency-based-routing`、`cost-based-routing`，並支援 `enforce_model_rate_limits` 將 RPM/TPM 變成 pre-call hard limit。這對 local Ollama/小 GPU 特別重要：不只要 fallback，也要避免同時 fan-out 把本機模型打爆。
- **skelm 今日仍是第一個現成 runtime prototype 候選。** `scottgl9/skelm` 今日 push，約 25 stars；README 仍明確展示 `agent({ backend: 'opencode', permissions: ... })`、typed TypeScript pipelines、default-deny permissions、gateway-owned exec/network/filesystem/MCP、durable wait/resume、persistent workflows。它仍最貼近「OpenCode 作 executor，runtime/gateway 作 orchestration 與權限邊界」。
- **Striatum 今日持續更新，從「中期參考」更像 production-state runner 藍圖。** `halbritt/striatum` 今日 22:00 UTC push；README 明確描述 terminal coding agent workflow runner，提供 multi-lane implement → review → repair → synthesize loops、leases、verdicts、daemon-owned Postgres、hash-chained audit log、repo durable Markdown artifacts、`corpus export` redacted JSONL。它太重，不建議 MVP 導入，但它的 `leases/verdicts/evidence/corpus export` 應提前進 schema 思考。
- **Palabre 今日持續更新，定位更清楚：read-only debate / decision-review sidecar。** `JuReyms/Palabre` 今日 push；README 說它可驅動 Claude Code、Codex CLI、Gemini CLI、Antigravity、OpenCode via `opencode run`、Ollama local HTTP，並提供 versioned JSON / NDJSON event stream、Markdown export。這非常適合 `debate_policy` 或 architecture/plan critique，不應作 implementation runner。
- **AiPlus 今日升級為「process/memory/audit pack」參考。** `izhiwen/AiPlus` 今日 push；README 強調 project memory、role-based dispatch、handoff/compact reminder、status、self-correct、tamper-evident hash-chain dispatch log、local JSONL memory。它不是 model router/runtime，但可借鑑「memory → dispatch → team → handoff → status → self-correct → audit」七段式流程，尤其是 long-session handoff 與 project memory。
- **新增較成熟的桌面/IDE 類候選：`generalaction/emdash`。** 約 4.8k stars、今日 push；README 定位為 desktop app，能在多個 git worktree 並行跑 Claude Code、Codex、OpenCode、Gemini、Amp 等 coding agents，支援 ticket ingestion、diff review、PR/CI/merge、local 或 SSH remote machines。它不是本地 Ollama router，也不是薄 CLI task manager，但證明「worktree-per-agent + parallel coding agent management + review/merge UI」已在產品化；可作 UI/ops 層長期參考。
- **新增/重看 CAST：`ek33450505/claude-agent-team`。** 約 6 stars、今日 push；雖偏 Claude Code，不是 OpenCode/Ollama 主線，但 README 提到 hook enforcement、SQLite audit trail、typed agent registry、23 agents、model tier assignment、1199 BATS tests、commit/push hard-block。其價值是 hook-gated lifecycle / local audit / role frontmatter contract，可抽象成 OpenCode task manager 的安全與品質 gate 模板。
- **其他今日新訊號多為低 star process/swarm 包。** 如 `Agentic-Vibe-Fleet`、`Termy`、`gaviero`、`GODMODE` 等，方向集中在 terminal coding-agent orchestration / multi-agent IDE / cross-model debate，但目前成熟度、供應鏈可信度或與 opencode+ollama 的貼合度不足，只列觀察，不納入主候選。

### 對既有結論的修正
- **修正 1：MVP 主棧不變，但 `resource_policy` 應升級為一級欄位。** LiteLLM hard RPM/TPM limits 與 routing strategy 提醒我們，本地 Ollama 不是無限資源；task manager 應能標記 `low_ram_single_slot`、`no_parallel_llm`、`rate_limit_group`，避免 parallel review/debate 壓垮本地模型。
- **修正 2：Striatum 的 schema 概念值得提前吸收。** 之前只把 Striatum 當 production runner 參考；今天建議把 `lease`、`verdict`、`evidence_bundle`、`corpus_export`、`audit_chain` 這些概念先放進中期資料模型，哪怕 MVP 仍用 markdown/YAML + thin-script。
- **修正 3：Palabre/AiPlus/CAST/Emdash 不能混成 runner 比較。** Palabre 是 debate sidecar，AiPlus/CAST 是 process + gate + audit pack，Emdash 是 desktop ops/worktree UI，skelm/Striatum 才是 runner/runtime 類；比較時應分層，避免選型混亂。
- **修正 4：桌面 UI / remote machine orchestration 是長期 ops 層，不是 MVP 必需。** Emdash 類工具值得追蹤，但目前主需求是 opencode+ollama task manager；先把可 diff、可審核、可測的 CLI/task-file 層做好，再考慮 UI。
- **修正 5：Claude/Codex 生態的 hook/agent registry 設計可借鑑，但不能直接套用。** CAST 類工具的 commit/push hard-block、typed agent registry、SQLite audit 很有價值；但因 OpenCode permission/config 已有原生 surface，OpenCode 路線應優先編譯到 OpenCode config，而不是複製 Claude Code hook 假設。

### 目前最推薦的開源方向
1. **MVP 主線維持：OpenCode + Ollama + LiteLLM + 薄 task manager。**
   - OpenCode：coding executor / role shell / per-agent permission config。
   - Ollama：local/private model serving baseline。
   - LiteLLM：model alias、fallback、routing strategy、hard rate limits、usage/cooldown、shadow/mirror experiments。
   - 薄 task manager：task lifecycle、policy routing、OpenCode runtime config generation、permission map、resource policy、worktree isolation、validation/review/debate artifact。
2. **第一個現成 runtime prototype 仍是 skelm。**
   - 優先驗證 `@skelm/opencode` backend、permission gateway、per-step fs/network/exec/MCP boundaries、durable wait/resume、audit journal。
3. **中期 production-state runner 參考：Striatum。**
   - 不建議 MVP 上 Postgres/daemon，但建議借鑑 leases、verdicts、evidence-backed artifacts、hash-chain audit、redacted JSONL corpus export。
4. **review/debate/process sidecars：ai-jury + Palabre + AiPlus/CAST。**
   - ai-jury：diff/PR verdict jury。
   - Palabre：architecture/plan debate + NDJSON/Markdown export。
   - AiPlus/CAST：project memory、handoff、role registry、hook/quality gate、audit log 模板。
5. **長期 ops/UI 參考：Emdash。**
   - 若未來要多人/多 repo/遠端機器/票務入口/PR merge UI，可研究 Emdash；目前不應替代 CLI-first task manager。

### 是否建議修改工作流 / 模型路由策略
- **建議修改：是，小幅但重要；不換主棧。** 今天建議把 `resource_policy`、`rate_limit_group`、`verdict/evidence`、`ops_ui_candidate` 這些概念納入 schema/roadmap。
- 建議 routing/task schema 補強：
  - `resource_policy`: `normal | low_ram_single_slot | no_parallel_llm | allow_parallel_review | remote_runner_ok`
  - `rate_limit_group`: `local-ollama-small | local-ollama-code | cloud-fallback | review-mirror`
  - `runner`: `thin-script | skelm | mastra | striatum | manual`
  - `integration_mode`: `external_runner | opencode_plugin | cli_wrapper | debate_cli | desktop_ops`
  - `executor`: `opencode | aider | verify-command | jury-panel | debate-panel`
  - `opencode_permission_map`: `{ read, edit, bash, external_directory, webfetch, websearch, task, skill, doom_loop }`
  - `review_policy`: `none | single_non_executor | jury_quorum | panel_vote`
  - `debate_policy`: `none | two_agent_debate | multi_agent_debate | chair_synthesis`
  - `verdict_policy`: `none | record_pass_fail | record_needs_revision | synthesize_final_verdict`
  - `artifact_policy`: `save_plan | save_config | save_prompt | save_diff | save_review | save_debate | save_verdict | save_evidence_bundle | save_solution_note | save_run_log | save_route_decision`
- 建議下一輪實測順序：
  1. 先把 OpenCode permission map schema 固化，並產一份 `OPENCODE_CONFIG_CONTENT` 範例。
  2. LiteLLM 設 `local-code` / `review-local` 的 hard RPM/TPM 或 single-slot policy，避免本地 fan-out。
  3. 用同一個低風險 repo task 跑 thin-script baseline 與 skelm minimal opencode backend smoke test。
  4. Palabre 只作 plan/debate sidecar，輸出 NDJSON/Markdown，不讓它改 repo。
  5. 把 review 結果寫成 `verdict + evidence_bundle`，為未來 Striatum/production runner 保留相容欄位。

### 值得持續追蹤的項目
- OpenCode 是否推出更穩定 non-interactive dispatch/session API、machine-readable run output、plugin model API、permission map 文件更新。
- skelm `@skelm/opencode` backend 實測是否真的可控 OpenCode agent 的 shell/filesystem/network/MCP 行為。
- Striatum 是否出現輕量 demo 或不需 Postgres 的模式；其 leases/verdicts/audit-chain/corpus export 能否抽成通用 schema。
- Palabre NDJSON v1 是否穩定，是否適合直接接入 task artifact / debate transcript。
- LiteLLM hard rate limit、routing groups、traffic mirroring 如何和 local Ollama capacity / validation result 綁成模型品質資料集。
- AiPlus/CAST 的 memory/handoff/hook-gate/audit 設計能否抽出成 OpenCode-compatible templates。
- Emdash 的 OpenCode support、worktree lifecycle、remote machine orchestration、PR/CI review UI 是否成熟到能作 ops layer。
- 本地 coding 模型（Qwen、DeepSeek、Kimi、GLM、MiniMax）在 OpenCode + Ollama 的 patch reliability、tool-use、長上下文、review precision、低 RAM single-slot 表現。

### 今日摘要
今天有實質新進展，但主線不變：仍推薦 **OpenCode + Ollama + LiteLLM + 薄 task manager**。最大更新是策略更偏「資源與證據治理」：LiteLLM 的 hard RPM/TPM limit 應用來保護本地 Ollama；Striatum 的 leases/verdicts/evidence/corpus export 應納入中期 schema；Palabre 適合作 read-only debate sidecar；AiPlus/CAST 可借鑑 memory/handoff/hook-gate/audit；Emdash 則代表長期 ops/UI 層。建議工作流小幅修改：新增 `resource_policy`、`rate_limit_group`、`verdict_policy`、`evidence_bundle`；下一步仍應先做 thin-script schema + skelm opencode backend smoke test，不要急著導入重型 daemon 或桌面平台。

### 來源/查核記錄
- GitHub API snapshot 2026-06-09 22:00 UTC：`anomalyco/opencode`、`BerriAI/litellm`、`ollama/ollama`、`langchain-ai/langgraph`、`microsoft/autogen`、`crewAIInc/crewAI`、`mastra-ai/mastra`、`temporalio/temporal`、`OpenHands/OpenHands`、`Aider-AI/aider`、`scottgl9/skelm`、`Suraj1235/open-dynamic-workflows`、`berkayturanci/ai-jury`、`halbritt/striatum`、`JuReyms/Palabre`、`keakon/chord`、`tiny-intelligence/localcoding`、`skgandikota/coracle`、`izhiwen/AiPlus`、`guyshonshon/vibestrate`、`earlvanze/sage-router`、`RBraga01/a-team`、`ucav/mozart-router`、`pockanoodles/Mahoraga`、`aiagentflow/aiagentflow`、`VikingOwl91/gnoma`、`XAIHT/Tlamatini`。
- GitHub search 2026-06-09：`opencode ollama orchestration`、`local coding agent orchestrator ollama`、`terminal AI coding agents orchestration` 等查詢；新增觀察 `generalaction/emdash`、`ek33450505/claude-agent-team`、`kacperpietrzyk/Termy`、`neich/gaviero` 等。
- OpenCode docs 2026-06-09：Agents / Build, Plan, General, Explore, Scout；Config precedence / `.opencode` / `OPENCODE_CONFIG_CONTENT`。
- LiteLLM docs 2026-06-09：load balancing strategies、deployment ordering、`enforce_model_rate_limits` hard RPM/TPM limit。
- README review 2026-06-09：`scottgl9/skelm`、`halbritt/striatum`、`JuReyms/Palabre`、`izhiwen/AiPlus`、`ek33450505/claude-agent-team`、`generalaction/emdash`。
