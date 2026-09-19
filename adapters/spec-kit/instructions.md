# arch_decision Spec Kit Integration

The project uses `arch_decision` as the architecture governance layer.

## Before Plan

Read:

- `.sdd/CANONICAL.md`
- `.sdd/decision-trees/decision-protocol.md`
- current architecture decision artifacts

Verify architecture acceptance.

## During Specify

Describe:

- what
- why
- requirements
- acceptance criteria

Do not make architecture decisions prematurely.

## During Plan

Plan how to implement the accepted architecture.

Do not replace accepted technology choices.

## During Tasks

Tasks must remain consistent with:

- accepted architecture
- selected technologies
- complexity budget

## During Implement

Do not introduce infrastructure or technologies that are not represented
by the accepted architecture.

If implementation requires a new architecture decision:

STOP.

Report:

`ARCHITECTURE_CHANGE_REQUEST`

## During Converge

Check implementation against:

- requirements
- plan
- tasks
- accepted architecture

Architecture drift must be reported rather than silently normalized.
