# Agent Adapter Contract

An Agent Adapter is an integration layer between an external
agent/workflow system and the canonical `arch_decision` governance model.

## Adapter MUST

1. Route to canonical rules.
2. Preserve canonical semantics.
3. Preserve decision status.
4. Preserve human confirmation requirements.
5. Preserve architecture change boundaries.
6. Preserve verification requirements.
7. Fail closed when an architecture gate cannot be evaluated safely.

## Adapter MUST NOT

1. Redefine decision semantics.
2. Redefine constraint priority.
3. Replace P0A/P0B semantics.
4. redefine AUTO / RECOMMEND / REQUIRE_CONFIRMATION / BLOCKED.
5. introduce technology preferences.
6. silently approve architecture changes.
7. silently downgrade a blocking condition.
8. create a second canonical architecture record.

## Authority

Canonical authority remains:

`.sdd/`

Agent-specific files are integration surfaces only.

## Architecture Change

Any workflow that discovers an architecture conflict must produce:

`ARCHITECTURE_CHANGE_REQUEST`

and return control to the canonical architecture decision workflow.

## Implementation Gate

Implementation is allowed only when:

`architecture.status = ACCEPTED`

and no required confirmation or blocking condition remains.
