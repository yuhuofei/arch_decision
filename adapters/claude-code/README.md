# Claude Code Adapter

This adapter exposes `arch_decision` canonical workflows to Claude Code.

## Purpose

Claude Code is the execution agent.

This adapter provides:

- architecture workflow entrypoints
- discovery entrypoints
- decision review entrypoints
- human confirmation gates
- verification entrypoints

The adapter does not redefine architecture rules.

## Canonical Sources

Before executing an architecture workflow, Claude Code MUST resolve:

1. `.sdd/LAYOUT.md`
2. `.sdd/CONVENTIONS.md`
3. `.sdd/CANONICAL.md`
4. `.sdd/decision-trees/decision-protocol.md`
5. `.sdd/workflows/new-project.md`
6. relevant `.sdd/knowledge/`
7. relevant `.sdd/decision-trees/`

## Commands

| Command | Purpose |
|---|---|
| `/arch-new-project` | Start a new project architecture workflow |
| `/arch-discover` | Run/re-run discovery |
| `/arch-decide` | Execute architecture and technology decisions |
| `/arch-review` | Review unresolved decisions |
| `/arch-gate` | Evaluate whether implementation may proceed |
| `/arch-verify` | Verify architecture against implementation |

## Important

These commands are routing surfaces.

The canonical meaning of:

- AUTO
- RECOMMEND
- REQUIRE_CONFIRMATION
- BLOCKED
- P0A
- P0B
- P1
- P2
- P3

is defined by `.sdd/`.

Do not redefine these semantics here.
