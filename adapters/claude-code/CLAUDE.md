# arch_decision — Claude Code Adapter

This repository uses `arch_decision` as its canonical architecture
decision governance layer.

Before making architecture or technology decisions:

1. Read `AGENTS.md`.
2. Read `.sdd/CANONICAL.md`.
3. Read `.sdd/LAYOUT.md`.
4. Follow the canonical workflow referenced by `AGENTS.md`.

## Architecture Gate

Do not implement a new project or architecture-changing feature until
the applicable `arch_decision` workflow has reached an accepted state.

The canonical definitions of:

- constraints
- priorities
- decision statuses
- candidate elimination
- scoring
- complexity budget
- verification

are under `.sdd/`.

This file only routes Claude Code to those definitions.

## Adapter Commands

Use:

- `/arch-new-project`
- `/arch-discover`
- `/arch-decide`
- `/arch-review`
- `/arch-gate`
- `/arch-verify`

Do not treat these commands as independent policy sources.
