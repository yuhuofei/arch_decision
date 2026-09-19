# Agent Adapters

Agent Adapters expose the canonical `arch_decision` governance system to
specific AI coding agents and SDD workflow engines.

## Purpose

The adapter layer is an integration layer.

It MUST NOT become a second source of truth for:

- architecture decision semantics
- constraint priority
- decision status
- technology selection rules
- scoring rules
- complexity budget
- verification semantics
- canonical ownership

Those semantics remain authoritative under `.sdd/`.

## Supported Adapters

| Adapter | Purpose |
|---|---|
| `claude-code` | Claude Code command/skill entrypoints |
| `spec-kit` | Spec Kit workflow integration |
| `openspec` | OpenSpec change-workflow integration |

## Architecture

```text
.sdd/
  |
  | canonical rules
  |
  +-------------------+
  |                   |
  v                   v
Claude Code       Spec Kit / OpenSpec
Adapter               Adapter
  |                   |
  +---------+---------+
            |
            v
       Coding Agent

