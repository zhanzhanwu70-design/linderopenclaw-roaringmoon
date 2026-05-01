# 影片文字簡報整理

影片：一个视频搞懂：Harness Engineering到底是什么？以及它和提示词工程和上下文工程有什么关系？
連結：https://www.youtube.com/watch?v=vbz0tu2UslY
作者：白白说大模型
時長：約 20 分 07 秒

## 一、影片核心結論

這支影片要回答三件事：
1. 什麼是 Prompt Engineering（提示詞工程）
2. 什麼是 Context Engineering（上下文工程）
3. 什麼是 Harness Engineering（駕馭工程）

作者的核心論述是：
- Prompt Engineering 解決模型「亂說話」與輸出不穩定的問題。
- Context Engineering 解決在有限上下文窗口內，如何把最合適的資訊送進模型的問題。
- Harness Engineering 則是把記憶、執行、回饋、編排等能力包成一個工程外殼，讓模型真正變成能工作的 Agent。

作者最後給出的公式非常重要：

> Agent = 大模型 + Harness

只要不是模型權重本身的那一部分，大多都可以視為 Harness Engineering 的範疇。

---

## 二、逐段理解

## 1. Prompt Engineering：怎麼跟模型說話

影片前半段先把大模型還原成最基本的樣子：
- 模型本質上是磁碟上的大型參數檔
- 載入顯卡記憶體後，透過 API 服務對外提供能力
- 其工作就是根據輸入內容預測下一個 token

因此，如果輸入指令太含糊，輸出就會發散。為了讓它更穩定，使用者會加入：
- 角色設定
- 背景資訊
- 歷史對話
- 參考文件
- 約束條件
- 輸出格式

這些共同構成提示詞，而有意識地設計這些提示詞，使模型穩定地朝目標輸出，就是 Prompt Engineering。

## 2. Context Engineering：模型應該看到什麼

影片第二段指出：
- 模型回答不準，往往是因為知道的不夠多
- 因此人們會持續把更多資料塞進模型
- 提示詞只是上下文的一部分
- 但上下文窗口有限，長對話會造成「上下文腐化」

作者把 Context Engineering 拆成三步：
1. **召回**：找出最相關資訊（歷史對話、外部資料、程式碼、錯誤訊息等）
2. **壓縮**：將資訊變小，例如先做摘要
3. **組裝**：調整資訊位置與順序，讓進入模型的上下文更緊密、更相關

影片特別強調：
- 就算使用同一個模型，不同工具因為上下文工程策略不同，效果也會差很多。

## 3. Harness Engineering：讓模型不只會聊天，而是會做事

影片第三段把模型從「只能聊天」拉到「可以執行任務」：
- 加上 Bash 沙箱
- 加上檔案系統
- 加上 MCP 等工具能力

於是模型可以：
- 讀寫檔案
- 執行命令
- 跑測試
- 回收執行錯誤再繼續推理

這形成了 ReAct 風格的循環：
- 提示詞工程 + 上下文工程負責組裝上下文
- 模型負責思考
- 外部程序負責執行
- 執行結果再回流到上下文中

影片進一步指出：Agent 會因為上下文膨脹與資訊汙染而逐漸跑偏，因此需要把一些穩定的核心資訊固定保留，例如：
- 專案目標
- 技術棧
- 背景
- 風格規範
- 禁止事項

作者稱這些為「規則文件」，例如：
- `CLAUDE.md`
- 或各家工具的 rules 檔

當這些文件變長，就要拆分，並在需要時再路由讀取。這構成了**記憶層**。

再加上：
- **執行層**（tools、shell、file system）
- **回饋層**（測試、錯誤、自動修復）
- **編排層**（任務拆解、階段規劃、全局控制）

這些層共同組成「包裹著大模型的工程外殼」，也就是 Harness Engineering。

## 4. Harness Engineering 如何落地

影片最後談落地方式，以 Claude Code / CLAUDE.md 為例：
- 最輕量的方式，是在 `CLAUDE.md` 裡清楚寫出背景、目標、限制、測試要求、Skill 使用規則
- 更進一步的方式，是引入像 **SpecKit** 這類擴充，將需求拆成多階段：
  - 生成約束
  - 明確需求
  - 制定計畫
  - 拆解任務
  - 最後修改與測試
- 每一階段都可能更新一次規則文件，讓每次注入模型的上下文都盡量只保留核心資訊

影片把這種方式叫做：
- **Spec-Driven Development (SDD)**

並把它視為 Harness Engineering 的一種工程化落地實踐。

---

## 三、你應該真正學會的東西

### 1. 三者不是互斥，而是層層包含
- Prompt Engineering ⊂ Context Engineering ⊂ Harness Engineering

### 2. Harness 不是單一 prompt，而是一整套系統設計
你不能只問「system prompt 怎麼寫」，還要問：
- 工具怎麼接
- 記憶怎麼存
- 任務怎麼拆
- 測試怎麼回饋
- 錯誤怎麼修
- 規則文件怎麼切

### 3. 同模型不同框架效果差很多，核心原因在 Harness
這正是你最近研究 OpenClaw、opencode、LangGraph、Ollama、ROS2 skill 時最該抓住的重點。

---

## 四、我對影片內容的評價

### 優點
- 脈絡清楚：從 prompt → context → harness 一路往上講
- 對初學者友善：先用聊天模型切入，再帶到 agent
- 很適合建立大局觀

### 侷限
- 一些術語和案例偏 Claude Code / coding agent 視角
- 對具體技術實作（例如 tool schema、permission model、search/browse/mcp）的細節講得不夠深
- 「全網資料不齊如有差異以我為準」這種說法偏個人風格，不應當成嚴格來源標準

---

## 五、用一句話教會你

> Prompt Engineering 是教模型怎麼回答，Context Engineering 是決定模型看到什麼，Harness Engineering 是把模型放進一個可執行、可記憶、可回饋、可編排的工程系統裡，讓它真正能交付任務。
