# Agent Communication Timeout Remediation Plan

## 目標

把目前 agent-to-agent 通訊中的 timeout 問題，從模糊的「沒回應」拆解成可觀測、可診斷、可逐步修復的系統問題。

本文件聚焦於：
- `sessions_send` timeout
- delivery / reply 狀態不明
- agent 忙碌、heartbeat、cron 與 session/context 肥大造成的延遲
- 重要任務需要可靠送達與確認

---

## 問題定義

目前系統中，`sessions_send` 的 timeout 可能來自多種不同原因，但現況沒有足夠觀測能力去區分：

1. 訊息根本沒送到目標 agent
2. 訊息已送達，但對方 agent 沒即時處理
3. 對方已產生回覆，但 reply / announce 回傳鏈路卡住
4. 對方 session/context 太肥，導致回覆生成慢
5. heartbeat / cron / monitor / 一般訊息與 agent 協作訊息混在一起排隊

因此，當前最核心的問題不是單純「timeout 太多」，而是：

> 系統無法清楚分辨送達、已讀、回覆、完成這幾個階段。

---

## 現況觀察

### 已知事實
- `sessions_send` 可能 timeout，但事後人工確認發現對方其實有收到
- 重要 agent 訊息常需要人工補確認
- 多個 agent 共享同一套 OpenClaw runtime 與通訊環境
- 有 heartbeat / cron / monitor 等背景活動
- 某些 session/context 已經很肥，容易拖慢推理與回覆

### 已知限制
- 目前缺少 delivery / reply 分離的狀態模型
- 缺少 agent activity monitor
- 缺少專門觀測 `sessions_send` 的 telemetry
- 缺少正式的 agent-to-agent ACK 協議

---

## 根因假設排序

### 高機率
1. **接收方 session/context 太肥**
   - 造成 prompt build 與回覆生成變慢
2. **多 agent + heartbeat / cron 排隊造成延遲**
3. **`sessions_send` 將送達與回覆視為同一個 timeout 窗口**
4. **回覆鏈路（announce / routing）偶發卡住**

### 次高機率
5. **monitor / hooks / logging 同步阻塞**
6. **模型本身延遲或 provider 偶發慢回**
7. **agent 沒有明確的 ACK / RUN / DONE 行為規範**

---

## 修復原則

### 1. delivery 與 reply 必須分離
不要再把 timeout 直接等同於「沒收到」。

### 2. 重要任務先求確認，再求完成
先收到 `ACK`，再追蹤執行狀態與最終完成。

### 3. 重要 agent 訊息要有更高優先級
不能和 heartbeat / cron / 普通聊天完全混在同一層 queue。

### 4. 先做可觀測，再談優化
沒有 telemetry，就只是在猜。

### 5. timeout 應分層
- delivery timeout
- reply timeout
- completion timeout

---

## 目標狀態模型

每個 agent-to-agent 任務應至少有以下狀態：

| 狀態 | 意義 |
|---|---|
| `sent` | 已送出 |
| `delivered` | 已送達目標 session |
| `seen` | 對方 agent 已讀 / 開始處理 |
| `acknowledged` | 對方明確 ACK |
| `running` | 對方正在執行任務 |
| `replied` | 對方已正式回覆 |
| `completed` | 任務完成 |
| `blocked` | 任務卡住 |
| `failed` | 任務失敗 |

---

## 通訊協議（Agent ACK Protocol v1）

### 所有重要 agent-to-agent 任務都應使用以下狀態碼

- `ACK` = 已收到
- `RUN` = 開始處理
- `DONE` = 完成
- `BLOCK` = 卡住
- `ASK` = 需要更多資訊

### 建議訊息格式

```text
[ACK] 已收到任務：研究 agent harness
[RUN] 開始處理，預估 10 分鐘
[DONE] 完成，摘要如下...
[BLOCK] 卡在 peer config，需補 token
[ASK] 請提供 Agent Card URL
```

### 最低成本確認規則
如果任務緊急且只需確認送達，允許對方先只回：
- `ACK`
- `收到`
- `1`

---

## 實作規劃

# Phase 1 — 先止血（優先）

## 1. 建立 ACK 協議並立即採用
### 目標
讓重要任務先確認「對方知道了」。

### 動作
- 所有重要 `sessions_send` 任務，第一句要求對方先回 `ACK`
- 大任務拆成三階段：
  1. delivery / ACK
  2. running
  3. done

### 驗收
- 重要任務不再只有「有回 / 沒回」兩種模糊狀態

---

## 2. timeout 不再等於未送達
### 目標
修正操作流程與認知模型。

### 動作
- 明文規則：timeout 不代表沒收到
- 遇到 timeout，進行：
  1. repeat ping
  2. 第三方交叉確認
  3. 人工確認

