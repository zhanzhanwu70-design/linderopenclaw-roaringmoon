# Agent Activity Monitor Spec

## Goal

Expose the real-time operating state of each agent so coordination problems, queueing, overload, and timeout root causes become visible.

## Core Questions
- Which agent is currently busy?
- Which agent is idle?
- Which agent is blocked?
- Which agent has a large context/session footprint?
- Which agent recently ACKed, replied, or timed out?

---

## Agent States

Each agent should be represented with one primary state:
- `idle`
- `working`
- `waiting`
- `blocked`
- `degraded`
- `offline`

---

## Required Fields per Agent

| Field | Meaning |
|---|---|
| `agentId` | Agent identifier |
| `state` | Current activity state |
| `currentTask` | Short description of active task |
| `lastAckAt` | Last time the agent ACKed a task |
| `lastReplyAt` | Last time the agent replied |
| `lastTimeoutAt` | Last timeout observed |
| `pendingTasks` | Number of outstanding tasks |
| `sessionCount` | Number of active sessions |
| `largestSessionTokens` | Largest known session/context size |
| `heartbeatEnabled` | Whether heartbeat is enabled |
| `lastHeartbeatAt` | Last heartbeat execution |
| `lastCronAt` | Last cron execution |
| `notes` | Operator notes / warnings |

---

## Suggested Derived Warnings

### Warning Levels
- `green` = healthy
- `yellow` = slow / mildly overloaded
- `orange` = degraded / repeated timeouts
- `red` = blocked or likely unhealthy

### Example Warning Rules
- `pendingTasks > 3` → yellow
- `largestSessionTokens > 120k` → yellow
- `largestSessionTokens > 180k` → orange
- `lastTimeoutAt` within 10 minutes and repeated > 2 → orange
- no reply for > 30 minutes during active work → red
- repeated `BLOCK` states without progress → red

---

## Minimal Display Format

```text
[AGENT] rowlet state=working pending=2 lastAck=12:30 lastReply=12:34 largestSession=84k
[AGENT] mrmime state=idle pending=0 lastAck=12:29 lastReply=12:29 largestSession=31k
[AGENT] charizard state=degraded pending=1 lastTimeout=12:28 largestSession=176k
```

---

## Correlation with Communication Tracking

This monitor should be used together with `sessions-send-observability-spec.md`.

Communication telemetry answers:
- what happened to a message

Activity monitor answers:
- what state the target agent was in when it happened

Together they help distinguish:
- delivery issue
- overloaded agent
- long-context slowdown
- execution blockage

---

## Success Criteria

The monitor is successful when operators can quickly tell:
- who should receive the next task
- who is overloaded
- who is a bad target for urgent requests
- whether a timeout is likely caused by agent load vs transport uncertainty
