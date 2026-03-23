# LLM Monitor Event Spec

目標：讓 monitor 在 **每次 agent 呼叫 LLM 時** 都能顯示即時狀態。

## 需要新增的事件

### 1. `llm_call_started`
在真正送出模型請求前觸發。

建議欄位：
- `type`: `llm_call_started`
- `agent`: agent id
- `sessionKey`: 會話 key
- `source`: discord / telegram / heartbeat / cron / webchat / tool_followup
- `model`: 模型名稱
- `provider`: provider 名稱
- `toolRound`: 第幾輪推理
- `timestamp`: ISO8601
- `toolsAvailable`: 當前可用 tools
- `reason`: user_message / heartbeat / cron / tool_result / retry

### 2. `llm_call_finished`
模型成功回傳後觸發。

建議欄位：
- `type`: `llm_call_finished`
- `agent`
- `sessionKey`
- `model`
- `provider`
- `latencyMs`
- `inputTokens`
- `outputTokens`
- `finishReason`
- `toolCallsCount`
- `timestamp`

### 3. `llm_call_error`
模型請求失敗時觸發。

建議欄位：
- `type`: `llm_call_error`
- `agent`
- `sessionKey`
- `model`
- `provider`
- `latencyMs`
- `errorType`
- `errorMessage`
- `timestamp`

## Monitor 顯示最小版本

開始時：
```text
[LLM CALL] roaringmoon -> minimax-portal/MiniMax-M2.5-highspeed
source=discord reason=user_message round=1
```

完成時：
```text
[LLM DONE] roaringmoon <- minimax-portal/MiniMax-M2.5-highspeed
latency=1833ms in=4210 out=312 toolCalls=0
```

失敗時：
```text
[LLM ERROR] roaringmoon !! minimax-portal/MiniMax-M2.5-highspeed
error=timeout latency=30000ms
```

## 實作位置（概念）
- Agent loop / runner 中真正呼叫 LLM API 的地方
- request 發送前 emit `llm_call_started`
- response 收到後 emit `llm_call_finished`
- catch error 時 emit `llm_call_error`

## 額外建議
- 把 `source` 與 `reason` 分開，方便之後分析 heartbeat / cron / user 對流量的影響
- 若 monitor 有 UI，可新增 `LLM Activity` 面板
- 若有 transcript/log sink，可把這三種事件都寫入 event stream
