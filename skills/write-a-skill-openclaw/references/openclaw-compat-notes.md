# OpenClaw Compatibility Notes

## Why this version exists

The original `write-a-skill` guidance is useful, but it is written as a generic agent skill authoring guide.
This version adapts the ideas to match OpenClaw conventions more closely.

## Main differences from the generic version

### 1. Directory structure
Prefer:

```text
skill-name/
├── SKILL.md
├── references/
├── scripts/
└── assets/
```

Instead of creating top-level files such as:
- `REFERENCE.md`
- `EXAMPLES.md`
- extra README-style docs

### 2. Fewer auxiliary documents
OpenClaw skills should avoid unnecessary documentation clutter.
Do not add:
- `README.md`
- `CHANGELOG.md`
- `QUICK_REFERENCE.md`
- `INSTALLATION_GUIDE.md`

### 3. Trigger quality matters
The `description` field is the most important trigger surface.
It must explicitly state:
- what the skill does
- when to use it

### 4. Progressive disclosure
Keep `SKILL.md` lean.
Move heavy details into `references/`.
Use `scripts/` only when they improve repeatability or save the agent from regenerating the same code repeatedly.

## Practical use

Use this skill when you want to:
- create a new OpenClaw skill from scratch
- refactor a generic skill into OpenClaw style
- clean up an overgrown skill folder
- review whether a skill is concise and triggerable
