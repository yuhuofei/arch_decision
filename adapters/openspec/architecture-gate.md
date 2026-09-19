# Architecture Impact Gate for OpenSpec

Run this gate after OpenSpec Explore and before applying a change.

## Read

- `.sdd/CANONICAL.md`
- `.sdd/decision-trees/decision-protocol.md`
- current `decision.json`
- current `technology-selection.md`
- OpenSpec proposal
- OpenSpec design

## Determine Whether the Change Affects

- system architecture
- service boundaries
- deployment topology
- programming language
- framework
- database
- cache
- queue
- infrastructure
- authentication architecture
- security boundary
- data ownership
- external system integration
- complexity budget

## Result

Return one of:

`NO_ARCHITECTURE_IMPACT`

`ARCHITECTURE_IMPACT`

`BLOCKED`

## NO_ARCHITECTURE_IMPACT

OpenSpec may continue with:

Propose → Review → Apply → Archive.

## ARCHITECTURE_IMPACT

Stop OpenSpec implementation.

Create:

`ARCHITECTURE_CHANGE_REQUEST`

Then invoke the canonical arch_decision workflow.

Do not make the architecture change directly in OpenSpec.

## BLOCKED

Stop.

Report:

- missing information
- affected decision
- why a safe reversible default is unavailable
- required human input