### 驗收
- 任務管理層不再直接把 timeout 判定為送達失敗

---

## 3. 對重要任務採用雙通道確認
### 目標
降低單一通道不可靠的風險。

### 通道策略
- 主通道：`sessions_send`
- 備援通道：Discord（或其他人類可見通道）
- 最後手段：第三方 agent / human confirmation

### 驗收
- 重要任務不再只依賴單一 timeout 結果

---

# Phase 2 — 加入觀測能力

## 4. 建立 `sessions_send` telemetry
### 目標
觀察通訊到底卡在哪。

### 需要紀錄的欄位
- `messageId`
- `fromAgent`
- `toAgent`
- `sessionKey`
- `sentAt`
- `ackAt`
- `replyAt`
- `completedAt`
- `timeoutType`（delivery / reply / completion）
- `status`

### 輸出形式
- JSONL log
- monitor event
- metrics endpoint

### 驗收
- 可以追蹤每則 agent-to-agent 訊息的生命週期

---

## 5. 建立 Agent Activity Monitor
### 目標
知道誰在忙、誰在卡、誰在 idle。

### 顯示內容
- agent 名稱
- 狀態（idle / working / blocked / waiting）
- 目前任務
- 最近 ACK 時間
- 最近 reply 時間
- session/context 大小

### 驗收
- 能回答「哪個 agent 現在在忙什麼」

---

## 6. 加入 session/context 體積觀察
### 目標
驗證 timeout 是否與 context 肥大有關。

### 指標
- token 數
- history 長度
- compaction 次數
- average response latency

### 驗收
- 可用數據判斷 timeout 與 session 肥度是否相關

---

# Phase 3 — 排程與優先級優化

## 7. 將 agent-to-agent 訊息列為高優先級
### 目標
避免被 heartbeat / cron / 一般聊天淹沒。

### 動作
- 協調訊息 queue 優先級高於 heartbeat / cron
- ACK 類訊息優先級最高

### 驗收
- `ACK` 類回覆延遲顯著下降

---

## 8. 分離 coordination session 與工作 session
### 目標
避免協作訊息被塞進肥大的工作 session。

### 動作
- 為 agent-to-agent 溝通建立短 session 或 coordination session
- 長討論、研究任務與控制訊息分流

### 驗收
- coordination 回覆比主工作 session 明顯更快

---

## 9. heartbeat / cron 干擾控制
### 目標
避免背景任務干擾重要通訊。

### 動作
- heartbeat 頻率重新檢查
- cron 任務避免高峰期密集執行
- monitor / logging 儘量改非同步

### 驗收
- timeout 尖峰與 heartbeat / cron 執行時間脫鉤

---

# Phase 4 — 平台化完善

## 10. 建立任務狀態機與結果收斂機制
### 目標
讓 agent 協作從鬆散互發，走向正式團隊作業流。

### 動作
- leader / worker 協作規範
- 任務完成格式標準化
- 任務結果自動匯總
- BLOCK / ASK 流程明確化

### 驗收
- 協作任務能形成完整可追蹤閉環

---

## 11. 建立失敗重試與 reroute 策略
### 目標
遇到 agent 不穩時自動補位。

### 動作
- timeout 後自動 repeat ping
- 若連續未回，交叉詢問第三方 agent
- 必要時 reroute 給替代 agent

### 驗收
- 單 agent 暫時失聯不再直接阻塞整條協作鏈

---

## 12. 將策略寫入系統與靈魂層
### 目標
讓規則長期穩定存在。

### 動作
- 寫入 `SOUL.md`
- 寫入協作 skill / protocol doc
- 對重要 agent 保持 ACK-first 文化

### 驗收
- agent 協作規範不再依賴人類每次重新提醒

---

## 短期立即可做（我的實作起點）

### 我會先從這三件開始：
1. 建立 **ACK-first** 的實際操作規範
2. 起草 **agent communication protocol** 文件
3. 補一份 **monitor / telemetry spec**，專門追蹤 `sessions_send`

---

## 建議輸出文件

1. `agent-communication-protocol.md`
2. `sessions-send-observability-spec.md`
3. `agent-activity-monitor-spec.md`
4. `coordination-session-guidelines.md`

---

## 成功標準

當以下條件成立時，表示 timeout 問題已經從「失控」變成「可管理」：

- timeout 不再直接等於未送達
- 所有重要任務先回 ACK
- 能觀測 sent / delivered / replied / completed 狀態
- 能快速看出哪個 agent 卡住
- 能區分是 delivery 慢、reply 慢，還是 completion 慢
- 有明確 fallback / reroute / human confirmation 流程

---

## 一句話總結

> `sessions_send` timeout 的真正解法，不是單純增加 timeout，而是建立一套可觀測、可分層、可確認、可補位的 agent 通訊協議與執行架構。
