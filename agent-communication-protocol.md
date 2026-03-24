# Agent Communication Protocol v1

## Phase 1: Immediate Stabilization

### Core Rules

1. **ACK-first for important tasks**
   - Any important agent-to-agent request must be acknowledged first.
   - The receiver should reply with `ACK` before doing long analysis or execution.

2. **Timeout != Not Delivered**
   - A `sessions_send` timeout must not be treated as proof of non-delivery.
   - Delivery and reply are separate states.

3. **Prefer short confirmations first**
   - For important requests, first reply with one of:
     - `ACK`
     - `收到`
     - `1`
   - Then follow up with execution status.

### Standard Status Codes

- `ACK` = received
- `RUN` = started processing
- `DONE` = completed
- `BLOCK` = blocked / cannot proceed
- `ASK` = need more info

### Suggested Response Format

```text
[ACK] 已收到任務：<summary>
[RUN] 開始處理
[DONE] 完成：<result>
[BLOCK] 卡住：<reason>
[ASK] 需要補充：<question>
```

### For urgent low-latency confirmation
Allowed minimal responses:
- `ACK`
- `收到`
- `1`

### Operational Rule
If a request is important, do **not** stay silent.
Even a short acknowledgement is better than no reply.
