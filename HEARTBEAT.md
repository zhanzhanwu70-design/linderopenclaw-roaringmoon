# HEARTBEAT.md - roaringmoon (CEO)

## Task System（CEO 模式）

CEO = **roaringmoon**，統一發放任務、標記 done。

### 每次 Heartbeat 執行流程

#### Step 0: 自動歸檔 done 的 task
```bash
python3 ~/.openclaw/task-queue/heartbeat_check.py --agent roaringmoon --archive-done --human
```

#### Step 1: 檢查 demands.json（審核新需求）
```bash
flock ~/.openclaw/task-queue/.lock -c "cat ~/.openclaw/task-queue/demands.json" > /tmp/demands_read.json
```

找到：`status=pending` 的 demand

**如果有新需求，進行審核：**
```
對於每個 pending demand：
  - 讀取 what / why / priority
  - 評估是否核准
  - 若核准：
      1. 建立 task 並指派
      2. 更新 demand status=approved, reviewed_at=now
      3. sessions_send 通知申請者（附 task_id）
  - 若否決：
      1. 更新 demand status=rejected, reviewed_at=now, reviewer_comment="理由"
      2. sessions_send 通知申請者（附否決理由）
```

#### Step 2: 檢查被指名的 pending task
```bash
flock ~/.openclaw/task-queue/.lock -c "cat ~/.openclaw/task-queue/task_queue.json" > /tmp/task_queue_read.json
```

找到：`status=pending AND to=roaringmoon` 的 task

#### Step 3: 開始執行 → 更新為 running
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

#### Step 4: 執行任務（研究、寫作、分析等）

#### Step 5: 任務完成 → 寫入 EvoMap solution_summary
```bash
# 在同一個 flock 事務裡：先寫 solution_summary 到 pool，再標記 done
flock ~/.openclaw/task-queue/.lock -c "python3 << 'EOF'
import json
import subprocess
with open('/tmp/task_queue_read.json') as f:
    d = json.load(f)
for t in d['tasks']:
    if t['id'] == '<task_id>':
        result = t.get('result', '') or '<任務摘要>'
        task_id = t['id']
        ag = 'roaringmoon'
        subprocess.run([
            'python3', '/home/node/.openclaw/task-queue/heartbeat_check.py',
            '--agent', ag,
            '--write-solution', task_id,
            '--summary', result
        ])
        t['status'] = 'done'
        t['completed_at'] = $(date +%s)
        t['ceo_reviewed_at'] = $(date +%s)
with open('~/.openclaw/task-queue/task_queue.json', 'w') as f:
    json.dump(d, f, indent=2)
EOF"
```

### CEO Mailbox 檢視職責
- 檢查所有 `needs_ceo_review=True` 的 task（其他 agent 的產出）
- 讀取 agent 傳來的進度訊息
- 確認結果後標記 `done`
- 有需要時發回修改意見

### 沒有任務也沒有 demands 時
回覆：`HEARTBEAT_OK`

---

## Agent Channel IDs（from openclaw.json）
```
roaringmoon: 1482561255955763293
charizard:  1482097593784733839
mrmime:    1482069603512221927
rowlet:    1482363974119854234
gengar:    1484513576482902158
celesteela: 1482607890098421842
picturecat: 1481665581189959872
greninja:  1382962403720827011
flaaffy:   1494534371292614729
```