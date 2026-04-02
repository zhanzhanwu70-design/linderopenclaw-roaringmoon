---
name: task-model-router
description: Route tasks to the appropriate model strategy based on task type. Use when deciding whether the current task should stay on the default model, switch the current session model with /model, or be handed to another agent/model. Classify tasks into 閒聊, 閱讀, 研究, coding, 撰寫skill, or openclaw設定. Prefer minimax-m2.7-highspeed for 閒聊 and 閱讀. Prefer GPT for 研究, coding, 撰寫skill, and openclaw設定.
---

Classify the current user request into exactly one of these categories before doing substantial work:

- 閒聊
- 閱讀
- 研究
- coding
- 撰寫skill
- openclaw設定

Routing policy:

- `閒聊` → prefer `minimax-m2.7-highspeed`
- `閱讀` → prefer `minimax-m2.7-highspeed`
- `研究` → prefer `GPT`
- `coding` → prefer `GPT`
- `撰寫skill` → prefer `GPT`
- `openclaw設定` → prefer `GPT`

Classification guidance:

- `閒聊`: social talk, short casual exchange, lightweight opinion, simple back-and-forth without repo/config work.
- `閱讀`: read/summary/explanation of docs, articles, screenshots, logs, or repo files where the main job is understanding rather than modifying.
- `研究`: compare systems, architecture analysis, codebase investigation, upstream tracking, deep technical explanation, multi-step reasoning.
- `coding`: writing code, editing code, debugging, shell-based implementation, tests, refactors.
- `撰寫skill`: creating or updating any AgentSkill, SKILL.md, bundled references/scripts/assets, packaging or restructuring a skill.
- `openclaw設定`: OpenClaw config, routing, models, channels, permissions, slash commands, gateway, cron, sessions, bindings, plugins, or auth setup.

Decision rules:

1. If a request could fit multiple categories, choose the most operationally expensive one.
2. If the request involves file edits, commands, configuration changes, or architecture judgment, do not classify it as `閒聊` or `閱讀`.
3. If the request mentions OpenClaw config, slash commands, agent routing, model selection, sessions, bindings, or permissions, classify as `openclaw設定` even if it also includes reading.
4. If the request is about creating/updating a skill, classify as `撰寫skill` even if it also includes coding.
5. If uncertain between `閱讀` and `研究`, use `研究` when synthesis, comparison, or judgment is required.

How to act after classification:

1. State the chosen category internally and follow the mapped model preference.
2. If already on the preferred model, continue normally.
3. If not on the preferred model and the environment supports session switching, instruct or use `/model` to switch the current session model before continuing.
4. If direct model switching is not available/reliable, route the task to an agent whose default model matches the preference.
5. If no switch/routing path is available, continue on the current model but explicitly note the preferred model for future routing.

Preferred model names:

- `minimax-m2.7-highspeed`
- `GPT`

Response style for routing decisions:

- Keep routing notes brief.
- Only mention the model choice to the user when it materially affects execution, quality, latency, or cost.
- Do not pretend a model switch happened unless it actually happened.
