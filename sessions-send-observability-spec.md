# sessions_send Observability Spec

## Goal

Provide visibility into agent-to-agent communication so timeouts can be diagnosed instead of treated as a black box.

## Problem

A `sessions_send` timeout may mean:
1. message not delivered
2. delivered but not yet processed
3. processed but no reply yet
4. reply generated but return/announce path delayed

Current system does not clearly separate these states.

---

## Required States

Each important agent-to-agent message should move through these states when possible:

- `sent`
- `delivered`
- `seen`
- `acknowledged`
- `running`
- `replied`
- `completed`
- `blocked`
- `failed`
- `timed_out`

---

## Event Model

### 1. `agent_message_sent`
Triggered immediately after a `sessions_send` request is issued.

Fields:
- `messageId`
- `fromAgent`
- `toAgent`
- `sessionKey`
- `sentAt`
- `requestType` (important / normal)
- `expectsAck` (boolean)
- `summary`

### 2. `agent_message_timeout`
Triggered when no response is observed within the timeout window.

Fields:
- `messageId`
- `fromAgent`
- `toAgent`
- `timeoutAt`
- `timeoutKind` (`delivery_or_reply_unknown` / `reply_timeout` / `completion_timeout`)
- `elapsedMs`

### 3. `agent_message_ack`
Triggered when the remote agent responds with `ACK` / `收到` / `1`.

Fields:
- `messageId`
- `fromAgent`
- `toAgent`
- `ackAt`
- `ackText`
- `elapsedMs`

### 4. `agent_message_status`
Triggered when the remote agent reports `RUN / DONE / BLOCK / ASK`.

Fields:
- `messageId`
- `status`
- `statusAt`
- `details`
- `elapsedMs`

### 5. `agent_message_completed`
Triggered when the task is concluded.

Fields:
- `messageId`
- `completedAt`
- `finalState` (`done` / `blocked` / `failed`)
- `elapsedMs`

---

## Minimal Logging Format

```text
[A2A-SEND] id=... from=roaringmoon to=rowlet session=agent:rowlet:... expectsAck=true
[A2A-ACK] id=... from=roaringmoon to=rowlet elapsed=842ms
[A2A-STATUS] id=... status=RUN elapsed=1345ms
[A2A-DONE] id=... elapsed=18422ms
```

If timeout occurs:

```text
[A2A-TIMEOUT] id=... from=roaringmoon to=rowlet elapsed=30000ms kind=delivery_or_reply_unknown
```

---

## Data to Correlate

To properly debug timeout behavior, correlate A2A communication with:
- target agent activity state
- target session/context size
- heartbeat execution windows
- cron execution windows
- monitor / hooks activity
- model latency when reply generation occurs

---

## Immediate Operational Rule

Until deep telemetry exists, use protocol-level observability:
- ask for `ACK` first
- treat timeout as unknown delivery state
- use repeat ping / third-party confirmation / human confirmation

---

## Success Criteria

This spec is successful when operators can answer:
- Was the message sent?
- Was it likely delivered?
- Did the target ACK it?
- Did the target start processing?
- Did the target finish?
- Where in the chain did delay happen?
