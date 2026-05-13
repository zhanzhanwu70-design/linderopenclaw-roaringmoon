更新日期：2026-05-12（晚間）

---

## 今日新發現

### 1. Archon — 開源 AI coding workflow engine
- Repo: `coleam00/Archon`
- 定位：首個開源「AI coding harness builder」，目標是讓 AI coding 流程可預測、可重複
- 核心概念：將開發流程編碼成 YAML workflow（plan → implement → validate → review → PR）
- 特色：每個 workflow run 有獨立 git worktree，可並列跑 5 個任務不衝突；AI 只在必要處運行，其餘用 deterministic bash/test 替代
- 類比：Dockerfile 之于基礎設施，GitHub Actions 之于 CI/CD，Archon 之于 AI coding workflows
- 評價：**高度值得關注**，直接解決「AI coding 每次行為不一致」的痛點，與 OpenCode/Ollama 生態天然互補

### 2. oh-my-openagent（OmO）— OpenCode 專用 harness
- Repo: `code-yeongyu/oh-my-openagent`
- 定位：OpenCode 的 team orchestration 層，支援多模型協作
- Team Mode 展示：同時調用 Kimi K2.6 + GPT-5.5
- 宣言：「模型每月變便宜、變聰明，沒有單一 provider 會主導，我們為開放市場而建構」
- 評價：**直接相關**，適合與 Ollama 整合做本地多模型路由

### 3. Agent Deck — 多 agent 終端 session 管理
- Repo: `asheshgoplani/agent-deck`
- 定位：終端 TUI，統一管理 Claude Code、OpenCode、Codex、Gemini 等多個 coding agent
- 功能：session 分組、快速切換、Fork 對話（保留完整歷史）、git worktree 整合
- 支援：Claude Code Skill + OpenCode 內建 Claude skill 兼容性
- 評價：對多 agent 並行工作流有幫助，但非 orchestration 層

### 4. Vibe Kanban — 規劃 → 執行 → Review 的 kanban 介面
- Repo: `BloopAI/vibe-kanban`
- 定位：將 coding agent 執行流程嵌入 kanban 板
- 功能：Issue 規劃 → Agent workspace（分支 + 終端 + dev server）→ Diff review → PR merge
- 支援：Claude Code、Codex、Gemini CLI、OpenCode 等 10+ coding agent
- 評價：**是 archon 的 UI 化版本**，適合需要人類介入審查的開發團隊

### 5. AgentsMesh — AI Agent 企業級 workforce 平台
- Repo: `AgentsMesh/AgentsMesh`
- 定位：遠程 AI 工作站（AgentPods）+ 多 agent 協作 + 任務追蹤
- 特色：Kanban 板綁定 ticket-pod、支援 Claude Code/Codex/Gemini CLI/Aider/OpenCode、自託管 runner、多租戶 RBAC
- 評價：偏企業級，本地 single-user 場景稍嫌複雜

### 6. OpenRelay — 多 Provider 配額統一代理
- Repo: `romgX/openrelay`
- 定位：彙聚多個 AI provider 配額（Groq、Cerebras、Gemini、DeepSeek、Ollama 等 34 個端點）到單一面板
- 特色：一鍵配置 Claude Code/Aider/OpenClaw 等工具的模型；可合併多個 Provider 配額成虛擬模型（如 "fast-group" = Groq + Cerebras）
- 評價：**非常適合本地多模型路由場景**，與 Ollama 整合潛力高

### 7. Strands Agents SDK — 模型驅動的 Python agent 建構
- Repo: `strands-agents/sdk-python`
- 定位：輕量級 Python SDK，model-driven approach
- 特色：支援 Ollama、Bedrock、Anthropic、LiteLLM 等；內建 MCP；支援 multi-agent 系統
- 評價：Python 生態豐富，適合與 LangGraph/本地 Ollama 整合

### 8. oh-my-claudecode — Claude Code 多 agent orchestration
- Repo: `Yeachan-Heo/oh-my-claudecode`
- 定位：Teams-first multi-agent orchestration for Claude Code
- 特色：NPM 包 / marketplace 安裝，零學習曲線
- 評價：綁定 Claude Code 本身，與 OpenCode + Ollama 軸線稍遠

---

## 對既有結論的修正

1. **Archon 是真正填補空白的开源项目** — 之前我們推薦的 `orchestra` + `clawcal` 方向，Archon 以更完整的形態實現了類似願景，並已有實際可用的 YAML workflow 定義。建議将 Archon 提升為核心候選。

2. **OpenRelay 解决了本地多模型路由的核心痛點** — 過去 LiteLLM 方案偏向 API proxy，OpenRelay 直接面對「多個 provider 配額分散」的實際問題，對本地 coding agent 場景更貼切。建議 LiteLLM + OpenRelay 雙軌並行評估。

3. **oh-my-openagent 值得重新關注** — 雖然之前我們對 OpenCode 生態的關注不足，但 OmO 的 team mode 展示了多模型協作的實際可行性，且與 Ollama 本地部署高度相容。

4. **Mastra 的關注優先級下調** — Mastra 仍是強大的 TypeScript 框架，但在本地 coding agent 這個細分場景中，Archon、OmO、OpenRelay 的針對性更強。Mastra 適合作為更廣義 AI 應用構建的后備選項。

---

## 當前最推薦的開源方向（更新版）

### 🥇 第一優先：Archon + OpenCode + Ollama
- **Archon** 作為 workflow engine（YAML 定義開發流程，AI 在關鍵步驟介入，deterministic 節點保證可重複性）
- **OpenCode**（或 omO）作為本地 coding agent
- **Ollama** 管理本地模型（Qwen2.5-Coder、CodeLlama、DeepSeek-Coder 等）
- 適合：單人/小團隊，想要可控、可重複的 AI coding 工作流

### 🥈 第二優先：LiteLLM + OpenRelay 雙軌
- **LiteLLM** 處理模型路由邏輯（動態任務分配、負載均衡、cost tracking）
- **OpenRelay** 處理多 provider 配額統一（Groq、Cerebras、DeepSeek 等免費/低成本配額）
- 適合：需要混合本地 + 雲端模型的場景，追求成本效益

### 🥉 第三優先：Vibe Kanban 配合 Archon 使用
- **Vibe Kanban** 提供人類可讀的 kanban 介面（規劃 → 執行 → Review）
- **Archon** 提供底層 workflow engine
- 適合：需要人類介入審查、團隊協作的場景

---

## 本地模型候選更新

| 模型 | 角色 | 備註 |
|------|------|------|
| Qwen2.5-Coder-32B | 本地主力 coding model | Ollama 首選 |
| CodeLlama-34B | 備用 coding model | 需求較低場景 |
| DeepSeek-Coder-33B | API 備選 | OpenRelay 可接入 |
| Gemma 4-12B | 輕量推理 / 路由决策 | 仍值得關注 |

---

## 持續追蹤項目

1. **Archon 生態成熟度** — 需觀察 YAML workflow 是否有社群持續貢獻、是否支援 MCP 工具擴展
2. **oh-my-openagent 的 OpenCode 版本** — 該專案同時有 `oh-my-claudecode` 和 `oh-my-codex`，需確認 OpenCode 支援程度
3. **Strands Agents + Ollama 整合** — SDK 支援 Ollama，本地 Python 工作流可能用得上
4. **LiteLLM 對 Ollama 的路由穩定性** — 仍需實際測試延遲與錯誤率

---

## 文件位置
`/home/node/.openclaw/workspace-roaringmoon/本地多模型-task-manager-每日研究.md`