
# Architecture Gate for Spec Kit

Before running a Spec Kit implementation workflow, verify the canonical
architecture state.

## Read

- `.sdd/CANONICAL.md`
- `.sdd/decision-trees/decision-protocol.md`
- `specs/001-project/decision.json`
- `specs/001-project/technology-selection.md`

## Gate

Implementation planning is allowed only when:

- required architecture decisions are accepted
- no blocking decisions remain
- required human confirmations are complete
- the selected architecture is internally consistent

## If the gate fails

Do not:

- select a replacement technology
- modify the architecture
- create implementation tasks that depend on an unresolved decision

Instead report:

`ARCHITECTURE_GATE_BLOCKED`

with:

- decision
- status
- evidence
- required human action

## If planning discovers architecture insufficiency

Report:

`ARCHITECTURE_CHANGE_REQUEST`

and return to the `arch_decision` workflow.
