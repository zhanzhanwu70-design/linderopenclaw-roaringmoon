---
name: write-a-skill-openclaw
description: Create or revise AgentSkills with OpenClaw-compatible structure, concise metadata, progressive disclosure, and reusable bundled resources. Use when the user asks to create a new skill, improve an existing SKILL.md, reorganize a skill folder, or package a skill for reuse.
---

# Write a Skill (OpenClaw-compatible)

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
- what task or domain the skill covers
- what user requests should trigger it
- whether it needs scripts or just instructions
- whether it needs reference materials
- whether the content is stable enough to be reusable

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
