# HEARTBEAT.md - roaringmoon

## Task System（CEO 模式）

CEO = **roaringmoon**，統一發放任務、標記 done。

### 每次 Heartbeat 執行流程

#### Step 1: 檢查被指名的 pending task
```bash
flock ~/.openclaw/task-queue/.lock -c "cat ~/.openclaw/task-queue/task_queue.json" > /tmp/task_queue_read.json
```

找到：`status=pending AND to=roaringmoon` 的 task

#### Step 2: 開始執行 → 更新為 running
```bash
flock ~/.openclaw/task-queue/.lock -c "python3 << 'EOF'
import json
with open('/tmp/task_queue_read.json') as f:
    d = json.load(f)
for t in d['tasks']:
    if t['id'] == '<task_id>':
        t['status'] = 'running'
        t['started_at'] = $(date +%s)
        t['run_count'] = t.get('run_count', 0) + 1
with open('~/.openclaw/task-queue/task_queue.json', 'w') as f:
    json.dump(d, f, indent=2)
EOF"
```

#### Step 3: 執行任務（研究、寫作、分析等）

#### Step 4: 過程中主動回報進度給 CEO（roaringmoon）
```bash
# 使用 sessions_send 發送進度更新給 CEO
# RoaringMoon channel: 1482561255955763293
sessions_send sessionKey: "agent:roaringmoon:discord:channel:1482561255955763293" message: "<task_id> 進度更新：目前完成...，遇到...，下一步..."
```

#### Step 5: 任務完成 → 標記等待 CEO 檢視
```bash
flock ~/.openclaw/task-queue/.lock -c "python3 << 'EOF'
import json
with open('/tmp/task_queue_read.json') as f:
    d = json.load(f)
for t in d['tasks']:
    if t['id'] == '<task_id>':
        t['status'] = 'completed'
        t['completed_at'] = $(date +%s)
        t['needs_ceo_review'] = True
        t['result'] = '<任務摘要>'
with open('~/.openclaw/task-queue/task_queue.json', 'w') as f:
    json.dump(d, f, indent=2)
EOF"
```

#### Step 6: 通知 CEO 檢視
```bash
# 發送最終結果給 CEO 的 mailbox
# RoaringMoon channel: 1482561255955763293
sessions_send sessionKey: "agent:roaringmoon:discord:channel:1482561255955763293" message: "✅ <task_id> 已完成，需要 CEO 檢視。摘要：<result>"
```

### CEO Mailbox 檢視職責（RoaringMoon）
RoaringMoon 的 heartbeat 還需要：
- 檢查所有 `needs_ceo_review=True` 的 task
- 讀取 agent 傳來的進度訊息
- 確認結果後標記 `done`
- 有需要時發回修改意見

---

## Shared Memory — CEO 審核職責

### Step 7: 檢查 Approved 資料夾（CEO 獨有）
```bash
# 檢查是否有待審核的知識
ls ~/.openclaw/shared-memory/memory/approved/

# 讀取待審核內容
cat ~/.openclaw/shared-memory/memory/approved/<filename.md>

# 審核完成後：
# 1. 移動到 wiki 或其他合適位置
# 2. 從 approved/ 刪除（或移到 approved/archived/）
# 3. 如果是值得記住的事實，同時更新 semantic/facts.json

# 2. 通知寫入的 agent 審核結果
sessions_send sessionKey: "agent:<agent>:discord:channel:<channel_id>" message: "✅ 你的知識已通過 CEO 審核，已移動到 wiki"
```

### Step 8: 讀取 Shared Memory（每次 heartbeat）
```bash
# 讀取最近的事件日誌，了解團隊最近進度
tail -20 ~/.openclaw/shared-memory/memory/episodic/$(date +%Y-%m).jsonl

# 讀取事實庫，了解已確認的資訊
cat ~/.openclaw/shared-memory/memory/semantic/facts.json

# 統計：有哪些 task 完成？誰完成了什麼？
grep "task_completed" ~/.openclaw/shared-memory/memory/episodic/$(date +%Y-%m).jsonl
```

---

### 沒有任務時
回覆：`HEARTBEAT_OK`

---

## Agent Channel IDs（from openclaw.json）
```
roaringmoon: 1482561255955763293
charizard:  1482097593784733839（主要）, 1482374570278129724（monitor）
mrmime:    1482069603512221927
rowlet:    1482363974119854234
gengar:    1484513576482902158
celesteela: 1482607890098421842
picturecat: 1481665581189959872
greninja:  1382962403720827011
flaaffy:   1494534371292614729
```
