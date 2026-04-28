# `write-a-skill` 的 OpenClaw 相容改寫版

來源：`mattpocock/skills/skills/write-a-skill/SKILL.md`
目的：保留原本的核心觀念，但改寫成更符合 OpenClaw / AgentSkills 慣例的版本。

---

```md
---
name: write-a-skill
description: Create or revise AgentSkills with OpenClaw-compatible structure, concise metadata, progressive disclosure, and reusable bundled resources. Use when the user asks to create a new skill, improve an existing SKILL.md, reorganize a skill folder, or package a skill for reuse.
---

# Write a Skill

Create skills that are concise, triggerable, and useful in repeated real tasks.

## Process

1. Understand the task domain.
2. Collect concrete usage examples.
3. Decide which parts belong in:
   - `SKILL.md`
   - `references/`
   - `scripts/`
   - `assets/`
4. Draft the skill.
5. Review and refine with the user.
6. Package only after the skill is actually useful.

## First gather the minimum requirements

Before drafting a skill, clarify:
- What task or domain the skill covers
- What user requests should trigger it
- Whether it needs scripts or just instructions
- Whether it needs reference materials
- Whether the content is stable enough to be reusable

If the usage pattern is still vague, ask for 2–5 realistic examples.

## Required structure

Use this layout:

```text
skill-name/
├── SKILL.md
├── references/      # optional
├── scripts/         # optional
└── assets/          # optional
```

Do **not** create extra documentation files such as:
- `README.md`
- `CHANGELOG.md`
- `QUICK_REFERENCE.md`
- `INSTALLATION_GUIDE.md`

Keep the skill minimal and execution-oriented.

## SKILL.md rules

### Frontmatter
Must contain only:
- `name`
- `description`

### Description requirements
The description is the primary trigger surface.
It must tell the agent:
1. what the skill does
2. when to use it

A good description should:
- be explicit
- mention task/domain/filetype triggers
- be understandable without reading the body

Example:

```text
Create, edit, and debug ROS2 nodes, launch files, QoS settings, and package scaffolding. Use when the user asks for ROS2 node code, rclpy/rclcpp packages, launch files, ROS2 debugging, or robotics middleware integration.
```

A weak description:

```text
Helps with robotics.
```

## Body rules

Keep the body focused on execution guidance:
- workflows
- decision rules
- output expectations
- references to bundled files

Do not repeat large reference content inside `SKILL.md`.
Move detailed material into `references/`.

## When to create `references/`

Use `references/` when:
- detailed material would make `SKILL.md` too large
- you need examples, schemas, API notes, checklists, or domain-specific docs
- the skill covers multiple subdomains and the details should load only on demand

Reference files should be linked directly from `SKILL.md`.
Avoid deeply nested reference chains.

## When to create `scripts/`

Use `scripts/` when:
- an operation is deterministic
- the same utility code would otherwise be generated repeatedly
- explicit error handling matters
- token savings and repeatability are important

Prefer scripts for:
- validation
- formatting
- repeatable transforms
- content extraction
- patching helpers

## When to create `assets/`

Use `assets/` when the skill needs reusable files that are used in output but do not need to be loaded into context, such as:
- templates
- example configs
- boilerplate files
- icons, fonts, or images

## Review checklist

Before finalizing a skill, verify:
- [ ] Description clearly states what it does
- [ ] Description clearly states when to use it
- [ ] `SKILL.md` is concise
- [ ] Detailed information is moved into `references/` when needed
- [ ] Scripts are only included when they add reliability or save repeated code generation
- [ ] No unnecessary auxiliary docs were added
- [ ] File structure matches OpenClaw skill conventions

## Iteration rule

After using the skill on real tasks:
1. notice where it struggles
2. tighten the instructions
3. split details into references if needed
4. add scripts only when repetition or fragility justifies them
5. re-test on a real task
```

---

## 我改了哪些地方

### 1. 改成 OpenClaw 的目錄慣例
原版偏向：
- `REFERENCE.md`
- `EXAMPLES.md`

我改成：
- `references/`
- `scripts/`
- `assets/`

這比較符合你現在環境與 `skill-creator` 的規範。

### 2. 移除會讓 skill 長歪的額外檔案暗示
OpenClaw 這邊比較明確反對產生：
- `README.md`
- `CHANGELOG.md`
- `QUICK_REFERENCE.md`

所以我把這部分明確寫出來。

### 3. 把原本偏通用 agent 的說法，改成更像 OpenClaw 的 trigger 語言
我保留了原本最重要的觀點：
- `description` 是 skill 是否被載入的核心

但把表達方式改得更符合 OpenClaw 實作與思路。

### 4. 把規則聚焦在「怎麼讓 skill 真正可執行」
我把內容收斂成：
- 怎麼判斷要不要拆 references
- 什麼情況才需要 scripts
- 什麼內容不該放 skill 裡
- 怎麼 review skill

這樣更適合你現在要的實務工作流。

---

## 使用建議

這份文件本身不是要取代你現有的 `skill-creator`，而是：
- 當成對外可分享的「OpenClaw 版 write-a-skill 說明」
- 或當成你之後整理公共 skill 的參考底稿

如果你要，我下一步可以再幫你：
1. 把這份真的做成一個可安裝的 skill 目錄
2. 跟你現在的 `skill-creator` 做逐段差異表
3. 合併成一個更精簡的公共 skill
